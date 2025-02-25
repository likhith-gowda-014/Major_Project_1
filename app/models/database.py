from supabase import create_client
from config.config import config

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def get_users():
    response = supabase.table("users").select("*").execute()
    return response.data
