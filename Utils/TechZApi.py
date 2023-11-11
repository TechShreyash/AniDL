import requests


class Gogo:
    def __init__(self) -> None:
        self.base = "https://api.anime-dex.workers.dev"

    def gogo_search(self, query):
        data = requests.get(f"{self.base}/search/{query}").json()
        return data["results"]

    def gogo_anime(self, id):
        data = requests.get(f"{self.base}/anime/{id}").json()
        return data
    
    def gogo_episode(self, id, ep):
        data = requests.get(f"{self.base}/episode/{id}-episode-{ep}").json()
        return data


class TechZApi(Gogo):
    def __init__(self) -> None:
        self.base = "https://api.anime-dex.workers.dev"
        super().__init__()
