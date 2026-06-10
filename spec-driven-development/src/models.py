"""Data models based on specifications"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from .config import VALID_CURRENCIES


@dataclass
class BitcoinPrice:
    """BitcoinPrice spec from bitcoin.spec.yaml"""
    price: float
    timestamp: datetime
    change_24h: float
    source: str
    symbol: str = "BTC"
    name: str = "Bitcoin"
    currency: str = "USD"

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError(f"Bitcoin price must be positive, got {self.price}")
        if not (1000 <= self.price <= 200000):
            raise ValueError(f"Bitcoin price seems unreasonable: {self.price}")
        if self.symbol != "BTC":
            raise ValueError("Bitcoin symbol must be 'BTC'")


@dataclass
class GoldPrice:
    """GoldPrice spec from gold.spec.yaml"""
    price: float
    timestamp: datetime
    change_24h: float
    source: str
    symbol: str = "XAU"
    name: str = "Gold"
    currency: str = "USD"
    unit: str = "troy ounce"

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError(f"Gold price must be positive, got {self.price}")
        if not (1000 <= self.price <= 3000):
            raise ValueError(f"Gold price seems unreasonable: {self.price}")
        if self.symbol != "XAU":
            raise ValueError("Gold symbol must be 'XAU'")
        if self.unit != "troy ounce":
            raise ValueError("Gold unit must be 'troy ounce'")


@dataclass
class ExchangeRate:
    """ExchangeRate spec from currency.spec.yaml"""
    rate: float
    timestamp: datetime
    source: str
    base_currency: str = "USD"
    target_currency: str = ""

    def __post_init__(self):
        if self.rate <= 0:
            raise ValueError(f"Exchange rate must be positive, got {self.rate}")
        if self.base_currency != "USD":
            raise ValueError(f"Base currency must be USD, got {self.base_currency}")
        if self.target_currency not in VALID_CURRENCIES:
            raise ValueError(
                f"Invalid target currency: {self.target_currency}. "
                f"Valid currencies: {', '.join(sorted(VALID_CURRENCIES))}"
            )


@dataclass
class PriceResponse:
    """Combined response containing multiple prices"""
    bitcoin: Optional[BitcoinPrice] = None
    gold: Optional[GoldPrice] = None
    exchange_rates: Optional[Dict[str, ExchangeRate]] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
        if not self.exchange_rates:
            self.exchange_rates = {}

    def to_dict(self) -> Dict:
        """
        Convert to dictionary representation.

        Returns:
            Dictionary containing all price data in serializable format
        """
        return {
            "bitcoin": self.bitcoin.__dict__ if self.bitcoin else None,
            "gold": self.gold.__dict__ if self.gold else None,
            "exchange_rates": {
                k: v.__dict__ for k, v in self.exchange_rates.items()
            } if self.exchange_rates else None,
            "timestamp": self.timestamp.isoformat(),
        }
