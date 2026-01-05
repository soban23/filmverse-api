from fastapi import APIRouter, Request
from app.database.reviews import (
    insert_review,
    delete_review,
    update_review,
    fetch_reviews_by_movie_id,
    fetch_reviews_by_user_id,
    fetch_review_by_review_id,
)
from app.models.reviews import Review
from uuid import UUID
import os

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/movie_id/{movie_id}")
async def get_review_by_movie_id(movie_id: int):

    data = await fetch_reviews_by_movie_id(movie_id)

    return data


@router.get("/review_id/{review_id}")
async def get_review_by_review_id(review_id: UUID):

    data = await fetch_review_by_review_id(review_id)

    return data


@router.get("/user_id/{user_id}")
async def get_review_by_user_id(user_id: UUID):

    data = await fetch_reviews_by_user_id(user_id)

    return data


@router.post("/")
async def post_review(review: Review, request: Request):

    review.user_id = request.state.user_id
    data = await insert_review(review)

    return data


@router.patch("/")
async def patch_reviews(review_id: UUID, message: str):

    data = await update_review(review_id, message)

    return data


@router.delete("/{review_id}")
async def del_review(review_id: UUID):

    data = await delete_review(review_id)

    return data
