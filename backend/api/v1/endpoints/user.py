# backend/api/v1/endpoints/user.py
from fastapi import APIRouter, HTTPException, status
from backend.schemas.user import UserCreate, UserResponse
from backend.services.user_service import create_user, get_all_users, get_user_by_email

router = APIRouter(prefix="/users", tags=["User"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(data: UserCreate):
    return await create_user(data)

@router.get("/", response_model=list[UserResponse])
async def get_users():
    return await get_all_users()

@router.get("/{email}", response_model=UserResponse)
async def get_user_by_email_endpoint(email: str):
    return await get_user_by_email(email)