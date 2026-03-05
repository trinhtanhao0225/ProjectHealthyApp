# backend/modules/exercise/filter_service.py
from backend.utils.logger import logger

def filter_exercises(filter_obj, muscle=None, equipment=None, level=None):
    """
    Lọc bài tập theo muscle, equipment, level
    """
    df = filter_obj.df.copy()

    if muscle and muscle.lower() not in ["all", ""]:
        muscle = muscle.lower()
        df = df[df['combined_muscles'].apply(lambda lst: muscle in lst)]

    if equipment and equipment.lower() not in ["all", ""]:
        equipment = equipment.lower()
        df = df[df['equipment'].apply(lambda lst: equipment in lst)]

    if level not in [None, "", "all"]:
        try:
            lvl_val = float(level)
            df = df[df["cluster_label"] == lvl_val]
        except:
            logger.warning(f"Level không hợp lệ: {level}")

    if df.empty:
        return {"count": 0, "results": []}

    cols_to_keep = [
        "name", "category", "combined_muscles", "equipment",
        "cluster_label", "reps", "sets", "MET", "video", "instructions"
    ]
    df = df[[c for c in cols_to_keep if c in df.columns]]

    return {"count": len(df), "results": df.to_dict(orient="records")}