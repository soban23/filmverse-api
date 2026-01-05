import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from app.database.users import fetch_user, update_refresh_token
import os


SECRET_KEY = f"{os.getenv("SECRET_KEY")}"
ALGORITHM = "HS256"


async def create_token(user_id, username, time):

    exp_time = datetime.now(timezone.utc) + timedelta(minutes=time)
    payload = {
        "user_id": str(user_id),
        "username": username,
        "exp": exp_time,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_without_exp(token):
    return jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False}
    )


async def verify_token(token):
    try:

        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded

    except ExpiredSignatureError:

        decoded = decode_without_exp(token)

        user = await fetch_user(decoded["user_id"])
        if not len(user):
            return False

        user = user[0]

        if user["refresh_token"]:
            new_access = await create_token(decoded["user_id"], decoded["username"], 60)
            return {"new_access_token": new_access}

        return False

    except InvalidTokenError:
        return False


async def logout(user_id):
    result = await update_refresh_token(user_id, None)
    return bool(len(result))
