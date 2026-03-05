# backend/api/v1/endpoints/recognition.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from backend.services.recognition_service import recognize_food
import os
import uuid
import shutil

router = APIRouter(prefix="/recognition", tags=["Recognition"])

@router.post("/upload")
async def recognize_uploaded_food(
    file: UploadFile = File(...),
    email: str = Form(None, description="Email người dùng (tùy chọn để lưu Food)"),
    day: str = Form(None, description="Ngày (tùy chọn để lưu Food)"),
    session: str = Form(None, description="Buổi ăn (tùy chọn để lưu Food)")
):
    """
    Upload ảnh → nhận diện món ăn → trả kết quả + lưu Food nếu có email/day/session
    """
    # Tạo file tạm
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")

    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Gọi service nhận diện
        result = await recognize_food(
            image_path=temp_path,
            email=email,
            day=day,
            session=session
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)