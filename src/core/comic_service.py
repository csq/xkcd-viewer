import random

from core.comic import Comic
from core.api_client import APIClient

class ComicService:
    def __init__(self, base_url):
        self.api_client = APIClient(base_url)
        self.last_id = self._get_latest_id()

    def get_comic_with_id(self, comic_id):
        self.last_id = comic_id
        comic_info = self.api_client.get_comic_info(comic_id)

        return Comic(
            id=comic_info["num"],
            month=comic_info["month"],
            day=comic_info["day"],
            year=comic_info["year"],
            title=comic_info["title"],
            alt=comic_info["alt"],
            image_url=comic_info["img"]
        )

    def _get_latest_id(self):
        comic_info = self.api_client.get_latest_comic()
        return comic_info["num"]
    
    def get_random_comic(self):
        latest_id = self._get_latest_id()
        comic_id = random.randint(1, latest_id)

        self.last_id = comic_id

        comic_info = self.api_client.get_comic_info(comic_id)

        return Comic(
            id=comic_info["num"],
            month=comic_info["month"],
            day=comic_info["day"],
            year=comic_info["year"],
            title=comic_info["title"],
            alt=comic_info["alt"],
            image_url=comic_info["img"]
        )

    def get_first_comic(self):
        self.last_id = 1
        comic_info = self.api_client.get_comic_info(1)

        return Comic(
            id=comic_info["num"],
            month=comic_info["month"],
            day=comic_info["day"],
            year=comic_info["year"],
            title=comic_info["title"],
            alt=comic_info["alt"],
            image_url=comic_info["img"]
        )
    
    def get_last_comic(self):
        self.last_id = self._get_latest_id()
        comic_info = self.api_client.get_latest_comic()

        return Comic(
            id=comic_info["num"],
            month=comic_info["month"],
            day=comic_info["day"],
            year=comic_info["year"],
            title=comic_info["title"],
            alt=comic_info["alt"],
            image_url=comic_info["img"]
        )
    
    def get_next_comic(self):
        self.last_id = self.last_id + 1

        if self.last_id > self._get_latest_id():
            self.last_id = self._get_latest_id()

        comic_info = self.api_client.get_comic_info(self.last_id)

        return Comic(
            id=comic_info["num"],
            month=comic_info["month"],
            day=comic_info["day"],
            year=comic_info["year"],
            title=comic_info["title"],
            alt=comic_info["alt"],
            image_url=comic_info["img"]
        )
    
    def get_previous_comic(self):
        self.last_id = self.last_id - 1

        if self.last_id < 1:
            self.last_id = 1

        comic_info = self.api_client.get_comic_info(self.last_id)

        return Comic(
            id=comic_info["num"],
            month=comic_info["month"],
            day=comic_info["day"],
            year=comic_info["year"],
            title=comic_info["title"],
            alt=comic_info["alt"],
            image_url=comic_info["img"]
        )