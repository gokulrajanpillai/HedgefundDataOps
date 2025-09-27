from __future__ import annotations
from typing import Optional, Tuple
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

class MarketRow(BaseModel):
    symbol: str = Field(..., min_length=1)
    regularMarketPrice: float
    regularMarketVolume: Optional[int] = None
    regularMarketTime: Optional[int] = None
    currency: Optional[str] = None
    marketState: Optional[str] = None

def validate_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Validate each row of the incoming DataFrame against the MarketRow schema.
    Returns (clean_df, reject_df) where reject_df contains rows that failed validation.
    """
    if df is None or df.empty:
        return df, pd.DataFrame(columns=["_error", *([] if df is None else df.columns)])
    ok_rows = []
    bad_rows = []
    for _, row in df.iterrows():
        rec = row.to_dict()
        try:
            MarketRow(**rec)  # validate
            ok_rows.append(rec)
        except ValidationError as e:
            rec_copy = {"_error": str(e)}
            rec_copy.update(rec)
            bad_rows.append(rec_copy)
    clean_df = pd.DataFrame(ok_rows) if ok_rows else pd.DataFrame(columns=df.columns)
    reject_cols = ["_error"] + list(df.columns)
    reject_df = pd.DataFrame(bad_rows, columns=reject_cols) if bad_rows else pd.DataFrame(columns=reject_cols)
    return clean_df, reject_df