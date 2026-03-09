from fastapi import APIRouter, Body, Path
from backend.schemas.chat import ChatMessageRequest, ChatMessageResponse
from backend.services.chat_service import (
    process_chat_message,
    get_chat_history_service,
    delete_chat_history_service
)

router = APIRouter(tags=["Chat"])


# =========================
# SEND MESSAGE
# =========================
@router.post("/message", response_model=ChatMessageResponse)
async def send_message(request: ChatMessageRequest = Body(...)):
    return await process_chat_message(request)


# =========================
# GET CHAT HISTORY
# =========================
@router.get("/history/{email}")
async def get_chat_history(email: str = Path(...)):
    return await get_chat_history_service(email)


# =========================
# DELETE CHAT HISTORY
# =========================
@router.delete("/history/{email}")
async def delete_chat_history(email: str = Path(...)):
    return await delete_chat_history_service(email)