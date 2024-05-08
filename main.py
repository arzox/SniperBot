from research import *
from swap import Swap
from watcher import TokensWatcher
from dextools_python import DextoolsAPIV2
from API import OinchAPI
from dateutil import relativedelta


if __name__ == "__main__":
    keys = load_api_keys("credientials.json")
    dextools = DextoolsAPIV2(keys['dextools'], plan="trial")
    oinch = OinchAPI(keys['oinch'])

    tokens_watcher = TokensWatcher(oinch)
    swap = Swap(keys['uniswap'])

    chain = "ether"
    duration = 1  # in hours
    refresh_rate = 60 * 3  # in minutes

    wb = set_sheet()

    time_to_stop = datetime.now() + timedelta(hours=duration)

    # Refresh every minute

    while datetime.now() <= time_to_stop:
        # Get all tokens created sort them to get the greatest
        tokens = get_token_list(dextools, chain, relativedelta.relativedelta(minutes=refresh_rate))
        for token in tokens.get("data").get("tokens"):
            security = security_check(dextools, token, chain)
            if security:
                print(f"Token {token['address']} is promising")
                store_token(security, token, chain, wb.active)
                tokens_watcher.add_token(token)
                swap.buy(token["address"])

        tokens_watcher.fetch_prices()
        tokens_watcher.calculate_emas()
        sleep(refresh_rate * 60)
    print("Done")
