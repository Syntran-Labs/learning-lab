# Extending the Architecture

Professional patterns for customization and extension.

---

## ⚠️ Overview

This guide teaches professional architectural patterns that make software extensible. You'll learn how to:

- ✅ Separate configuration from code
- ✅ Use dependency injection for flexibility
- ✅ Design extensible systems that scale

All examples use **mock data** (this is an educational project, not a financial service).

---

## Part 1: Configuration Management

### The Problem: Hardcoded Config

Initial implementations often hardcode configuration:

```python
# ❌ BAD: Config is mixed with logic
class PriceFetcher:
    BITCOIN_DATA = {"price": 67890.50, "source": "coingecko", ...}
    GOLD_DATA = {"price": 2087.75, ...}
    EXCHANGE_RATES = {"EUR": 0.92, "GBP": 0.79, ...}
    
    def fetch_bitcoin(self):
        return BitcoinPrice(**self.BITCOIN_DATA, ...)
```

**Problems:**
- Changing prices requires editing code
- Testing is difficult (can't override values)
- Configuration mixed with business logic
- Not scalable for real APIs

### The Solution: Extract Configuration

Move all static data to a configuration module:

```python
# ✅ GOOD: Config in one place
# src/config.py
BITCOIN_CONFIG = {"price": 67890.50, "source": "coingecko", ...}
GOLD_CONFIG = {"price": 2087.75, ...}
EXCHANGE_RATES_CONFIG = {"EUR": 0.92, "GBP": 0.79, ...}
VALID_CURRENCIES = {"EUR", "GBP", "JPY", ...}

# src/price_fetcher.py
from .config import BITCOIN_CONFIG

class PriceFetcher:
    def fetch_bitcoin(self):
        return BitcoinPrice(**BITCOIN_CONFIG, ...)
```

**Benefits:**
- ✅ Configuration in one place
- ✅ Easy to override for tests
- ✅ Ready to load from environment variables later
- ✅ Clear separation: config vs. logic

### Why This Matters

**For Testing:**
```python
def test_custom_bitcoin_price():
    # Create test config without modifying source
    test_config = {**BITCOIN_CONFIG, "price": 99999.0}
    # Can now test edge cases easily
```

**For Production Evolution:**
```python
# Later: load from environment
import os

BITCOIN_CONFIG = {
    "price": float(os.getenv("BITCOIN_PRICE", "67890.50")),
    "source": os.getenv("PRICE_SOURCE", "coingecko"),
}
```

---

## Part 2: Dependency Injection

### The Problem: Dependencies Hardcoded

Services often create their own dependencies:

```python
# ❌ BAD: Tightly coupled, untestable
class PriceFetcher:
    def __init__(self):
        # Hardcoded dependency
        self.data_source = CoinGeckoAPI()  # Always this API!
    
    def fetch_bitcoin(self):
        return self.data_source.get_bitcoin()  # Can't test without real API
```

**Problems:**
- Can't test without external services
- Hard to swap implementations
- Difficult to mock for testing
- Not flexible for different use cases

### The Solution: Protocol-Based Design

Define a contract that data sources must follow:

```python
# ✅ GOOD: Protocol-based design
from typing import Protocol, Dict, Set

class PriceDataProvider(Protocol):
    """Contract that all providers must follow"""
    def get_bitcoin_data(self) -> Dict: ...
    def get_gold_data(self) -> Dict: ...
    def get_exchange_rate(self, currency: str) -> float: ...
    def get_supported_currencies(self) -> Set[str]: ...

class PriceFetcher:
    def __init__(self, provider: PriceDataProvider = None):
        # Dependency injected; default if not provided
        self.provider = provider or MockPriceDataProvider()
    
    def fetch_bitcoin(self):
        data = self.provider.get_bitcoin_data()
        return BitcoinPrice(timestamp=..., **data)
```

Implement the protocol:

```python
class MockPriceDataProvider:
    """Default: returns mock data from config"""
    def get_bitcoin_data(self) -> Dict:
        return BITCOIN_CONFIG.copy()
    
    def get_exchange_rate(self, currency: str) -> float:
        return EXCHANGE_RATES_CONFIG.get(currency, 1.0)
    
    # ... other methods
```

**Benefits:**
- ✅ Testable: inject mock providers in tests
- ✅ Flexible: swap providers at runtime
- ✅ Clear contract: protocol defines requirements
- ✅ Extensible: implement protocol for new sources

### Testing with DI

Now testing is simple:

```python
def test_with_custom_price():
    class TestProvider(MockPriceDataProvider):
        def get_bitcoin_data(self):
            return {**BITCOIN_CONFIG, "price": 99999.0}
    
    fetcher = PriceFetcher(provider=TestProvider())
    assert fetcher.fetch_bitcoin().price == 99999.0  # ✅ Works!
```

No need to mock external APIs, no complex setup.

---

## Part 3: Clear Extension Pattern

### The Problem: Adding New Assets is Scattered

Before refactoring, adding a new asset (e.g., Ethereum) required:

1. Add `ETHEREUM_DATA` to `PriceFetcher` class
2. Add `EthereumPrice` model in `models.py`
3. Add `fetch_ethereum()` method in `PriceFetcher`
4. Update CLI with new command
5. Edit multiple test files
6. No clear pattern; feels like scattered edits

### The Solution: The 6-Step Pattern

Now there's a clear, discoverable pattern:

```
1. Spec       → specs/ethereum.spec.yaml
2. Model      → src/models.py (add EthereumPrice)
3. Config     → src/config.py (add ETHEREUM_CONFIG)
4. Provider   → src/providers.py (add get_ethereum_data())
5. Fetcher    → src/price_fetcher.py (add fetch_ethereum())
6. CLI        → src/cli.py (add command)
```

Each change goes in a **logical place**. Each follows an **obvious pattern**.

### Comparison: Before vs. After

| Aspect | Before | After |
|--------|--------|-------|
| **Where to start** | Unclear | Write spec first |
| **Where does config go** | In service class | config.py (one place) |
| **Where does data access go** | In service class | providers.py (protocol) |
| **How to test alternative data** | Mock the entire service | Inject a provider |
| **Adding new asset location** | Scattered across 5+ files | 6 focused changes |
| **Pattern clarity** | No clear pattern | Obvious, repeatable pattern |

---

## Key Principles

### 1. Separation of Concerns

Each module has one job:

- **config.py** — Holds all static data
- **providers.py** — Handles data source abstraction
- **models.py** — Defines data structures and validation
- **price_fetcher.py** — Orchestrates fetching
- **cli.py** — User interface

### 2. Protocol-Based Design

Define contracts, not implementations:

```python
# Protocol: "What should a provider do?"
class PriceDataProvider(Protocol):
    def get_bitcoin_data(self) -> Dict: ...

# Implementation: "How should a provider do it?"
class MockPriceDataProvider:
    def get_bitcoin_data(self) -> Dict:
        return BITCOIN_CONFIG.copy()
```

### 3. Dependency Injection

Never hardcode dependencies:

```python
# ❌ BAD
fetcher = PriceFetcher(MockPriceDataProvider())  # Hardcoded

# ✅ GOOD
def create_fetcher(provider: PriceDataProvider = None):
    return PriceFetcher(provider or MockPriceDataProvider())
```

### 4. Configuration as Data

Configuration is separate from code:

```python
# ❌ BAD: Config in code
class PriceFetcher:
    BITCOIN_PRICE = 67890.50  # In source!

# ✅ GOOD: Config in data file
# config.py
BITCOIN_CONFIG = {"price": 67890.50}
```

---

## Next Steps

Ready to apply these patterns?

**→ [Step-by-Step Tutorial: Add a New Asset](08-tutorial-add-ethereum.md)**

Want to contribute back?

**→ [Contributing Guide](05-contribute.md)**

---

**Previous:** [Contributing](05-contribute.md) | **Next:** [Tutorial: Add Ethereum](08-tutorial-add-ethereum.md)
