# backend/modules/exercise/data_loader.py
import pandas as pd
import ast
from pathlib import Path
from backend.utils.logger import logger

class ExerciseFilter:
    def __init__(self, csv_path: str = None):
        self.csv_path = csv_path or str(Path(__file__).parent.parent.parent.parent / "data"/ "processed" / "processed_data_filtered.csv")
        self.df = self._load_and_normalize()

    def _load_and_normalize(self):
        logger.info(f"Loading exercise data from: {self.csv_path}")
        if not Path(self.csv_path).exists():
            raise FileNotFoundError(f"Không tìm thấy CSV tại {self.csv_path}")

        df = pd.read_csv(self.csv_path)

        # Chuẩn hóa cluster_label (level)
        if 'cluster_label' in df.columns:
            df['cluster_label'] = pd.to_numeric(df['cluster_label'].astype(str).str.strip(), errors='coerce')

        # Chuẩn hóa list columns
        for col in ['combined_muscles', 'equipment']:
            if col in df.columns:
                df[col] = df[col].apply(self._to_list_safe)
                df[col] = df[col].apply(lambda lst: [str(i).strip().lower() for i in lst])
                df[col] = df[col].apply(lambda lst: ['none'] if not lst else lst)

        # Cột lowercase để tra cứu tên
        if "name" in df.columns:
            df["name_lower"] = df["name"].astype(str).str.lower().str.strip()

        logger.info(f"Loaded {len(df)} exercises")
        return df

    def _to_list_safe(self, x):
        if isinstance(x, str):
            try:
                val = ast.literal_eval(x)
                return val if isinstance(val, list) else [val]
            except:
                return [x.strip()]
        elif isinstance(x, list):
            return x
        elif pd.isna(x):
            return []
        else:
            return [str(x)]