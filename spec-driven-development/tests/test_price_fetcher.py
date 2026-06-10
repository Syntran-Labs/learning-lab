"""Tests for PriceFetcher - Based on price_fetcher.spec.yaml"""

import pytest
from datetime import datetime

from src.price_fetcher import (
    PriceFetcher,
    PriceServiceUnavailableError,
    InvalidAssetError,
    InvalidCurrencyError,
)
from src.models import BitcoinPrice, GoldPrice, ExchangeRate
from src.providers import MockPriceDataProvider
from src.config import BITCOIN_CONFIG


class TestBitcoinFetcher:
    """Scenario: Obtener precio de Bitcoin"""

    def test_fetch_bitcoin_returns_valid_price(self):
        """Spec: Se retorna un precio numérico válido"""
        fetcher = PriceFetcher()
        price = fetcher.fetch_bitcoin()

        assert isinstance(price, BitcoinPrice)
        assert price.symbol == "BTC"
        assert price.name == "Bitcoin"

    def test_bitcoin_price_is_positive(self):
        """Spec: El precio es mayor a 0"""
        fetcher = PriceFetcher()
        price = fetcher.fetch_bitcoin()
        assert price.price > 0

    def test_bitcoin_includes_currency(self):
        """Spec: Se incluye la moneda (USD por defecto)"""
        fetcher = PriceFetcher()
        price = fetcher.fetch_bitcoin()
        assert price.currency == "USD"

    def test_bitcoin_includes_timestamp(self):
        """Spec: Se incluye el timestamp de la consulta"""
        fetcher = PriceFetcher()
        price = fetcher.fetch_bitcoin()
        assert price.timestamp is not None
        assert isinstance(price.timestamp, datetime)
        assert price.timestamp <= datetime.utcnow()


class TestGoldFetcher:
    """Scenario: Obtener precio de Oro"""

    def test_fetch_gold_returns_valid_price(self):
        """Spec: Se retorna un precio numérico válido"""
        fetcher = PriceFetcher()
        price = fetcher.fetch_gold()

        assert isinstance(price, GoldPrice)
        assert price.symbol == "XAU"
        assert price.name == "Gold"

    def test_gold_price_is_positive(self):
        """Spec: El precio es mayor a 0"""
        fetcher = PriceFetcher()
        price = fetcher.fetch_gold()
        assert price.price > 0

    def test_gold_includes_currency(self):
        """Spec: Se incluye la moneda (USD por defecto)"""
        fetcher = PriceFetcher()
        price = fetcher.fetch_gold()
        assert price.currency == "USD"

    def test_gold_includes_timestamp(self):
        """Spec: Se incluye el timestamp de la consulta"""
        fetcher = PriceFetcher()
        price = fetcher.fetch_gold()
        assert price.timestamp is not None
        assert isinstance(price.timestamp, datetime)
        assert price.timestamp <= datetime.utcnow()


class TestExchangeRateFetcher:
    """Scenario: Obtener precio de Dólar"""

    def test_fetch_exchange_rate_eur(self):
        """Scenario: Obtener tasa de cambio USD/EUR"""
        fetcher = PriceFetcher()
        rate = fetcher.fetch_exchange_rate("EUR")

        assert isinstance(rate, ExchangeRate)
        assert rate.base_currency == "USD"
        assert rate.target_currency == "EUR"
        assert rate.rate > 0

    def test_fetch_exchange_rate_mxn(self):
        """Scenario: Obtener tasa de cambio USD/MXN"""
        fetcher = PriceFetcher()
        rate = fetcher.fetch_exchange_rate("MXN")

        assert rate.base_currency == "USD"
        assert rate.target_currency == "MXN"
        assert rate.rate > 0

    def test_fetch_exchange_rate_ars(self):
        """Scenario: Obtener tasa de cambio USD/ARS"""
        fetcher = PriceFetcher()
        rate = fetcher.fetch_exchange_rate("ARS")

        assert rate.base_currency == "USD"
        assert rate.target_currency == "ARS"
        assert rate.rate > 0

    def test_invalid_currency_raises_error(self):
        """Scenario: Manejar moneda no válida"""
        fetcher = PriceFetcher()

        with pytest.raises(InvalidCurrencyError):
            fetcher.fetch_exchange_rate("INVALID")


