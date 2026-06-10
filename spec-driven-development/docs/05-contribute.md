# Contributing to Price Fetcher SDD Example

Thank you for your interest in contributing! This project is meant to be a clear, educational example of Spec Driven Development. All contributions are welcome.

## 🎯 Contribution Guidelines

### Before You Start

1. Make sure you understand the [SDD methodology](LEARNING.md)
2. Review the existing [specifications](specs/) and [tests](tests/)
3. Check open issues to avoid duplicate work

### Types of Contributions

#### 📖 Documentation
- Improve README or LEARNING.md
- Add comments explaining concepts
- Create examples or tutorials

#### 🐛 Bug Fixes
- Fix typos in specs or code
- Correct validation logic
- Fix test issues

#### ✨ Improvements
- Add new asset types (e.g., Silver, Oil)
- Expand currency pairs
- Improve code organization
- Add new specifications and tests

#### 🎓 Learning Resources
- Create example use cases
- Write blog posts (link in README)
- Create video tutorials

---

## 🔄 Development Workflow

### 1. Fork & Clone

```bash
git clone https://github.com/yourusername/sdd_test.git
cd sdd_test
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/add-silver-prices` ✅
- `docs/improve-learning-guide` ✅
- `fix/validation-bug` ✅
- `wip/experiment` ❌ (too vague)

### 3. Set Up Development Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Make Your Changes

Follow the SDD process if adding features:

**a) Write Specification** (specs/your_feature.spec.yaml)
```yaml
spec:
  name: YourFeatureName
  description: What it does
  version: 1.0.0

scenarios:
  - name: "Describe the behavior"
    given: [...]
    when: [...]
    then: [...]
```

**b) Write Tests** (tests/test_your_feature.py)
```python
def test_your_feature(self):
    """Spec: Your spec scenario name"""
    # Arrange
    # Act
    # Assert
```

**c) Write Code** (src/your_module.py)
```python
# Implementation that passes tests
```

**d) Refactor**
```bash
pytest tests/ -v  # Ensure all tests pass
```

### 5. Verify Tests Pass

```bash
pytest tests/ -v

# Expected: All tests pass, including your new ones
```

### 6. Commit with Clear Messages

```bash
git add .
git commit -m "Add silver price fetching with specifications

- Add specs/silver.spec.yaml with scenarios
- Add GoldPrice validation tests
- Implement fetch_silver() method
- All 45 tests passing"
```

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request with:
- Clear title explaining the change
- Description of what and why
- Link to any related issues
- Confirmation that tests pass

---

## ✅ Contribution Checklist

Before submitting a PR, verify:

- [ ] Tests added/updated for new features
- [ ] All 41+ tests pass locally: `pytest tests/ -v`
- [ ] Code follows PEP 8 style
- [ ] Type hints included for new functions
- [ ] Docstrings added to new functions
- [ ] Specifications created for new features
- [ ] No breaking changes to existing API
- [ ] Commit messages are clear and descriptive
- [ ] README updated if needed (e.g., new currency)
- [ ] Acknowledgments added if using external resources

---

## 📝 Code Style Guidelines

### Python Style (PEP 8)

```python
# ✅ Good
def fetch_bitcoin(self) -> BitcoinPrice:
    """Fetch Bitcoin price."""
    return BitcoinPrice(...)

# ❌ Bad
def fetch_bitcoin(self):
    return BitcoinPrice(...)
```

### Type Hints

```python
# ✅ Good
def fetch_exchange_rate(self, target_currency: str) -> ExchangeRate:
    pass

# ❌ Bad
def fetch_exchange_rate(self, target_currency):
    pass
```

### Docstrings

```python
# ✅ Good
def fetch_all(
    self,
    fetch_bitcoin: bool = True,
    fetch_gold: bool = True,
    fetch_rates: Optional[List[str]] = None,
) -> PriceResponse:
    """
    Fetch all available prices in a single call.

    Args:
        fetch_bitcoin: Whether to include Bitcoin price
        fetch_gold: Whether to include Gold price
        fetch_rates: List of currency codes for exchange rates

    Returns:
        PriceResponse: Combined price response
    """

# ❌ Bad
def fetch_all(self, fb=True, fg=True, fr=None):
    # Fetch stuff
    pass
```

---

## 🧪 Testing Guidelines

### Test Naming

```python
# ✅ Good - Describes what is tested
def test_bitcoin_price_must_be_positive(self):
    pass

# ❌ Bad - Too vague
def test_bitcoin(self):
    pass
```

### Test Structure (Arrange-Act-Assert)

```python
def test_fetch_bitcoin_returns_valid_price(self):
    # Arrange
    fetcher = PriceFetcher()
    
    # Act
    price = fetcher.fetch_bitcoin()
    
    # Assert
    assert isinstance(price, BitcoinPrice)
    assert price.price > 0
```

### Spec Comments

Always link tests to specifications:

```python
def test_fetch_bitcoin_returns_valid_price(self):
    """Spec: Se retorna un precio numérico válido"""
    # This comment references the specification
```

---

## 🎓 Specification Guidelines

### Scenario Structure

Every scenario should have Given-When-Then:

```yaml
scenarios:
  - name: "Clear, user-friendly description"
    given:
      - "Precondition 1"
      - "Precondition 2"
    when:
      - "Action or trigger"
    then:
      - "Expected result 1"
      - "Expected result 2"
```

### Data Examples

Include realistic examples:

```yaml
examples:
  valid_price:
    symbol: "BTC"
    price: 45000.50
    currency: "USD"
```

### Properties

Define invariants:

```yaml
properties:
  - name: "Prices always positive"
    constraint: "price > 0"
```

---

## 🚫 What NOT to Do

- ❌ Don't break existing tests
- ❌ Don't change API without discussion
- ❌ Don't commit without running tests
- ❌ Don't add external dependencies without justification
- ❌ Don't submit PR without linking to specification
- ❌ Don't modify LEARNING.md to simplify concepts

---

## 📊 PR Review Process

Your PR will be reviewed for:

1. **Correctness** - Does it solve the issue?
2. **Tests** - Are all tests passing?
3. **Code Quality** - Is it clean and maintainable?
4. **Documentation** - Is it clear what changed?
5. **SDD Compliance** - Does it follow SDD methodology?

Feedback will be constructive and collaborative. 🤝

---

## 🆘 Need Help?

- 📖 Read [LEARNING.md](LEARNING.md) for SDD concepts
- 🔍 Review existing [specifications](specs/)
- 💬 Ask questions in your PR or open an issue
- 🔗 Check [OpenSpec docs](https://github.com/Fission-AI/OpenSpec/)

---

## 🏗️ Ready to Extend?

After contributing, learn about professional extension patterns:

- **[Extending Architecture](07-extending-architecture.md)** — Dependency injection, configuration management, extensibility patterns
- **[Tutorial: Add Ethereum](08-tutorial-add-ethereum.md)** — Step-by-step guide to extend the system with a new asset

---

## 🎉 Recognition

All contributors will be:
- Mentioned in README
- Thanked in commit messages
- Recognized as project maintainers (if regular contributions)

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

<div align="center">

**Thank you for helping make SDD examples better!** ❤️

[← Back to README](../README.md) | [← Examples](04-examples.md) | [← AI Transparency](06-ai-transparency.md) | [Architecture →](07-extending-architecture.md)

</div>
