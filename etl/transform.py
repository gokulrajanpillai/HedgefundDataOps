from __future__ import annotations
import pandas as pd

def normalize_quotes(df: pd.DataFrame) -> pd.DataFrame:
    """Select and order canonical columns for downstream storage."""
    cols = [
        "symbol",
        "regularMarketPrice",
        "regularMarketVolume",
        "regularMarketTime",
        "currency",
        "marketState",
    ]
    return df.loc[:, [c for c in cols if c in df.columns]].copy()