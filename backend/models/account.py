# backend/models/account.py
from beanie import Document, Indexed
from pydantic import EmailStr
from typing import Annotated

EmailIndexed = Annotated[EmailStr, Indexed(unique=True)]

class Account(Document):
    email: EmailIndexed
    password: str

    class Settings:
        name = "Accounts"