
# Developer Setup Guide

This document explains how to set up a local development environment for the **Hedge Fund Data Reliability Platform – Layer 1**.

## 1. Prerequisites
- Python **3.11** installed
- Git
- Docker (optional, for later layers)

## 2. Clone the Repository
```bash
git clone <your-repo-url>
cd hedgefund-dataops
```

## 3. Create and Activate a Virtual Environment (venv)
```bash
python3 -m venv .venv
```

Activate it:
- Linux / MacOS:
  ```bash
  source .venv/bin/activate
  ```
- Windows (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

When active, your shell prompt will show:
```
(.venv) $
```

## 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. API Keys Setup (.env)
Create a `.env` file in the root directory:
```env
FINNHUB_API_KEY=your_finnhub_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

- Get a free Finnhub key → https://finnhub.io  
- Get a free Alpha Vantage key → https://www.alphavantage.co  

## 6. Configure Platform Priority
Edit `etl/platforms.yaml`:
```yaml
platform_priority:
  - Finnhub
  - AlphaVantage
  - Yahoo
```

Change the order as needed.

## 7. Run the Pipeline
```bash
python run_layer1.py
```

Expected output:
```
[INFO] Attempting Finnhub...
[INFO] Finnhub succeeded with 3 rows.
[Layer1] Clean rows: 3, Rejected rows: 0
```

Outputs:
- `data/layer1/quotes_clean.parquet` → validated rows  
- `data/layer1/quotes_rejects.parquet` → rejected rows with `_error`  

## 8. Run Tests
```bash
pytest -q
```

## 9. Deactivate Environment
When finished working:
```bash
deactivate
```
