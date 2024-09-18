from .base_client import BaseClient


class URLhausClient(BaseClient):

    def get_recent_urls(self, limit=3):
        endpoint = f"urls/recent/limit/{limit}/"
        return self.get(endpoint)

    def add_tag(self, tag):
        endpoint = "tag/"
        payload = {
            "tag": tag
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        return self.post(endpoint, data=payload, headers=headers)