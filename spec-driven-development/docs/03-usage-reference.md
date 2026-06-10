# Usage Reference

Complete guide to using Price Fetcher via CLI and Python API.

---

## 📋 Table of Contents

1. [CLI Commands](#cli-commands)
2. [Python API](#python-api)
3. [Common Patterns](#common-patterns)
4. [Error Handling](#error-handling)
5. [FAQ](#faq)

---

## CLI Commands

### `python -m src bitcoin`

Get Bitcoin price.

```bash
$ python -m src bitcoin
============================================================
  Bitcoin Price
============================================================

  Bitcoin              $ 67,890.50 USD (+2.45%)

  Source: coingecko
  Time: 2026-06-10T15:32:44.123456
```

---

### `python -m src gold`

Get Gold price per troy ounce.

```bash
$ python -m src gold
============================================================
  Gold Price
============================================================

  Gold (per oz)        $  2,087.75 USD (+0.35%)

  Source: london_metal_exchange
  Time: 2026-06-10T15:32:44.123456
```

---

### `python -m src rate <CURRENCY>`

Get USD exchange rate for specific currency.

```bash
$ python -m src rate EUR
============================================================
  Exchange Rate: USD -> EUR
============================================================

  1 USD =     0.9200 EUR

  Source: open_exchange_rates
  Time: 2026-06-10T15:32:44.123456
```

**Supported currencies:**
```
EUR  GBP  JPY  AUD  CAD  CHF  CNY  INR  MXN  ARS  BRL  CLP
```

---

### `python -m src all [CURRENCIES]`

Get Bitcoin, Gold, and exchange rates in one command.

```bash
# Default (EUR, MXN, ARS)
$ python -m src all

# Custom currencies
$ python -m src all EUR,GBP,JPY

# Single currency
$ python -m src all MXN
```

---

### `python -m src json [CURRENCIES]`

Export all prices as JSON (perfect for integration).

```bash
# Print to console
$ python -m src json

# Save to file
$ python -m src json > prices.json

# Custom currencies
$ python -m src json EUR,GBP,JPY
```

**Output format:**
```json
{
  "bitcoin": {...},
  "gold": {...},
  "exchange_rates": {...},
  "timestamp": "2026-06-10T15:32:44.123456"
}
```

---

### `python -m src help`

Show all available commands and usage.

---

## Python API

### Basic Usage

```python
from src.price_fetcher import PriceFetcher

fetcher = PriceFetcher()
```

### Fetch Bitcoin

```python
btc = fetcher.fetch_bitcoin()

print(f"Bitcoin: ${btc.price:,.2f}")
print(f"Change: {btc.change_24h:+.2f}%")
print(f"Updated: {btc.timestamp}")
```

**Returns:** `BitcoinPrice` object with:
- `price: float` - Current price in USD
- `currency: str` - Currency code ("USD")
- `change_24h: float` - 24-hour change percentage
- `timestamp: datetime` - Last update time
- `symbol: str` - "BTC"
- `name: str` - "Bitcoin"
- `source: str` - Data source identifier

---

### Fetch Gold

```python
gold = fetcher.fetch_gold()

print(f"Gold: ${gold.price:,.2f}/oz")
print(f"Change: {gold.change_24h:+.2f}%")
```

**Returns:** `GoldPrice` object with:
- `price: float` - Price per troy ounce in USD
- `currency: str` - "USD"
- `unit: str` - "troy ounce"
- `change_24h: float` - 24-hour change percentage
- `timestamp: datetime` - Last update time
- `symbol: str` - "XAU"
- `name: str` - "Gold"
- `source: str` - Data source

---

### Fetch Exchange Rate

```python
# Single currency
rate = fetcher.fetch_exchange_rate("EUR")
print(f"1 USD = {rate.rate} EUR")

# Multiple currencies
rates = fetcher.fetch_multiple_rates(["EUR", "GBP", "JPY"])
for currency, rate in rates.items():
    print(f"1 USD = {rate.rate} {currency}")
```

**Returns:** `ExchangeRate` object (for single) or dict (for multiple)

---

### Fetch All Prices

```python
# Get everything
response = fetcher.fetch_all(
    fetch_bitcoin=True,
    fetch_gold=True,
    fetch_rates=["EUR", "MXN", "ARS"]
)

# Access data
print(f"Bitcoin: ${response.bitcoin.price}")
print(f"Gold: ${response.gold.price}")

# Iterate rates
for currency, rate in response.exchange_rates.items():
    print(f"{currency}: {rate.rate}")

# Convert to dict
data_dict = response.to_dict()
```

---

## Common Patterns

### Save Prices to JSON File

```python
import json
from src.price_fetcher import PriceFetcher

fetcher = PriceFetcher()
response = fetcher.fetch_all()

with open("prices.json", "w") as f:
    json.dump(response.to_dict(), f, indent=2)
```

---

### Check if Currency is Supported

```python
currency = "EUR"
if fetcher.validate_currency(currency):
    rate = fetcher.fetch_exchange_rate(currency)
else:
    print(f"{currency} not supported")
```

---

### Get List of Supported Currencies

```python
currencies = fetcher.get_supported_currencies()
print("Supported:", ", ".join(currencies))

# Output: Supported: ARS, AUD, BRL, CAD, CHF, CNY, EUR, GBP, INR, JPY, MXN
```

---

### Use in Flask Web App

```python
from flask import Flask, jsonify
from src.price_fetcher import PriceFetcher

app = Flask(__name__)
fetcher = PriceFetcher()

@app.route('/api/prices')
def get_prices():
    response = fetcher.fetch_all(fetch_rates=["EUR", "GBP", "JPY"])
    return jsonify(response.to_dict())

@app.route('/api/bitcoin')
def get_bitcoin():
    btc = fetcher.fetch_bitcoin()
    return jsonify({
        "symbol": btc.symbol,
        "price": btc.price,
        "currency": btc.currency
    })

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Error Handling

### Invalid Currency

```python
from src.price_fetcher import PriceFetcher, InvalidCurrencyError

fetcher = PriceFetcher()

try:
    rate = fetcher.fetch_exchange_rate("INVALID")
except InvalidCurrencyError as e:
    print(f"Error: {e}")
    print("Valid currencies:", fetcher.get_supported_currencies())
```

---

### Price Model Validation

Data models validate automatically:

```python
from src.models import BitcoinPrice
from datetime import datetime

# This raises ValueError (price out of range)
try:
    btc = BitcoinPrice(
        price=500.0,  # Should be 1,000-200,000
        timestamp=datetime.now(),
        change_24h=0.0,
        source="test"
    )
except ValueError as e:
    print(f"Validation error: {e}")
```

---

## FAQ

### How do I get current prices?

Use the CLI for quick checks:
```bash
python -m src all
```

Or Python API for programmatic access:
```python
fetcher.fetch_all()
```

### Can I use real API data instead of mock data?

Yes! Edit `BITCOIN_DATA`, `GOLD_DATA`, or `EXCHANGE_RATES` constants in `src/price_fetcher.py` to integrate with real APIs.

### How do I integrate this into my project?

**As a library:**
```python
from src.price_fetcher import PriceFetcher
fetcher = PriceFetcher()
# Use as shown above
```

**As a CLI tool:**
```bash
python -m src json > prices.json
```

---

### What Python versions are supported?

Python 3.10 and higher. Check your version:
```bash
python --version
```

### How do I update prices or currencies?

1. **For mock data:** Edit constants in `src/price_fetcher.py`
2. **For real APIs:** Modify `fetch_*` methods to call external APIs
3. **For new currencies:** Add to `EXCHANGE_RATES` dict and `ExchangeRate.VALID_CURRENCIES`

---

### Are the prices real?

No, they're realistic mock data for demonstration. This is an educational project, not a real financial service.

---

### Can I use this in production?

As-is, no (mock data). But you can use it as a template to integrate real price sources.

---

[← Back to README](../README.md) | [→ Examples](04-examples.md)
