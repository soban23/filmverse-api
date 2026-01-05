import os
import resend


async def send_email(user_email: str, user_name: str, movies: list):

    url = os.getenv("HDTODAY_WEBSITE_LINK", "https://hdtodayz.to")
    message = ""
    for movie in movies:
        message += f"\n{movie["movie_name"]} ({movie["year"]}) {movie["hdtoday_print"]} print available --> {url}/{movie["hdtoday_link"]}"

    resend.api_key = os.environ["RESEND_API_KEY"]

    params: resend.Emails.SendParams = {
        "from": "Filmayn Notification <onboarding@resend.dev>",
        "to": [f"{user_email}"],
        "subject": f"{user_name} new print available for watchlisted movie",
        "html": f"<div>{message}<div>",
    }

    email = resend.Emails.send(params)
    print(email)
