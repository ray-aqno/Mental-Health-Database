import pytest
from bs4 import BeautifulSoup
from simple_scraper import CollegeScraper, MENTAL_HEALTH_KEYWORDS, NON_MENTAL_KEYWORDS


def make_soup(html):
    return BeautifulSoup(html, 'html.parser')


def test_accepts_mental_health_page():
    html = """
    <html><body>
    <h1>Campus Counseling Center</h1>
    <p>Our mental health and counseling services provide therapy for anxiety and depression.</p>
    <p>Contact: counseling@college.edu</p>
    </body></html>
    """
    scraper = CollegeScraper()
    soup = make_soup(html)
    resources = scraper.extract_resources(soup, 'https://example.edu/counseling')
    assert resources, "Expected resources for mental health page"
    assert any('counsel' in r.get('service_name','').lower() or 'mental' in r.get('description','').lower() for r in resources)


def test_rejects_dental_page():
    html = """
    <html><body>
    <h1>Dental Clinic</h1>
    <p>Our dental clinic provides oral health services and cleanings.</p>
    <p>Contact: dental@college.edu</p>
    </body></html>
    """
    scraper = CollegeScraper()
    soup = make_soup(html)
    resources = scraper.extract_resources(soup, 'https://example.edu/dental')
    assert not resources, "Expected no resources for dental page"


def test_rejects_academic_program_page():
    html = """
    <html><body>
    <h1>Undergraduate Programs</h1>
    <p>Explore majors, courses, and curriculum for the upcoming year.</p>
    </body></html>
    """
    scraper = CollegeScraper()
    soup = make_soup(html)
    resources = scraper.extract_resources(soup, 'https://example.edu/programs')
    assert not resources, "Expected no resources for academic programs page"
