from fastapi import APIRouter, Request
from app.database.watchlist import (
    insert_watchlist,
    fetch_watchlist,
    delete_watchlist,
    update_watchlist,
    fetch_watchlist_by_user_id,
)
from app.database.movies import get_movie_details
from app.models.watchlist import Watchlist
from uuid import UUID
import os

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])


@router.get("/{user_id}/{movie_id}")
async def get_watchlist(user_id: UUID, movie_id: int):

    data = await fetch_watchlist(user_id, movie_id)

    return data


@router.post("/")
async def post_watchlist(watchlist: Watchlist, request: Request):

    watchlist.user_id = request.state.user_id
    movie_details = await get_movie_details(watchlist.movie_id)
    movie_details = movie_details.data

    if len(movie_details) and movie_details[0]["hdtoday_print"] == "HD":
        watchlist.notification_flag = False
    data = await insert_watchlist(watchlist)

    return data


@router.patch("/")
async def patch_watchlist(watchlist: Watchlist, request: Request):

    watchlist.user_id = request.state.user_id
    movie_details = await get_movie_details(watchlist.movie_id)
    movie_details = movie_details.data
    if len(movie_details) and movie_details[0]["hdtoday_print"] == "HD":
        watchlist.notification_flag = False

    data = await update_watchlist(
        watchlist.notification_flag, watchlist.user_id, watchlist.movie_id
    )

    return data


@router.delete("/{movie_id}")
async def del_watchlist(movie_id: int, request: Request):

    user_id = request.state.user_id
    data = await delete_watchlist(user_id, movie_id)

    return data


@router.get("/{user_id}")
async def get_watchlist_by_user_id(user_id: UUID):

    data = await fetch_watchlist_by_user_id(user_id)

    return data
