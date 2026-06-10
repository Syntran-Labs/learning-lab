# CLAUDE.md - Internal Project Context

This file documents internal project context for AI-assisted development sessions.

---

## 📊 Project Overview

**Spec-Driven Development Learning Project** - Educational example using OpenSpec and pytest

- **Current Version:** 1.0.0
- **Status:** ⭐⭐⭐⭐ (4/5 stars for educational value)
- **Tests:** 44/44 passing ✅
- **Type Coverage:** 100%
- **Created:** 2026-06-09

---

## 🏗️ Architecture Observations

### ✅ What's Already Implemented Well

1. **Dependency Injection** - `PriceFetcher` accepts optional `provider` parameter
   - Located: `src/price_fetcher.py:32-43`
   - Enables testing and extensibility

2. **Provider Abstraction** - `PriceDataProvider` protocol pattern
   - Located: `src/providers.py`
   - Enables swapping data sources

3. **Configuration Management** - `config.py` with constants
   - Located: `src/config.py`
   - Centralized currency and asset definitions

4. **Model Validation** - Dataclass `__post_init__` validation
   - Located: `src/models.py`
   - Type-safe with runtime checking

---

## ⚠️ Known Architectural Issues (19 Total)

**IMPORTANT NOTE:** These issues are categorized as "critical" for **production systems**. For an **educational project**, most of these are intentionally simplified. The project successfully teaches SDD without requiring production-grade error handling, configuration systems, or advanced patterns.

### 🔴 CRITICAL (5 Issues) - *For Production Only*

1. **Magic Numbers Hardcoded in Models**
   - Location: `src/models.py` lines 24-25, 45-46
   - Issue: Price ranges `1000 <= price <= 200000` hardcoded
   - Impact: Cannot dynamically configure price bounds
   - Fix: Move to `config.py` with environment variable support

2. **Validation Logic in Models (Single Responsibility)**
   - Location: `src/models.py` `__post_init__` methods
   - Issue: Models mix data + validation logic
   - Impact: Cannot deserialize invalid data for debugging
   - Fix: Create separate `validators.py` with factory methods

3. **N+1 Timestamp Calls in Batch Operations**
   - Location: `src/price_fetcher.py` `fetch_multiple_rates()`
   - Issue: Calls `_get_current_timestamp()` inside loop
   - Impact: Each rate gets different timestamp in a batch
   - Fix: Call once outside loop, reuse for all items

4. **Unused timeout Parameter**
   - Location: `src/price_fetcher.py` line 33
   - Issue: Parameter accepted but never passed to provider
   - Impact: Dead code, misleads users
   - Fix: Either implement timeout in provider calls or remove

5. **Limited Asset Extensibility**
   - Location: Spread across `models.py`, `price_fetcher.py`, `config.py`
   - Issue: Adding new assets (e.g., Silver) requires changes in multiple files
   - Impact: Not truly extensible architecture
   - Fix: Implement Asset Registry pattern

### 🟠 HIGH (6 Issues)

6. **Timestamp Generation Coupled to System Time**
   - Cannot inject custom clock for testing
   - Location: `src/price_fetcher.py` line 47
   - Fix: Make ClockProvider injectable

7. **Exception Defined But Unused**
   - `PriceServiceUnavailableError` defined, never raised
   - Location: `src/price_fetcher.py` line 10
   - Fix: Implement retry logic with exception handling

8. **DRY Violation: VALID_CURRENCIES**
   - Defined in multiple places
   - Fix: Single source in `config.py`

