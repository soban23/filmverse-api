import os


async def get_tmdb_creds():
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv("TMDB_API_KEY")}",
    }
    tmdb_site = os.getenv("TMDB_API_SITE")
    return {"headers": headers, "tmdb_site": tmdb_site}
