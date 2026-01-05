from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import (
    movies,
    users,
    follows,
    watchlist,
    ratings,
    reviews,
    likes,
    scrape,
)
from app.database.connect_db import supabase
from .middleware import CombinedMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(CombinedMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],  # Vite default port
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.include_router(users.router)
app.include_router(movies.router)
app.include_router(follows.router)
app.include_router(watchlist.router)
app.include_router(ratings.router)
app.include_router(reviews.router)
app.include_router(likes.router)
app.include_router(scrape.router)


@app.get("/")
def home():
    return {"message": "FastAPI backend working"}
