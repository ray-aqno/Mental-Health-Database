## Fix: ImportError for SimpleCollegeScraper in CI tests

This repo's tests expect a class named `SimpleCollegeScraper` to be importable from `Scripts/simple_scraper.py`.
The current implementation defines `CollegeScraper`. To avoid changing tests, we add a compatibility alias.

Step-by-step fix applied (verbatim):

1. Edit `Scripts/simple_scraper.py` and add the following line near the bottom (after class definitions):

```
# Backwards-compatible export for older tests/tools
SimpleCollegeScraper = CollegeScraper
```

2. Commit the change and push to your branch:

```bash
git add Scripts/simple_scraper.py
git commit -m "compat: expose SimpleCollegeScraper alias for tests"
git push
```

3. Re-run CI or tests locally:

```bash
python3 -m pytest -q
```

Why this is safe:
- It's a single-line alias; no behavior change; preserves newer `CollegeScraper` name while restoring compatibility.

If you'd prefer to update tests instead (rename imports), edit test files that import `SimpleCollegeScraper` and change to `CollegeScraper`.

End of instructions.
