"""Price data providers for dependency injection"""

from typing import Protocol, Set, Dict
from .config import BITCOIN_CONFIG, GOLD_CONFIG, EXCHANGE_RATES_CONFIG, VALID_CURRENCIES


class PriceDataProvider(Protocol):
    """Protocol defining the interface for price data providers"""

    def get_bitcoin_data(self) -> Dict:
        """Get Bitcoin price data"""
        ...

    def get_gold_data(self) -> Dict:
        """Get Gold price data"""
        ...

    def get_exchange_rate(self, currency: str) -> float:
        """Get exchange rate for a specific currency"""
        ...

    def get_supported_currencies(self) -> Set[str]:
        """Get set of supported currency codes"""
        ...


class MockPriceDataProvider:
    """
    Default provider that returns hardcoded mock data.
    Implements PriceDataProvider protocol.
    """

    def get_bitcoin_data(self) -> Dict:
        """Return Bitcoin price data from config"""
        return BITCOIN_CONFIG.copy()

    def get_gold_data(self) -> Dict:
        """Return Gold price data from config"""
        return GOLD_CONFIG.copy()

    def get_exchange_rate(self, currency: str) -> float:
        """Return exchange rate for target currency"""
        return EXCHANGE_RATES_CONFIG.get(currency, 1.0)

    def get_supported_currencies(self) -> Set[str]:
        """Return set of supported currencies"""
        return VALID_CURRENCIES.copy()
