# backend/api/v1/endpoints/chat.py
from fastapi import APIRouter, Body, HTTPException
from backend.schemas.chat import ChatMessageRequest, ChatMessageResponse
from backend.modules.rag.runner import run_food_search 
from backend.utils.logger import logger
from typing import Dict, Any, List, Optional
router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/message", response_model=ChatMessageResponse)
async def send_message(request: ChatMessageRequest = Body(...)):
    """
    Gửi tin nhắn và nhận phản hồi từ RAG (gọi trực tiếp run_food_search như test_rag.py)
    """
    try:
        logger.info(f"Chat message: '{request.message}' | User: {request.email or 'guest'}")

        # Chuẩn bị user_info cho RAG (giống test_rag.py)
        user_info = {
            "email": request.email or "guest",
            "name": request.name or "User",
            "health_info": request.health_info or {}
        }

        # Gọi thẳng run_food_search (không subprocess, không file temp)
        rag_result = run_food_search(
            query=request.message,
            user_info=user_info
        )

        # Xử lý reply (dựa trên output của run_food_search)
        reply = ""
        if rag_result.get("error"):
            reply = rag_result["error"]
        elif rag_result.get("summary"):
            reply = rag_result["summary"]
        elif rag_result.get("status") == "success":
            reply = rag_result.get("summary") or "Không tìm thấy thông tin. Vui lòng thử lại với từ khóa khác."
        else:
            reply = "Không thể xử lý yêu cầu. Vui lòng thử lại với từ khóa cụ thể hơn."

        # Generate suggestions (giữ nguyên logic cũ)
        suggestions = generate_suggestions(request.message)

        return ChatMessageResponse(
            success=True,
            reply=reply.strip(),
            suggestions=suggestions,
            raw_data=rag_result,
        )

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return ChatMessageResponse(
            success=False,
            reply="❌ Lỗi xử lý tin nhắn. Vui lòng thử lại.\n\nGợi ý: Hỏi về thực phẩm cụ thể như 'cá hồi', 'rau xanh', 'gạo lứt'.",
            suggestions=[
                "Cá hồi có những chất gì?",
                "Thực phẩm tốt cho tim mạch",
                "Món ăn từ rau xanh"
            ],
            error=str(e)
        )

def generate_suggestions(message: str) -> List[str]:
    msg = message.lower()
    suggestions = []

    if any(kw in msg for kw in ["dinh dưỡng", "calo", "đạm"]):
        suggestions.append("Gợi ý thực phẩm thay thế")

    if any(kw in msg for kw in ["dị ứng", "bệnh"]):
        suggestions.append("Thực phẩm an toàn khác")

    if any(kw in msg for kw in ["giảm cân", "tăng cân"]):
        suggestions.append("Kế hoạch ăn chi tiết")

    if not suggestions:
        suggestions = ["Thực phẩm tương tự", "Cách chế biến", "Kế hoạch ăn hôm nay"]

    return suggestions[:3]