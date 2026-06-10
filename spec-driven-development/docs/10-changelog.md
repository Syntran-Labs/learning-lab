# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-09

### Added

#### Specifications (YAML-based)
- `specs/price_fetcher.spec.yaml` - Main specification with 6 scenarios
- `specs/bitcoin.spec.yaml` - Bitcoin-specific scenarios and validation rules
- `specs/gold.spec.yaml` - Gold-specific scenarios and validation rules
- `specs/currency.spec.yaml` - Currency exchange rate scenarios for 12 pairs

#### Implementation
- `src/price_fetcher.py` - PriceFetcher service class with methods:
  - `fetch_bitcoin()` - Get Bitcoin price
  - `fetch_gold()` - Get Gold price
  - `fetch_exchange_rate(currency)` - Get USD exchange rate
  - `fetch_multiple_rates(currencies)` - Get multiple rates at once
  - `fetch_all()` - Get all prices in one call
  - `validate_asset()` - Validate supported assets
  - `validate_currency()` - Validate supported currencies
  - `_get_current_timestamp()` - Internal timestamp helper

- `src/models.py` - Data models with validation:
  - `BitcoinPrice` - Bitcoin price model (price range: 1k-200k)
  - `GoldPrice` - Gold price model (price range: 1k-3k)
  - `ExchangeRate` - Exchange rate model (12 supported pairs)
  - `PriceResponse` - Combined response model
  - Custom validation for all models based on specs

#### Tests (pytest-based)
- `tests/test_models.py` - 21 tests for model validation:
  - Bitcoin price validation (5 tests)
  - Gold price validation (6 tests)
  - Exchange rate validation (7 tests)
  - Combined response handling (3 tests)

- `tests/test_price_fetcher.py` - 20 tests for functionality:
  - Bitcoin fetching (4 tests)
  - Gold fetching (4 tests)
  - Exchange rate fetching (4 tests)
  - Batch operations (5 tests)
  - Error handling (3 tests)

#### Documentation
- `README.md` - Complete project guide with quick start and examples
- `LEARNING.md` - Comprehensive SDD and OpenSpec learning guide
- `CONTRIBUTING.md` - Guidelines for contributors
- `LICENSE` - MIT license
- `CHANGELOG.md` - This file

#### Configuration
- `requirements.txt` - Python dependencies (pytest, pytest-bdd, pydantic, etc.)
- `pytest.ini` - Pytest configuration
- `.gitignore` - Git ignore rules
- `.claude/settings.json` - Claude Code settings

### Statistics

- **Total Tests**: 41 (all passing ✅)
- **Lines of Code**: ~200 (clean, documented)
- **Specifications**: 4 YAML files with 20+ scenarios
- **Supported Assets**: Bitcoin, Gold
- **Supported Currencies**: EUR, GBP, JPY, AUD, CAD, CHF, CNY, INR, MXN, ARS, BRL, CLP
- **Test Coverage**: 100% of specifications

### Architecture Phases Completed

✅ **Phase 1: SPECIFY**
- Wrote 4 specifications in YAML format
- Defined scenarios, data types, and properties
- Created realistic examples for each asset type

✅ **Phase 2: GENERATE**
- Generated test suite from specifications
- Created 41 tests based on specification scenarios
- Organized tests by component (models, fetcher)

✅ **Phase 3: RED**
- All tests written with NotImplementedError
- Tests failed as expected (RED phase)
- Verified test suite integrity

✅ **Phase 4: GREEN**
- Implemented all 5 core methods
- All 41 tests passing
- Code meets specification requirements

✅ **Phase 5: REFACTOR**
- Extracted magic numbers to class constants
- Reduced code duplication (4 timestamp calls → 1 method)
- Enhanced documentation with comprehensive docstrings
- Improved type hints for Python 3.10+ compatibility
- Organized code for maintainability

### Project Goals

This is an **educational project** designed to:
- ✅ Demonstrate Spec Driven Development in practice
- ✅ Show how to write executable specifications
- ✅ Teach the Red-Green-Refactor cycle
- ✅ Provide a simple, self-contained example
- ✅ Serve as a template for new SDD projects

### Technologies Used

- **Language**: Python 3.10+
- **Testing**: pytest 9.0.2, pytest-bdd 8.1.0
- **Data Validation**: pydantic 2.13.4
- **Task Automation**: pytest, git

### Acknowledgments

Special thanks to:
- [**Fission-AI/OpenSpec**](https://github.com/Fission-AI/OpenSpec/) - For the OpenSpec framework that enables executable specifications
- pytest and pytest-bdd communities for excellent testing tools
- Python community for amazing development tools

---

## Development Notes

### What This Project IS

✅ A learning tool for understanding SDD  
✅ A template for starting new SDD projects  
✅ A reference for proper specification writing  
✅ An example of clean Python code  
✅ A demonstration of test-driven development  

### What This Project IS NOT

❌ A production system (uses mock data)  
❌ A financial service (for educational use only)  
❌ A complete price API (intentionally simplified)  
❌ A framework or library (standalone example)  

### Future Enhancement Ideas

Potential extensions (following SDD methodology):
- Real API integration (CoinGecko, Alpha Vantage)
- REST API endpoint (FastAPI)
- Price history tracking
- CLI tool
- Docker containerization
- CI/CD pipeline integration
- Additional assets (Silver, Oil, Crypto)

All future work would follow the same SDD pattern: Specify → Generate → Red → Green → Refactor

---

## Version History

### Versions Not Released

#### 0.5.0 (Pre-Release Phase REFACTOR)
- Extracted data constants
- Improved documentation
- Refactored for code quality

#### 0.4.0 (Pre-Release Phase GREEN)
- Implemented all core methods
- All 41 tests passing

#### 0.3.0 (Pre-Release Phase RED)
- Generated test suite
- Tests written, failing as expected

#### 0.2.0 (Pre-Release Phase SPECIFY)
- Wrote specifications in YAML
- Defined scenarios and data types

#### 0.1.0 (Pre-Release Phase INIT)
- Project structure created
- Initial setup

---

<div align="center">

**This project is a learning resource for Spec Driven Development**

See [README.md](../README.md) for usage and [02-learning-sdd.md](02-learning-sdd.md) for concepts.

</div>
