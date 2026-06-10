# Tutorial: Adding a New Asset (Ethereum Example)

Step-by-step guide to extend the Price Fetcher with a new asset using professional patterns.

---

## Prerequisites

Before you start:

- ✅ Read [Extending the Architecture](07-extending-architecture.md)
- ✅ Understand the 6-step pattern (Spec → Model → Config → Provider → Fetcher → CLI)
- ✅ Have your development environment ready
- ✅ Know how to run tests: `pytest tests/ -v`

---

## Step 1: Write the Specification

Spec-Driven Development always starts with a specification.

Create `specs/ethereum.spec.yaml`:

```yaml
---
openspec: 1.0
title: Ethereum Price
parent: PriceFetcher
version: 1.0.0

scenarios:
  - title: "Obtener precio de Ethereum"
    given: "El servicio de precios está disponible"
    when: "Se solicita el precio de Ethereum"
    then:
      - "Se retorna un precio numérico válido"
      - "El símbolo es 'ETH'"
      - "El nombre es 'Ethereum'"
      - "La moneda es 'USD'"
      - "Se incluye el timestamp de la consulta"

  - title: "Precio de Ethereum es razonable"
    given: "El precio de Ethereum está dentro de rangos históricos"
    then:
      - "El precio debe estar entre 500 y 50,000 USD"
      - "El cambio 24h es un porcentaje válido"

  - title: "Ethereum identifica correctamente su símbolo"
    then:
      - "symbol == 'ETH'"
      - "name == 'Ethereum'"

data_types:
  EthereumPrice:
    fields:
      price: float
      timestamp: datetime
      change_24h: float
      source: str
      symbol: str = "ETH"
      name: str = "Ethereum"
      currency: str = "USD"

examples:
  - symbol: ETH
    name: Ethereum
    price: 3425.50
    currency: USD
    change_24h: 5.25
    source: "coingecko"
    timestamp: "2026-06-10T02:30:00Z"

  - symbol: ETH
    name: Ethereum
    price: 3421.75
    currency: USD
    change_24h: 4.82
    source: "coinmarketcap"
    timestamp: "2026-06-10T02:31:00Z"
```

**Why this matters:** The specification is your contract. Tests will verify it's implemented correctly.

---

## Step 2: Add the Data Model

Edit `src/models.py` and add the `EthereumPrice` dataclass:

```python
@dataclass
class EthereumPrice:
    """EthereumPrice spec from ethereum.spec.yaml"""
    price: float
    timestamp: datetime
    change_24h: float
    source: str
    symbol: str = "ETH"
    name: str = "Ethereum"
    currency: str = "USD"

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError(f"Ethereum price must be positive, got {self.price}")
        if not (500 <= self.price <= 50000):
            raise ValueError(f"Ethereum price seems unreasonable: {self.price}")
        if self.symbol != "ETH":
            raise ValueError("Ethereum symbol must be 'ETH'")
```

### 📊 Choosing Price Bounds

The bounds in `__post_init__` represent realistic price ranges:

- **Lower bound (500):** Minimum realistic price with safety margin
- **Upper bound (50,000):** Maximum realistic price with safety margin

For Ethereum, this captures historical range (roughly $0.50 to $4,800) with 2x buffer on each side.

**For your asset:**
1. Research historical price range
2. Add 2x buffer on each side for safety
3. Update bounds if the asset moves significantly

---

## Step 3: Add Configuration

Edit `src/config.py` and add the mock data:

```python
ETHEREUM_CONFIG = {
    "price": 3425.50,
    "change_24h": 5.25,
    "source": "coingecko",
    "symbol": "ETH",
    "name": "Ethereum",
    "currency": "USD",
}
```

**Why this matters:** Configuration is separate from code. Easy to update prices without touching logic.

---

## Step 4: Extend the Provider Protocol

Edit `src/providers.py` and update **both** the protocol and the default implementation:

### Update the Protocol

```python
class PriceDataProvider(Protocol):
    """Protocol defining the interface for price data providers"""

    def get_bitcoin_data(self) -> Dict: ...
    def get_gold_data(self) -> Dict: ...
    def get_ethereum_data(self) -> Dict: ...  # ← NEW
    def get_exchange_rate(self, currency: str) -> float: ...
    def get_supported_currencies(self) -> Set[str]: ...
```

### Update the Default Implementation

```python
class MockPriceDataProvider:
    """Default provider that returns hardcoded mock data."""

    def get_bitcoin_data(self) -> Dict:
        return BITCOIN_CONFIG.copy()

    def get_gold_data(self) -> Dict:
        return GOLD_CONFIG.copy()

    def get_ethereum_data(self) -> Dict:  # ← NEW
        return ETHEREUM_CONFIG.copy()

    def get_exchange_rate(self, currency: str) -> float:
        return EXCHANGE_RATES_CONFIG.get(currency, 1.0)

    def get_supported_currencies(self) -> Set[str]:
        return VALID_CURRENCIES.copy()
```

