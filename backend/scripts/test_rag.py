# scripts/test_rag.py
import sys
import json
from backend.modules.rag.runner import run_food_search
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Cần query"}, ensure_ascii=False))
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    result = run_food_search(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))