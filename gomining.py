import requests
from config import *

class GoMining:
    def __init__(self):
        self.access = GOMINING_ACCESS_TOKEN
        self.refresh = GOMINING_REFRESH_TOKEN

    def headers(self):
        return {
            "Authorization": f"Bearer {self.access}",
            "Accept": "application/json"
        }

    def get_daily_reward(self):
        url = f"{GOMINING_BASE}/mining/rewards/daily"
        r = requests.get(url, headers=self.headers())
        return r.json()

    def mining_on(self):
        url = f"{GOMINING_BASE}/mining/mode/enable"
        r = requests.post(url, headers=self.headers())
        return r.json()
    
    def get_dashboard(self):
        url = f"{GOMINING_BASE}/user/dashboard"
        r = requests.get(url, headers=self.headers())
        return r.json()

