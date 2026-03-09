# backend/api/v1/router.py
from fastapi import APIRouter

# Import các router từ endpoints
from backend.api.v1.endpoints import auth
# Nếu bạn có thêm các phần khác (recognition, exercise, food, user, account), import ở đây
from backend.api.v1.endpoints import recognition, account,exercise,user, chat,food

api_router = APIRouter()

# Include các router con
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Nếu có thêm endpoint khác, include ở đây
api_router.include_router(recognition.router, prefix="/recognition", tags=["Recognition"])
# api_router.include_router(exercise.router, prefix="/exercise", tags=["Exercise"])
# api_router.include_router(food.router, prefix="/food", tags=["Food"])
# api_router.include_router(user.router, prefix="/users", tags=["User"])
api_router.include_router(account.router, prefix="/accounts", tags=["Account"])
api_router.include_router(exercise.router, prefix="/exercise", tags=["Exercise"])
api_router.include_router(user.router, prefix="/users", tags=["User"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(food.router, prefix="/food", tags=["Food"])