"""
College Mental Health Resource Scraper
Reads targets from college_targets.json and scrapes mental health service pages.
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import time
import os
from datetime import datetime
from urllib.parse import urljoin, urlparse

# Configuration
TARGETS_FILE = os.path.join(os.path.dirname(__file__), 'college_targets.json')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'scraped_colleges_data.json')
MIN_QUALITY_SCORE = 30  # Minimum score to keep a resource (0-100)

# Quality indicators - words that suggest real content vs garbage
QUALITY_KEYWORDS = [
    'counseling', 'therapy', 'psychological', 'mental health', 'wellness',
    'crisis', 'support', 'anxiety', 'depression', 'stress', 'appointment',
    'session', 'confidential', 'psychiatry', 'psychologist', 'therapist'
]

# Garbage indicators - words that suggest error pages or cookie notices
GARBAGE_KEYWORDS = [
    '404', 'not found', 'error', 'page not found', 'cookie', 'cookies',
    'accept', 'privacy policy', 'terms of use', 'javascript required',
    'enable javascript', 'we use cookies', 'just a moment'
]


class CollegeScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        self.session.timeout = 15
        self.colleges_data = []
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'low_quality': 0
        }

    def load_targets(self):
        """Load college targets from JSON file."""
        with open(TARGETS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['colleges']

    def is_valid_url(self, url):
        """Check if URL is valid and reachable."""
        try:
            parsed = urlparse(url)
            return all([parsed.scheme, parsed.netloc])
        except Exception:
            return False

    def fetch_page(self, url):
        """Fetch a page with error handling."""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            return None

    def score_content(self, soup, text):
        """Score content quality (0-100)."""
        score = 50  # Base score
        text_lower = text.lower()

        # Check for quality keywords
        for keyword in QUALITY_KEYWORDS:
            if keyword in text_lower:
                score += 5

        # Check for garbage keywords
        for keyword in GARBAGE_KEYWORDS:
            if keyword in text_lower:
                score -= 15

        # Check for actual content length
        if len(text) > 200:
            score += 10
        if len(text) > 500:
            score += 10

        # Check for contact info (good sign)
        if re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', text):  # Email
            score += 10
        if re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text):  # Phone
            score += 10

        return max(0, min(100, score))

    def extract_resources(self, soup, url):
        """Extract mental health resources from HTML."""
        resources = []

        # Remove script and style elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        page_text = soup.get_text()

        # Skip low-quality pages early
        quality_score = self.score_content(soup, page_text)
        if quality_score < MIN_QUALITY_SCORE:
            return resources

        # Strategy 1: Look for contact/service sections
        contact_sections = soup.find_all(['div', 'section', 'article'],
            class_=re.compile(r'contact|service|resource|info', re.I))

        for section in contact_sections[:5]:
            resource = self.extract_from_section(section, url)
            if resource and resource.get('service_name'):
                resources.append(resource)

        # Strategy 2: Look for relevant headings
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        for heading in headings[:10]:
            heading_text = heading.get_text(strip=True).lower()
            if any(kw in heading_text for kw in ['counseling', 'mental', 'wellness', 'caps', 'psych', 'health']):
                resource = self.extract_near_heading(heading, url)
                if resource:
                    resources.append(resource)

        # Strategy 3: Fallback - create from page content
        if not resources:
            resource = self.extract_fallback(soup, page_text, url)
            if resource:
                resources.append(resource)

        return resources

    def extract_from_section(self, section, url):
        """Extract resource from a section element."""
        section_text = section.get_text()

        # Skip low-quality sections
        if self.score_content(section, section_text) < MIN_QUALITY_SCORE:
            return None

        resource = {
            "service_name": "",
            "description": "",
            "contact_email": "",
            "contact_phone": "",
            "contact_website": url,
            "department": "Student Affairs",
            "office_hours": "",
            "location": "",
            "freshman_notes": ""
        }

        # Get heading
        heading = section.find(['h1', 'h2', 'h3', 'h4', 'h5'])
        if heading:
            resource['service_name'] = self.clean_text(heading.get_text())

        # Get description from paragraphs
        paragraphs = section.find_all('p')
        descriptions = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30]
        if descriptions:
            resource['description'] = self.clean_text(descriptions[0])[:500]

        # Extract contact info
        resource['contact_email'] = self.extract_email(section_text)
        resource['contact_phone'] = self.extract_phone(section_text)
        resource['office_hours'] = self.extract_hours(section_text)
        resource['location'] = self.extract_location(section_text)

        return resource

    def extract_near_heading(self, heading, url):
        """Extract resource from content near a heading."""
        resource = {
            "service_name": self.clean_text(heading.get_text()),
            "description": "",
            "contact_email": "",
            "contact_phone": "",
            "contact_website": url,
            "department": "Student Affairs",
            "office_hours": "",
            "location": "",
            "freshman_notes": ""
        }

        # Get following content
        content_parts = []
        for sibling in heading.find_next_siblings(limit=5):
            if sibling.name in ['h1', 'h2', 'h3', 'h4']:
                break
            content_parts.append(sibling.get_text())

        content_text = ' '.join(content_parts)

        # Get description
        first_para = heading.find_next('p')
        if first_para:
            resource['description'] = self.clean_text(first_para.get_text())[:500]

        # Extract contact info
        resource['contact_email'] = self.extract_email(content_text)
        resource['contact_phone'] = self.extract_phone(content_text)
        resource['office_hours'] = self.extract_hours(content_text)
        resource['location'] = self.extract_location(content_text)

        return resource

    def extract_fallback(self, soup, page_text, url):
        """Fallback extraction when no structure found."""
        resource = {
            "service_name": "Counseling and Mental Health Services",
            "description": "",
            "contact_email": "",
            "contact_phone": "",
            "contact_website": url,
            "department": "Student Affairs",
            "office_hours": "",
            "location": "",
            "freshman_notes": "Visit the counseling center website for information about services."
        }

        # Get main title
        title = soup.find('h1')
        if title:
            resource['service_name'] = self.clean_text(title.get_text())

        # Get first meaningful paragraph
        paragraphs = soup.find_all('p')
        for para in paragraphs:
            text = para.get_text(strip=True)
            if len(text) > 50:
                resource['description'] = self.clean_text(text)[:500]
                break

        # Extract contact info
        resource['contact_email'] = self.extract_email(page_text)
        resource['contact_phone'] = self.extract_phone(page_text)
        resource['office_hours'] = self.extract_hours(page_text)
        resource['location'] = self.extract_location(page_text)

        # Only return if we have some useful data
        if resource['contact_email'] or resource['contact_phone'] or resource['description']:
            return resource
        return None

    def extract_email(self, text):
        """Extract email address."""
        match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        return match.group(0) if match else ""

    def extract_phone(self, text):
        """Extract phone number."""
        match = re.search(r'(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        return match.group(0) if match else ""

    def extract_hours(self, text):
        """Extract office hours."""
        pattern = r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[\s\w,-]*(?:AM|PM|am|pm|\d{1,2}[:\s]\d{1,2})'
        match = re.search(pattern, text, re.IGNORECASE)
        return self.clean_text(match.group(0))[:200] if match else ""

    def extract_location(self, text):
        """Extract location/address."""
        keywords = ['room', 'building', 'hall', 'center', 'floor', 'suite', 'address']
        for keyword in keywords:
            pattern = rf'{keyword}\s+[\w\s,.-]{{5,100}}'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return self.clean_text(match.group(0))[:200]
        return ""

    def clean_text(self, text):
        """Clean and normalize text."""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def deduplicate_resources(self, resources):
        """Remove duplicate resources by name."""
        unique = {}
        for resource in resources:
            name = resource.get('service_name', '').lower().strip()
            if name and name not in unique:
                unique[name] = resource
        return list(unique.values())

    def filter_low_quality(self, resources):
        """Filter out low-quality resources."""
        filtered = []
        for resource in resources:
            text = json.dumps(resource)
            score = self.score_content(None, text)
            if score >= MIN_QUALITY_SCORE:
                filtered.append(resource)
            else:
                self.stats['low_quality'] += 1
        return filtered

    def scrape_college(self, college):
        """Scrape mental health resources for a single college."""
        all_resources = []
        urls = college.get('mental_health_urls', [])

        for url in urls:
            if not self.is_valid_url(url):
                continue

            response = self.fetch_page(url)
            if not response:
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            resources = self.extract_resources(soup, url)
            all_resources.extend(resources)

            # Rate limiting
            time.sleep(1)

        # Deduplicate
        unique_resources = self.deduplicate_resources(all_resources)

        # Filter low quality
        unique_resources = self.filter_low_quality(unique_resources)

        return unique_resources

    def scrape_all(self):
        """Scrape all target colleges."""
        colleges = self.load_targets()
        self.stats['total'] = len(colleges)

        print(f"Starting scrape of {len(colleges)} colleges...\n")

        for i, college in enumerate(colleges, 1):
            # Skip manual entries
            if college.get('source') == 'manual':
                print(f"[{i}/{len(colleges)}] {college['name']}: SKIP (manual entry)")
                self.stats['skipped'] += 1
                continue

            print(f"[{i}/{len(colleges)}] Scraping {college['name']} ({college.get('state', 'unknown')})...")

            resources = self.scrape_college(college)

            college_data = {
                "name": college['name'],
                "location": college['location'],
                "latitude": college['latitude'],
                "longitude": college['longitude'],
                "website": college['website'],
                "resources": resources,
                "scraped_at": datetime.now().isoformat()
            }

            if resources:
                self.colleges_data.append(college_data)
                print(f"  [OK] Found {len(resources)} resource(s)")
                self.stats['success'] += 1
            else:
                print(f"  [FAIL] No resources found")
                self.stats['failed'] += 1

            time.sleep(1)  # Rate limiting between colleges

        return self.colleges_data

    def save_results(self):
        """Save scraped data to JSON file."""
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.colleges_data, f, indent=2, ensure_ascii=False)

        print(f"\n[OK] Saved {len(self.colleges_data)} colleges to {OUTPUT_FILE}")

    def print_stats(self):
        """Print scraping statistics."""
        print("\n" + "="*50)
        print("SCRAPING STATISTICS")
        print("="*50)
        print(f"Total colleges:     {self.stats['total']}")
        print(f"Successfully scraped: {self.stats['success']}")
        print(f"Failed:            {self.stats['failed']}")
        print(f"Skipped (manual):  {self.stats['skipped']}")
        print(f"Low quality filtered: {self.stats['low_quality']}")
        print("="*50)


def main():
    print("="*60)
    print("College Mental Health Resource Scraper")
    print("="*60)
    print(f"Targets: {TARGETS_FILE}")
    print(f"Output:  {OUTPUT_FILE}")
    print("="*60 + "\n")

    scraper = CollegeScraper()
    data = scraper.scrape_all()

    if data:
        scraper.save_results()
        scraper.print_stats()
        print(f"\n[OK] Complete! Scraped {len(data)} colleges.")
    else:
        print("\n[FAIL] No data collected. Check URLs and try again.")


if __name__ == "__main__":
    main()
