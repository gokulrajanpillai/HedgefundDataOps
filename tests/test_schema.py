from etl.validate import validate_dataframe
import pandas as pd

def test_valid_row_passes():
    df = pd.DataFrame([{
        "symbol": "AAPL",
        "regularMarketPrice": 180.5,
        "regularMarketVolume": 12345,
        "regularMarketTime": 1693612800,
        "currency": "USD",
        "marketState": "REGULAR"
    }])
    clean, rejects = validate_dataframe(df)
    assert len(clean) == 1
    assert len(rejects) == 0

def test_invalid_row_rejected():
    df = pd.DataFrame([{
        "symbol": "",  # invalid
        "regularMarketPrice": "NaN",  # invalid type
    }])
    clean, rejects = validate_dataframe(df)
    assert len(clean) == 0
    assert len(rejects) == 1