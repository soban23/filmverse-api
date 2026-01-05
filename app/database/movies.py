from app.database.connect_db import supabase
from app.models.movies import Movie
from uuid import UUID


async def update_movie_print(movie_id: int, hdtoday_print: str, hdtoday_link: str):
    response = (
        supabase.table("movies")
        .update({"hdtoday_print": hdtoday_print, "hdtoday_link": hdtoday_link})
        .eq("movie_id", movie_id)
        .execute()
    )

    return response.data


async def insert_movie(movie: Movie):

    response = (
        supabase.table("movies")
        .insert(
            {
                "movie_id": movie.movie_id,
                "movie_name": movie.movie_name,
                "poster": movie.poster,
                "hdtoday_link": movie.hdtoday_link,
                "hdtoday_print": movie.hdtoday_print,
                "year": movie.year,
            }
        )
        .execute()
    )
    return response


async def get_movie_details(movie_id: int):

    response = supabase.table("movies").select("*").eq("movie_id", movie_id).execute()

    return response


async def update_movie(movie_id: int, rating: int, flag: int):

    old = (
        supabase.table("movies")
        .select("accumalated_rating, num_of_ratings")
        .eq("movie_id", movie_id)
        .execute()
    )

    if not len(old.data):
        return f"movie doesnt exist"
    old = old.data[0]
    old_acc = old["accumalated_rating"]
    old_count = old["num_of_ratings"]

    if flag == 1:
        new_acc = old_acc + rating
        new_count = old_count + 1
    elif flag == -1:
        new_acc = old_acc - rating
        new_count = old_count - 1
    else:
        new_acc = old_acc + rating
        new_count = old_count

    response = (
        supabase.table("movies")
        .update({"accumalated_rating": new_acc, "num_of_ratings": new_count})
        .eq("movie_id", movie_id)
        .execute()
    )

    return response
