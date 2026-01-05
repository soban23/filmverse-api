from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class Rating(BaseModel):
    movie_id: int
    user_id: Optional[UUID] = None
    rating: int = Field(..., ge=1, le=10)
