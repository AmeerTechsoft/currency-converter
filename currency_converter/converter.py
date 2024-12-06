import requests
import yfinance as yf
import json
import os
from datetime import datetime, timedelta


# Constants
CACHE_FILE = "exchange_rates.json"
CACHE_DURATION_HOURS = 1


# Caching Functions
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    return {}


def save_cache(data):
    with open(CACHE_FILE, "w") as file:
        json.dump(data, file)


def get_cached_rate(base_currency, target_currency):
    cache = load_cache()
    key = f"{base_currency}_{target_currency}"
    if (
        key in cache
        and datetime.strptime(cache[key]["timestamp"], "%Y-%m-%d %H:%M:%S")
        > datetime.now() - timedelta(hours=CACHE_DURATION_HOURS)
    ):
        return cache[key]["rate"]
    return None


def cache_rate(base_currency, target_currency, rate):
    cache = load_cache()
    cache[f"{base_currency}_{target_currency}"] = {
        "rate": rate,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_cache(cache)


# Fetching Functions
def get_exchange_rate_yahoo(base_currency: str, target_currency: str) -> float:
    ticker = f"{base_currency}{target_currency}=X"
    data = yf.Ticker(ticker)
    price = data.info.get("regularMarketPrice")
    if price is None:
        raise ValueError(f"Exchange rate for {base_currency} to {target_currency} not available.")
    return price


def get_exchange_rate_google(base_currency: str, target_currency: str) -> float:
    url = f"https://www.google.com/finance/quote/{base_currency}-{target_currency}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    rate_element = soup.find("div", {"class": "YMlKec fxKbKc"})
    if rate_element:
        return float(rate_element.text.replace(",", ""))
    raise ValueError(f"Exchange rate for {base_currency} to {target_currency} not available.")


# CurrencyConverter Class
class CurrencyConverter:
    def __init__(self, use_yahoo: bool = True):
        self.use_yahoo = use_yahoo

    def get_rate(self, base_currency: str, target_currency: str) -> float:
        # Check cache
        cached_rate = get_cached_rate(base_currency, target_currency)
        if cached_rate:
            return cached_rate

        # Fetch live rate
        if self.use_yahoo:
            rate = get_exchange_rate_yahoo(base_currency, target_currency)
        else:
            rate = get_exchange_rate_google(base_currency, target_currency)

        # Cache the rate
        cache_rate(base_currency, target_currency, rate)
        return rate

    def convert(self, amount: float, base_currency: str, target_currency: str) -> float:
        rate = self.get_rate(base_currency, target_currency)
        return amount * rate
