
import json
from backend.utils.logger import logger

def extract_info(df, predicted_label):
    filtered = df[df['dish_name'] == predicted_label]
    if filtered.empty:
        logger.warning(f"Không tìm thấy dữ liệu cho: {predicted_label}")
        return {"ingredients": [], "portion_size": "", "nutrition": {}}

    row = filtered.iloc[0]
    nutrition = row['nutritional_profile']
    if isinstance(nutrition, str):
        try:
            nutrition = json.loads(nutrition)
        except:
            nutrition = {}

    return {
        "ingredients": row['ingredients'],
        "portion_size": row['portion_size'],
        "nutrition": nutrition
    }