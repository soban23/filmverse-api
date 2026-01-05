from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class Review(BaseModel):
    movie_id: int
    user_id: Optional[UUID] = None
    message: str
