"""
Tests for simple_scraper.py regex extraction helpers.

Run with: pytest test_scraper.py -v
"""

import pytest
from simple_scraper import SimpleCollegeScraper


@pytest.fixture
def scraper():
    return SimpleCollegeScraper()


# ===== extract_email =====

class TestExtractEmail:
    def test_standard_email(self, scraper):
        assert scraper.extract_email("Contact us at caps@osu.edu for help") == "caps@osu.edu"

    def test_subdomain_email(self, scraper):
        assert scraper.extract_email("Email health.services@student.osu.edu") == "health.services@student.osu.edu"

    def test_plus_addressing(self, scraper):
        assert scraper.extract_email("Send to caps+info@uc.edu") == "caps+info@uc.edu"

    def test_no_email(self, scraper):
        assert scraper.extract_email("Call us at 555-1234") == ""

    def test_empty_string(self, scraper):
        assert scraper.extract_email("") == ""

    def test_multiple_emails_returns_first(self, scraper):
        result = scraper.extract_email("Email caps@osu.edu or wellness@osu.edu")
        assert result == "caps@osu.edu"

    def test_email_with_numbers(self, scraper):
        assert scraper.extract_email("Email: dept123@university.edu") == "dept123@university.edu"

    def test_invalid_email_no_tld(self, scraper):
        assert scraper.extract_email("Not an email: user@localhost") == ""


# ===== extract_phone =====

class TestExtractPhone:
    def test_parentheses_format(self, scraper):
        assert scraper.extract_phone("Call (614) 292-5766") == "(614) 292-5766"

    def test_dashes_format(self, scraper):
        assert scraper.extract_phone("Phone: 614-292-5766") == "614-292-5766"

    def test_dots_format(self, scraper):
        assert scraper.extract_phone("Phone: 614.292.5766") == "614.292.5766"

    def test_no_separators(self, scraper):
        assert scraper.extract_phone("Call 6142925766 now") == "6142925766"

    def test_with_country_code(self, scraper):
        result = scraper.extract_phone("Call +1-614-292-5766")
        # Should capture the phone number (implementation may vary on +1 prefix)
        assert "614" in result
        assert "292" in result
        assert "5766" in result

    def test_no_phone(self, scraper):
        assert scraper.extract_phone("Email us at caps@osu.edu") == ""

    def test_empty_string(self, scraper):
        assert scraper.extract_phone("") == ""

    def test_multiple_phones_returns_first(self, scraper):
        result = scraper.extract_phone("Main: (614) 292-5766, Fax: (614) 292-0000")
        assert result == "(614) 292-5766"

    def test_phone_with_spaces(self, scraper):
        result = scraper.extract_phone("Call (614) 292 5766")
        assert "614" in result


# ===== extract_hours =====

class TestExtractHours:
    def test_standard_hours(self, scraper):
        result = scraper.extract_hours("Monday-Friday 8:00 AM - 5:00 PM")
        assert "Monday" in result or "Mon" in result
        assert "AM" in result or "am" in result

    def test_abbreviated_days(self, scraper):
        result = scraper.extract_hours("Mon-Fri 9:00 AM to 4:30 PM")
        assert result != ""

    def test_no_hours(self, scraper):
        assert scraper.extract_hours("Visit our office for details") == ""

    def test_empty_string(self, scraper):
        assert scraper.extract_hours("") == ""

    def test_hours_with_24_7(self, scraper):
        # This may or may not match depending on the regex;
        # just ensure it doesn't crash
        result = scraper.extract_hours("Monday-Friday 8:00 AM - 5:00 PM, 24/7 Crisis Line")
        assert "AM" in result or "am" in result


# ===== extract_location =====

class TestExtractLocation:
    def test_room_number(self, scraper):
        result = scraper.extract_location("Located in Room 320, Student Center, Main Campus")
        assert "Room" in result or "room" in result

    def test_building_name(self, scraper):
        result = scraper.extract_location("Visit us at building A, second floor wing")
        assert "building" in result.lower()

    def test_hall_reference(self, scraper):
        result = scraper.extract_location("We are in Hall of Science, 2nd Floor, West Wing")
        assert "Hall" in result or "hall" in result

    def test_floor_reference(self, scraper):
        result = scraper.extract_location("Located on Floor 4, Student Services Building")
        assert "Floor" in result or "floor" in result

    def test_suite_reference(self, scraper):
        result = scraper.extract_location("Our office is Suite 530 in the Clifton Court Building")
        assert "Suite" in result or "suite" in result

    def test_center_reference(self, scraper):
        result = scraper.extract_location("Visit the Center for Student Wellness on campus")
        assert "Center" in result or "center" in result

    def test_no_location(self, scraper):
        assert scraper.extract_location("Call us for more information about our services") == ""

    def test_empty_string(self, scraper):
        assert scraper.extract_location("") == ""


# ===== extract_freshman_info =====

class TestExtractFreshmanInfo:
    def test_freshman_keyword(self, scraper):
        text = "All services are available. Freshman students receive priority scheduling during fall."
        result = scraper.extract_freshman_info(text)
        assert "freshman" in result.lower() or "Freshman" in result

    def test_first_year_keyword(self, scraper):
        text = "We offer workshops. First-year students can attend special orientation sessions."
        result = scraper.extract_freshman_info(text)
        assert "first-year" in result.lower() or "First-year" in result

    def test_new_student_keyword(self, scraper):
        text = "Resources for everyone. New student orientation includes mental health info."
        result = scraper.extract_freshman_info(text)
        assert "new student" in result.lower() or "New student" in result

    def test_no_freshman_info(self, scraper):
        assert scraper.extract_freshman_info("General counseling services available to all.") == ""

    def test_empty_string(self, scraper):
        assert scraper.extract_freshman_info("") == ""


# ===== clean_text =====

class TestCleanText:
    def test_extra_whitespace(self, scraper):
        assert scraper.clean_text("  hello   world  ") == "hello world"

    def test_newlines_and_tabs(self, scraper):
        assert scraper.clean_text("hello\n\t\tworld") == "hello world"

    def test_none_input(self, scraper):
        assert scraper.clean_text(None) == ""

    def test_empty_string(self, scraper):
        assert scraper.clean_text("") == ""

    def test_already_clean(self, scraper):
        assert scraper.clean_text("hello world") == "hello world"


# ===== deduplicate_resources =====

class TestDeduplicateResources:
    def test_removes_duplicates(self, scraper):
        resources = [
            {"service_name": "CAPS", "description": "v1"},
            {"service_name": "CAPS", "description": "v2"},
            {"service_name": "Wellness", "description": "v3"},
        ]
        result = scraper.deduplicate_resources(resources)
        names = [r["service_name"] for r in result]
        assert names == ["CAPS", "Wellness"]

    def test_keeps_first_occurrence(self, scraper):
        resources = [
            {"service_name": "CAPS", "description": "first"},
            {"service_name": "CAPS", "description": "second"},
        ]
        result = scraper.deduplicate_resources(resources)
        assert result[0]["description"] == "first"

    def test_empty_list(self, scraper):
        assert scraper.deduplicate_resources([]) == []

    def test_no_duplicates(self, scraper):
        resources = [
            {"service_name": "A"},
            {"service_name": "B"},
        ]
        assert len(scraper.deduplicate_resources(resources)) == 2
