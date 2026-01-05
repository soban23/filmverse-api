from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class Movie(BaseModel):
    movie_id: int
    hdtoday_link: Optional[str] = None
    hdtoday_print: Optional[str] = Field(default="NA", pattern="^(NA|CAM|HD)$")
    movie_name: Optional[str] = None
    poster: Optional[str] = None
    year: Optional[int] = None
