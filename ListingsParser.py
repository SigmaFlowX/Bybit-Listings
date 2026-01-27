import csv
import re
import time
import requests
from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API_URL = "https://api.bybit.com/v5/announcements/index"
HEADERS = {"User-Agent": "Mozilla/5.0"}
LOCALE = "en-US"
LIMIT = 50

KEYWORDS = {"list", "listing", "listed", "lists"}
STOP_WORDS = {"usdc", "convert", "delisting", "delist"}
STOP_TICKERS = {"UTC", "USDT", "USD", "NFT", "BTC", "ETH"}

TICKER_REGEX = re.compile(r"\b([A-Z]{2,}USDT|[A-Z]{2,})\b")


def create_session() -> requests.Session:
    retry = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",)
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def extract_tickers(text: str) -> set[str]:
    return {t for t in TICKER_REGEX.findall(text) if t not in STOP_TICKERS}


def is_valid_listing(text: str) -> bool:
    text_l = text.lower()
    if not any(k in text_l for k in KEYWORDS):
        return False
    if any(w in text_l for w in STOP_WORDS):
        return False
    return True


def fetch_page(session: requests.Session, page: int) -> list[dict]:
    r = session.get(
        API_URL,
        params={
            "locale": LOCALE,
            "page": page,
            "limit": LIMIT
        },
        headers=HEADERS,
        timeout=30
    )
    r.raise_for_status()
    return r.json().get("result", {}).get("list", [])


def parse_all_listings(max_pages: int = 200) -> list[dict]:
    session = create_session()
    seen = set()
    rows = []

    for page in range(1, max_pages + 1):
        print("page number", page)
        items = fetch_page(session, page)
        if not items:
            break

        for ann in items:
            text = f"{ann.get('title','')} {ann.get('description','')}"
            if not is_valid_listing(text):
                continue

            tickers = extract_tickers(text)
            if not tickers:
                continue

            ts = ann.get("dateTimestamp")
            if not ts:
                continue

            listing_time = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

            for ticker in tickers:
                key = (ticker, listing_time)
                if key not in seen:
                    seen.add(key)
                    rows.append({
                        "ticker": ticker,
                        "listing_time": listing_time
                    })

        time.sleep(0.3)

    return rows


def save_to_csv(data: list[dict], filename: str) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=("ticker", "listing_time"))
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    data = parse_all_listings(max_pages=200)
    save_to_csv(data, "bybit_listings.csv")
