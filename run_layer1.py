from __future__ import annotations
from pathlib import Path
import pandas as pd

from etl.config import load_tickers
from etl.ingestion import fetch_market_data
from etl.validate import validate_dataframe
from etl.transform import normalize_quotes

DATA_DIR = Path(__file__).resolve().parent / "data" / "layer1"

def main():
    cfg = load_tickers()
    symbols = cfg.get("symbols", [])
    print(f"[Layer1] Ingesting symbols: {symbols}")
    raw = fetch_market_data(symbols)
    print(f"[Layer1] Raw rows: {len(raw)}")
    clean, rejects = validate_dataframe(raw)
    print(f"[Layer1] Clean rows: {len(clean)}, Rejected rows: {len(rejects)}")
    clean = normalize_quotes(clean)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    clean_path = DATA_DIR / "quotes_clean.parquet"
    reject_path = DATA_DIR / "quotes_rejects.parquet"
    clean.to_parquet(clean_path, index=False)
    rejects.to_parquet(reject_path, index=False)
    print(f"[Layer1] Saved clean → {clean_path}")
    print(f"[Layer1] Saved rejects → {reject_path}")

if __name__ == "__main__":
    main()