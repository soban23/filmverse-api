from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    password: str
    name: str
    username: str
    avatar: Optional[str] = None
    refresh_token: Optional[str] = None


class User_Update(BaseModel):
    user_id: Optional[UUID] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    avatar: Optional[str] = None
    refresh_token: Optional[str] = None


class Login_User(BaseModel):
    email: EmailStr
    password: str
