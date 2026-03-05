# backend/modules/recognition/classifier.py
"""
Module tính embedding và classify ảnh bằng CLIP
Tương thích transformers mới (BaseModelOutputWithPooling)
"""

import torch
import torch.nn.functional as F
from backend.utils.logger import logger

def get_pooled_embedding(outputs):
    """
    Lấy embedding pooled từ output của CLIP (image hoặc text)
    - Nếu outputs là tensor → dùng trực tiếp
    - Nếu là BaseModelOutputWithPooling → dùng pooler_output
    - Fallback: mean pooling last_hidden_state
    """
    if isinstance(outputs, torch.Tensor):
        return outputs

    if hasattr(outputs, 'pooler_output') and outputs.pooler_output is not None:
        return outputs.pooler_output

    if hasattr(outputs, 'last_hidden_state'):
        return outputs.last_hidden_state.mean(dim=1)  # mean pooling

    raise ValueError(f"Output CLIP không hỗ trợ lấy embedding: {type(outputs)}")


def compute_image_embedding(model, processor, image, device):
    """
    Tính embedding ảnh từ CLIP model
    """
    logger.info("Tính embedding ảnh...")
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
        image_emb = get_pooled_embedding(outputs)
        image_emb = F.normalize(image_emb, p=2, dim=-1)

    logger.info(f"Image embedding shape: {image_emb.shape}")
    return image_emb


def compute_text_embeddings_batch(model, processor, labels_batch, device):
    """
    Tính embedding text cho batch labels
    """
    logger.debug(f"Tính embedding text cho batch {len(labels_batch)} nhãn")
    inputs = processor(
        text=labels_batch,
        return_tensors="pt",
        padding=True,
        truncation=True
    ).to(device)

    with torch.no_grad():
        outputs = model.get_text_features(**inputs)
        text_emb = get_pooled_embedding(outputs)
        text_emb = F.normalize(text_emb, p=2, dim=-1)

    return text_emb


def classify(recognizer):
    """
    Phân loại ảnh bằng cosine similarity giữa image và text embeddings
    """
    if recognizer.df is None or recognizer.candidate_labels is None:
        raise ValueError("Dataset hoặc candidate_labels chưa load")

    logger.info("Bắt đầu classify ảnh...")

    # 1. Tính embedding ảnh
    image_emb = compute_image_embedding(
        recognizer.clip_model,
        recognizer.clip_processor,
        recognizer.raw_image,
        recognizer.device
    )

    # 2. Tính embedding text theo batch
    text_emb_list = []
    batch_size = 8  # Giảm xuống 8 để an toàn trên CPU (có thể tăng nếu GPU)

    logger.info(f"Tính embedding text cho {len(recognizer.candidate_labels)} nhãn (batch size = {batch_size})...")

    for i in range(0, len(recognizer.candidate_labels), batch_size):
        batch_labels = recognizer.candidate_labels[i:i + batch_size]
        emb = compute_text_embeddings_batch(
            recognizer.clip_model,
            recognizer.clip_processor,
            batch_labels,
            recognizer.device
        )
        text_emb_list.append(emb.cpu())

        if (i // batch_size) % 5 == 0:
            logger.debug(f"Đã xử lý {i + batch_size}/{len(recognizer.candidate_labels)} nhãn")

    all_text_emb = torch.cat(text_emb_list, dim=0)

    # 3. Tính similarity
    logger.info("Tính similarity...")
    similarities = torch.matmul(image_emb.cpu(), all_text_emb.t())

    # 4. Lấy nhãn có similarity cao nhất
    idx = similarities.argmax(dim=1).item()
    predicted = recognizer.candidate_labels[idx]

    logger.info(f"Dự đoán: {predicted} (similarity max: {similarities[0, idx]:.4f})")
    return predicted