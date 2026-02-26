"""
Simple College Mental Health Resource Scraper
Lightweight alternative using requests + BeautifulSoup
Targets: UC, OSU, Miami, Xavier, UDayton, OU, NKU, Wright State, Purdue, Case Western
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import time
from datetime import datetime
from urllib.parse import urljoin


# College configuration
COLLEGES_CONFIG = [
    {
        "name": "University of Cincinnati",
        "short_name": "UC",
        "location": "Cincinnati, Ohio",
        "latitude": 39.1329,
        "longitude": -84.5150,
        "website": "https://www.uc.edu",
        "mental_health_urls": [
            "https://www.uc.edu/campus-life/caps.html",
            "https://www.uc.edu/studentaffairs/counseling.html"
        ]
    },
    {
        "name": "The Ohio State University",
        "short_name": "OSU",
        "location": "Columbus, Ohio",
        "latitude": 40.0067,
        "longitude": -83.0305,
        "website": "https://www.osu.edu",
        "mental_health_urls": [
            "https://ccs.osu.edu/",
            "https://swc.osu.edu/"
        ]
    },
    {
        "name": "Miami University",
        "short_name": "Miami",
        "location": "Oxford, Ohio",
        "latitude": 39.5097,
        "longitude": -84.7330,
        "website": "https://www.miamioh.edu",
        "mental_health_urls": [
            "https://miamioh.edu/student-life/student-counseling-service/",
            "https://miamioh.edu/student-wellness/"
        ]
    },
    {
        "name": "Xavier University",
        "short_name": "Xavier",
        "location": "Cincinnati, Ohio",
        "latitude": 39.1484,
        "longitude": -84.4745,
        "website": "https://www.xavier.edu",
        "mental_health_urls": [
            "https://www.xavier.edu/counseling/",
            "https://www.xavier.edu/health-wellness/"
        ]
    },
    {
        "name": "University of Dayton",
        "short_name": "UDayton",
        "location": "Dayton, Ohio",
        "latitude": 39.7400,
        "longitude": -84.1800,
        "website": "https://www.udayton.edu",
        "mental_health_urls": [
            "https://www.udayton.edu/studev/counselingcenter/",
            "https://www.udayton.edu/studenthealth/"
        ]
    },
    {
        "name": "Ohio University",
        "short_name": "OU",
        "location": "Athens, Ohio",
        "latitude": 39.3292,
        "longitude": -82.1013,
        "website": "https://www.ohio.edu",
        "mental_health_urls": [
            "https://www.ohio.edu/student-affairs/counseling",
            "https://www.ohio.edu/wellness/"
        ]
    },
    {
        "name": "Northern Kentucky University",
        "short_name": "NKU",
        "location": "Highland Heights, Kentucky",
        "latitude": 39.0325,
        "longitude": -84.4661,
        "website": "https://www.nku.edu",
        "mental_health_urls": [
            "https://www.nku.edu/academics/hhs/programs/counseling.html",
            "https://inside.nku.edu/healthwellness.html"
        ]
    },
    {
        "name": "Wright State University",
        "short_name": "Wright State",
        "location": "Dayton, Ohio",
        "latitude": 39.7806,
        "longitude": -84.0533,
        "website": "https://www.wright.edu",
        "mental_health_urls": [
            "https://www.wright.edu/student-affairs/student-counseling-and-wellness",
            "https://www.wright.edu/wellness/"
        ]
    },
    {
        "name": "Purdue University",
        "short_name": "Purdue",
        "location": "West Lafayette, Indiana",
        "latitude": 40.4237,
        "longitude": -86.9212,
        "website": "https://www.purdue.edu",
        "mental_health_urls": [
            "https://www.purdue.edu/caps/",
            "https://www.purdue.edu/wellness/"
        ]
    },
    {
        "name": "Case Western Reserve University",
        "short_name": "Case Western",
        "location": "Cleveland, Ohio",
        "latitude": 41.5045,
        "longitude": -81.6081,
        "website": "https://www.case.edu",
        "mental_health_urls": [
            "https://case.edu/studentlife/healthcounseling/counseling-services/",
            "https://case.edu/wellness/"
        ]
    }
]


class SimpleCollegeScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.colleges_data = []

    def scrape_all_colleges(self):
        """Scrape all configured colleges"""
        print(f"Starting scrape of {len(COLLEGES_CONFIG)} colleges...\n")
        
        for i, college_config in enumerate(COLLEGES_CONFIG, 1):
            print(f"[{i}/{len(COLLEGES_CONFIG)}] Scraping {college_config['name']}...")
            
            college_data = self.scrape_college(college_config)
            if college_data:
                self.colleges_data.append(college_data)
                print(f"  ✓ Found {len(college_data['resources'])} resources")
            else:
                print(f"  ✗ No resources found")
            
            # Be polite - wait between requests
            time.sleep(2)
            print()
        
        return self.colleges_data

    def scrape_college(self, college_config):
        """Scrape a single college's mental health resources"""
        all_resources = []
        
        for url in college_config['mental_health_urls']:
            try:
                print(f"  Fetching: {url}")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                resources = self.extract_resources(soup, url)
                all_resources.extend(resources)
                
            except requests.RequestException as e:
                print(f"  Error fetching {url}: {str(e)}")
                continue
        
        # Deduplicate resources
        unique_resources = self.deduplicate_resources(all_resources)
        
        # If no resources found, create a default one
        if not unique_resources:
            unique_resources = [self.create_default_resource(college_config)]
        
        college_data = {
            "name": college_config['name'],
            "location": college_config['location'],
            "latitude": college_config['latitude'],
            "longitude": college_config['longitude'],
            "website": college_config['website'],
            "resources": unique_resources,
            "scraped_at": datetime.now().isoformat()
        }
        
        return college_data

    def extract_resources(self, soup, url):
        """Extract mental health resources from HTML"""
        resources = []
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get page text
        page_text = soup.get_text()
        
        # Strategy 1: Look for contact information sections
        contact_sections = soup.find_all(['div', 'section', 'article'], class_=re.compile(r'contact|service|resource', re.I))
        
        if contact_sections:
            for section in contact_sections[:5]:
                resource = self.extract_resource_from_section(section, url)
                if resource and resource.get('service_name'):
                    resources.append(resource)
        
        # Strategy 2: Look for headings + following content
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        for heading in headings[:10]:
            heading_text = heading.get_text(strip=True).lower()
            if any(keyword in heading_text for keyword in ['counseling', 'mental health', 'wellness', 'caps', 'psychological']):
                resource = self.extract_resource_near_heading(heading, url)
                if resource:
                    resources.append(resource)
        
        # If no structured resources, create one from page content
        if not resources:
            resource = self.extract_from_full_page(soup, page_text, url)
            if resource:
                resources.append(resource)
        
        return resources

    def extract_resource_from_section(self, section, url):
        """Extract resource data from a section element"""
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
        
        # Get section text
        section_text = section.get_text()
        
        # Service name from heading
        heading = section.find(['h1', 'h2', 'h3', 'h4', 'h5'])
        if heading:
            resource['service_name'] = self.clean_text(heading.get_text())
        
        # Description from paragraph
        para = section.find('p')
        if para:
            resource['description'] = self.clean_text(para.get_text())[:500]
        
        # Extract contact info
        resource['contact_email'] = self.extract_email(section_text)
        resource['contact_phone'] = self.extract_phone(section_text)
        resource['office_hours'] = self.extract_hours(section_text)
        resource['location'] = self.extract_location(section_text)
        resource['freshman_notes'] = self.extract_freshman_info(section_text)
        
        return resource

    def extract_resource_near_heading(self, heading, url):
        """Extract resource from content near a heading"""
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
        
        # Get next siblings (following content)
        content_parts = []
        for sibling in heading.find_next_siblings(limit=5):
            if sibling.name in ['h1', 'h2', 'h3', 'h4']:
                break
            content_parts.append(sibling.get_text())
        
        content_text = ' '.join(content_parts)
        
        # Extract first paragraph as description
        first_para = heading.find_next('p')
        if first_para:
            resource['description'] = self.clean_text(first_para.get_text())[:500]
        
        # Extract contact info
        resource['contact_email'] = self.extract_email(content_text)
        resource['contact_phone'] = self.extract_phone(content_text)
        resource['office_hours'] = self.extract_hours(content_text)
        resource['location'] = self.extract_location(content_text)
        resource['freshman_notes'] = self.extract_freshman_info(content_text)
        
        return resource

    def extract_from_full_page(self, soup, page_text, url):
        """Extract resource from full page when no structure found"""
        resource = {
            "service_name": "Counseling and Mental Health Services",
            "description": "",
            "contact_email": "",
            "contact_phone": "",
            "contact_website": url,
            "department": "Student Affairs",
            "office_hours": "",
            "location": "",
            "freshman_notes": "Visit the website for information about services for new students."
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
        
        # Extract contact info from full page
        resource['contact_email'] = self.extract_email(page_text)
        resource['contact_phone'] = self.extract_phone(page_text)
        resource['office_hours'] = self.extract_hours(page_text)
        resource['location'] = self.extract_location(page_text)
        
        return resource if resource['contact_email'] or resource['contact_phone'] else None

    # Helper extraction methods
    def extract_email(self, text):
        """Extract email address"""
        match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        return match.group(0) if match else ""

    def extract_phone(self, text):
        """Extract phone number"""
        match = re.search(r'(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        return match.group(0) if match else ""

    def extract_hours(self, text):
        """Extract office hours"""
        pattern = r'(Monday|Mon|M)[\s\w,-]*(Friday|Fri|F)[^\.]*(?:\d{1,2}[:\s]*(?:AM|PM|am|pm))'
        match = re.search(pattern, text, re.IGNORECASE)
        return self.clean_text(match.group(0))[:200] if match else ""

    def extract_location(self, text):
        """Extract location/address"""
        location_keywords = ['room', 'building', 'hall', 'center', 'floor', 'suite', 'address']
        for keyword in location_keywords:
            pattern = rf'{keyword}\s+[\w\s,.-]{{10,100}}'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return self.clean_text(match.group(0))[:200]
        return ""

    def extract_freshman_info(self, text):
        """Extract freshman-specific information"""
        freshman_keywords = ['freshman', 'first-year', 'new student', 'incoming student', 'first year']
        for keyword in freshman_keywords:
            if keyword.lower() in text.lower():
                # Get context around keyword
                idx = text.lower().find(keyword.lower())
                start = max(0, idx - 100)
                end = min(len(text), idx + 300)
                context = text[start:end]
                return self.clean_text(context)
        return ""

    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def deduplicate_resources(self, resources):
        """Remove duplicate resources"""
        unique = {}
        for resource in resources:
            name = resource.get('service_name', '')
            if name and name not in unique:
                unique[name] = resource
        return list(unique.values())

    def create_default_resource(self, college_config):
        """Create a default resource entry"""
        return {
            "service_name": "Counseling and Mental Health Services",
            "description": f"Mental health support services available to students at {college_config['name']}. Contact the counseling center for more information.",
            "contact_email": "",
            "contact_phone": "",
            "contact_website": college_config['mental_health_urls'][0] if college_config['mental_health_urls'] else college_config['website'],
            "department": "Student Affairs / Counseling Center",
            "office_hours": "Please visit the website for current hours",
            "location": "Check website for location details",
            "freshman_notes": "New students should visit the counseling center website or contact them directly for information about available services."
        }

    def save_to_json(self, filename='scraped_colleges_data.json'):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.colleges_data, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Saved {len(self.colleges_data)} colleges to {filename}")


def main():
    print("="*70)
    print("College Mental Health Resource Scraper - Simple Version")
    print("="*70)
    print("\nTarget Colleges:")
    for college in COLLEGES_CONFIG:
        print(f"  • {college['name']} ({college['short_name']})")
    print("\n" + "="*70 + "\n")
    
    scraper = SimpleCollegeScraper()
    data = scraper.scrape_all_colleges()
    
    if data:
        scraper.save_to_json()
        print(f"\n{'='*70}")
        print(f"Scraping Complete! Collected data from {len(data)} colleges.")
        print(f"{'='*70}\n")
    else:
        print("\n✗ No data collected. Please check URLs and try again.\n")


if __name__ == "__main__":
    main()
