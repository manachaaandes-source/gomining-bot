import requests
from config import *

class GoMiningClient:
    def __init__(self):
        self.access_token = GOMINING_ACCESS_TOKEN
        self.refresh_token = GOMINING_REFRESH_TOKEN

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json"
        }

    def refresh_tokens(self):
        url = f"{GOMINING_BASE}/auth/refresh"
        data = {"refresh_token": self.refresh_token}

        r = requests.post(url, json=data)
        if r.status_code == 200:
            tokens = r.json()
            self.access_token = tokens["access_token"]
            return True
        else:
            print("Token refresh failed:", r.text)
            return False

    def get_daily_reward(self):
        url = f"{GOMINING_BASE}/mining/rewards/daily"
        r = requests.get(url, headers=self._headers())

        if r.status_code == 401:
            self.refresh_tokens()
            r = requests.get(url, headers=self._headers())

        return r.json()

    def enable_mining_mode(self):
        url = f"{GOMINING_BASE}/mining/mode/enable"
        r = requests.post(url, headers=self._headers())
        return r.json()
