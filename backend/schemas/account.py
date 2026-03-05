# backend/schemas/account.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict  # ← Thêm import Dict ở đây

# Phần CRUD cũ (đăng ký, login, response)
class AccountCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Mật khẩu tối thiểu 6 ký tự")

class AccountLogin(BaseModel):
    email: EmailStr
    password: str

class AccountResponse(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True  # Hỗ trợ chuyển từ MongoDB document

# Phần Action-based mới (giống exercise)
class AccountActionRequest(BaseModel):
    action: str = Field(..., description="Hành động: get_all, register, login, get_by_email, update_password")
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    new_password: Optional[str] = None

class AccountActionResponse(BaseModel):
    status: str = "success"
    data: Optional[Dict] = None  # ← Dict đã được import từ typing
    message: Optional[str] = None