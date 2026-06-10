"""Tests for data models - Based on specs"""

import pytest
from datetime import datetime

from src.models import BitcoinPrice, GoldPrice, ExchangeRate, PriceResponse


class TestBitcoinPrice:
    """Scenarios from bitcoin.spec.yaml"""

    def test_valid_bitcoin_price(self):
        """Example: valid_bitcoin_price"""
        price = BitcoinPrice(
            price=45000.50,
            timestamp=datetime(2026, 6, 9, 10, 30, 0),
            change_24h=2.5,
            source="coingecko",
            symbol="BTC",
            name="Bitcoin",
            currency="USD",
        )
        assert price.symbol == "BTC"
        assert price.price == 45000.50
        assert price.currency == "USD"

    def test_bitcoin_price_must_be_positive(self):
        """Spec: Bitcoin price must be positive"""
        with pytest.raises(ValueError, match="must be positive"):
            BitcoinPrice(
                price=-100.0,
                timestamp=datetime.now(),
                change_24h=0.0,
                source="test",
            )

    def test_bitcoin_price_must_be_reasonable(self):
        """Spec: Price of Bitcoin is razonable - between 1,000 and 200,000"""
        with pytest.raises(ValueError, match="unreasonable"):
            BitcoinPrice(
                price=500.0,  # Too low
                timestamp=datetime.now(),
                change_24h=0.0,
                source="test",
            )

        with pytest.raises(ValueError, match="unreasonable"):
            BitcoinPrice(
                price=250000.0,  # Too high
                timestamp=datetime.now(),
                change_24h=0.0,
                source="test",
            )

    def test_bitcoin_symbol_must_be_btc(self):
        """Spec: Bitcoin symbol must be 'BTC'"""
        with pytest.raises(ValueError, match="BTC"):
            BitcoinPrice(
                symbol="BTC_WRONG",
                price=50000.0,
                timestamp=datetime.now(),
                change_24h=0.0,
                source="test",
            )

    def test_bitcoin_defaults(self):
        """Spec: Bitcoin debe cotizar en USD"""
        price = BitcoinPrice(
            price=50000.0,
            timestamp=datetime.now(),
            change_24h=0.0,
            source="test",
        )
        assert price.symbol == "BTC"
        assert price.name == "Bitcoin"
        assert price.currency == "USD"


class TestGoldPrice:
    """Scenarios from gold.spec.yaml"""

    def test_valid_gold_price(self):
        """Example: valid_gold_price"""
        price = GoldPrice(
            price=2045.50,
            timestamp=datetime(2026, 6, 9, 10, 30, 0),
            change_24h=0.5,
            source="london_metal_exchange",
            symbol="XAU",
            name="Gold",
            currency="USD",
            unit="troy ounce",
        )
        assert price.symbol == "XAU"
        assert price.price == 2045.50
        assert price.unit == "troy ounce"

    def test_gold_price_must_be_positive(self):
        """Spec: Gold price must be positive"""
        with pytest.raises(ValueError, match="must be positive"):
            GoldPrice(
                price=-100.0,
                timestamp=datetime.now(),
                change_24h=0.0,
                source="test",
            )

    def test_gold_price_must_be_reasonable(self):
        """Spec: Price of Gold is reasonable - between 1,000 and 3,000"""
        with pytest.raises(ValueError, match="unreasonable"):
            GoldPrice(
                price=500.0,  # Too low
                timestamp=datetime.now(),
                change_24h=0.0,
                source="test",
            )

        with pytest.raises(ValueError, match="unreasonable"):
            GoldPrice(
                price=5000.0,  # Too high
                timestamp=datetime.now(),
                change_24h=0.0,
                source="test",
            )

    def test_gold_symbol_must_be_xau(self):
        """Spec: Gold symbol must be 'XAU'"""
        with pytest.raises(ValueError, match="XAU"):
            GoldPrice(
                symbol="AU",
                price=2000.0,
                timestamp=datetime.now(),
                change_24h=0.0,
                source="test",
            )

    def test_gold_unit_must_be_troy_ounce(self):
        """Spec: Gold unit must be 'troy ounce'"""
        with pytest.raises(ValueError, match="troy ounce"):
            GoldPrice(
                unit="gram",
                price=2000.0,
                timestamp=datetime.now(),
                change_24h=0.0,
                source="test",
            )

    def test_gold_defaults(self):
        """Spec: Oro debe cotizar en USD por onza"""
        price = GoldPrice(
            price=2000.0,
            timestamp=datetime.now(),
            change_24h=0.0,
            source="test",
        )
        assert price.symbol == "XAU"
        assert price.name == "Gold"
        assert price.currency == "USD"
        assert price.unit == "troy ounce"


