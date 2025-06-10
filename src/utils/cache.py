import os

class Cache:
    def __init__(self):
        self.cache_directory = self._get_cache_directory()

    def _get_cache_directory(self):
        cache_directory = os.path.expanduser("~/.cache/xkcd-viewer")
        os.makedirs(cache_directory, exist_ok=True)
        return cache_directory

    def save_to_cache(self, comic_id, image):
        image_path = os.path.join(self.cache_directory, f"{comic_id}.png")
        image.save(image_path)

    def get_from_cache(self, comic_id):
        image_path = os.path.join(self._get_cache_directory(), f"{comic_id}.png")
        return image_path if os.path.exists(image_path) else None
