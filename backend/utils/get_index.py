import faiss
import numpy as np

def get_faiss_index(rag_df):
    embedding_dimension = rag_df['embeddings'].iloc[0].shape[0]
    index = faiss.IndexFlatL2(embedding_dimension)

    # Sửa chính tả: 'embeddings' ✅
    embedding_matrix = np.array(rag_df['embeddings'].tolist()).astype('float32')

    index.add(embedding_matrix)
    return index

def get_food_index(foods_df, model):
    # Tạo embedding cho từng description của món ăn
    embeddings = model.encode(foods_df['description'].tolist(), convert_to_numpy=True)
    embeddings = embeddings.astype('float32')

    # Build FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index