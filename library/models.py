from abc import ABC, abstractmethod
from typing import List

import requests


class Asset(ABC):
    def __init__(self, name: str, quantity: float):
        self.name = name
        self.quantity = quantity

    @abstractmethod
    def get_asset_price(self, api_base_url: str, api_key: str) -> float:
        pass

    def calculate_value(self, api_base_url: str, api_key: str) -> float:
        return self.get_asset_price(api_base_url, api_key) * self.quantity


class Stock(Asset):
    def get_asset_price(self, api_base_url: str, api_key: str) -> float:
        # Assume a real API call to get the stock price
        response = requests.get(f'{api_base_url}/{self.name}/prev?',
                                params={'adjusted': 'true', 'apiKey': api_key},
                                headers={'content-type': 'application/json'})
        if not response.ok:
            raise Exception('Failed to get stock price')
        results = response.json()
        return results['results'][0]['c']


class Crypto(Asset):
    def get_asset_price(self, api_base_url: str, api_key: str) -> float:
        # Assume a real API call to get the stock price
        response = requests.get(f'{api_base_url}/X:{self.name}USD/prev?',
                                params={'adjusted': 'true', 'apiKey': api_key},
                                headers={'content-type': 'application/json'})
        if not response.ok:
            raise Exception('Failed to get stock price')
        results = response.json()
        return results['results'][0]['c']


class Portfolio:
    def __init__(self, name: str):
        self.name = name
        self.assets: List[Asset] = []

    def add_asset(self, asset: Asset):
        self.assets.append(asset)

    def calculate_total_value(self, api_base_url: str, api_key: str) -> float:
        return sum([asset.calculate_value(api_base_url, api_key) for asset in self.assets])
