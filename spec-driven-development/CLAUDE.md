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

### 🔴 CRITICAL (5 Issues)

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

## 🚀 Recommended Next Steps (Priority Order)

### Phase 1: Fix Critical Issues (10-12 hours)
- [ ] Extract magic numbers to config with env var support
- [ ] Implement clock provider for testability
- [ ] Fix N+1 timestamp calls in batch operations
- [ ] Remove or implement unused timeout parameter
- [ ] Implement Asset Registry pattern for extensibility

### Phase 2: High Priority Fixes (4-6 hours)
- [ ] Implement retry logic with `PriceServiceUnavailableError`
- [ ] Consolidate `VALID_CURRENCIES` to single source
- [ ] Add concurrency specifications and tests
- [ ] Add performance SLA specifications

### Phase 3: Medium Priority (6-8 hours)
- [ ] Add decimal place validation
- [ ] Complete all spec scenario tests
- [ ] Update CHANGELOG with realistic version history
- [ ] Document failed refactoring patterns

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

### Strengths ⭐⭐⭐⭐
- Clear SDD demonstration (Specify → Red → Green → Refactor)
- Professional Python code quality
- Comprehensive testing (100% spec coverage)
- Good documentation structure
- Honest about AI usage

### Areas for Improvement ⭐⭐⭐
- Some hardcoded values should be configurable
- Validation logic should be separated
- Missing concurrency/performance specifications
- Could show more real-world patterns
- Doesn't demonstrate failed refactoring

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
