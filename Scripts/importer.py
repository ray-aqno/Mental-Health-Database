"""
Consolidated importer for college mental health data.
Supports full import (colleges + resources) and resources-only mode.
Uses the bulk endpoint for single-request imports with upsert.

Usage:
    python importer.py                              # Full import from scraped_colleges_data.json
    python importer.py --file starter_data.json     # Import from a specific file
    python importer.py --base-url http://host:port  # Custom API base URL
    python importer.py --api-key YOUR_KEY           # Provide API key for auth
    python importer.py --skip-validation            # Skip validation step
"""

import argparse
import json
import sys
import urllib3
import re

import requests

# Disable SSL warnings for localhost
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_API_BASE = "http://localhost:58346/api"
DEFAULT_DATA_FILE = "scraped_colleges_data.json"

# Validation thresholds - relaxed for real-world scraped data
MIN_DESCRIPTION_LENGTH = 10


def validate_email(email):
    """Validate email format."""
    if not email:
        return True
    pattern = r'^[\w.-]+@[\w.-]+\.\w+$'
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """Validate phone format - lenient for scraped data."""
    if not phone:
        return True
    # Allow any reasonable phone-like string (digits, spaces, dashes, parens, dots, plus)
    cleaned = re.sub(r'[\s\-\(\)\.\+]', '', phone)
    return len(cleaned) >= 7 and cleaned.replace('x', '').isdigit()


def validate_resource(resource):
    """Validate a single resource. Returns (is_valid, error_message)."""
    # Check for service name
    if not resource.get("service_name"):
        return False, "Missing service_name"

    # Check for at least some contact info
    has_contact = any([
        resource.get("contact_email"),
        resource.get("contact_phone"),
        resource.get("contact_website")
    ])
    if not has_contact:
        return False, "No contact information"

    # Validate email format
    if not validate_email(resource.get("contact_email", "")):
        return False, "Invalid email format"

    # Validate phone format
    if not validate_phone(resource.get("contact_phone", "")):
        return False, "Invalid phone format"

    # Check description length
    desc = resource.get("description", "")
    if desc and len(desc) < MIN_DESCRIPTION_LENGTH:
        return False, f"Description too short ({len(desc)} chars)"

    return True, None


def validate_college(college):
    """Validate a single college. Returns (is_valid, error_message)."""
    # Check required fields
    required = ["name", "location", "latitude", "longitude", "website"]
    for field in required:
        if not college.get(field):
            return False, f"Missing {field}"

    # Validate lat/long
    try:
        lat = float(college.get("latitude", 0))
        lng = float(college.get("longitude", 0))
        if not (-90 <= lat <= 90 and -180 <= lng <= 180):
            return False, "Invalid coordinates"
    except (ValueError, TypeError):
        return False, "Invalid coordinates"

    # Check for resources
    resources = college.get("resources", [])
    if not resources:
        return False, "No resources"

    # Validate resources
    for i, resource in enumerate(resources):
        is_valid, error = validate_resource(resource)
        if not is_valid:
            return False, f"Resource {i}: {error}"

    return True, None


def validate_data(data):
    """Validate entire dataset. Returns (valid_data, invalid_data, errors)."""
    valid = []
    invalid = []
    errors = []

    for college in data:
        is_valid, error = validate_college(college)
        if is_valid:
            valid.append(college)
        else:
            invalid.append(college)
            errors.append(f"{college.get('name', 'Unknown')}: {error}")

    return valid, invalid, errors


def build_resource_payload(resource_data, college_id=0):
    """Build a single resource JSON payload from scraped data format.
    
    This is the single source of truth for mapping scraped field names
    (snake_case) to API field names (camelCase).
    """
    return {
        "collegeId": college_id,
        "serviceName": resource_data.get("service_name", "Counseling Services"),
        "description": resource_data.get("description", ""),
        "contactEmail": resource_data.get("contact_email", ""),
        "contactPhone": resource_data.get("contact_phone", ""),
        "contactWebsite": resource_data.get("contact_website", ""),
        "department": resource_data.get("department", ""),
        "officeHours": resource_data.get("office_hours", ""),
        "location": resource_data.get("location", ""),
        "freshmanNotes": resource_data.get("freshman_notes", ""),
    }


def build_college_payload(college_data):
    """Build a single college JSON payload (with nested resources) from scraped data format."""
    resources = college_data.get("resources", [])
    return {
        "name": college_data.get("name"),
        "location": college_data.get("location"),
        "latitude": college_data.get("latitude"),
        "longitude": college_data.get("longitude"),
        "website": college_data.get("website"),
        "resources": [build_resource_payload(r) for r in resources],
    }


