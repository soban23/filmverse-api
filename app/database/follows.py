from app.database.connect_db import supabase
from app.models.follows import Follow
from uuid import UUID


async def insert_follow(follow: Follow):

    response = (
        supabase.table("follows")
        .insert(
            {
                "follower_id": str(follow.follower_id),
                "following_id": str(follow.following_id),
            }
        )
        .execute()
    )
    return response.data


async def delete_follow(follow: Follow):
    response = (
        supabase.table("follows")
        .delete()
        .eq("following_id", str(follow.following_id))
        .eq("follower_id", str(follow.follower_id))
        .execute()
    )
    return response.data


async def fetch_follow(follow: Follow):
    response = (
        supabase.table("follows")
        .select("*")
        .eq("following_id", follow.following_id)
        .eq("follower_id", follow.follower_id)
        .execute()
    )
    return response.data


async def fetch_followers(user_id: UUID):
    response = (
        supabase.table("follows")
        .select("*, users:follower_id(*)")
        .eq("following_id", user_id)
        .execute()
    )
    return response.data


async def fetch_followings(user_id: UUID):
    response = (
        supabase.table("follows")
        .select("*, users:following_id(*)")
        .eq("follower_id", user_id)
        .execute()
    )
    return response.data


async def fetch_what_followings_rated_the_movie(user_id: UUID, movie_id: int):
    response = supabase.rpc(
        "fetch_what_followings_rated_the_movie",
        {"p_user_id": str(user_id), "p_movie_id": movie_id},
    ).execute()

    return response.data


async def fetch_what_followings_watchlisted_the_movie(user_id: UUID, movie_id: int):
    response = supabase.rpc(
        "fetch_what_followings_watchlisted_the_movie",
        {"p_user_id": str(user_id), "p_movie_id": movie_id},
    ).execute()

    return response.data
