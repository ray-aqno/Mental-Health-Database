try:
    from bs4 import BeautifulSoup
except Exception:
    # reuse fallback from simple_scraper to avoid duplication at runtime
    from simple_scraper import BeautifulSoup


class Parser:
    def __init__(self, parser_type='html.parser'):
        self.parser_type = parser_type

    def parse(self, content):
        return BeautifulSoup(content, self.parser_type)