### ⚠️ Protocol Contract

The `PriceDataProvider` protocol is a **contract**. Your custom provider **must implement all methods**.

If you forget a method, the code will compile but fail at runtime:

```python
# ❌ WRONG: Missing get_supported_currencies()
class IncompleteProvider(MockPriceDataProvider):
    def get_ethereum_data(self):
        return {...}
    # Missing other methods!

# This compiles:
fetcher = PriceFetcher(provider=IncompleteProvider())

# But this crashes:
fetcher.fetch_exchange_rate("EUR")  # AttributeError!
```

**Always implement all protocol methods.** Use your IDE's "Implement missing methods" feature.

---

## Step 5: Add the Fetcher Method

Edit `src/price_fetcher.py`:

### Import the New Model

```python
from .models import BitcoinPrice, GoldPrice, EthereumPrice, ExchangeRate, PriceResponse
```

### Add the Fetch Method

```python
def fetch_ethereum(self) -> EthereumPrice:
    """
    Fetch Ethereum price.

    Returns:
        EthereumPrice: Ethereum price with current timestamp

    Spec: ethereum.spec.yaml
    """
    data = self.provider.get_ethereum_data()
    return EthereumPrice(
        timestamp=self._get_current_timestamp(),
        **data,
    )
```

**Pattern:** All fetch methods follow the same structure:
1. Get data from provider
2. Create model with timestamp
3. Return typed object

---

## Step 6: Write Tests

### Test the Model

Edit `tests/test_models.py` and add Ethereum model tests:

```python
class TestEthereumPrice:
    """Scenario: Obtener precio de Ethereum"""

    def test_valid_ethereum_price(self):
        """Spec: Se retorna un precio numérico válido"""
        from src.config import ETHEREUM_CONFIG
        
        eth = EthereumPrice(
            timestamp=datetime.now(),
            **ETHEREUM_CONFIG
        )
        assert eth.symbol == "ETH"
        assert eth.name == "Ethereum"

    def test_ethereum_price_must_be_positive(self):
        """Spec: El precio es mayor a 0"""
        with pytest.raises(ValueError):
            EthereumPrice(
                price=-100,
                timestamp=datetime.now(),
                change_24h=0,
                source="test",
            )

    def test_ethereum_price_must_be_reasonable(self):
        """Spec: El precio es razonable (500-50000)"""
        with pytest.raises(ValueError):
            EthereumPrice(
                price=100,  # Too low
                timestamp=datetime.now(),
                change_24h=0,
                source="test",
            )

    def test_ethereum_symbol_must_be_eth(self):
        """Spec: El símbolo debe ser 'ETH'"""
        with pytest.raises(ValueError):
            EthereumPrice(
                price=3425.50,
                timestamp=datetime.now(),
                change_24h=0,
                source="test",
                symbol="WRONG",
            )
```

### Test the Fetcher

Edit `tests/test_price_fetcher.py` and add Ethereum fetcher tests:

```python
class TestEthereumFetcher:
    """Scenario: Obtener precio de Ethereum"""

    def test_fetch_ethereum_returns_valid_price(self):
        """Spec: Se retorna un precio numérico válido"""
        fetcher = PriceFetcher()
        eth = fetcher.fetch_ethereum()

        assert isinstance(eth, EthereumPrice)
        assert eth.symbol == "ETH"
        assert eth.name == "Ethereum"

    def test_ethereum_price_is_positive(self):
        """Spec: El precio es mayor a 0"""
        fetcher = PriceFetcher()
        eth = fetcher.fetch_ethereum()
        assert eth.price > 0

    def test_ethereum_includes_timestamp(self):
        """Spec: Se incluye el timestamp de la consulta"""
        fetcher = PriceFetcher()
        eth = fetcher.fetch_ethereum()
        assert eth.timestamp is not None
        assert isinstance(eth.timestamp, datetime)
        assert eth.timestamp <= datetime.utcnow()
```

---

## Step 7: Add CLI Support

Edit `src/cli.py` and add the command handler:

```python
def cmd_ethereum(self) -> None:
    """Show Ethereum price"""
    self.print_header("Ethereum Price")
    eth = self.fetcher.fetch_ethereum()
    self.print_price("Ethereum", eth.price, eth.currency, eth.change_24h)
    print(f"\n  Source: {eth.source}")
    print(f"  Time: {eth.timestamp.isoformat()}\n")
```

Update the `run()` method:

```python
elif command == "ethereum":
    self.cmd_ethereum()
```

Update the help text:

```python
def print_help(self) -> None:
    self.print_header("Price Fetcher CLI - Help")
    print("Usage: python -m src.cli <command> [options]\n")
    print("Commands:\n")
    print("  bitcoin              Show Bitcoin price")
    print("  gold                 Show Gold price")
    print("  ethereum             Show Ethereum price")  # ← NEW
    print("  rate <CURRENCY>      Show USD exchange rate (e.g., rate EUR)")
    # ... rest of help ...
```

