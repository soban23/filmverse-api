import requests
from bs4 import BeautifulSoup
import re
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_movie_data_hdtoday(film_name, film_year):
    try:
        film_name = (
            film_name.strip()
            .replace('"', "")
            .replace("'", "")
            .replace("“", "")
            .replace("”", "")
        )
        slug = re.sub(r"[^a-z0-9]+", "-", film_name.lower()).strip("-")
        base_url = os.getenv("HDTODAY_SEARCH_LINK", "https://hdtodayz.to/search/")
        url = f"{base_url}{slug}"
        print(f"url: {url}")
        req = requests.get(url)
        req.raise_for_status()
        soup = BeautifulSoup(req.content, "html.parser")

        films = soup.find_all("div", class_="flw-item")
        for film in films:
            title_tag = film.find("h2", class_="film-name")
            title = title_tag.a.text.strip() if title_tag and title_tag.a else None
            year_tag = film.find("span", class_="fdi-item")
            year = year_tag.text.strip() if year_tag else None
            type_tag = film.find("span", class_="fdi-type")
            film_type = type_tag.text.strip() if type_tag else None
            if film_type:
                film_type = film_type.lower()
            if title:
                title = title.lower()

            if (
                title == film_name.lower()
                and film_type == "movie"
                and str(year) == str(film_year)
            ):

                quality_tag = film.find("div", class_="pick")
                quality = quality_tag.get_text(strip=True) if quality_tag else None
                image_tag = film.find("img", class_="film-poster-img")
                image_url = image_tag["data-src"] if image_tag else None
                movie_tag = film.find("a", class_="film-poster-ahref")
                movie_url = movie_tag["href"] if movie_tag else None
                duration_tag = film.find("span", class_="fdi-duration")
                duration = duration_tag.get_text(strip=True) if duration_tag else None

                return {
                    "title": title,
                    "year": year,
                    "duration": duration,
                    "quality": quality,
                    "type": film_type,
                    "image_url": image_url,
                    "movie_url": movie_url,
                }

        return False
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        return False
