import json
from json import dumps
import pandas as pd


class TokensWatcher:
    def __init__(self, oinchAPI):
        self.oinchAPI = oinchAPI
        self.tokens = {}  # Dictionnary with token address as key and token data as value

    def add_token(self, token):
        self.tokens[token["address"]] = []

    def fetch_prices(self):
        if self.tokens:
            tokens_prices = self.oinchAPI.get_prices(list(self.tokens.keys()))
            print(tokens_prices)
            for token, price in tokens_prices.items():
                try:
                    self.tokens.get(token).append(price)
                except Exception as e:
                    print(f"Token {token} not found in the list of tokens")
            print(dumps(self.tokens))

    def calculate_emas(self):
        for token in self.tokens:
            if len(self.tokens[token]) > 1:
                df = pd.DataFrame(self.tokens[token], columns=["price"])
                EMA2 = df["price"].ewm(span=2, adjust=False).mean()
                EMA5 = df["price"].ewm(span=5, adjust=False).mean()
                if EMA2 < EMA5:
                    sell(token)

    """
    Remove token from the list
    """
    def clean(self, token):
        pass