class APIClient:
    """Thin wrapper around the Mental Health Database API."""

    def __init__(self, base_url=DEFAULT_API_BASE, api_key=""):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.verify = False
        if api_key:
            self.session.headers["X-Api-Key"] = api_key

    def health_check(self):
        """Check if the API is reachable."""
        try:
            resp = self.session.get(f"{self.base_url}/colleges", timeout=5)
            return resp.status_code == 200
        except requests.ConnectionError:
            return False

    def get_colleges(self):
        """Fetch all colleges from the API."""
        resp = self.session.get(f"{self.base_url}/colleges")
        resp.raise_for_status()
        return resp.json()

    def bulk_import(self, colleges_payload):
        """Import colleges via the bulk endpoint (upsert)."""
        resp = self.session.post(
            f"{self.base_url}/colleges/bulk",
            json=colleges_payload,
        )
        resp.raise_for_status()
        return resp.json()


def load_data_file(filepath):
    """Load and validate a JSON data file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[FAIL] File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[FAIL] Invalid JSON in {filepath}: {e}")
        sys.exit(1)

    if not isinstance(data, list):
        print(f"[FAIL] Expected a JSON array in {filepath}, got {type(data).__name__}")
        sys.exit(1)

    if len(data) == 0:
        print(f"[WARN] Data file is empty: {filepath}")
        sys.exit(1)

    return data


def run_import(filepath, base_url, api_key, skip_validation=False):
    """Main import flow: load file → validate → build payloads → bulk import."""
    print("=" * 70)
    print("COLLEGE MENTAL HEALTH DATA IMPORTER")
    print("=" * 70)

    # Load data
    print(f"\n[FILE] Loading data from: {filepath}")
    colleges_data = load_data_file(filepath)
    total_resources = sum(len(c.get("resources", [])) for c in colleges_data)
    print(f"   Found {len(colleges_data)} college(s) with {total_resources} total resource(s)")

    # Validate data
    if not skip_validation:
        print("\n[CHECK] Validating data...")
        valid_data, invalid_data, errors = validate_data(colleges_data)

        if invalid_data:
            print(f"   [WARN]  {len(invalid_data)} college(s) failed validation and will be skipped:")
            for error in errors[:5]:
                print(f"      • {error}")
            if len(errors) > 5:
                print(f"      ... and {len(errors) - 5} more")
            print(f"\n   [OK] {len(valid_data)} college(s) passed validation")
            colleges_data = valid_data
        else:
            print(f"   [OK] All {len(colleges_data)} colleges passed validation")
    else:
        print("\n[SKIP] Validation skipped (--skip-validation flag)")

    if not colleges_data:
        print("\n[FAIL] No valid data to import")
        sys.exit(1)

    # Connect to API
    print(f"\n[NET] Connecting to API: {base_url}")
    client = APIClient(base_url=base_url, api_key=api_key)

    if not client.health_check():
        print("[FAIL] API is not reachable. Is the server running?")
        print(f"   Tried: {base_url}/colleges")
        print("\n   Start the server with: dotnet run")
        sys.exit(1)
    print("   [OK] API is reachable")

    # Build payloads
    print("\n[DATA] Building import payloads...")
    payloads = [build_college_payload(c) for c in colleges_data]

    # Preview
    print("\n   Colleges to import:")
    for p in payloads:
        r_count = len(p.get("resources", []))
        print(f"     • {p['name']} ({p['location']}) — {r_count} resource(s)")

    # Bulk import
    print(f"\n[SEND] Sending bulk import request...")
    try:
        result = client.bulk_import(payloads)
        print(f"   [OK] {result.get('message', 'Import complete')}")
    except requests.HTTPError as e:
        print(f"   [FAIL] Import failed: {e.response.status_code}")
        try:
            detail = e.response.json()
            print(f"      {detail.get('message', e.response.text[:200])}")
        except Exception:
            print(f"      {e.response.text[:200]}")
        sys.exit(1)

    # Verify
    print("\n📊 Verifying import...")
    try:
        colleges = client.get_colleges()
        db_resources = sum(len(c.get("resources", [])) for c in colleges)
        print(f"   Database now contains: {len(colleges)} college(s), {db_resources} resource(s)")
    except Exception as e:
        print(f"   [WARN] Could not verify: {e}")

    print("\n" + "=" * 70)
    print(f"[OK] IMPORT COMPLETE!")
    print(f"   [NET] View your data at: http://localhost:58346")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Import college mental health data into the database."
    )
    parser.add_argument(
        "--file",
        default=DEFAULT_DATA_FILE,
        help=f"Path to the JSON data file (default: {DEFAULT_DATA_FILE})",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_API_BASE,
        help=f"API base URL (default: {DEFAULT_API_BASE})",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="API key for authenticated write access",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip data validation before import",
    )

    args = parser.parse_args()
    run_import(args.file, args.base_url, args.api_key, args.skip_validation)


if __name__ == "__main__":
    main()
