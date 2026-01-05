from app.database.connect_db import supabase
from app.models.ratings import Rating
from uuid import UUID


async def insert_rating(rating: Rating):
    response = (
        supabase.table("ratings")
        .insert(
            {
                "movie_id": rating.movie_id,
                "user_id": str(rating.user_id),
                "rating": rating.rating,
            }
        )
        .execute()
    )
    return response.data


async def update_rating(rating: Rating):
    response = (
        supabase.table("ratings")
        .update({"rating": rating.rating})
        .eq("user_id", rating.user_id)
        .eq("movie_id", rating.movie_id)
        .execute()
    )

    return response.data


async def delete_rating(user_id: UUID, movie_id: int):
    response = (
        supabase.table("ratings")
        .delete()
        .eq("user_id", user_id)
        .eq("movie_id", movie_id)
        .execute()
    )
    return response.data


async def fetch_rating(user_id: UUID, movie_id: int):

    response = (
        supabase.table("ratings")
        .select("*")
        .eq("movie_id", movie_id)
        .eq("user_id", user_id)
        .execute()
    )
    return response.data


async def fetch_rated_movies_by_user_id(user_id: UUID):
    response = supabase.rpc(
        "fetch_rated_movies_by_user_id", {"p_user_id": str(user_id)}
    ).execute()

    return response.data
