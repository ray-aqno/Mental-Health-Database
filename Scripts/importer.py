"""
Consolidated importer for college mental health data.
Supports full import (colleges + resources) and resources-only mode.
Uses the bulk endpoint for single-request imports with upsert.

Usage:
    python importer.py                              # Full import from scraped_colleges_data.json
    python importer.py --file starter_data.json     # Import from a specific file
    python importer.py --base-url http://host:port  # Custom API base URL
    python importer.py --api-key YOUR_KEY           # Provide API key for auth
"""

import argparse
import json
import sys
import urllib3

import requests

# Disable SSL warnings for localhost
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_API_BASE = "http://localhost:58346/api"
DEFAULT_DATA_FILE = "scraped_colleges_data.json"


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
        print(f"❌ File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {filepath}: {e}")
        sys.exit(1)

    if not isinstance(data, list):
        print(f"❌ Expected a JSON array in {filepath}, got {type(data).__name__}")
        sys.exit(1)

    if len(data) == 0:
        print(f"⚠ Data file is empty: {filepath}")
        sys.exit(1)

    return data


def run_import(filepath, base_url, api_key):
    """Main import flow: load file → build payloads → bulk import."""
    print("=" * 70)
    print("COLLEGE MENTAL HEALTH DATA IMPORTER")
    print("=" * 70)

    # Load data
    print(f"\n📂 Loading data from: {filepath}")
    colleges_data = load_data_file(filepath)
    total_resources = sum(len(c.get("resources", [])) for c in colleges_data)
    print(f"   Found {len(colleges_data)} college(s) with {total_resources} total resource(s)")

    # Connect to API
    print(f"\n🌐 Connecting to API: {base_url}")
    client = APIClient(base_url=base_url, api_key=api_key)

    if not client.health_check():
        print("❌ API is not reachable. Is the server running?")
        print(f"   Tried: {base_url}/colleges")
        print("\n   Start the server with: dotnet run")
        sys.exit(1)
    print("   ✓ API is reachable")

    # Build payloads
    print("\n📦 Building import payloads...")
    payloads = [build_college_payload(c) for c in colleges_data]

    # Preview
    print("\n   Colleges to import:")
    for p in payloads:
        r_count = len(p.get("resources", []))
        print(f"     • {p['name']} ({p['location']}) — {r_count} resource(s)")

    # Bulk import
    print(f"\n🚀 Sending bulk import request...")
    try:
        result = client.bulk_import(payloads)
        print(f"   ✓ {result.get('message', 'Import complete')}")
    except requests.HTTPError as e:
        print(f"   ❌ Import failed: {e.response.status_code}")
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
        print(f"   ⚠ Could not verify: {e}")

    print("\n" + "=" * 70)
    print(f"✅ IMPORT COMPLETE!")
    print(f"   🌐 View your data at: http://localhost:58346")
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

    args = parser.parse_args()
    run_import(args.file, args.base_url, args.api_key)


if __name__ == "__main__":
    main()
