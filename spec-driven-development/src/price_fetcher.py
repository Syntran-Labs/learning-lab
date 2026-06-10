"""Price Fetcher implementation based on specifications"""

from datetime import datetime
from typing import Dict, List, Optional

from .models import BitcoinPrice, GoldPrice, ExchangeRate, PriceResponse
from .providers import PriceDataProvider, MockPriceDataProvider


class PriceServiceUnavailableError(Exception):
    """Raised when the price service is unavailable"""


class InvalidAssetError(Exception):
    """Raised when an invalid asset is requested"""


class InvalidCurrencyError(Exception):
    """Raised when an invalid currency is requested"""


class PriceFetcher:
    """
    Main service to fetch prices of Bitcoin, Gold, and Exchange Rates.
    Implements specification from price_fetcher.spec.yaml
    """

    VALID_ASSETS = {"BTC", "XAU", "USD"}
    BITCOIN_SYMBOL = "BTC"
    GOLD_SYMBOL = "XAU"

    def __init__(
        self, provider: Optional[PriceDataProvider] = None, timeout: int = 5
    ) -> None:
        """
        Initialize PriceFetcher.

        Args:
            provider: Price data provider (default: MockPriceDataProvider)
            timeout: Request timeout in seconds (default: 5)
        """
        self.provider = provider or MockPriceDataProvider()
        self.timeout = timeout

    def _get_current_timestamp(self) -> datetime:
        """Get current UTC timestamp for price data."""
        return datetime.utcnow()

    def fetch_bitcoin(self) -> BitcoinPrice:
        """
        Fetch Bitcoin price.

        Returns:
            BitcoinPrice: Bitcoin price with current timestamp

        Spec: bitcoin.spec.yaml
        """
        data = self.provider.get_bitcoin_data()
        return BitcoinPrice(
            timestamp=self._get_current_timestamp(),
            **data,
        )

    def fetch_gold(self) -> GoldPrice:
        """
        Fetch Gold price.

        Returns:
            GoldPrice: Gold price with current timestamp

        Spec: gold.spec.yaml
        """
        data = self.provider.get_gold_data()
        return GoldPrice(
            timestamp=self._get_current_timestamp(),
            **data,
        )

    def fetch_exchange_rate(self, target_currency: str) -> ExchangeRate:
        """
        Fetch exchange rate for USD to target currency.

        Args:
            target_currency: ISO 4217 currency code (e.g., 'EUR', 'MXN')

        Returns:
            ExchangeRate: USD to target currency exchange rate

        Raises:
            InvalidCurrencyError: If target_currency is not supported

        Spec: currency.spec.yaml
        """
        if not self.validate_currency(target_currency):
            raise InvalidCurrencyError(
                f"Invalid target currency: {target_currency}. "
                f"Valid currencies: {', '.join(sorted(self.provider.get_supported_currencies()))}"
            )

        rate = self.provider.get_exchange_rate(target_currency)
        return ExchangeRate(
            rate=rate,
            timestamp=self._get_current_timestamp(),
            source="open_exchange_rates",
            base_currency="USD",
            target_currency=target_currency,
        )

    def fetch_multiple_rates(
        self, target_currencies: List[str]
    ) -> Dict[str, ExchangeRate]:
        """
        Fetch multiple exchange rates in a single call.

        Args:
            target_currencies: List of ISO 4217 currency codes

        Returns:
            Dictionary mapping currency codes to ExchangeRate objects
        """
        return {
            currency: self.fetch_exchange_rate(currency)
            for currency in target_currencies
        }

    def fetch_all(
        self,
        fetch_bitcoin: bool = True,
        fetch_gold: bool = True,
        fetch_rates: Optional[List[str]] = None,
    ) -> PriceResponse:
        """
        Fetch all available prices in a single call.

        Args:
            fetch_bitcoin: Whether to include Bitcoin price (default: True)
            fetch_gold: Whether to include Gold price (default: True)
            fetch_rates: List of currency codes for exchange rates (default: None)

        Returns:
            PriceResponse: Combined price response with requested data

        Spec: price_fetcher.spec.yaml - "Obtener múltiples precios en una sola llamada"
        """
        bitcoin = self.fetch_bitcoin() if fetch_bitcoin else None
        gold = self.fetch_gold() if fetch_gold else None
        exchange_rates = (
            self.fetch_multiple_rates(fetch_rates) if fetch_rates else {}
        )

        return PriceResponse(
            bitcoin=bitcoin,
            gold=gold,
            exchange_rates=exchange_rates,
            timestamp=self._get_current_timestamp(),
        )

    def validate_asset(self, asset: str) -> bool:
        """
        Validate if asset is supported.

        Args:
            asset: Asset symbol to validate

        Returns:
            True if asset is supported, False otherwise
        """
        return asset in self.VALID_ASSETS

    def validate_currency(self, currency: str) -> bool:
        """
        Validate if currency is supported.

        Args:
            currency: Currency code to validate

        Returns:
            True if currency is supported, False otherwise
        """
        return currency in self.provider.get_supported_currencies() or currency == "USD"

    def get_supported_currencies(self) -> List[str]:
        """
        Get list of supported currency codes.

        Returns:
            Sorted list of supported currency codes
        """
        return sorted(self.provider.get_supported_currencies())
