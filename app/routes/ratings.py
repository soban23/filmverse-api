from fastapi import APIRouter, Request
from app.database.ratings import (
    insert_rating,
    fetch_rating,
    delete_rating,
    update_rating,
    fetch_rated_movies_by_user_id,
)
from app.database.movies import update_movie
from app.models.ratings import Rating
from uuid import UUID
import os

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.get("/{user_id}/{movie_id}")
async def get_rating(user_id: UUID, movie_id: int):

    data = await fetch_rating(user_id, movie_id)

    return data


@router.post("/")
async def post_rating(rating: Rating, request: Request):

    rating.user_id = request.state.user_id
    data = await insert_rating(rating)
    if len(data):
        movie = await update_movie(rating.movie_id, rating.rating, 1)

    return data


@router.patch("/")
async def patch_ratings(rating: Rating, request: Request):

    rating.user_id = request.state.user_id
    old_rating = await fetch_rating(rating.user_id, rating.movie_id)

    data = await update_rating(rating)

    if len(data) and len(old_rating):
        old_rating = old_rating[0]["rating"]
        new_rating = data[0]["rating"]
        change_rating = new_rating - old_rating
        movie = await update_movie(rating.movie_id, change_rating, 0)

    return data


@router.delete("/{movie_id}")
async def del_rating(movie_id: int, request: Request):

    user_id = request.state.user_id
    data = await delete_rating(user_id, movie_id)

    if len(data):

        rating = data[0]["rating"]

        movie = await update_movie(movie_id, rating, -1)

    return data


@router.get("/{user_id}")
async def get_rated_movies_by_user_id(user_id: UUID):

    data = await fetch_rated_movies_by_user_id(user_id)

    return data
