from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class Follow(BaseModel):
    follower_id: Optional[UUID] = None
    following_id: UUID
