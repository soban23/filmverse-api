from fastapi import APIRouter, Request
from app.database.follows import (
    insert_follow,
    fetch_follow,
    delete_follow,
    fetch_what_followings_rated_the_movie,
    fetch_what_followings_watchlisted_the_movie,
)
from app.models.follows import Follow
from uuid import UUID
import os

router = APIRouter(prefix="/follows", tags=["follows"])


@router.get("/{follower_id}/{following_id}")
async def get_follow(follower_id: UUID, following_id: UUID):
    follow = Follow(follower_id=follower_id, following_id=following_id)
    data = await fetch_follow(follow)

    return data


@router.post("/")
async def post_follow(follow: Follow, request: Request):

    follow.follower_id = request.state.user_id
    data = await insert_follow(follow)

    return data


@router.delete("/{following_id}")
async def del_follow(following_id: UUID, request: Request):
    follower_id = request.state.user_id
    follow = Follow(follower_id=follower_id, following_id=following_id)
    data = await delete_follow(follow)

    return data


@router.get("/ratings/{user_id}/{movie_id}")
async def get_what_followings_rated_the_movie(user_id: UUID, movie_id: int):

    data = await fetch_what_followings_rated_the_movie(user_id, movie_id)

    return data


@router.get("/watchlist/{user_id}/{movie_id}")
async def get_what_followings_watchlisted_the_movie(user_id: UUID, movie_id: int):

    data = await fetch_what_followings_watchlisted_the_movie(user_id, movie_id)

    return data
