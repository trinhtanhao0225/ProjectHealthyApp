# backend/schemas/chat.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatMessageRequest(BaseModel):
    message: str = Field(..., description="Tin nhắn người dùng gửi")
    email: Optional[str] = Field(None, description="Email người dùng")
    name: Optional[str] = Field(None, description="Tên người dùng")
    health_info: Optional[Dict[str, Any]] = Field(None, description="Thông tin sức khỏe")

class ChatMessageResponse(BaseModel):
    success: bool = True
    reply: str
    suggestions: List[str] = Field(default_factory=list)
    raw_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None