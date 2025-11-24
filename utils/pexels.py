import os
import requests
from dotenv import load_dotenv

# .env fayldan API kalitini yuklaymiz
load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def search_pexels(query: str, per_page: int = 10):
    """
    Pexels API orqali rasm qidiradi.
    query: qidiruv so‘zi (ingliz tilida bo‘lishi kerak)
    per_page: nechta rasm qaytarilishi (default 10)
    """
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            photos = data.get("photos", [])
            return [photo["src"]["medium"] for photo in photos]
        else:
            print(f"Pexels API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error searching Pexels: {e}")
        return []