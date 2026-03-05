# backend/services/recognition_service.py
from fastapi import HTTPException
import os
import uuid
import shutil

from backend.modules.recognition.loader import load_food_dataset
from backend.modules.recognition.recognizer import FoodRecognizer
from backend.modules.recognition.classifier import classify
from backend.modules.recognition.extractor import extract_info

from backend.models.food import Food  # model Food bạn đã có
from backend.utils.logger import logger

async def recognize_food(image_path: str, email: str = None, day: str = None, session: str = None):
    """
    Nhận diện món ăn từ ảnh, lưu record Food nếu có email/day/session
    """
    try:
        # Load dataset (giống code cũ)
        df, labels = load_food_dataset()

        # Tạo recognizer
        recognizer = FoodRecognizer(image_path)
        recognizer.df = df
        recognizer.candidate_labels = labels

        # Classify
        predicted_label = classify(recognizer)

        # Extract info
        info = extract_info(df, predicted_label)

        # Chuẩn bị kết quả
        result = {
            "status": "success",
            "dish_name": predicted_label,
            "nutrition": info["nutrition"],
            "ingredients": info["ingredients"],
            "portion_size": info["portion_size"],
            "raw_info": info
        }

        # Nếu có email/day/session → lưu record Food
        if email and day and session:
            food_data = {
                "email": email,
                "dish_name": predicted_label,
                "ingredients": info["ingredients"],
                "portion_size": info["portion_size"],
                "nutrition": info["nutrition"],
                "image_url": image_path,  # hoặc upload lên Cloudinary sau
                "day": day,
                "session": session,
                "is_recognized": True
            }

            record = Food(**food_data)
            await record.insert()
            result["saved_food_id"] = str(record.id)
            logger.info(f"Saved recognized food for {email}: {predicted_label}")

        return result

    except Exception as e:
        logger.error(f"Recognition error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))