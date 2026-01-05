import requests

from app.tmdb_creds import get_tmdb_creds


async def get_popular_movies(page_number: int):
    tmdb_creds = await get_tmdb_creds()
    tmdb_site = tmdb_creds["tmdb_site"]
    headers = tmdb_creds["headers"]

    url = f"{tmdb_site}discover/movie?include_adult=false&include_video=false&language=en-US&page={page_number}&sort_by=popularity.desc"

    response = requests.get(url, headers=headers)

    return response.json()


async def search_movies(movie_name: str):

    tmdb_creds = await get_tmdb_creds()
    tmdb_site = tmdb_creds["tmdb_site"]
    headers = tmdb_creds["headers"]

    url = f"{tmdb_site}search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"

    response = requests.get(url, headers=headers)

    return response.json()


async def get_movie_details_by_id(movie_id: int):

    tmdb_creds = await get_tmdb_creds()
    tmdb_site = tmdb_creds["tmdb_site"]
    headers = tmdb_creds["headers"]

    url = f"{tmdb_site}movie/{movie_id}?language=en-US"

    response = requests.get(url, headers=headers)

    return response.json()


async def now_playing(page_number: int):
    tmdb_creds = await get_tmdb_creds()
    tmdb_site = tmdb_creds["tmdb_site"]
    headers = tmdb_creds["headers"]

    url = f"{tmdb_site}movie/now_playing?language=en-US&page={page_number}"

    response = requests.get(url, headers=headers)

    return response.json()


async def top_rated(page_number: int):
    tmdb_creds = await get_tmdb_creds()
    tmdb_site = tmdb_creds["tmdb_site"]
    headers = tmdb_creds["headers"]

    url = f"{tmdb_site}movie/top_rated?language=en-US&page={page_number}"

    response = requests.get(url, headers=headers)

    return response.json()


async def trending():
    tmdb_creds = await get_tmdb_creds()
    tmdb_site = tmdb_creds["tmdb_site"]
    headers = tmdb_creds["headers"]

    url = f"{tmdb_site}trending/movie/day?language=en-US"

    response = requests.get(url, headers=headers)

    return response.json()


async def recommendations(movie_id: int):
    tmdb_creds = await get_tmdb_creds()
    tmdb_site = tmdb_creds["tmdb_site"]
    headers = tmdb_creds["headers"]

    url = f"{tmdb_site}movie/{movie_id}/recommendations?language=en-US&page=1"

    response = requests.get(url, headers=headers)

    return response.json()
