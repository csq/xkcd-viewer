import os

from core.comic import Comic
from core.db import DB

class Cache:
    def __init__(self):
        self.cache_directory = self._get_cache_directory()

    def _get_cache_directory(self):
        cache_directory = os.path.expanduser("~/.cache/xkcd-viewer")
        os.makedirs(cache_directory, exist_ok=True)
        return cache_directory

    def save_to_cache(self, comic_num, image):
        image_path = os.path.join(self.cache_directory, f"{comic_num}.png")
        image.save(image_path)

    def get_from_cache(self, comic_num):
        conn = DB().get_conn()
        data = Comic.get_by_num(conn, comic_num)
        image_path = os.path.join(self._get_cache_directory(), f"{comic_num}.png")

        if data != None and os.path.exists(image_path):
            data.image_url = image_path
            return data

        return None
