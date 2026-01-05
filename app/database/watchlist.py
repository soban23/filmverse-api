from app.database.connect_db import supabase
from app.models.watchlist import Watchlist
from uuid import UUID


async def insert_watchlist(watchlist: Watchlist):
    response = (
        supabase.table("watchlist")
        .insert(
            {
                "movie_id": watchlist.movie_id,
                "user_id": str(watchlist.user_id),
                "notification_flag": watchlist.notification_flag,
            }
        )
        .execute()
    )
    return response.data


async def update_watchlist(notification_flag: bool, user_id: UUID, movie_id: int):
    response = (
        supabase.table("watchlist")
        .update({"notification_flag": notification_flag})
        .eq("user_id", user_id)
        .eq("movie_id", movie_id)
        .execute()
    )

    return response.data


async def delete_watchlist(user_id: UUID, movie_id: int):
    response = (
        supabase.table("watchlist")
        .delete()
        .eq("user_id", user_id)
        .eq("movie_id", movie_id)
        .execute()
    )
    return response.data


async def update_watchlist_by_movie_id(notification_flag: bool, movie_id: int):
    response = (
        supabase.table("watchlist")
        .update({"notification_flag": notification_flag})
        .eq("movie_id", movie_id)
        .execute()
    )

    return response.data


async def fetch_watchlist(user_id: UUID, movie_id: int):

    response = (
        supabase.table("watchlist")
        .select("*")
        .eq("movie_id", movie_id)
        .eq("user_id", user_id)
        .execute()
    )
    return response.data


async def fetch_watchlist_by_user_id(user_id: UUID):
    response = supabase.rpc(
        "fetch_watchlist_by_user_id", {"p_user_id": str(user_id)}
    ).execute()

    return response.data


async def fetch_watchlist_for_notifications():

    response = supabase.rpc("fetch_watchlist_for_notifications").execute()

    return response.data
