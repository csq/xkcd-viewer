import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_comic_info(self, comic_id):
        response = requests.get(f"{self.base_url}{comic_id}/info.0.json")
        response.raise_for_status()
        return response.json()

    def get_latest_comic(self):
        response = requests.get(f"{self.base_url}/info.0.json")
        response.raise_for_status()
        return response.json()