---

## Verification Checklist

Run all tests to verify everything works:

```bash
# ✅ Run all tests (should all pass)
pytest tests/ -v

# ✅ Try the CLI
python -m src ethereum

# ✅ Try the 'all' command
python -m src all EUR,GBP

# ✅ Try the 'help' command
python -m src help

# ✅ Try custom provider (optional)
python -c "
from src.price_fetcher import PriceFetcher
from src.providers import MockPriceDataProvider
from src.config import ETHEREUM_CONFIG

class TestProvider(MockPriceDataProvider):
    def get_ethereum_data(self):
        return {**ETHEREUM_CONFIG, 'price': 99999.0}

fetcher = PriceFetcher(provider=TestProvider())
print(f'Custom ETH price: \${fetcher.fetch_ethereum().price}')
"
```

All passing? ✅ You've successfully extended the system!

---

## 🔒 Security Consideration: Custom Providers

This tutorial teaches how to create custom providers with **mock data**. If you later extend this to use **real APIs**, follow these practices:

### ❌ WRONG: Unsafe Provider

```python
class UnsafeProvider(MockPriceDataProvider):
    def get_ethereum_data(self):
        # API key hardcoded! ✗
        response = requests.get(
            "https://api.example.com/price?key=sk-1234567890abcdef"
        )
        return response.json()  # No validation! ✗
```

**Problems:**
- API key hardcoded (will leak if committed to git!)
- No response validation (trusts untrusted data)
- No error handling (crashes on bad response)
- No rate limiting (might abuse service)

### ✅ CORRECT: Safe Provider

```python
import os
import requests
from typing import Dict

class SafeProvider(MockPriceDataProvider):
    def __init__(self):
        # Load API key from environment, never hardcode
        self.api_key = os.getenv("COINGECKO_API_KEY")
        if not self.api_key:
            raise ValueError("COINGECKO_API_KEY environment variable not set")
    
    def get_ethereum_data(self) -> Dict:
        try:
            # Use environment variable for API endpoint
            response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={
                    "ids": "ethereum",
                    "vs_currencies": "usd",
                    "include_24hr_change": "true"
                },
                timeout=5,  # Prevent hanging forever
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()  # Check for HTTP errors
            
            # Validate response structure before using
            data = response.json()
            if "ethereum" not in data or "usd" not in data["ethereum"]:
                raise ValueError("Invalid API response structure")
            
            return {
                "price": float(data["ethereum"]["usd"]),
                "change_24h": float(data["ethereum"].get("usd_24h_change", 0)),
                "source": "coingecko",
                "symbol": "ETH",
                "name": "Ethereum",
                "currency": "USD",
            }
        except requests.RequestException as e:
            # Log error but don't expose API details
            raise RuntimeError(f"Failed to fetch Ethereum price: {str(e)}")
```

**Security practices:**
- ✅ API key from environment, never hardcoded
- ✅ Response validation before using data
- ✅ Error handling without exposing internals
- ✅ Request timeout to prevent hanging
- ✅ HTTPS only (URL uses https://)

**If you create a real provider:**

1. **Never hardcode API keys** — Use environment variables or secure vaults
2. **Validate external data** — Don't trust third-party API responses
3. **Add rate limiting** — Prevent accidental abuse of external services
4. **Use HTTPS only** — Encrypt data in transit
5. **Handle errors gracefully** — Don't expose API details in error messages
6. **Add logging** — For debugging in production (don't log sensitive data)

---

## Key Principles You Learned

1. **Spec First:** Always start with a specification
2. **Separation of Concerns:** Config, models, providers, fetchers — each has its place
3. **Protocol-Based Design:** Use protocols to define contracts
4. **Dependency Injection:** Providers are injected, not hardcoded
5. **Consistency:** New assets follow the same pattern as existing ones
6. **Security:** When extending to real APIs, follow secure practices

---

## Result: 6 Clear, Focused Changes

Compare adding an asset with this guide vs. the scattered approach:

**Old way:** Edit PriceFetcher class (3 places), models.py, cli.py (3 places), test files (2 places) = scattered, unclear pattern

**New way:** Spec → Model → Config → Provider → Fetcher → CLI = clear, repeatable pattern

---

## Next Steps

✅ **Your new asset works!** Now you can:

1. **Test it thoroughly** — Add more test cases for edge cases
2. **Contribute it back** — See [Contributing Guide](05-contribute.md)
3. **Document it** — Add examples showing the new asset
4. **Extend further** — Add Silver (XAG), Platinum (XPT), Bonds, etc.

---

**Previous:** [Extending Architecture](07-extending-architecture.md) | **Home:** [Documentation](../README.md)
