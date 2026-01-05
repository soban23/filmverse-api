from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.auth import verify_token
import re

PUBLIC_PATHS = {
    "/users/login",
    "/users/register",
    "/movies/trending",
    "/docs",
    "/openapi.json",
    "/users/all",
}


class CombinedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        print(f"[REQUEST] {request.method} {request.url.path}")

        # Check if path matches /movies/{number} pattern (public movie detail endpoint)
        movie_detail_pattern = re.match(r'^/movies/\d+$', request.url.path)
        
        if (
            request.url.path in PUBLIC_PATHS
            or request.url.path.startswith("/movies/popular")
            or request.url.path.startswith("/movies/toprated")
            or request.url.path.startswith("/movies/nowplaying")
            or request.url.path.startswith("/movies/search")
            or movie_detail_pattern
        ):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=401, content={"error": "Missing Authorization Header"}
            )

        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401, content={"error": "Invalid Authorization format"}
            )

        token = auth_header.split(" ")[1]

        decoded = await verify_token(token)
        if not decoded:
            return JSONResponse(
                status_code=401, content={"error": "Invalid or expired token"}
            )

        if decoded.get("new_access_token"):
            return JSONResponse(
                content={"new_access_token": decoded["new_access_token"]}
            )

        request.state.user_id = decoded["user_id"]
        request.state.username = decoded["username"]

        try:
            response = await call_next(request)
            return response
        except Exception as e:
            print(f"[Middleware Error] {e}")
            return JSONResponse(
                status_code=500, content={"error": "Internal Server Error"}
            )
