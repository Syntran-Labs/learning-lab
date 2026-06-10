"""Command Line Interface for Price Fetcher"""

import json
import sys
from datetime import datetime
from typing import Optional, List

from .price_fetcher import PriceFetcher, InvalidCurrencyError


class PriceFetcherCLI:
    """CLI interface for Price Fetcher"""

    def __init__(self):
        self.fetcher = PriceFetcher()

    def print_header(self, title: str) -> None:
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")

    def print_price(self, label: str, price: float, currency: str, change: float = None) -> None:
        """Print formatted price"""
        change_str = f" ({change:+.2f}%)" if change is not None else ""
        print(f"  {label:<20} ${price:>10,.2f} {currency}{change_str}")

    def print_rate(self, base: str, target: str, rate: float) -> None:
        """Print formatted exchange rate"""
        print(f"  1 {base:<3} = {rate:>10.4f} {target}")

    def cmd_bitcoin(self) -> None:
        """Show Bitcoin price"""
        self.print_header("Bitcoin Price")
        btc = self.fetcher.fetch_bitcoin()
        self.print_price("Bitcoin", btc.price, btc.currency, btc.change_24h)
        print(f"\n  Source: {btc.source}")
        print(f"  Time: {btc.timestamp.isoformat()}\n")

    def cmd_gold(self) -> None:
        """Show Gold price"""
        self.print_header("Gold Price")
        gold = self.fetcher.fetch_gold()
        self.print_price("Gold (per oz)", gold.price, gold.currency, gold.change_24h)
        print(f"\n  Source: {gold.source}")
        print(f"  Time: {gold.timestamp.isoformat()}\n")

    def cmd_rate(self, currency: str) -> None:
        """Show exchange rate for currency"""
        try:
            self.print_header(f"Exchange Rate: USD -> {currency}")
            rate = self.fetcher.fetch_exchange_rate(currency)
            self.print_rate(rate.base_currency, rate.target_currency, rate.rate)
            print(f"\n  Source: {rate.source}")
            print(f"  Time: {rate.timestamp.isoformat()}\n")
        except InvalidCurrencyError as e:
            print(f"\n❌ Error: {e}\n")
            print("  Valid currencies:")
            for curr in self.fetcher.get_supported_currencies():
                print(f"    • {curr}")
            print()

    def cmd_all(self, rates: Optional[List[str]] = None) -> None:
        """Show all prices"""
        if rates is None:
            rates = ["EUR", "MXN", "ARS"]

        self.print_header("All Prices")

        response = self.fetcher.fetch_all(
            fetch_bitcoin=True,
            fetch_gold=True,
            fetch_rates=rates,
        )

        # Bitcoin
        if response.bitcoin:
            self.print_price(
                "Bitcoin",
                response.bitcoin.price,
                response.bitcoin.currency,
                response.bitcoin.change_24h,
            )

        # Gold
        if response.gold:
            self.print_price(
                "Gold (per oz)",
                response.gold.price,
                response.gold.currency,
                response.gold.change_24h,
            )

        # Exchange rates
        if response.exchange_rates:
            print()
            for currency, rate in sorted(response.exchange_rates.items()):
                self.print_rate(rate.base_currency, currency, rate.rate)

        print(f"\n  Updated: {response.timestamp.isoformat()}\n")

    def cmd_json(self, rates: Optional[List[str]] = None) -> None:
        """Output all prices as JSON"""
        if rates is None:
            rates = ["EUR", "MXN", "ARS"]

        response = self.fetcher.fetch_all(
            fetch_bitcoin=True,
            fetch_gold=True,
            fetch_rates=rates,
        )

        # Convert to JSON-serializable format
        data = {
            "bitcoin": {
                "symbol": response.bitcoin.symbol,
                "name": response.bitcoin.name,
                "price": response.bitcoin.price,
                "currency": response.bitcoin.currency,
                "change_24h": response.bitcoin.change_24h,
                "source": response.bitcoin.source,
                "timestamp": response.bitcoin.timestamp.isoformat(),
            } if response.bitcoin else None,
            "gold": {
                "symbol": response.gold.symbol,
                "name": response.gold.name,
                "price": response.gold.price,
                "currency": response.gold.currency,
                "unit": response.gold.unit,
                "change_24h": response.gold.change_24h,
                "source": response.gold.source,
                "timestamp": response.gold.timestamp.isoformat(),
            } if response.gold else None,
            "exchange_rates": {
                curr: {
                    "base_currency": rate.base_currency,
                    "target_currency": rate.target_currency,
                    "rate": rate.rate,
                    "source": rate.source,
                    "timestamp": rate.timestamp.isoformat(),
                }
                for curr, rate in response.exchange_rates.items()
            } if response.exchange_rates else {},
            "timestamp": response.timestamp.isoformat(),
        }

        print(json.dumps(data, indent=2))

    def print_help(self) -> None:
        """Show help message"""
        self.print_header("Price Fetcher CLI - Help")
        print("Usage: python -m src.cli <command> [options]\n")
        print("Commands:\n")
        print("  bitcoin              Show Bitcoin price")
        print("  gold                 Show Gold price")
        print("  rate <CURRENCY>      Show USD exchange rate (e.g., rate EUR)")
        print("  all [CURR1,CURR2...] Show all prices (default: EUR,MXN,ARS)")
        print("  json [CURR1,CURR2...]Output as JSON (default: EUR,MXN,ARS)")
        print("  help                 Show this message\n")
        print("Examples:\n")
        print("  python -m src.cli bitcoin")
        print("  python -m src.cli rate EUR")
        print("  python -m src.cli all EUR,GBP,JPY")
        print("  python -m src.cli json\n")

    def run(self, args: List[str]) -> None:
        """Run CLI with given arguments"""
        if not args:
            self.print_help()
            return

        command = args[0].lower()

        if command == "bitcoin":
            self.cmd_bitcoin()

        elif command == "gold":
            self.cmd_gold()

        elif command == "rate":
            if len(args) < 2:
                print("\n❌ Error: rate command requires a currency\n")
                print("Usage: python -m src.cli rate <CURRENCY>\n")
                print("Examples:")
                print("  python -m src.cli rate EUR")
                print("  python -m src.cli rate MXN\n")
                return
            self.cmd_rate(args[1].upper())

        elif command == "all":
            rates = None
            if len(args) > 1:
                rates = [c.strip().upper() for c in args[1].split(",")]
            self.cmd_all(rates)

        elif command == "json":
            rates = None
            if len(args) > 1:
                rates = [c.strip().upper() for c in args[1].split(",")]
            self.cmd_json(rates)

        elif command == "help":
            self.print_help()

        else:
            print(f"\n❌ Unknown command: {command}\n")
            self.print_help()


def main() -> None:
    """Main entry point"""
    cli = PriceFetcherCLI()
    cli.run(sys.argv[1:])


if __name__ == "__main__":
    main()
