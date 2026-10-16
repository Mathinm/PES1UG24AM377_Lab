# Lab 5 – Reflection

**Student:** Mathin M (PES1UG24AM377)

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the style issues from Flake8 and Pylint: renaming functions to snake_case, adding docstrings, wrapping long lines and splitting `if x: return y` onto two lines. They are mechanical and do not change behaviour. The hardest was `global adoption_count` (W0603). Just deleting `global` would break the code, so I had to decide where the count should really live. Counting adopted rows in the database fixed the warning and also a hidden bug: the old counter went up even when `adopt()` was given a pet id that didn't exist. The bare `except` was also tricky, because I first had to work out what it was actually catching (indexing `None` when no pet is available) before I could replace it with an explicit check.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

Nothing was a pure false positive, but some findings depend on context. Bandit B311 flags `random.randint` because it is not cryptographically secure. For a demo shelter's adoption code that risk is small, and in a game or simulation this warning would usually be ignored. Since adoption codes act like tokens, I switched to `secrets` anyway. Pylint W0603 (global statement) and the docstring checks are design and style rules rather than bugs, and a small script could reasonably skip them. The tools also overlap: the bare `except` was reported by both Pylint (W0702) and Flake8 (E722), and the long lines by both C0301 and E501.

### 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally:** run Flake8 and Pylint in the editor and through a `pre-commit` hook, so style problems are caught before a commit is made.
- **In CI:** a GitHub Actions job runs `flake8`, `pylint --fail-under=9.5` and `bandit -r . -ll` on every push and pull request, and the merge is blocked if any of them fail.
- **Configuration:** keep the rules in `pyproject.toml` / `.flake8` so the whole team uses the same line length and disabled checks, and use `# nosec` or `# pylint: disable=` only with a comment explaining why.
- Look at Bandit's Medium and High findings before style warnings.

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** the SQL injection is gone. With parameterised queries, a pet name containing quotes or SQL is stored as plain text and never executed.
- **Correctness:** `register_pet` no longer leaks tags between calls, the adoption count always matches the database, and `adopt()` reports whether it actually adopted a pet.
- **Robustness:** errors are no longer silently swallowed. Only `sqlite3.Error` is caught, and it is reported.
- **Readability:** consistent snake_case names, docstrings on every function, and short lines make the file easier to read and review.
- **Reusability:** the `__main__` guard means the module can be imported (for example in tests) without running the demo.
- **Measured:** Pylint went from 3.95 to 10.00/10, and Bandit and Flake8 went from 3 and 5 findings to 0.
