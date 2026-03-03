"""One-time cleanup: remove non-mental-health resources from seed data.

Flags a resource as bad if its service_name or description contains
keywords associated with dental services, academic degree programs,
error pages, cookie banners, or other irrelevant content.
"""
import json, os, re, sys

BAD_PATTERNS = [
    # Dental / medical (non-mental-health)
    r'\bdental\b', r'\bdentistry\b', r'\boral health\b', r'\bwhitening\b',
    r'\bcleaning services\b',
    # Academic programs / departments (not student services)
    r"\bmaster'?s program", r'\bdoctoral program', r'\baccredited.*program',
    r'\badmissions\b.*\bprogram', r'\bcurriculum\b', r'\btuition\b',
    r'\bdepartment of counseling\b', r'\bcounselor education\b',
    r'\bcounseling education\b', r'\bcounseling admissions\b',
    r'\bclinical mental health counseling\b.*learning',
    r'\bCACREP\b', r'\baccreditation of counseling\b',
    r'\binterviewed in\b', r'\bcounseling today magazine\b',
    r'\bsupport iup counseling students\b',
    r'\binvest in the world',
    r'\bunique program\b.*state system',
    r'\bassistant dean\b.*department chair',
    r'\bprogram coordinator\b',
    # Error / garbage pages
    r'\b404\b', r'\bpage not found\b', r'\boops\b.*not found',
    r'\bwe use cookies\b', r'\bjavascript required\b',
    r'\benable javascript\b',
    # Generic university marketing (not a service)
    r'\bsmarter model\b.*stronger kentucky',
    r'\btransdisciplinary strategy\b',
    r'\bCATS AI\b',
    r'\bfinding your passion\b.*journey',
    r'\ba to z list\b',
    # Weather / generic pages
    r'\bweather\b.*\binformation\b', r'\bcancellations\b.*weather',
    # Vague non-service pages
    r'\bhighlights\b$',
    r'\bevents\b$',
    # Degree-program variant catches
    r"\bexplore wku'?s\b.*master",
    r'\bschool counseling and clinical\b',
]

# Also remove resources whose description is essentially empty or an error
MIN_DESC_LENGTH = 20

def is_bad_resource(r):
    name = (r.get("service_name") or "").strip()
    desc = (r.get("description") or "").strip()
    combined = f"{name} {desc}"

    # Pattern match
    for pat in BAD_PATTERNS:
        if re.search(pat, combined, re.IGNORECASE):
            return True, f"pattern: {pat}"

    # Empty / trivially short description with no contact info
    has_contact = any([
        r.get("contact_email"),
        r.get("contact_phone"),
        r.get("contact_website"),
    ])
    if len(desc) < MIN_DESC_LENGTH and not has_contact:
        return True, "no description and no contact info"

    return False, ""


def clean_file(path):
    if not os.path.exists(path):
        print(f"  SKIP (not found): {path}")
        return

    data = json.load(open(path, "r", encoding="utf-8"))
    total_before = sum(len(c.get("resources", [])) for c in data)
    removed = []

    for college in data:
        clean = []
        for r in college.get("resources", []):
            bad, reason = is_bad_resource(r)
            if bad:
                removed.append((college["name"], r.get("service_name", "?"), reason))
            else:
                clean.append(r)
        college["resources"] = clean

    # Drop colleges that ended up with zero resources
    colleges_before = len(data)
    data = [c for c in data if c.get("resources")]
    colleges_after = len(data)

    total_after = sum(len(c.get("resources", [])) for c in data)

    print(f"\n  {os.path.basename(path)}:")
    print(f"    Colleges: {colleges_before} -> {colleges_after}")
    print(f"    Resources: {total_before} -> {total_after}  (removed {total_before - total_after})")
    if removed:
        print(f"    Removed resources:")
        for cname, rname, reason in removed:
            print(f"      [{cname[:35]}] {rname[:60]} ({reason})")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"    Written: {path}")


if __name__ == "__main__":
    base = os.path.dirname(__file__)
    print("=== Cleaning seed data ===")
    clean_file(os.path.join(base, "scraped_colleges_data.json"))
    clean_file(os.path.join(base, "starter_colleges_data.json"))
    print("\nDone.")
