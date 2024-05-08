import pandas as pd


def calculate_emas(token):
        if len(token) > 1:
            df = pd.DataFrame(token, columns=["price"])
            df["EMA2"] = df["price"].ewm(span=2, adjust=False).mean()
            df["EMA5"] = df["price"].ewm(span=5, adjust=False).mean()
            print(df)


token = (pd.Series(range(100))).tolist()
calculate_emas(token)
