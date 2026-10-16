# Lab 5 – Issue Table (`pet_shelter.py`)

**Student:** Mathin M (PES1UG24AM377) · **Repo:** L5_16_pet_shelter

Scores before → after: **Pylint 3.95 → 10.00/10**, **Bandit 3 → 0 issues**, **Flake8 5 → 0 issues**.
Reports: `reports/before/` (original) and `reports/after/` (also copied to the repo root).

| # | Issue | Tool / Code | Type | Severity | Line(s) (original) | Description | Fix Approach |
|---|-------|-------------|------|----------|--------------------|-------------|--------------|
| 1 | SQL injection | Bandit B608 | Security | Medium | 10 | `INSERT` built with `%` string formatting, so a name like `x'); DROP TABLE pets;--` is injected into the SQL | Use `?` placeholders and pass `(name, species, age)` as parameters |
| 2 | Mutable default argument | Pylint W0102 | Bug | Medium | 9 | `tags=[]` is created once and shared, so every call keeps appending to the same list | Default to `None` and create a new list inside the function |
| 3 | Bare `except` | Pylint W0702 / Flake8 E722 | Bug | Medium | 29–30 | `except:` swallows everything (even `KeyboardInterrupt`) and hides the real cause; it was only there to catch `None[0]` when no pet is left | Remove the try/except; check `if row is None: return None` explicitly |
| 4 | Silent `try/except/pass` with broad exception | Bandit B110 / Pylint W0718 | Bug / Security | Low | 36–37 | `except Exception: pass` hides database failures in `clearUnadopted` | Catch only `sqlite3.Error` and report the error |
| 5 | Insecure random generator | Bandit B311 | Security | Low | 22 | `random.randint` is predictable; adoption codes act like tokens | Use `secrets.randbelow(9000) + 1000` |
| 6 | Global mutable state | Pylint W0603 | Design | Low | 6, 16, 18 | `global adoption_count` is incremented even if the pet id doesn't exist or is already adopted, so the count can drift from the DB | Remove the global; `adoption_count()` queries `COUNT(*) WHERE adopted = 1`; `adopt()` returns whether a row was updated |
| 7 | Non-snake_case names | Pylint C0103 | Style | Low | 9, 21, 25, 33, 40 | `registerPet`, `adoptionCode`, etc. break PEP 8 naming | Renamed to `register_pet`, `adoption_code`, `oldest_available`, `clear_unadopted`, `shelter_status` |
| 8 | Missing docstrings | Pylint C0114 / C0116 | Style | Low | 1, 9–45 | No module or function docstrings | Added a module docstring and one per function |
| 9 | Lines too long | Flake8 E501 / Pylint C0301 | Style | Low | 5, 10, 27 | SQL strings up to 116 chars (limit 79 / 100) | Wrapped calls across lines and used implicit string concatenation |
| 10 | Multiple statements on one line | Flake8 E701 / Pylint C0321 | Style | Low | 41 | `if adoption_count > 0: return "active"` | Moved the `return` onto its own line |
| 11 | `%` formatting instead of f-string | Pylint C0209 | Style | Low | 10 | Old-style formatting | Resolved by #1 (parameterised query; no string formatting at all) |
| 12 | Module runs on import | (manual review) | Design | Low | 54 | `main()` is called at import time | Wrapped in `if __name__ == "__main__":` |

## Commits

1. **Bandit** – parameterised SQL (B608), `secrets` for adoption codes (B311), no silent except (B110)
2. **Pylint** – mutable default, global state, bare except, snake_case names, docstrings, `__main__` guard
3. **Flake8** – wrapped long lines (E501), split one-line `if` (E701)

Program output is unchanged in behaviour: `Kiwi PET-XXXX active`.
