from _html_compat import BeautifulSoup


class Parser:
    def __init__(self, parser_type='html.parser'):
        self.parser_type = parser_type

    def parse(self, content):
        return BeautifulSoup(content, self.parser_type)
