from app.database.connect_db import supabase
from app.models.likes import Like
from uuid import UUID

async def insert_like(like: Like):
    response = (
        supabase.table("likes")
        .insert({
            "review_id": str(like.review_id),
            "user_id": str(like.user_id),
            "is_like": like.is_like
        })
        .execute()
    )
    return response.data

async def update_like(like: Like):
    response = (
    supabase.table("likes")
    .update({"is_like": like.is_like})
    .eq("review_id", like.review_id)
    .eq("user_id", like.user_id)
    .execute()
    )
    

    return response.data

async def delete_like(review_id: UUID, user_id: UUID):
    response = (
    supabase.table("likes")
    .delete()
    .eq("review_id", review_id)
    .eq("user_id", user_id)
    .execute()
    )
    return response.data



async def fetch_likes_by_user_id(user_id: UUID):
    response = (
    supabase.rpc("fetch_likes_by_user_id", { "p_user_id": str(user_id)})
    .execute()
)
    
    return response.data 

async def fetch_users_that_like_the_review(review_id: UUID):
    response = (
    supabase.rpc("fetch_users_that_like_the_review", { "p_review_id": str(review_id)})
    .execute()
)
    
    return response.data 