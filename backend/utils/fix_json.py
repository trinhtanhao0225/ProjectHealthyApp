import math
import json

def fix_json_value(obj):
    """
    Fix NaN/Inf để JSON hợp lệ
    """
    if isinstance(obj, dict):
        return {k: fix_json_value(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [fix_json_value(v) for v in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    else:
        return obj