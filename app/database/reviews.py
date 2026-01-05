from app.database.connect_db import supabase
from app.models.reviews import Review
from uuid import UUID


async def insert_review(review: Review):
    response = (
        supabase.table("reviews")
        .insert(
            {
                "movie_id": review.movie_id,
                "user_id": str(review.user_id),
                "message": review.message,
            }
        )
        .execute()
    )
    return response.data


async def update_review(review_id: UUID, message: str):
    response = (
        supabase.table("reviews")
        .update({"message": message})
        .eq("review_id", review_id)
        .execute()
    )

    return response.data


async def delete_review(review_id: UUID):
    response = supabase.table("reviews").delete().eq("review_id", review_id).execute()
    return response.data


async def fetch_review_by_review_id(review_id: UUID):
    response = (
        supabase.table("reviews").select("*").eq("review_id", review_id).execute()
    )
    return response.data


async def fetch_reviews_by_movie_id(movie_id: int):
    response = supabase.rpc(
        "fetch_reviews_by_movie_id", {"p_movie_id": movie_id}
    ).execute()
    return response.data


async def fetch_reviews_by_user_id(user_id: UUID):
    response = supabase.rpc(
        "fetch_reviews_by_user_id", {"p_user_id": str(user_id)}
    ).execute()
    return response.data


async def update_review_likes(review_id: UUID, likes: int, dislikes: int):
    response = (
        supabase.table("reviews")
        .update({"likes": likes, "dislikes": dislikes})
        .eq("review_id", review_id)
        .execute()
    )

    return response.data
