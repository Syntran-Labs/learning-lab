"""Shared pytest fixtures for Price Fetcher tests"""

import pytest

from src.price_fetcher import PriceFetcher


@pytest.fixture
def fetcher():
    """Create a PriceFetcher instance with default provider"""
    return PriceFetcher()