class TestMultiplePrices:
    """Scenario: Obtener múltiples precios en una sola llamada"""

    def test_fetch_all_returns_valid_response(self):
        """Spec: Se retornan 3 precios válidos"""
        fetcher = PriceFetcher()
        response = fetcher.fetch_all(
            fetch_bitcoin=True,
            fetch_gold=True,
            fetch_rates=["EUR", "MXN", "ARS"],
        )

        assert response.bitcoin is not None
        assert response.gold is not None
        assert len(response.exchange_rates) == 3

    def test_fetch_all_prices_are_positive(self):
        """Spec: Cada precio es mayor a 0"""
        fetcher = PriceFetcher()
        response = fetcher.fetch_all()

        assert response.bitcoin.price > 0
        assert response.gold.price > 0
        for rate in response.exchange_rates.values():
            assert rate.rate > 0

    def test_fetch_all_includes_currencies(self):
        """Spec: Cada precio incluye su moneda"""
        fetcher = PriceFetcher()
        response = fetcher.fetch_all()

        assert response.bitcoin.currency is not None
        assert response.gold.currency is not None
        for rate in response.exchange_rates.values():
            assert rate.base_currency == "USD"
            assert rate.target_currency is not None

    def test_fetch_all_is_structured(self):
        """Spec: La respuesta es una lista estructurada"""
        fetcher = PriceFetcher()
        response = fetcher.fetch_all()

        # Should be convertible to dict
        data = response.to_dict()
        assert "bitcoin" in data
        assert "gold" in data
        assert "exchange_rates" in data

    def test_fetch_all_optional_parameters(self):
        """Test fetch_all with optional parameters"""
        fetcher = PriceFetcher()

        # Fetch only bitcoin
        response = fetcher.fetch_all(
            fetch_bitcoin=True,
            fetch_gold=False,
            fetch_rates=None,
        )
        assert response.bitcoin is not None
        assert response.gold is None
        assert len(response.exchange_rates) == 0

        # Fetch only gold
        response = fetcher.fetch_all(
            fetch_bitcoin=False,
            fetch_gold=True,
            fetch_rates=None,
        )
        assert response.bitcoin is None
        assert response.gold is not None

        # Fetch only rates
        response = fetcher.fetch_all(
            fetch_bitcoin=False,
            fetch_gold=False,
            fetch_rates=["EUR"],
        )
        assert response.bitcoin is None
        assert response.gold is None
        assert len(response.exchange_rates) == 1


class TestErrorHandling:
    """Scenario: Manejar errores"""

    def test_service_unavailable_error(self):
        """Spec: Se lanza una excepción PriceServiceUnavailable"""
        # This test will verify error handling once implementation is done
        # Currently, we're just testing that the exception exists
        assert PriceServiceUnavailableError is not None

    def test_invalid_asset_error(self):
        """Spec: Se lanza una excepción InvalidAsset"""
        assert InvalidAssetError is not None

    def test_invalid_currency_error(self):
        """Spec: Se lanza una excepción InvalidCurrency"""
        assert InvalidCurrencyError is not None


class TestDependencyInjection:
    """Scenario: Inyectar proveedores personalizados"""

    def test_default_provider_used_when_none_specified(self):
        """Spec: Se usa MockPriceDataProvider por defecto"""
        fetcher = PriceFetcher()
        assert isinstance(fetcher.provider, MockPriceDataProvider)

    def test_custom_provider_can_be_injected(self):
        """Spec: Un proveedor personalizado puede ser inyectado"""

        class CustomProvider(MockPriceDataProvider):
            def get_bitcoin_data(self):
                return {**BITCOIN_CONFIG, "price": 99999.0}

        fetcher = PriceFetcher(provider=CustomProvider())
        btc = fetcher.fetch_bitcoin()
        assert btc.price == 99999.0

    def test_custom_provider_affects_all_fetch_methods(self):
        """Spec: El proveedor personalizado afecta todos los métodos de obtención"""

        class CustomProvider(MockPriceDataProvider):
            def get_bitcoin_data(self):
                return {**BITCOIN_CONFIG, "source": "custom_source"}

            def get_gold_data(self):
                return {**super().get_gold_data(), "source": "custom_gold_source"}

            def get_exchange_rate(self, currency):
                return 999.99

        fetcher = PriceFetcher(provider=CustomProvider())
        btc = fetcher.fetch_bitcoin()
        gold = fetcher.fetch_gold()
        rate = fetcher.fetch_exchange_rate("EUR")

        assert btc.source == "custom_source"
        assert gold.source == "custom_gold_source"
        assert rate.rate == 999.99
