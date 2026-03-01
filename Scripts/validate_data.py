"""
Data Validation Utility for College Mental Health Resources
Validates scraped data before import to ensure quality.
"""

import json
import re
import os
import sys
from datetime import datetime

SCRAPED_FILE = os.path.join(os.path.dirname(__file__), 'scraped_colleges_data.json')
MANUAL_FILE = os.path.join(os.path.dirname(__file__), 'manual_ohio_schools.json')

# Quality thresholds
MIN_RESOURCES_PER_COLLEGE = 1
MIN_DESCRIPTION_LENGTH = 20
MIN_COLLEGE_NAME_LENGTH = 3

# Required fields for resources
REQUIRED_RESOURCE_FIELDS = [
    'service_name',
    'description',
    'contact_email',
    'contact_phone',
    'contact_website',
]

# Optional but preferred fields
PREFERRED_RESOURCE_FIELDS = [
    'department',
    'office_hours',
    'location',
    'freshman_notes',
]


class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {
            'colleges': 0,
            'resources': 0,
            'colleges_valid': 0,
            'colleges_with_issues': 0,
            'resources_valid': 0,
            'resources_with_issues': 0,
            'empty_resources': 0,
            'no_contact': 0,
            'short_description': 0,
        }

    def add_error(self, msg):
        self.errors.append(msg)

    def add_warning(self, msg):
        self.warnings.append(msg)


def validate_email(email):
    """Validate email format."""
    if not email:
        return True  # Optional
    pattern = r'^[\w.-]+@[\w.-]+\.\w+$'
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """Validate phone format."""
    if not phone:
        return True  # Optional
    # Remove common formatting and check
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    return cleaned.isdigit() and len(cleaned) >= 10


def validate_url(url):
    """Validate URL format."""
    if not url:
        return True  # Optional
    pattern = r'^https?://[\w\-\.]+'
    return bool(re.match(pattern, url, re.IGNORECASE))


def validate_lat_long(lat, lng):
    """Validate latitude and longitude."""
    try:
        lat = float(lat)
        lng = float(lng)
        return -90 <= lat <= 90 and -180 <= lng <= 180
    except (ValueError, TypeError):
        return False


def validate_college(college, result):
    """Validate a single college entry."""
    issues = []

    # Check required fields
    required = ['name', 'location', 'latitude', 'longitude', 'website']
    for field in required:
        if not college.get(field):
            issues.append(f"Missing required field: {field}")

    # Validate name
    name = college.get('name', '')
    if len(name) < MIN_COLLEGE_NAME_LENGTH:
        issues.append(f"College name too short: '{name}'")

    # Validate lat/long
    if not validate_lat_long(college.get('latitude'), college.get('longitude')):
        issues.append(f"Invalid coordinates: {college.get('latitude')}, {college.get('longitude')}")

    # Validate website URL
    if not validate_url(college.get('website')):
        issues.append(f"Invalid website URL: {college.get('website')}")

    # Check resources
    resources = college.get('resources', [])
    if not resources:
        issues.append("No resources found")
        result.stats['empty_resources'] += 1
    elif len(resources) < MIN_RESOURCES_PER_COLLEGE:
        issues.append(f"Too few resources: {len(resources)}")

    # Validate each resource
    for i, resource in enumerate(resources):
        resource_issues = validate_resource(resource, i, result)
        issues.extend(resource_issues)

    if issues:
        result.add_error(f"College '{name}': {'; '.join(issues)}")
        result.stats['colleges_with_issues'] += 1
    else:
        result.stats['colleges_valid'] += 1

    result.stats['colleges'] += 1
    result.stats['resources'] += len(resources)


def validate_resource(resource, index, result):
    """Validate a single resource entry."""
    issues = []

    # Check required fields
    for field in REQUIRED_RESOURCE_FIELDS:
        if not resource.get(field):
            issues.append(f"Missing: {field}")

    # Validate email
    if not validate_email(resource.get('contact_email')):
        issues.append("Invalid email format")

    # Validate phone
    if not validate_phone(resource.get('contact_phone')):
        issues.append("Invalid phone format")

    # Validate URL
    if not validate_url(resource.get('contact_website')):
        issues.append("Invalid contact website URL")

    # Check description length
    desc = resource.get('description', '')
    if desc and len(desc) < MIN_DESCRIPTION_LENGTH:
        issues.append(f"Description too short ({len(desc)} chars)")
        result.stats['short_description'] += 1

    # Check for no contact info at all
    has_contact = any([
        resource.get('contact_email'),
        resource.get('contact_phone'),
        resource.get('contact_website')
    ])
    if not has_contact:
        issues.append("No contact information (email, phone, or website)")
        result.stats['no_contact'] += 1

    if issues:
        result.stats['resources_with_issues'] += 1
    else:
        result.stats['resources_valid'] += 1

    return issues


