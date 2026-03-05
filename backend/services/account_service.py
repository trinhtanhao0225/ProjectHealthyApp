from fastapi import HTTPException
from typing import Dict, Any

from backend.models.account import Account
from backend.schemas.account import AccountResponse
from backend.utils.logger import logger


async def execute_account_action(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Xử lý tất cả action cho Account
    Các action hỗ trợ:
    - get_all
    - register
    - login
    - get_by_email
    - update_password
    """

    action = request.get("action")
    logger.info(f"Request data: {request}")
    result = {}

    try:
        logger.info(f"Account action called: {action}")

        # =========================
        # GET ALL ACCOUNTS
        # =========================
        if action == "get_all":

            accounts = await Account.find_all().to_list(100)

            result = {
                "accounts": [
                    AccountResponse.model_validate(acc).model_dump()
                    for acc in accounts
                ]
            }

        # =========================
        # REGISTER
        # =========================
        elif action == "register":

            email = request.get("email")
            password = request.get("password")

            if not email or not password:
                raise ValueError("Thiếu email hoặc password")

            exists = await Account.find_one(Account.email == email)

            if exists:
                raise HTTPException(
                    status_code=400,
                    detail="Email đã tồn tại"
                )

            account = Account(
                email=email,
                password=password  # TODO: hash password
            )

            await account.insert()

            result = {
                "email": email,
                "message": "Đăng ký thành công"
            }

        # =========================
        # LOGIN
        # =========================
        elif action == "login":

            email = request.get("email")
            password = request.get("password")

            if not email or not password:
                raise ValueError("Thiếu email hoặc password")

            account = await Account.find_one(Account.email == email)

            if not account or account.password != password:
                raise HTTPException(
                    status_code=401,
                    detail="Thông tin đăng nhập không đúng"
                )

            result = {
                "email": email,
                "message": "Đăng nhập thành công"
            }

        # =========================
        # GET ACCOUNT BY EMAIL
        # =========================
        elif action == "get_by_email":

            email = request.get("email")

            if not email:
                raise ValueError("Thiếu email")

            account = await Account.find_one(Account.email == email)

            if not account:
                raise HTTPException(
                    status_code=404,
                    detail="Không tìm thấy tài khoản"
                )

            result = AccountResponse.model_validate(account).model_dump()

        # =========================
        # UPDATE PASSWORD
        # =========================
        elif action == "update_password":

            email = request.get("email")
            new_password = request.get("new_password")

            if not email or not new_password:
                raise ValueError("Thiếu email hoặc new_password")

            account = await Account.find_one(Account.email == email)

            if not account:
                raise HTTPException(
                    status_code=404,
                    detail="Không tìm thấy tài khoản"
                )

            account.password = new_password  # TODO: hash password
            await account.save()

            result = {
                "message": "Cập nhật mật khẩu thành công"
            }

        else:
            raise ValueError("Sai action")

        logger.info(f"Account action {action} completed")

        return {
            "status": "success",
            "data": result
        }

    except HTTPException as he:

        logger.warning(f"Account action failed: {he.detail}")

        return {
            "status": "error",
            "message": he.detail
        }

    except Exception as e:

        logger.error(f"Account action error: {str(e)}")

        return {
            "status": "error",
            "message": str(e)
        }