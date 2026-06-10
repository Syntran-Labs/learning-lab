# Price Fetcher - Spec Driven Development

<div align="center">

![SDD](https://img.shields.io/badge/Methodology-SDD-blue?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-44%2F44%20✓-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Type Coverage](https://img.shields.io/badge/Type%20Coverage-100%25-brightgreen?style=flat-square)
![Built with AI](https://img.shields.io/badge/Built%20with-AI-purple?style=flat-square)

**A learning project demonstrating Spec Driven Development using OpenSpec and pytest**

*Not "AI garbage" — deliberately designed, thoroughly reviewed, professionally structured for educational purposes*

</div>

---

## ✨ What Is This?

A **learning project** demonstrating how to build professional software using **Spec Driven Development (SDD)** methodology. It fetches prices for Bitcoin, Gold, and currency exchange rates.

### Educational vs. Production

| Aspect | This Project | Real Production App |
|--------|--------------|-------------------|
| **Purpose** | Teach SDD methodology | Serve real users |
| **Data** | Mock data (hardcoded) | Real APIs (CoinGecko, etc.) |
| **Error Handling** | Basic example | Comprehensive retry/fallback logic |
| **Configuration** | Simple centralized | Environment-based multi-env setup |
| **Focus** | Red-Green-Refactor cycle | Performance, security, reliability |

**Key Point:** This is an educational example that uses **professional architecture patterns** to show students how production systems are structured — without the complexity of real APIs or deployment concerns.

---

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/sdd_test.git
cd sdd_test
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\Activate.ps1 (Windows)

# Install and run
pip install -r requirements.txt
pytest tests/ -v                    # Run tests (44 passing)
python -m src bitcoin              # Get Bitcoin price
```

**[→ Detailed setup guide](docs/01-getting-started.md)**

---

## 🏗️ Architecture Decisions Explained

This project uses professional patterns **on purpose** — to teach students how real systems are built. Here's why:

### Why Dependency Injection?

**What It Is:**
```python
fetcher = PriceFetcher(provider=CustomProvider())  # Inject dependency
```

**Why It Matters for Learning:**
- ✅ **Testability**: Students can inject mock providers (seen in `tests/`)
- ✅ **Flexibility**: Shows how to swap implementations without modifying code
- ✅ **SOLID Principle**: Teaches "D" in SOLID (Dependency Inversion)
- ✅ **Real-world**: Every production app uses this pattern

**What Students Learn:**
"My code should depend on abstractions, not concrete implementations"

---

### Why Config Separation?

**What It Is:**
```python
# src/config.py - All hardcoded test data in one place
BITCOIN_CONFIG = {...}
EXCHANGE_RATES_CONFIG = {...}
VALID_CURRENCIES = {...}
```

**Why It Matters for Learning:**
- ✅ **Clarity**: Students instantly see where test data lives
- ✅ **Maintainability**: Change test data once, not scattered throughout code
- ✅ **Scalability Pattern**: Real apps use config files for different environments
- ✅ **Separation of Concerns**: Data ≠ Logic

**What Students Learn:**
"Configuration should be separate from business logic"

---

### Why Provider Abstraction?

**What It Is:**
```python
class PriceDataProvider(Protocol):
    def get_bitcoin_data(self) -> Dict[str, Any]: ...
    # ... defines the contract
```

**Why It Matters for Learning:**
- ✅ **Contracts**: Shows how components communicate via interfaces
- ✅ **Swappability**: MockPriceDataProvider can become RealAPIProvider
- ✅ **Testing Pattern**: Easy to create test doubles
- ✅ **Architecture**: Demonstrates layered architecture

**What Students Learn:**
"Define clear contracts between components"

---

## 🔌 Extensible Architecture Example

This project demonstrates **professional extensibility patterns**:

### Dependency Injection
```python
from src.price_fetcher import PriceFetcher
from src.providers import MockPriceDataProvider

# Use default provider
fetcher = PriceFetcher()

# Inject a custom provider
class MyProvider(MockPriceDataProvider):
    def get_bitcoin_data(self):
        return {"price": 99999.0, ...}

custom_fetcher = PriceFetcher(provider=MyProvider())
```

### Adding a New Asset (e.g., Ethereum)
Just 6 focused changes following a clear pattern:

1. Write `specs/ethereum.spec.yaml`
2. Add `EthereumPrice` model in `src/models.py`
3. Add `ETHEREUM_CONFIG` to `src/config.py`
4. Extend `PriceDataProvider` protocol in `src/providers.py`
5. Add `fetch_ethereum()` to `PriceFetcher`
6. Add CLI command in `src/cli.py`

**[→ Detailed guide](docs/07-extending-architecture.md) | [→ Step-by-step tutorial](docs/08-tutorial-add-ethereum.md)****

---

## 📖 Documentation

| Document | For | Content |
|----------|-----|---------|
| **[Getting Started](docs/01-getting-started.md)** | New users | Installation, first commands, troubleshooting |
| **[Learning SDD](docs/02-learning-sdd.md)** | Students | SDD concepts, Red-Green-Refactor cycle |
| **[Usage Reference](docs/03-usage-reference.md)** | Developers | CLI commands, Python API, patterns |
| **[Examples](docs/04-examples.md)** | Builders | Real-world use cases, integrations |
| **[Contributing](docs/05-contribute.md)** | Contributors | How to contribute, guidelines |
| **[Built with AI](docs/06-ai-transparency.md)** | Everyone | How AI was used responsibly |
| **[Extending Architecture](docs/07-extending-architecture.md)** | Advanced learners | DI, config extraction, protocol design, extensibility |
| **[Tutorial: Add Ethereum](docs/08-tutorial-add-ethereum.md)** | Hands-on builders | Step-by-step guide to extend with new assets |
| **[Acknowledgments](docs/09-acknowledgments.md)** | Everyone | Credits and thanks to projects and communities |
| **[Changelog](docs/10-changelog.md)** | Maintainers | Version history and release notes |
| **[Code of Conduct](docs/11-code-of-conduct.md)** | Community | Community standards and expectations |

---

## 💡 What You'll Learn

- ✅ How to write executable specifications
- ✅ The Red-Green-Refactor cycle in practice
- ✅ Test-driven development with pytest
- ✅ Professional Python code quality
- ✅ **Dependency injection patterns** (Protocol-based design)
- ✅ **Configuration management** (separation of concerns)
- ✅ **Extensible architecture** (clear patterns for new features)
- ✅ Responsible AI in software development

---

## 📊 Project Stats

```
44 tests (100%)           100% type hints          Professional architecture
100% docstrings          11 documented guides     Pure learning focus
DI + Config              Extensible patterns      Zero production cruft
```

**Intentional Design:**
- ✅ Professional patterns → Show real-world structure
- ❌ No production complexity → Keep focus on SDD methodology
- ✅ Mock data → Fast feedback loop for learning
- ❌ No deployment code → CI/CD is beyond scope
- ✅ 100% test coverage → Demonstrate test-first development

---

## 🤖 About AI & Quality

This project uses AI responsibly:
- ✅ Clear specifications first
- ✅ Every line reviewed by humans
- ✅ Comprehensive testing
- ✅ Honest transparency
- ✅ Professional quality standards

**[Learn how AI was used →](docs/06-ai-transparency.md)**

---

## 🔗 Key Links

- **[OpenSpec](https://github.com/Fission-AI/OpenSpec/)** — The specification framework we use
- **[Changelog](docs/10-changelog.md)** — Version history
- **[Code of Conduct](docs/11-code-of-conduct.md)** — Community standards
- **[Acknowledgments](docs/09-acknowledgments.md)** — Credits and thanks

---

## 🙏 Acknowledgments

Special thanks to:
- **[Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec/)** — Specification framework that makes executable documentation possible
- **pytest & pytest-bdd** — Testing frameworks
- **Python community** — For amazing tools and standards

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

<div align="center">

**Ready to learn SDD? [Start here →](docs/01-getting-started.md)**

</div>
