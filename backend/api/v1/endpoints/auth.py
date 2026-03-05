from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def auth_status():
    return {"auth": "basic", "message": "Chưa triển khai full auth"}