"""
Shared BeautifulSoup import with a minimal fallback parser.

Both simple_scraper.py and parser.py need BeautifulSoup.  Keeping the
fallback in one place (here) avoids a circular import and satisfies DRY.

Usage:
    from _html_compat import BeautifulSoup
"""

try:
    from bs4 import BeautifulSoup  # noqa: F401  – re-exported
except Exception:
    import re

    class _FallbackElement:
        """Minimal stand-in for a bs4 Tag."""

        def __init__(self, tag, text, children=None):
            self.name = tag
            self._text = text
            self._children = children or []

        def get_text(self, strip=False):
            if strip:
                return re.sub(r'\s+', ' ', self._text).strip()
            return self._text

        def find(self, *args, **kwargs):
            names = args[0] if isinstance(args[0], (list, tuple)) else [args[0]]
            for c in self._children:
                if c.name in names:
                    return c
            return None

        def find_all(self, *args, **kwargs):
            names = args[0] if isinstance(args[0], (list, tuple)) else [args[0]]
            return [c for c in self._children if c.name in names]

        def find_next(self, name=None):
            return None

        def find_next_siblings(self, limit=None):
            return []

        def decompose(self):
            self._text = ''

    class BeautifulSoup:  # type: ignore[no-redef]
        """Very small heuristic HTML parser used when bs4 is not installed."""

        def __init__(self, html, parser):
            if isinstance(html, bytes):
                try:
                    html = html.decode('utf-8')
                except Exception:
                    html = html.decode('latin-1', errors='replace')
            self._html = html
            self._text = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.S | re.I)
            self._text = re.sub(r'<style.*?>.*?</style>', '', self._text, flags=re.S | re.I)
            self._children = []
            for tag in re.findall(r'<(h[1-5]|p)\b[^>]*>(.*?)</\1>', self._text, flags=re.S | re.I):
                name, inner = tag
                clean = re.sub(r'<[^>]+>', '', inner)
                self._children.append(_FallbackElement(name.lower(), clean))

        def get_text(self):
            return re.sub(r'<[^>]+>', '', self._html)

        def find(self, *args, **kwargs):
            names = args[0] if isinstance(args[0], (list, tuple)) else args[0]
            if isinstance(names, str):
                names = [names]
            for c in self._children:
                if c.name in names:
                    return c
            return None

        def find_all(self, *args, **kwargs):
            names = args[0] if isinstance(args[0], (list, tuple)) else args[0]
            if isinstance(names, str):
                names = [names]
            return [c for c in self._children if c.name in names]

        def __call__(self, *args, **kwargs):
            return []
