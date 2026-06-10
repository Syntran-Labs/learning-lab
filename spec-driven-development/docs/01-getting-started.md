# Getting Started

Get this project running in **5 minutes**.

---

## Prerequisites

- Python 3.10 or higher
- pip (comes with Python)
- Git (optional, but recommended)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sdd_test.git
cd sdd_test
```

Or download as ZIP and extract.

### 2. Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows PowerShell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Verify Installation

Run the tests to confirm everything works:

```bash
pytest tests/ -v
```

Expected output: `41 passed` ✅

---

## First Commands

### Get Bitcoin Price

```bash
python -m src bitcoin
```

Output:
```
============================================================
  Bitcoin Price
============================================================

  Bitcoin              $ 67,890.50 USD (+2.45%)

  Source: coingecko
  Time: 2026-06-10T15:32:44.123456
```

### Get Gold Price

```bash
python -m src gold
```

### Get Exchange Rate

```bash
python -m src rate EUR
python -m src rate MXN
```

### See All Prices

```bash
python -m src all EUR,GBP,JPY
```

### Export as JSON

```bash
python -m src json > prices.json
```

### View Help

```bash
python -m src help
```

---

## Using as Python Module

```python
from src.price_fetcher import PriceFetcher

fetcher = PriceFetcher()
btc = fetcher.fetch_bitcoin()

print(f"Bitcoin: ${btc.price:,.2f}")
```

**[→ More usage examples](04-examples.md)**

---

## Troubleshooting

### "Python 3.10+ required"

Check your Python version:

```bash
python --version
```

If you have Python 3.9 or lower, [install Python 3.10+](https://www.python.org/downloads/)

### "ModuleNotFoundError: No module named 'src'"

Make sure you're in the project root directory:

```bash
# Correct ✅
cd /path/to/sdd_test
python -m src bitcoin

# Wrong ❌
cd src
python -m src bitcoin
```

### "Tests fail to import"

Ensure virtual environment is activated and dependencies installed:

```bash
# Activate venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

### Virtual Environment Not Activating

**Windows PowerShell:**
If you get an error about execution policy:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
venv\Scripts\Activate.ps1
```

---

## Next Steps

- **Learn SDD:** [→ Learning SDD](02-learning-sdd.md)
- **Understand Usage:** [→ Usage Reference](03-usage-reference.md)
- **See Examples:** [→ Real-world Examples](04-examples.md)
- **Run Tests:** `pytest tests/ -v`

---

## Getting Help

- Read the [Usage Reference](03-usage-reference.md)
- Check [Examples](04-examples.md) for real-world use
- Read [FAQ in Usage Guide](03-usage-reference.md#troubleshooting)
- Open an issue on GitHub

---

[← Back to README](../README.md)
