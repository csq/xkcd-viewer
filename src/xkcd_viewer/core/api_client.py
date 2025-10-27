import requests

from .db import DB
from .comic import Comic

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.connection = DB().get_conn()

    def get_comic_info(self, comic_num):
        response = requests.get(f"{self.base_url}{comic_num}/info.0.json")

        try:
            response = response.json()
        except requests.exceptions.JSONDecodeError:
            response = requests.get(f"{self.base_url}1969/info.0.json")
            response = response.json()

        comic = Comic(
            num=response["num"],
            month=response["month"],
            day=response["day"],
            year=response["year"],
            title=response["title"],
            alt=response["alt"],
            image_url=response["img"]
        )
        comic.save(self.connection)
        return response

    def get_latest_comic(self):
        response = requests.get(f"{self.base_url}/info.0.json")
        response.raise_for_status()
        response = response.json()
        comic = Comic(
            num=response["num"],
            month=response["month"],
            day=response["day"],
            year=response["year"],
            title=response["title"],
            alt=response["alt"],
            image_url=response["img"]
        )
        comic.save(self.connection)
        return response