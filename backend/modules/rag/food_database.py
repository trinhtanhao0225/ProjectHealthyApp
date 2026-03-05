# app/modules/rag/food_database.py
from typing import Dict, List, Optional
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
from backend.utils.logger import logger
from backend.utils.get_index import get_faiss_index, get_food_index  # import từ code cũ của bạn
from backend.modules.rag.data_loader import load_rag_data
class FoodDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("Khởi tạo FoodDatabase singleton...")
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        
        self.rag_df, self.foods_df, self.input_foods_df, self.nutrients_df = load_rag_data()

        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

        self.rag_index = get_faiss_index(self.rag_df)
        self.food_index = get_food_index(self.foods_df, self.model)

        self._details_cache: Dict[int, Dict] = {}
        self._build_details_cache()

        logger.info(f"FoodDatabase ready: {len(self._details_cache)} cached foods")

    def _build_details_cache(self):
        for fdc_id in self.foods_df['fdcId'].unique():
            data = self.nutrients_df[self.nutrients_df['fdcId'] == fdc_id]
            if data.empty:
                continue

            desc = self.foods_df[self.foods_df['fdcId'] == fdc_id]['description'].iloc[0]
            nutrients = {}

            for _, row in data.iterrows():
                name = str(row['nutrient.name']).lower()
                amount = row['amount']
                unit = str(row['nutrient.unitName']).lower()

                if name in nutrients and nutrients[name]['unit'] == unit:
                    nutrients[name]['amount'] += amount
                else:
                    nutrients[name] = {'amount': amount, 'unit': unit}

            self._details_cache[fdc_id] = {'description': desc, 'nutrients': nutrients}

    def search_food(self, query: str, k: int = 60) -> pd.DataFrame:
        query_emb = self.model.encode([query], convert_to_numpy=True).astype('float32')
        _, indices = self.food_index.search(query_emb, k)
        top_df = self.foods_df.iloc[indices[0]].copy()

        filtered = []
        for _, row in top_df.iterrows():
            details = self.get_food_details(row['fdcId'])
            if details and details['nutrients'].get('protein', {}).get('amount', 0) >= 5 and \
               details['nutrients'].get('energy', {}).get('amount', 0) <= 600:
                filtered.append(row)

        filtered_df = pd.DataFrame(filtered)[['fdcId', 'description']]
        logger.info(f"Search '{query}' → {len(filtered_df)} món sau filter")
        return filtered_df

    def get_food_details(self, fdc_id: int) -> Optional[Dict]:
        return self._details_cache.get(fdc_id)

    def get_ingredients(self, fdc_id: int) -> List[str]:
        data = self.input_foods_df[self.input_foods_df['fdcId'] == fdc_id]
        if data.empty:
            return []

        desc = self.get_food_details(fdc_id)['description'] if fdc_id in self._details_cache else f"fdcId {fdc_id}"
        lines = [f"---- Ingredients for {desc} ----"]
        for _, row in data.iterrows():
            name = row.get('inputFood.foodDescription', 'Unknown')
            cat = row.get('inputFood.foodCategory.description', 'Unknown')
            lines.append(f"- {name} (Category: {cat})")
        return lines


# Singleton
food_db = FoodDatabase()