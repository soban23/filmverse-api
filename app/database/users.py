from app.database.connect_db import supabase
from app.models.users import User, User_Update
from uuid import UUID
from typing import Optional
from pydantic import EmailStr


async def insert_user(user: User):
    response = (
        supabase.table("users")
        .insert(
            {
                "name": user.name,
                "email": user.email,
                "username": user.username,
                "password": user.password,
                "avatar": user.avatar,
                "refresh_token": user.refresh_token,
            }
        )
        .execute()
    )
    return response.data


async def update_user(user: User_Update):
    response = supabase.rpc(
        "update_user_profile",
        {
            "p_user_id": str(user.user_id),
            "p_name": user.name,
            "p_email": user.email,
            "p_username": user.username,
            "p_password": user.password,
            "p_avatar": user.avatar,
        },
    ).execute()

    return response.data


async def delete_user(user_id: UUID):
    response = supabase.table("users").delete().eq("user_id", user_id).execute()
    return response.data


async def fetch_user(user_id: UUID):

    response = supabase.table("users").select("*").eq("user_id", user_id).execute()
    return response.data


async def fetch_user_by_email(email: EmailStr):

    response = supabase.table("users").select("*").eq("email", email).execute()
    return response.data


async def update_refresh_token(user_id: UUID, refresh_token: Optional[str] = None):
    response = (
        supabase.table("users")
        .update({"refresh_token": refresh_token})
        .eq("user_id", user_id)
        .execute()
    )

    return response.data


async def fetch_all_users():

    response = supabase.table("users").select("user_id, name, username").execute()
    return response.data
