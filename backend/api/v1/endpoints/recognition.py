# backend/api/v1/endpoints/recognition.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.services.recognition_service import recognize_food

router = APIRouter(tags=["Recognition"])


class RecognitionRequest(BaseModel):
    image_url: str
    email: Optional[str] = None
    day: Optional[str] = None
    session: Optional[str] = None


@router.post("/")
async def recognize_food_from_url(data: RecognitionRequest):
    """
    Nhận link ảnh → nhận diện món ăn
    """

    try:
        result = await recognize_food(
            image_path=data.image_url,
            email=data.email,
            day=data.day,
            session=data.session
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))