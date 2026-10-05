import os
import requests
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


class SpotifyAPI:

    def __init__(self):

        if not YOUTUBE_API_KEY:
            raise ValueError(
                "YouTube API Key is missing in .env"
            )

        self.api_key = YOUTUBE_API_KEY

    def search_songs(self, query, limit=10):

        url = "https://www.googleapis.com/youtube/v3/search"

        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "videoCategoryId": "10",
            "maxResults": limit,
            "key": self.api_key
        }

        try:

            response = requests.get(
                url,
                params=params,
                timeout=15
            )

            if response.status_code != 200:

                print("YouTube API Error:")
                print(response.status_code)
                print(response.text)

                return []

            data = response.json()

            songs = []

            for item in data.get("items", []):

                video_id = item["id"]["videoId"]
                snippet = item["snippet"]

                songs.append({
                    "name": snippet["title"],
                    "artist": snippet["channelTitle"],
                    "album": "YouTube Music",
                    "image": snippet["thumbnails"]["high"]["url"],
                    "spotify_url": f"https://www.youtube.com/watch?v={video_id}",
                    "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                    "video_id": video_id,
                    "preview_url": None
                })

            return songs

        except Exception as error:

            print("YouTube API Error:", error)

            return []

    def get_recommendations(self, genre, limit=10):

        return self.search_songs(
            query=genre,
            limit=limit
        )