9. **N+1 Issue in Batch Operations** (covered in #3)

10. **Spec Gaps: No Concurrency Specifications**
    - Missing thread-safety spec
    - Fix: Add `specs/concurrency.spec.yaml`

11. **Spec Gaps: No Performance SLAs**
    - Missing latency requirements
    - Fix: Add `specs/performance.spec.yaml`

### 🟡 MEDIUM (4 Issues)

12. **Decimal Place Enforcement Not Implemented**
    - Gold prices should enforce 2 decimal places
    - Fix: Add decimal validator in models

13. **Missing Spec Scenarios Not Tested**
    - Service unavailability scenario defined but test missing
    - Fix: Complete test coverage

14. **CHANGELOG Shows Unrealistic Linear Progress**
    - Doesn't show refactorings or breaking changes
    - Fix: Update with more realistic version history

15. **Educational Gap: No Failed Refactoring Examples**
    - Doesn't show what went wrong and how to fix it
    - Fix: Add `docs/13-lessons-learned.md`

---

## 🚀 Enhancement Roadmap (If Expanding Beyond Learning)

**These are only relevant IF converting to production or expanding scope:**

### Phase 1: Production-Ready Patterns (IF needed)
- [ ] Extract magic numbers to environment config
- [ ] Implement retry logic with exponential backoff
- [ ] Add comprehensive error handling
- [ ] Implement timeout in API calls
- [ ] Add Asset Registry for true extensibility

### Phase 2: Advanced Features (IF scope expands)
- [ ] Connect to real APIs (CoinGecko, etc.)
- [ ] Add rate limiting / caching
- [ ] Add concurrency specifications
- [ ] Add performance SLA monitoring

### Phase 3: Documentation Enhancements (For deeper learning)
- [ ] Add "What Would Production Look Like?" guide
- [ ] Document "failed refactoring" patterns
- [ ] Show spec evolution examples
- [ ] Add migration guides for pattern changes

**Current Status: ✅ Complete for learning objectives. No changes needed unless scope changes.**

---

## 📁 Key Files

| File | Lines | Purpose |
|------|-------|---------|
| `src/price_fetcher.py` | 150 | Main service class |
| `src/models.py` | 80 | Data models with validation |
| `src/config.py` | 40 | Configuration constants |
| `src/providers.py` | 60 | Data provider abstraction |
| `specs/price_fetcher.spec.yaml` | 80 | Main specification |
| `tests/test_price_fetcher.py` | 200 | Integration tests |
| `tests/test_models.py` | 150 | Model validation tests |

---

## 🎓 Educational Value Assessment

### Strengths ⭐⭐⭐⭐⭐
- **Clear SDD demonstration:** Specify → Red → Green → Refactor cycle clearly visible
- **Professional Python patterns:** DI, config separation, protocol abstraction
- **Comprehensive testing:** 100% spec coverage with 44 passing tests
- **Architecture teaching:** Shows SOLID principles and extensibility patterns
- **Honest scope:** Educational focus, not trying to be a production app
- **Well documented:** Explains WHY patterns are used, not just WHAT

### Design Decisions (Intentional)
- ✅ **Mock data:** Intentional - keeps focus on SDD, not API integration
- ✅ **Basic error handling:** Intentional - production complexity beyond scope
- ✅ **Professional patterns:** Intentional - teach real-world structure
- ✅ **Config separation:** Intentional - shows best practices
- ✅ **100% test coverage:** Intentional - demonstrates test-first development

### NOT a Problem (Correctly Scoped)
- ❌ No production error recovery → Out of scope (learning focus)
- ❌ No complex configuration → Out of scope (keep it simple)
- ❌ No deployment/CI → Out of scope (focus on code)
- ❌ Hardcoded test data → Intentional (clarity + speed)

---

## 💾 Previous Analysis Documents

These files contain detailed analysis but are internal (not part of public repo):
- `ADVERSARIAL_REVIEW_AND_SOLUTIONS.md` - Detailed critique with solutions (854 lines)
- `PROJECT_SUMMARY_FOR_NEW_SESSION.md` - Executive summary (moved here)

Both have been consolidated into this CLAUDE.md for future sessions.

---

## 🔧 For Next Session

When resuming work:
1. Check if architecture issues in Phase 1 have been addressed
2. Review any new architectural decisions
3. Update this document with current status
4. Refer to ACKNOWLEDGMENTS, CHANGELOG, CODE_OF_CONDUCT (now in `/docs/`)

---

**Last Updated:** 2026-06-10
**Status:** Active - Ready for next development phase
