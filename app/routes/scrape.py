from fastapi import APIRouter, Request
from app.utils.daily_scraper import run_scraper
from uuid import UUID
import os

router = APIRouter(prefix="/scrape", tags=["Scrape"])


@router.get("/")
async def scraper(request: Request):

    user_id = request.state.user_id
    admin_id = os.getenv("ADMIN_UUID")

    if user_id != admin_id:
        return False
    data = await run_scraper()
    return data
