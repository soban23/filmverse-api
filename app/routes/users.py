from fastapi import APIRouter, Request
from app.database.users import (
    insert_user,
    fetch_user,
    delete_user,
    update_user,
    update_refresh_token,
    fetch_user_by_email,
    fetch_all_users,
)
from app.models.users import User, User_Update, Login_User
from app.utils.auth import create_token
from uuid import UUID
import os
import bcrypt

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/all")
async def get_all_users():

    data = await fetch_all_users()

    return data


@router.get("/")
async def get_user(request: Request):

    user_id = request.state.user_id

    data = await fetch_user(user_id)

    return data


@router.post("/")
async def post_user(user: User):

    data = await insert_user(user)

    return data


@router.patch("/")
async def patch_user(user: User_Update, request: Request):

    user_id = request.state.user_id
    user.user_id = user_id
    if user.password:
        password_bytes = user.password.encode("utf-8")
        user.password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode()

    data = await update_user(user)

    return data


@router.delete("/")
async def del_user(request: Request):
    user_id = request.state.user_id
    data = await delete_user(user_id)

    return data


@router.post("/register")
async def register(user: User):
    try:
        password_bytes = user.password.encode("utf-8")
        user.password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode()

        data = await insert_user(user)
        if not len(data):
            return {"error": "Failed to create user"}

        user_row = data[0]

        access_token = await create_token(user_row["user_id"], user_row["username"], 60)
        refresh_token = await create_token(user_row["user_id"], user_row["username"], 300)

        await update_refresh_token(user_row["user_id"], refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "user_id": user_row["user_id"],
                "username": user_row["username"],
                "email": user_row["email"],
            },
        }
    except Exception as e:
        print(f"[Register Error] {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"Registration failed: {str(e)}"}


@router.post("/login")
async def login(login_user: Login_User):

    data = await fetch_user_by_email(login_user.email)
    if not len(data):
        return {"error": "Invalid credentials"}

    user_row = data[0]

    hashed = user_row["password"].encode("utf-8")
    password = login_user.password.encode("utf-8")

    if not bcrypt.checkpw(password, hashed):
        return {"error": "Invalid credentials"}

    access_token = await create_token(user_row["user_id"], user_row["username"], 60)
    refresh_token = await create_token(user_row["user_id"], user_row["username"], 300)

    await update_refresh_token(user_row["user_id"], refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "user_id": user_row["user_id"],
            "username": user_row["username"],
            "email": user_row["email"],
        },
    }
