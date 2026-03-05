# app/modules/rag/data_loader.py
import pandas as pd
import numpy as np
import os
from pathlib import Path
from backend.utils.logger import logger

def load_rag_data(base_path: str = None):
    """
    Load tất cả dữ liệu cần cho RAG từ thư mục processed.
    Trả về tuple: (rag_df, foods_df, input_foods_df, nutrients_df)
    """
    if base_path is None:
        base_path = str(Path(__file__).parent.parent.parent.parent / "data" / "processed")

    logger.info(f"Loading RAG data from: {base_path}")

    try:
        rag_df = pd.read_pickle(os.path.join(base_path, 'rag_df.pkl'))
        rag_df['embeddings'] = rag_df['embeddings'].apply(lambda x: np.array(x, dtype=np.float32))

        foods_df = pd.read_csv(os.path.join(base_path, 'foods.csv'))
        input_foods_df = pd.read_csv(os.path.join(base_path, 'input_foods.csv'))
        nutrients_df = pd.read_csv(os.path.join(base_path, 'food_nutrients.csv'))

        logger.info(f"Loaded: {len(foods_df)} foods | {len(rag_df)} chunks | {len(nutrients_df)} nutrients")
        return rag_df, foods_df, input_foods_df, nutrients_df

    except Exception as e:
        logger.error(f"Load RAG data failed: {str(e)}")
        raise