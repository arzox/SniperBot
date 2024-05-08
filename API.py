import requests
import json


class OinchAPI:
    def __init__(self, api_key):
        self.headers = {
            "Authorization": f"Bearer {api_key}"
        }

    def get_prices(self, addresses):
        endpoint = f"https://api.1inch.dev/price/v1.1/1/{addresses[0]}"
        for address in addresses[1:]:
            endpoint += f",{address}"
        return requests.get(endpoint, headers=self.headers, params={"currency": "USD"}).json()
