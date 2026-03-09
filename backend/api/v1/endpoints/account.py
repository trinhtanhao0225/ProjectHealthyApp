# backend/api/v1/endpoints/account.py
from fastapi import APIRouter, Body
from backend.schemas.account import AccountActionRequest, AccountActionResponse
from backend.services.account_service import execute_account_action

router = APIRouter(tags=["Account"])

@router.post("/action", response_model=AccountActionResponse)
async def account_action(request: AccountActionRequest = Body(...)):
    """
    Endpoint tổng hợp tất cả action cho Account (giống kiểu exercise)
    - action: get_all, register, login, get_by_email, update_password
    """
    result = await execute_account_action(request.dict())
    return AccountActionResponse(**result)