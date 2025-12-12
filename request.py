import requests
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

BNR_URL = "https://www.bnr.ro/nbrfxrates.xml"
CACHE_FILE = "rates_cache.json"


def fetch_and_parse_rates():
    response = requests.get(BNR_URL, timeout=10)
    response.raise_for_status()

    root = ET.fromstring(response.text)

    rates = {"RON": 1.0}

    for rate in root.iter("Rate"):
        currency = rate.attrib.get("currency")
        multiplier = int(rate.attrib.get("multiplier", "1"))
        value = float(rate.text)

        rates[currency] = value / multiplier

    return {
        "timestamp": datetime.now().isoformat(),
        "rates": rates
    }


def load_from_cache():
    if not os.path.exists(CACHE_FILE):
        return None

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def save_to_cache(data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_rates():
    cached = load_from_cache()
    if cached:
        print("Loaded rates from cache")
        return cached

    print("Fetching rates from BNR")
    data = fetch_and_parse_rates()
    save_to_cache(data)
    return data


if __name__ == "__main__":
    data = get_rates()
    print(data)
