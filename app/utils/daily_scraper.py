from collections import defaultdict
from app.database.watchlist import (
    fetch_watchlist_for_notifications,
    update_watchlist_by_movie_id,
)
from app.database.movies import update_movie_print
from app.services.scrapers.scrape_hdtoday import get_movie_data_hdtoday
from app.utils.send_email import send_email


async def run_scraper():

    rows = await fetch_watchlist_for_notifications()

    users_by_movie_id = defaultdict(list)

    movies_by_id = {}

    for row in rows:
        movie_id = row["movie_id"]

        users_by_movie_id[movie_id].append(
            {
                "email": row["email"],
                "name": row["name"],
            }
        )

        movies_by_id[movie_id] = {
            "movie_name": row["movie_name"],
            "hdtoday_link": row["hdtoday_link"],
            "hdtoday_print": row["hdtoday_print"],
            "year": row["year"],
        }

    updated_movies = {}

    for movie_id, movie in movies_by_id.items():

        scrape_data = await get_movie_data_hdtoday(movie["movie_name"], movie["year"])

        if not scrape_data:
            continue

        scraped_link = scrape_data["movie_url"]
        scraped_quality = scrape_data["quality"]

        if movie["hdtoday_print"] != scraped_quality:
            updated_movies[movie_id] = {
                "movie_name": movie["movie_name"],
                "hdtoday_link": scraped_link,
                "hdtoday_print": scraped_quality,
                "year": movie["year"],
            }
            await update_movie_print(movie_id, scraped_quality, scraped_link)
            if scraped_quality == "HD":
                await update_watchlist_by_movie_id(False, movie_id)

    movies_for_user = defaultdict(lambda: {"name": None, "movies": []})

    for movie_id, user_list in users_by_movie_id.items():
        if movie_id in updated_movies:

            for user in user_list:
                email = user["email"]

                if movies_for_user[email]["name"] is None:
                    movies_for_user[email]["name"] = user["name"]

                movies_for_user[email]["movies"].append(updated_movies[movie_id])

    for email, data in movies_for_user.items():
        await send_email(email, data["name"], data["movies"])
