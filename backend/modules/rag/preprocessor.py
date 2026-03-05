# app/modules/rag/preprocessor.py
import re
import json
from typing import List, Dict
from backend.utils.logger import log

def normalize_name(s: str) -> str:
    if not s:
        return ""
    s = s.lower().strip()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())

def preprocess_results(raw_items: List[Dict], max_items=40, max_chars=15000, max_chars_per_item=400) -> List[Dict]:
    log(f"Preprocess bắt đầu: {len(raw_items)} items")
    seen = set()
    clean = []
    total_chars = 0

    for item in raw_items:
        name = item.get("description") or item.get("name") or ""
        key = normalize_name(name)
        if not key or key in seen:
            continue
        seen.add(key)

        # Sửa phần rút gọn nutrients
        nutrients = item.get("nutrients", {})
        short_nut = {}

        if isinstance(nutrients, dict):
            # Lấy 'amount' từ dict con để sort theo giá trị số
            sortable = []
            for k, v in nutrients.items():
                # v có thể là dict {'amount': ..., 'unit': ...} hoặc số trực tiếp
                amount = v.get('amount') if isinstance(v, dict) else v
                try:
                    amount_value = float(amount) if amount is not None else 0
                except (ValueError, TypeError):
                    amount_value = 0
                sortable.append((k, amount_value, v))  # giữ nguyên v để sau dùng

            # Sort theo amount giảm dần, lấy top 3
            sorted_items = sorted(sortable, key=lambda x: x[1], reverse=True)[:3]

            # Lấy lại nutrients gốc (giữ dict đầy đủ)
            for k, _, v in sorted_items:
                short_nut[k] = v  # giữ nguyên {'amount': ..., 'unit': ...}

        # Các phần còn lại giữ nguyên
        ingredients = item.get("ingredients", [])[:20]

        desc = str(item.get("description", "")).strip()
        if len(desc) > max_chars_per_item:
            desc = desc[:max_chars_per_item].rstrip() + " ..."

        clean_item = {
            "fdcId": int(item.get("fdcId")) if item.get("fdcId") is not None else None,
            "name": name.strip(),
            "description": desc,
            "nutrients": short_nut,
            "ingredients": ingredients
        }

        size = len(json.dumps(clean_item, ensure_ascii=False))
        if total_chars + size > max_chars:
            break
        total_chars += size
        clean.append(clean_item)

        if len(clean) >= max_items:
            break

    log(f"Preprocess xong: {len(clean)} items")
    return clean