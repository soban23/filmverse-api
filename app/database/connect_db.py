import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()


try:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    supabase: Client = create_client(str(url), str(key))


except Exception as e:
    print(f"Failed to connect: {e}")
