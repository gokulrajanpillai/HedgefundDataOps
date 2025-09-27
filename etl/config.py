from __future__ import annotations
from pathlib import Path
import yaml

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "tickers.yaml"

def load_tickers(path: Path | str = DEFAULT_CONFIG_PATH) -> dict:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}