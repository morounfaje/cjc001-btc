\# CJC001-BTC



A simulation-only Python backtester for Bitcoin. One engine runs one strategy at a time, with fees and slippage included from the start. No brokers, no API keys, no real money.



\## How it works



\- A signal is computed at the close of bar t and acted on at the open of bar t+1, so no result uses future information.

\- $10,000 virtual capital, long-only, one position at a time.

\- Costs: 0.1% fee and 0.05% slippage on every trade (set in `config.py`).

\- Every strategy is judged against buy and hold, run through the same engine and the same costs.

\- The last 25% of the data is a sealed holdout. Strategies are developed on the first 75% only.



\## Layout



\- `config.py` - asset-specific settings (costs, bars per year, starting capital)

\- `data/` - download and validation of hourly BTC-USD prices

\- `engine/` - portfolio, costs, backtest loop, metrics, run recorder

\- `strategies/` - one file per strategy (SMA crossover and buy and hold so far)

\- `tests/` - automated tests, including a no-lookahead test

\- `run.py` - runs strategies and prints a scorecard



\## Data



Hourly BTC-USD from Yahoo Finance. The raw CSV is not included in this repository. Each saved run records a fingerprint of the exact data file it used, so a result can be tied to specific data.



\## Run it



&#x20;   pip install -r requirements.txt

&#x20;   python -m data.download

&#x20;   python run.py

&#x20;   python -m pytest



\## AI assistance



This project was built with AI assistance (Claude). The author set the research questions, made the decisions and interpreted the results; the AI helped write and debug code and explain concepts, step by step.

