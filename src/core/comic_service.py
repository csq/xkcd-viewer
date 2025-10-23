import random

from core.comic import Comic
from core.api_client import APIClient
from utils.cache import Cache

class ComicService:
    def __init__(self, base_url):
        self.api_client = APIClient(base_url)
        self.last_num = self._get_latest_num()

    def _get_from_cache(self, num):
        self.last_num = int(num)
        return Cache().get_from_cache(num)

    def get_comic_with_num(self, comic_num):
        cache = self._get_from_cache(comic_num)

        if cache is not None:
            return cache

        comic_info = self.api_client.get_comic_info(comic_num)
        self.last_num = comic_info["num"]

        return Comic(
            num=comic_info["num"],
            month=comic_info["month"],
            day=comic_info["day"],
            year=comic_info["year"],
            title=comic_info["title"],
            alt=comic_info["alt"],
            image_url=comic_info["img"]
        )

    def _get_latest_num(self):
        comic_info = self.api_client.get_latest_comic()
        return comic_info["num"]

    def get_random_comic(self):
        latest_num = self._get_latest_num()
        comic_num = random.randint(1, latest_num)

        self.last_num = comic_num

        cache = self._get_from_cache(self.last_num)

        if cache is not None:
            return cache

        comic_info = self.api_client.get_comic_info(comic_num)

        return Comic(
            num=comic_info["num"],
            month=comic_info["month"],
            day=comic_info["day"],
            year=comic_info["year"],
            title=comic_info["title"],
            alt=comic_info["alt"],
            image_url=comic_info["img"]
        )

    def get_first_comic(self):
        self.last_num = 1

        cache = self._get_from_cache(self.last_num)

        if cache is not None:
            return cache

        comic_info = self.api_client.get_comic_info(1)

        return Comic(
            num=comic_info["num"],
            month=comic_info["month"],
            day=comic_info["day"],
            year=comic_info["year"],
            title=comic_info["title"],
            alt=comic_info["alt"],
            image_url=comic_info["img"]
        )
    
    def get_last_comic(self):
        self.last_num = self._get_latest_num()

        cache = self._get_from_cache(self.last_num)

        if cache is not None:
            return cache

        comic_info = self.api_client.get_latest_comic()

        return Comic(
            num=comic_info["num"],
            month=comic_info["month"],
            day=comic_info["day"],
            year=comic_info["year"],
            title=comic_info["title"],
            alt=comic_info["alt"],
            image_url=comic_info["img"]
        )
    
    def get_next_comic(self):
        self.last_num = self.last_num + 1

        if self.last_num > self._get_latest_num():
            self.last_num = self._get_latest_num()

        cache = self._get_from_cache(self.last_num)

        if cache is not None:
            return cache

        comic_info = self.api_client.get_comic_info(self.last_num)

        return Comic(
            num=comic_info["num"],
            month=comic_info["month"],
            day=comic_info["day"],
            year=comic_info["year"],
            title=comic_info["title"],
            alt=comic_info["alt"],
            image_url=comic_info["img"]
        )
    
    def get_previous_comic(self):
        self.last_num = self.last_num - 1

        if self.last_num < 1:
            self.last_num = 1

        cache = self._get_from_cache(self.last_num)

        if cache is not None:
            return cache

        comic_info = self.api_client.get_comic_info(self.last_num)

        return Comic(
            num=comic_info["num"],
            month=comic_info["month"],
            day=comic_info["day"],
            year=comic_info["year"],
            title=comic_info["title"],
            alt=comic_info["alt"],
            image_url=comic_info["img"]
        )