class TestExchangeRate:
    """Scenarios from currency.spec.yaml"""

    def test_valid_usd_to_eur(self):
        """Example: usd_to_eur"""
        rate = ExchangeRate(
            rate=0.92,
            timestamp=datetime(2026, 6, 9, 10, 30, 0),
            source="fixer.io",
            base_currency="USD",
            target_currency="EUR",
        )
        assert rate.base_currency == "USD"
        assert rate.target_currency == "EUR"
        assert rate.rate == 0.92

    def test_valid_usd_to_mxn(self):
        """Example: usd_to_mxn"""
        rate = ExchangeRate(
            rate=17.45,
            timestamp=datetime(2026, 6, 9, 10, 30, 0),
            source="open_exchange_rates",
            base_currency="USD",
            target_currency="MXN",
        )
        assert rate.target_currency == "MXN"
        assert 15 <= rate.rate <= 25

    def test_valid_usd_to_ars(self):
        """Example: usd_to_ars"""
        rate = ExchangeRate(
            rate=850.50,
            timestamp=datetime(2026, 6, 9, 10, 30, 0),
            source="bcra",
            base_currency="USD",
            target_currency="ARS",
        )
        assert rate.target_currency == "ARS"
        assert rate.rate > 0

    def test_exchange_rate_must_be_positive(self):
        """Spec: Exchange rate must be positive"""
        with pytest.raises(ValueError, match="must be positive"):
            ExchangeRate(
                base_currency="USD",
                target_currency="EUR",
                rate=-0.5,
                timestamp=datetime.now(),
                source="test",
            )

    def test_base_currency_must_be_usd(self):
        """Spec: Base currency must be USD"""
        with pytest.raises(ValueError, match="must be USD"):
            ExchangeRate(
                base_currency="EUR",
                target_currency="GBP",
                rate=1.2,
                timestamp=datetime.now(),
                source="test",
            )

    def test_invalid_target_currency(self):
        """Spec: Manejar moneda no válida"""
        with pytest.raises(ValueError, match="Invalid target currency"):
            ExchangeRate(
                base_currency="USD",
                target_currency="INVALID",
                rate=1.0,
                timestamp=datetime.now(),
                source="test",
            )

    def test_all_valid_currencies(self):
        """All currencies in VALID_CURRENCIES should work"""
        from src.config import VALID_CURRENCIES

        for currency in VALID_CURRENCIES:
            rate = ExchangeRate(
                rate=1.5,
                timestamp=datetime.now(),
                source="test",
                base_currency="USD",
                target_currency=currency,
            )
            assert rate.target_currency == currency


class TestPriceResponse:
    """Tests for combined price response"""

    def test_empty_response(self):
        """PriceResponse can be created empty"""
        response = PriceResponse()
        assert response.bitcoin is None
        assert response.gold is None
        assert response.exchange_rates == {}

    def test_response_with_all_prices(self):
        """PriceResponse with all prices"""
        now = datetime.now()
        btc = BitcoinPrice(
            price=50000.0,
            timestamp=now,
            change_24h=0.0,
            source="test",
        )
        gold = GoldPrice(
            price=2000.0,
            timestamp=now,
            change_24h=0.0,
            source="test",
        )
        rate = ExchangeRate(
            base_currency="USD",
            target_currency="EUR",
            rate=0.92,
            timestamp=now,
            source="test",
        )

        response = PriceResponse(
            bitcoin=btc,
            gold=gold,
            exchange_rates={"EUR": rate},
            timestamp=now,
        )

        assert response.bitcoin == btc
        assert response.gold == gold
        assert response.exchange_rates["EUR"] == rate

    def test_response_to_dict(self):
        """PriceResponse can be converted to dict"""
        response = PriceResponse()
        data = response.to_dict()
        assert "bitcoin" in data
        assert "gold" in data
        assert "exchange_rates" in data
        assert "timestamp" in data
