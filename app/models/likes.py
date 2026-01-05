from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class Like(BaseModel):
    review_id: UUID
    user_id: Optional[UUID] = None
    is_like: bool
