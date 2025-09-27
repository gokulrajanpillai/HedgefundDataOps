from __future__ import annotations
import os, time
from typing import Iterable, List
import requests
import pandas as pd
from dotenv import load_dotenv
import yaml
from pathlib import Path

# Load env
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# API endpoints
YF_URL = "https://query1.finance.yahoo.com/v7/finance/quote"
AV_URL = "https://www.alphavantage.co/query"
FH_URL = "https://finnhub.io/api/v1/quote"

# Load platform priority from YAML
PLATFORM_CONFIG = Path(__file__).resolve().parent / "platforms.yaml"
with open(PLATFORM_CONFIG, "r", encoding="utf-8") as f:
    PLATFORM_PRIORITY = yaml.safe_load(f).get("platform_priority", ["Finnhub", "AlphaVantage", "Yahoo"])


def _single_get(url: str, params: dict, timeout: int = 10) -> requests.Response:
    """Perform a single HTTP GET. If 429 is returned, raise immediately."""
    resp = requests.get(url, params=params, timeout=timeout)
    if resp.status_code == 429:
        raise requests.exceptions.HTTPError("429 Too Many Requests")
    resp.raise_for_status()
    return resp


def _fetch_from_finnhub(symbols: Iterable[str]) -> pd.DataFrame:
    """Fetch market data from Finnhub API."""
    if not FINNHUB_API_KEY:
        print("[ERROR] Finnhub API key not set in .env")
        return pd.DataFrame()

    results = []
    for symbol in symbols:
        try:
            params = {"symbol": symbol, "token": FINNHUB_API_KEY}
            resp = _single_get(FH_URL, params=params)
            data = resp.json()
            if data and "c" in data:  # 'c' is current price
                results.append({
                    "symbol": symbol,
                    "regularMarketPrice": float(data.get("c") or 0),  # current price
                    "regularMarketVolume": int(data.get("v", 0) or 0),  # volume
                    "regularMarketTime": None,  # free tier doesn’t include timestamp
                    "currency": "USD",
                    "marketState": "REGULAR",
                })
            time.sleep(0.3)
        except Exception as e:
            print(f"[WARN] Finnhub fetch failed for {symbol}: {e}")
            raise
    return pd.DataFrame(results)


def _fetch_from_alpha_vantage(symbols: Iterable[str]) -> pd.DataFrame:
    """Fetch market data from Alpha Vantage."""
    if not ALPHA_VANTAGE_API_KEY:
        print("[ERROR] Alpha Vantage API key not set in .env")
        return pd.DataFrame()

    results = []
    for symbol in symbols:
        try:
            params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": ALPHA_VANTAGE_API_KEY}
            resp = _single_get(AV_URL, params=params)
            data = resp.json().get("Global Quote", {})
            if data:
                results.append({
                    "symbol": data.get("01. symbol"),
                    "regularMarketPrice": float(data.get("05. price", 0) or 0),
                    "regularMarketVolume": int(data.get("06. volume", 0) or 0),
                    "regularMarketTime": None,
                    "currency": "USD",
                    "marketState": "REGULAR",
                })
            time.sleep(0.3)
        except Exception as e:
            print(f"[WARN] Alpha Vantage fetch failed for {symbol}: {e}")
            raise
    return pd.DataFrame(results)


def _fetch_from_yahoo(symbols: Iterable[str]) -> pd.DataFrame:
    """Fetch market data from Yahoo Finance API (one symbol at a time)."""
    results = []
    for symbol in symbols:
        try:
            resp = _single_get(YF_URL, params={"symbols": symbol})
            data = resp.json().get("quoteResponse", {}).get("result", [])
            if data:
                results.extend(data)
            time.sleep(0.3)
        except Exception as e:
            print(f"[WARN] Yahoo fetch failed for {symbol}: {e}")
            raise
    return pd.DataFrame(results)


def fetch_market_data(symbols: Iterable[str]) -> pd.DataFrame:
    """Try platforms in configured order until one works."""
    syms: List[str] = list(symbols)
    if not syms:
        return pd.DataFrame()

    last_error = None
    for platform in PLATFORM_PRIORITY:
        try:
            if platform == "Finnhub":
                print("[INFO] Attempting Finnhub...")
                df = _fetch_from_finnhub(syms)
            elif platform == "AlphaVantage":
                print("[INFO] Attempting Alpha Vantage...")
                df = _fetch_from_alpha_vantage(syms)
            elif platform == "Yahoo":
                print("[INFO] Attempting Yahoo Finance...")
                df = _fetch_from_yahoo(syms)
            else:
                print(f"[WARN] Unknown platform {platform}, skipping.")
                continue

            if not df.empty and not df["regularMarketPrice"].isnull().all():
                print(f"[INFO] {platform} succeeded with {len(df)} rows.")
                # Ensure canonical schema
                for col in ["symbol", "regularMarketPrice", "regularMarketVolume", "regularMarketTime", "currency", "marketState"]:
                    if col not in df.columns:
                        df[col] = None
                return df

        except Exception as e:
            last_error = e
            print(f"[WARN] {platform} failed: {e}. Trying next platform...")

    print("[ERROR] All platforms failed.")
    if last_error:
        raise last_error
    return pd.DataFrame()