def check_garbage_data(resource):
    """Check for garbage/invalid data patterns."""
    garbage_patterns = [
        (r'404[\s\-]*(not[\s\-]*found)?', '404 error page'),
        (r'page[\s\-]*not[\s\-]*found', 'Page not found'),
        (r'error[\s\-]*\d+', 'Error code'),
        (r'javascript[\s\-]*required', 'JS required page'),
        (r'enable[\s\-]*javascript', 'Enable JavaScript'),
        (r'just[\s\-]*a[\s\-]*moment', 'Cloudflare/loading'),
        (r'cookie', 'Cookie notice'),
    ]

    text = json.dumps(resource).lower()

    for pattern, description in garbage_patterns:
        if re.search(pattern, text):
            return description

    return None


def load_data_file(filepath):
    """Load JSON data file."""
    if not os.path.exists(filepath):
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_data_file(filepath, result):
    """Validate a data file and add results."""
    data = load_data_file(filepath)

    if not data:
        result.add_warning(f"File is empty: {filepath}")
        return

    for college in data:
        validate_college(college, result)


def print_report(result, verbose=False):
    """Print validation report."""
    print("\n" + "="*60)
    print("DATA VALIDATION REPORT")
    print("="*60)

    # Statistics
    print(f"\n-- STATISTICS:")
    print(f"   Total colleges:      {result.stats['colleges']}")
    print(f"   Total resources:     {result.stats['resources']}")
    print(f"   Valid colleges:      {result.stats['colleges_valid']}")
    print(f"   Colleges with issues: {result.stats['colleges_with_issues']}")
    print(f"   Valid resources:     {result.stats['resources_valid']}")
    print(f"   Resources with issues: {result.stats['resources_with_issues']}")

    # Common issues
    print(f"\n-- COMMON ISSUES:")
    print(f"   Empty resource lists: {result.stats['empty_resources']}")
    print(f"   No contact info:      {result.stats['no_contact']}")
    print(f"   Short descriptions:   {result.stats['short_description']}")

    # Errors
    if result.errors:
        print(f"\n-- ERRORS ({len(result.errors)}):")
        for error in result.errors[:20]:  # Limit output
            print(f"   • {error}")
        if len(result.errors) > 20:
            print(f"   ... and {len(result.errors) - 20} more")

    # Warnings
    if result.warnings:
        print(f"\n-- WARNINGS ({len(result.warnings)}):")
        for warning in result.warnings[:10]:
            print(f"   • {warning}")
        if len(result.warnings) > 10:
            print(f"   ... and {len(result.warnings) - 10} more")

    # Summary
    print("\n" + "="*60)
    if result.stats['colleges_with_issues'] == 0:
        print("-- VALIDATION PASSED - Data looks good!")
    else:
        print(f"-- VALIDATION FAILED - {result.stats['colleges_with_issues']} college(s) with issues")
    print("="*60)

    return result.stats['colleges_with_issues'] == 0


def main():
    print("="*60)
    print("College Mental Health Data Validator")
    print("="*60)

    result = ValidationResult()

    # Validate scraped data
    if os.path.exists(SCRAPED_FILE):
        print(f"\n-- Validating: {SCRAPED_FILE}")
        validate_data_file(SCRAPED_FILE, result)
    else:
        result.add_warning(f"Scraped file not found: {SCRAPED_FILE}")

    # Validate manual data
    if os.path.exists(MANUAL_FILE):
        print(f"-- Validating: {MANUAL_FILE}")
        validate_data_file(MANUAL_FILE, result)
    else:
        result.add_warning(f"Manual file not found: {MANUAL_FILE}")

    # Print report
    passed = print_report(result)

    # Exit code
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
