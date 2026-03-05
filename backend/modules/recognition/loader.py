from datasets import load_dataset
import pandas as pd
import warnings
from backend.utils.logger import logger

_dataset_df = None
_candidate_labels = None

def load_food_dataset(force_reload=False):
    global _dataset_df, _candidate_labels
    
    if _dataset_df is not None and not force_reload:
        return _dataset_df, _candidate_labels

    warnings.filterwarnings("ignore")
    logger.info("Đang load dataset Codatta/MM-Food-100K...")

    try:
        ds = load_dataset("Codatta/MM-Food-100K", split="train", streaming=False)
        df = ds.to_pandas().dropna(subset=["dish_name", "image_url"]).reset_index(drop=True)
        labels = df['dish_name'].unique().tolist()

        _dataset_df = df
        _candidate_labels = labels

        logger.info(f"Load thành công: {len(df)} samples, {len(labels)} món ăn unique")
        return df, labels

    except Exception as e:
        logger.error(f"Lỗi load dataset: {e}")
        raise