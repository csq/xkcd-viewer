import os.path
import json

class Preferences:
    _PREFERENCES_FILE_NAME = "preferences.json"
    _PREFERENCES_FILE_PATH = os.path.expanduser(f"~/.config/xkcd-viewer/{_PREFERENCES_FILE_NAME}")

    def __init__(self):
        if not self._exists_preferences_file():
            self._create_preferences_file()

    def _create_preferences_file(self):
        os.makedirs(os.path.dirname(self._PREFERENCES_FILE_PATH), exist_ok=True)
        default_preferences = {
            "theme": "yaru",
            "resolution": "640x480"
        }
        with open(self._PREFERENCES_FILE_PATH, "w") as f:
            f.write(json.dumps(default_preferences, indent=4))
            f.close()
    
    def _exists_preferences_file(self):
        return os.path.exists(self._PREFERENCES_FILE_PATH)

    def save_preferences(self, key, value):
        with open(self._PREFERENCES_FILE_PATH, "r") as f:
            preferences = json.load(f)
        preferences[key] = value
        with open(self._PREFERENCES_FILE_PATH, "w") as f:
            json.dump(preferences, f, indent=4)

    def get_preferences(self):
        with open(self._PREFERENCES_FILE_PATH, "r") as f:
            return json.load(f)