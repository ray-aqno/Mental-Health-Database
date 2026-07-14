#!/usr/bin/env python3
from simple_scraper import CollegeScraper, BeautifulSoup
import sys


def make_soup(html):
    return BeautifulSoup(html, 'html.parser')


def run_tests():
    scraper = CollegeScraper()
    failures = 0

    # Test 1: mental health page should be accepted
    html1 = """
    <html><body>
    <h1>Campus Counseling Center</h1>
    <p>Our mental health and counseling services provide therapy for anxiety and depression.</p>
    <p>Contact: counseling@college.edu</p>
    </body></html>
    """
    r1 = scraper.extract_resources(make_soup(html1), 'https://example.edu/counseling')
    if not r1:
        print('FAIL: mental health page was rejected')
        failures += 1
    else:
        print('PASS: mental health page accepted')

    # Test 2: dental page should be rejected
    html2 = """
    <html><body>
    <h1>Dental Clinic</h1>
    <p>Our dental clinic provides oral health services and cleanings.</p>
    <p>Contact: dental@college.edu</p>
    </body></html>
    """
    r2 = scraper.extract_resources(make_soup(html2), 'https://example.edu/dental')
    if r2:
        print('FAIL: dental page was accepted')
        failures += 1
    else:
        print('PASS: dental page rejected')

    # Test 3: academic program page should be rejected
    html3 = """
    <html><body>
    <h1>Undergraduate Programs</h1>
    <p>Explore majors, courses, and curriculum for the upcoming year.</p>
    </body></html>
    """
    r3 = scraper.extract_resources(make_soup(html3), 'https://example.edu/programs')
    if r3:
        print('FAIL: academic program page was accepted')
        failures += 1
    else:
        print('PASS: academic program page rejected')

    if failures:
        print(f"\n{failures} test(s) failed")
        return 2
    print('\nAll tests passed')
    return 0


if __name__ == '__main__':
    sys.exit(run_tests())
