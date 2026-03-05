from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from backend.core.config import settings
from backend.models.user import User
from backend.models.account import Account

async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URI)

    db = client[settings.MONGO_DB_NAME]

    await init_beanie(
        database=db,
        document_models=[
            User,
            Account
        ]
    )