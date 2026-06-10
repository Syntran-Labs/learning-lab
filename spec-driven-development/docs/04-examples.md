# Real-World Examples

Complete, working examples of how to use Price Fetcher in different scenarios.

---

## 📖 Table of Contents

1. [Quick CLI Usage](#quick-cli-usage)
2. [Python Module Usage](#python-module-usage)
3. [Integration Examples](#integration-examples)
4. [Before & After Refactoring](#before--after-refactoring)
5. [Using in Your Own Project](#using-in-your-own-project)

---

## Quick CLI Usage

### Example 1: Check Bitcoin Price

```bash
$ python -m src bitcoin
============================================================
  Bitcoin Price
============================================================

  Bitcoin              $ 67,890.50 USD (+2.45%)

  Source: coingecko
  Time: 2026-06-10T15:32:44.123456
```

**Real-world use:** Quick price check before trading decision

---

### Example 2: Compare Exchange Rates

```bash
$ python -m src all EUR,GBP,JPY,MXN
============================================================
  All Prices
============================================================

  Bitcoin              $ 67,890.50 USD (+2.45%)
  Gold (per oz)        $  2,087.75 USD (+0.35%)

  1 USD =     0.9200 EUR
  1 USD =     0.7900 GBP
  1 USD =   150.2500 JPY
  1 USD =    17.4500 MXN

  Updated: 2026-06-10T15:32:44.123456
```

**Real-world use:** Quick international market snapshot

---

### Example 3: Export for Processing

```bash
$ python -m src json EUR,GBP > market_data.json
$ cat market_data.json
{
  "bitcoin": {
    "symbol": "BTC",
    "name": "Bitcoin",
    "price": 67890.5,
    "currency": "USD",
    "change_24h": 2.45,
    "source": "coingecko",
    "timestamp": "2026-06-10T15:32:44.123456"
  },
  "gold": {...},
  "exchange_rates": {...},
  "timestamp": "2026-06-10T15:32:44.123456"
}
```

**Real-world use:** Data export for analytics pipeline

---

## Python Module Usage

### Example 1: Fetch Single Price

```python
from src.price_fetcher import PriceFetcher

# Create fetcher
fetcher = PriceFetcher()

# Get Bitcoin price
btc = fetcher.fetch_bitcoin()

# Use the data
print(f"Bitcoin is trading at ${btc.price:,.2f}")
print(f"24-hour change: {btc.change_24h:+.2f}%")
print(f"Last updated: {btc.timestamp}")

# Output:
# Bitcoin is trading at $67,890.50
# 24-hour change: +2.45%
# Last updated: 2026-06-10 15:32:44.123456
```

---

### Example 2: Handle Invalid Currency

```python
from src.price_fetcher import PriceFetcher, InvalidCurrencyError

fetcher = PriceFetcher()

try:
    rate = fetcher.fetch_exchange_rate("INVALID")
except InvalidCurrencyError as e:
    print(f"Error: {e}")
    print("Supported currencies:", fetcher.get_supported_currencies())

# Output:
# Error: Invalid target currency: INVALID. Valid currencies: ARS, AUD, ...
# Supported currencies: ['ARS', 'AUD', 'BRL', 'CAD', 'CHF', 'CNY', 'EUR', 'GBP', 'INR', 'JPY', 'MXN']
```

---

### Example 3: Batch Operations

```python
from src.price_fetcher import PriceFetcher

fetcher = PriceFetcher()

# Get all prices at once
response = fetcher.fetch_all(
    fetch_bitcoin=True,
    fetch_gold=True,
    fetch_rates=["EUR", "MXN", "ARS"]
)

# Access individual items
print(f"Bitcoin: ${response.bitcoin.price}")
print(f"Gold: ${response.gold.price}/oz")

# Iterate exchange rates
for currency, rate in response.exchange_rates.items():
    print(f"1 USD = {rate.rate} {currency}")

# Convert to dict for JSON serialization
import json
data_json = json.dumps({
    "data": response.to_dict()
}, indent=2)
```

---

## Integration Examples

### Example 1: Flask Web API

```python
from flask import Flask, jsonify
from src.price_fetcher import PriceFetcher

app = Flask(__name__)
fetcher = PriceFetcher()

@app.route('/api/prices')
def get_prices():
    """Get all prices as JSON"""
    response = fetcher.fetch_all(fetch_rates=["EUR", "GBP", "JPY"])
    return jsonify(response.to_dict())

@app.route('/api/bitcoin')
def get_bitcoin():
    """Get Bitcoin price"""
    btc = fetcher.fetch_bitcoin()
    return jsonify({
        "symbol": btc.symbol,
        "price": btc.price,
        "currency": btc.currency,
        "change_24h": btc.change_24h
    })

@app.route('/api/exchange-rate/<currency>')
def get_rate(currency):
    """Get exchange rate for specific currency"""
    try:
        rate = fetcher.fetch_exchange_rate(currency.upper())
        return jsonify({
            "base": rate.base_currency,
            "target": rate.target_currency,
            "rate": rate.rate
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

---

### Example 2: Scheduled Data Collection

```python
import json
from datetime import datetime
from src.price_fetcher import PriceFetcher

def collect_prices():
    """Collect prices and save to file"""
    fetcher = PriceFetcher()
    
    # Fetch all data
    response = fetcher.fetch_all(fetch_rates=["EUR", "GBP", "JPY"])
    
    # Create data file
    filename = f"prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump(response.to_dict(), f, indent=2)
    
    print(f"Prices saved to {filename}")

# Use with cron or task scheduler
# Run this daily: python -c "from script import collect_prices; collect_prices()"
```

---

### Example 3: Email Alert System

```python
import smtplib
from email.mime.text import MIMEText
from src.price_fetcher import PriceFetcher

def send_alert_if_btc_high(threshold=70000):
    """Send email if Bitcoin price exceeds threshold"""
    fetcher = PriceFetcher()
    btc = fetcher.fetch_bitcoin()
    
    if btc.price > threshold:
        # Create email
        msg = MIMEText(f"Bitcoin is now ${btc.price:,.2f}!")
        msg['Subject'] = f"BTC Alert: ${btc.price:,.2f}"
        msg['From'] = "alerts@example.com"
        msg['To'] = "user@example.com"
        
        # Send email (configure your SMTP settings)
        # with smtplib.SMTP('localhost') as server:
        #     server.send_message(msg)
        
        print(f"Alert: BTC is ${btc.price:,.2f}!")
        return True
    
    return False

# send_alert_if_btc_high(threshold=70000)
```

---

## Before & After Refactoring

### Before (Had Code Smells)

```python
def fetch_bitcoin(self) -> BitcoinPrice:
    return BitcoinPrice(
        price=67890.50,
        timestamp=datetime.utcnow(),  # 🔴 Magic value
        change_24h=2.45,               # 🔴 Hardcoded
        source="coingecko",            # 🔴 String repeated
        symbol="BTC",
        name="Bitcoin",
        currency="USD",
    )

def fetch_gold(self) -> GoldPrice:
    return GoldPrice(
        price=2087.75,
        timestamp=datetime.utcnow(),   # 🔴 Same call again
        change_24h=0.35,               # 🔴 Duplicated
        # ...
    )

def fetch_exchange_rate(self, target_currency: str) -> ExchangeRate:
    # ... validation ...
    exchange_rates = {
        "EUR": 0.92,                   # 🔴 Inline dictionary
        "GBP": 0.79,
        # ... 10 more ...
    }
```

**Problems:**
- ❌ `datetime.utcnow()` called multiple times
- ❌ Exchange rates duplicated in each method
- ❌ Magic numbers scattered everywhere
- ❌ Hard to update prices or rates
- ❌ Not testable (can't mock timestamp easily)

---

### After (Clean, Professional)

```python
class PriceFetcher:
    # Constants organized at class level
    BITCOIN_DATA = {
        "price": 67890.50,
        "change_24h": 2.45,
        "source": "coingecko",
        # ...
    }
    
    GOLD_DATA = {
        "price": 2087.75,
        "change_24h": 0.35,
        # ...
    }
    
    EXCHANGE_RATES = {
        "EUR": 0.92,
        "GBP": 0.79,
        # ... all 12 currencies ...
    }

    def _get_current_timestamp(self) -> datetime:
        """✅ Single source of truth for timestamps"""
        return datetime.utcnow()

    def fetch_bitcoin(self) -> BitcoinPrice:
        return BitcoinPrice(
            price=self.BITCOIN_DATA["price"],
            timestamp=self._get_current_timestamp(),
            # ...
        )
```

**Benefits:**
- ✅ Single timestamp method (DRY principle)
- ✅ Constants at top level (easy to update)
- ✅ No magic numbers in methods
- ✅ Testable (can mock _get_current_timestamp)
- ✅ Professional, maintainable code

---

## Using in Your Own Project

### Step 1: Copy the Pattern

Use this project as a template for YOUR SDD project:

```bash
# Clone this project
git clone https://github.com/yourusername/sdd_test.git
cd sdd_test

# Create your own specs
cp specs/price_fetcher.spec.yaml specs/my_feature.spec.yaml

# Edit the spec to match your needs
# Then follow the SDD cycle:
# 1. Write spec
# 2. Write tests based on spec
# 3. Watch tests fail (RED)
# 4. Write code (GREEN)
# 5. Refactor (REFACTOR)
```

---

### Step 2: Create Your Own Specification

```yaml
# specs/your_feature.spec.yaml
spec:
  name: YourFeatureName
  description: What it does
  version: 1.0.0

scenarios:
  - name: "User story description"
    given:
      - "Initial state"
    when:
      - "User action"
    then:
      - "Expected outcome"

data_types:
  YourModel:
    field1: type
    field2: type

examples:
  valid_example:
    field1: value1
    field2: value2
```

---

### Step 3: Follow SDD Cycle

```bash
# 1. SPECIFY: Write your spec ✓ (done above)

# 2. GENERATE: Create test file based on spec
# tests/test_your_feature.py

# 3. RED: Watch tests fail
pytest tests/test_your_feature.py
# Output: FAILED - NotImplementedError

# 4. GREEN: Write code to pass tests
# src/your_module.py
# Implement the functionality

# 5. REFACTOR: Improve without breaking tests
# Extract constants, improve names, etc.
pytest tests/  # Still passing!
```

---

## Tips & Best Practices

✅ **Do:**
- Write specs BEFORE code
- Keep specifications readable
- Test against the spec, not implementation
- Refactor after tests pass
- Document with examples

❌ **Don't:**
- Skip the spec writing phase
- Write tests for implementation details
- Refactor without tests passing
- Make assumptions about behavior
- Assume code will speak for itself

---

<div align="center">

**These examples show that the SDD process produces:**
- ✅ Understandable code
- ✅ Reliable behavior
- ✅ Easy integration
- ✅ Maintainable projects

**Use these patterns in your own work!**

[← Back to README](../README.md) | [← Usage Reference](03-usage-reference.md) | [Contributing →](05-contribute.md)

</div>
