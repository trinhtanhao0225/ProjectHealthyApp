# backend/modules/exercise/info_retriever.py
from backend.utils.logger import logger

def get_exercise_by_name(filter_obj, exercise_name: str):
    """
    Tra cứu thông tin bài tập theo tên
    """
    ex = exercise_name.lower().strip()
    row = filter_obj.df[filter_obj.df["name_lower"] == ex]

    if row.empty:
        logger.warning(f"Không tìm thấy bài tập: {exercise_name}")
        return None

    row = row.iloc[0]

    try:
        MET = float(row.get("MET", 0))
    except:
        MET = 0

    return {
        "name": row.get("name"),
        "MET": MET,
        "video": row.get("video"),
        "instructions": row.get("instructions"),
        "equipment": row.get("equipment"),
        "muscles": row.get("combined_muscles")
    }