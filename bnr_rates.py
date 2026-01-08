import requests
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

BNR_URL = "https://www.bnr.ro/nbrfxrates.xml"
CACHE_FILE = "rates_cache.json"
CACHE_MAX_AGE = 24 * 60 * 60

def fetch_and_parse_rates():

    """
    Descarca cursurile de la BNR, le parseaza din XML
    si returneaza un dictionar cu ratele valutare
    """

    try:
        response = requests.get(BNR_URL, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.text)
    except (requests.RequestException, ET.ParseError) as e:
        raise RuntimeError(f"Failed to fetch or parse BNR rates: {e}")

    namespace = {"bnr": "http://www.bnr.ro/xsd"}

    rates = {"RON": 1.0}

    for rate in root.findall(".//bnr:Rate", namespace):
        currency = rate.attrib.get("currency")
        multiplier = int(rate.attrib.get("multiplier", "1"))
        value = float(rate.text)
        rates[currency] = value / multiplier

    return {
        "timestamp": datetime.now().isoformat(),
        "rates": rates
    }


def load_from_cache():
    """
    Incarca datele din fisierul cache daca exista
    """
    if not os.path.exists(CACHE_FILE):
        return None

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

def is_cache_valid(cached_data):
    """
    Verifica daca datele din cache sunt mai noi de 24h
    """
    try:
        cache_time = datetime.fromisoformat(cached_data["timestamp"])
        age_seconds = (datetime.now() - cache_time).total_seconds()
        return age_seconds < CACHE_MAX_AGE
    except Exception:
        return False

def save_to_cache(data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_rates():
    """
    Decide inteligent:
    - foloseste cache daca e valid (<24h)
    - refetch daca e expirat
    - fallback la cache daca BNR pica
    """

    cached = load_from_cache()

    # Daca avem cache si e valid, il folosim direct
    if cached and is_cache_valid(cached):
        print("Using cached rates (still valid)")
        return cached

    # Altfel incercam fetch live
    try:
        print("Fetching rates from BNR")
        data = fetch_and_parse_rates()
        save_to_cache(data)
        return data

    except RuntimeError:
        # Daca fetch-ul pica, dar avem cache vechi
        if cached:
            print("Using cached rates (BNR unavailable)")
            return cached
        raise


if __name__ == "__main__":
    data = get_rates()
    print(data)
