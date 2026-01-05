from fastapi import APIRouter, Request
from app.database.likes import (
    insert_like,
    delete_like,
    update_like,
    fetch_likes_by_user_id,
    fetch_users_that_like_the_review,
)
from app.database.reviews import update_review_likes, fetch_review_by_review_id
from app.models.likes import Like
from uuid import UUID
import os

router = APIRouter(prefix="/likes", tags=["likes"])


@router.get("/user_id/{user_id}")
async def get_likes_by_user_id(user_id: UUID):

    data = await fetch_likes_by_user_id(user_id)

    return data


@router.post("/")
async def post_like(like: Like, request: Request):

    like.user_id = request.state.user_id
    data = await insert_like(like)
    if len(data):
        review_id = data[0]["review_id"]
        review = await fetch_review_by_review_id(review_id)
        if len(review):
            likes = review[0]["likes"]
            dislikes = review[0]["dislikes"]
            if like.is_like:
                likes = likes + 1
            else:
                dislikes = dislikes + 1

            updated_review = await update_review_likes(review_id, likes, dislikes)

    return data


@router.patch("/")
async def patch_likes(like: Like, request: Request):

    like.user_id = request.state.user_id
    old_data = await fetch_likes_by_user_id(like.user_id)
    if len(old_data):
        if old_data[0]["is_like"] == like.is_like:
            return old_data
        data = await update_like(like)
        if len(data):
            review_id = data[0]["review_id"]
            review = await fetch_review_by_review_id(review_id)
            if len(review):
                likes = review[0]["likes"]
                dislikes = review[0]["dislikes"]
                if like.is_like:
                    likes = likes + 1
                    dislikes = dislikes - 1
                else:
                    likes = likes - 1
                    dislikes = dislikes + 1

                updated_review = await update_review_likes(review_id, likes, dislikes)

    return data


@router.delete("/{review_id}")
async def del_like(review_id: UUID, request: Request):

    user_id = request.state.user_id
    data = await delete_like(review_id, user_id)
    if len(data):
        review_id = data[0]["review_id"]
        review = await fetch_review_by_review_id(review_id)
        if len(review):
            likes = review[0]["likes"]
            dislikes = review[0]["dislikes"]
            if data[0]["is_like"]:
                likes = likes - 1
            else:
                dislikes = dislikes - 1

            updated_review = await update_review_likes(review_id, likes, dislikes)

    return data


@router.get("review_id/{review_id}")
async def get_users_that_like_the_review(review_id: UUID):

    data = await fetch_users_that_like_the_review(review_id)

    return data
