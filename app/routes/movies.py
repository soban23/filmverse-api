from fastapi import APIRouter
from app.services.tmdb_service import (
    get_popular_movies,
    search_movies,
    get_movie_details_by_id,
    top_rated,
    trending,
    recommendations,
    now_playing,
)
from app.services.scrapers.scrape_hdtoday import get_movie_data_hdtoday
from app.database.movies import get_movie_details, insert_movie
from app.models.movies import Movie
from app.utils.daily_scraper import run_scraper
from uuid import UUID
import os

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/popular/{page_number}")
async def popular_movies(page_number: int = 1):
    if page_number < 1 or page_number > 500:
        return False
    data = await get_popular_movies(page_number)

    return data


@router.get("/toprated/{page_number}")
async def toprated_movies(page_number: int = 1):
    if page_number < 1 or page_number > 500:
        return False
    data = await top_rated(page_number)

    return data


@router.get("/trending")
async def trending_movies():

    data = await trending()

    return data


@router.get("/nowplaying/{page_number}")
async def nowplaying_movies(page_number: int = 1):
    if page_number < 1 or page_number > 500:
        return False
    data = await now_playing(page_number)

    return data


@router.get("/recommendations/{movie_id}")
async def recommend_movies(movie_id: int):

    data = await recommendations(movie_id)

    return data


@router.get("/{movie_id}")
async def get_movie(movie_id: int):

    movie_details = await get_movie_details_by_id(movie_id)

    movie_details_from_db = await get_movie_details(movie_id)

    if not len(movie_details_from_db.data):

        movie_name = movie_details["original_title"]
        date_string = movie_details["release_date"]
        movie_year = date_string[:4]

        if not movie_name or not movie_year:
            return {"error:": "movie year or name not available"}

        scrape_data = await get_movie_data_hdtoday(movie_name, movie_year)

        movie_data_for_db = Movie(
            movie_id=movie_id,
            poster=f"{os.getenv("TMDB_IMAGE_PATH")}{movie_details["poster_path"]}",
            movie_name=movie_details["original_title"],
            year=int(movie_year),
        )
        if scrape_data:
            hdtoday_movie_url = scrape_data["movie_url"]
            hdtoday_movie_print = scrape_data["quality"]
            movie_data_for_db.hdtoday_link = hdtoday_movie_url
            movie_data_for_db.hdtoday_print = hdtoday_movie_print

        inserted_movie = await insert_movie(movie_data_for_db)

        movie_details_from_db = inserted_movie.data[0]

    else:
        movie_details_from_db = movie_details_from_db.data[0]

    if movie_details_from_db["hdtoday_link"]:
        url = os.getenv("HDTODAY_WEBSITE_LINK", "https://hdtodayz.to")

        movie_details_from_db["hdtoday_link"] = (
            f"{url}{movie_details_from_db["hdtoday_link"]}"
        )

    rating = 0
    if (
        movie_details_from_db["accumalated_rating"]
        and movie_details_from_db["num_of_ratings"]
    ):
        rating = (
            movie_details_from_db["accumalated_rating"]
            / movie_details_from_db["num_of_ratings"]
        )

    movie_details_from_db["rating"] = rating
    movie_details["db_data"] = movie_details_from_db
    movie_details["tmdb_image_path"] = os.getenv("TMDB_IMAGE_PATH")

    return movie_details


@router.get("/search/{movie_name}")
async def get_search_movies(movie_name: str):
    if movie_name:
        data = await search_movies(movie_name)
        return data
    return f"not enough params"
