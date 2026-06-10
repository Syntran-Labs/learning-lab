"""Configuration and mock data for Price Fetcher"""

BITCOIN_CONFIG = {
    "price": 67890.50,
    "change_24h": 2.45,
    "source": "coingecko",
    "symbol": "BTC",
    "name": "Bitcoin",
    "currency": "USD",
}

GOLD_CONFIG = {
    "price": 2087.75,
    "change_24h": 0.35,
    "source": "london_metal_exchange",
    "symbol": "XAU",
    "name": "Gold",
    "currency": "USD",
    "unit": "troy ounce",
}

EXCHANGE_RATES_CONFIG = {
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 150.25,
    "AUD": 1.52,
    "CAD": 1.37,
    "CHF": 0.88,
    "CNY": 7.24,
    "INR": 83.12,
    "MXN": 17.45,
    "ARS": 850.50,
    "BRL": 4.97,
    "CLP": 945.30,
}

VALID_CURRENCIES = {
    "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY",
    "INR", "MXN", "ARS", "BRL", "CLP"
}
