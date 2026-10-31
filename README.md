# StockVision AI 📈

A locally runnable stock-market analytics dashboard built with Flask, SQLite, Plotly.js and scikit-learn. Designed for an educational internship project and GitHub portfolio.

## Features

- Search common company names or Yahoo Finance ticker symbols (including Indian `.NS` symbols).
- Historical OHLCV stock data, date ranges, candlestick/line charts, 20-session moving average and volume charts.
- Random Forest next-session forecasts for 1, 5 or 7 sessions using recursive lag-based features.
- Chronological 80/20 evaluation: MAE, RMSE and R² (no random time-series shuffle).
- Stock comparison on aligned trading dates, normalized to 100.
- SQLite registration, login, personal watchlist and prediction history.
- Statistical insights derived from actual price data.

## Run locally (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

If activation is blocked, first run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal. Edit `.env` and set a unique random `SECRET_KEY` before running. Open **http://127.0.0.1:5000**. SQLite is created automatically in `instance/`.

Python 3.12 or 3.13 recommended; ensure the selected interpreter has compatible scientific Python wheels. Internet is required for Yahoo Finance data and Plotly.js CDN. No paid APIs are needed.

## Model methodology

For each training target close at trading session *t*, features are constructed using **only closes before t**: lagged closes at t-1, t-2, t-3, t-5; means of the preceding 5, 10 and 20 sessions; and volatility of recent returns. Samples are sorted chronologically; the first 80% train a `RandomForestRegressor`, and the final 20% measure held-out MAE/RMSE/R². After evaluation, the model is retrained on all samples. Future predictions recursively append each predicted close to the price history; this is inherently error-prone over multiple sessions. No unknown future volume is used.

**Limitations:** forecasts are illustrative, not reliable investment advice. The holdout test is a single chronological split, not walk-forward backtesting. The displayed one-step 90th-percentile absolute error is *not* a calibrated multi-step prediction interval. The forecast chart uses session offsets rather than actual exchange trading calendars. Yahoo Finance may throttle or temporarily fail. Prices are adjusted via yfinance and can differ from unadjusted exchange quotes. Company-name search uses a small mapping; other stocks should be entered by ticker. Currency depends on exchange. Stock data is not streamed live. Historical volume is charted but not included in the ML feature set.

## Testing

```powershell
pytest -q
```

Tests use synthetic data and do not require internet access. Web routes and external Yahoo Finance connectivity have not been integration-tested in this environment.

## Repository guidance

Commit source files and this README, **not** `.env`, local SQLite databases, virtual environments or trained models. Add project screenshots under `screenshots/` after running locally.

## Folder overview

- `app.py`: Flask routes and authentication
- `models/`: SQLite schema
- `services/`: Yahoo Finance retrieval, prediction orchestration, analysis
- `ml/`: features, training and forecasting
- `templates/`: Jinja HTML pages
- `static/`: CSS, JS and SVG logo
- `tests/`: offline model unit tests

## Future improvements

Walk-forward evaluation, exchange trading calendars, cached stock prices, richer company search and offline chart bundling.
