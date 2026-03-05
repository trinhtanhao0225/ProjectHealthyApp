# backend/scripts/test_recognition.py (sửa lại)
import sys
import json
import os
from backend.services.recognition_service import recognize_food

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Cần đường dẫn ảnh"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    image_path = sys.argv[1].strip()  # loại bỏ khoảng trắng thừa
    print(f"Đường dẫn nhận: {image_path}", file=sys.stderr)

    # Kiểm tra file tồn tại
    if not os.path.isfile(image_path):
        print(json.dumps({
            "status": "error",
            "message": f"Không tìm thấy file ảnh: {image_path}"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = recognize_food(image_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))