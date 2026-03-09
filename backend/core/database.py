from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from backend.core.config import settings
from backend.models.user import User
from backend.models.account import Account
from backend.models.chat_history import ChatHistory
from backend.models.exercise_detail import ExerciseDetail
from backend.models.exercise_group import ExerciseGroup
from backend.models.food import Food
from backend.models.workout_plan import WorkoutPlan
async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URI)

    db = client[settings.MONGO_DB_NAME]

    await init_beanie(
        database=db,
        document_models=[
            User,
            Account,
            ChatHistory,
            ExerciseDetail,
            ExerciseGroup,
            Food,
            WorkoutPlan
        ]
    )