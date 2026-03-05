import torch
from PIL import Image
import requests
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel
import sys
from backend.utils.logger import logger

class FoodRecognizer:
    def __init__(self, image_path, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Sử dụng thiết bị: {self.device}")

        self.raw_image = self._load_image(image_path)

        logger.info("Đang load CLIP model...")
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        self.df = None
        self.candidate_labels = None

    def _load_image(self, image_path):
        try:
            if image_path.startswith(('http://', 'https://')):
                logger.info("Tải ảnh từ URL...")
                response = requests.get(image_path, timeout=30)
                response.raise_for_status()
                return Image.open(BytesIO(response.content)).convert("RGB")
            else:
                logger.info("Load ảnh từ local...")
                return Image.open(image_path).convert("RGB")
        except Exception as e:
            logger.error(f"Lỗi load ảnh: {e}")
            raise