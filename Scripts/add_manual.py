"""One-time: add University of Cincinnati with manual CAPS data."""
import json, os

UC_ENTRY = {
    "name": "University of Cincinnati",
    "location": "Cincinnati, Ohio",
    "latitude": 39.1329,
    "longitude": -84.515,
    "website": "https://www.uc.edu",
    "resources": [
        {
            "service_name": "Counseling and Psychological Services (CAPS)",
            "description": "CAPS provides short-term individual counseling, group therapy, crisis intervention, psychiatric services, and referrals for University of Cincinnati students. CAPS takes a collaborative, strengths-based approach to help students identify tools, resources, and strategies to meet their mental health goals.",
            "contact_email": "caps@uc.edu",
            "contact_phone": "(513) 556-0648",
            "contact_website": "https://www.uc.edu/campus-life/caps.html",
            "department": "Student Affairs",
            "office_hours": "Monday-Friday 8:00 AM - 5:00 PM",
            "location": "Steger Student Life Center, Suite 325, University of Cincinnati",
            "freshman_notes": "All enrolled UC students are eligible for CAPS services at no additional cost. First-year students can access same-day crisis consultations and scheduled appointments."
        },
        {
            "service_name": "CAPS Crisis Support",
            "description": "After-hours crisis support is available 24/7 for UC students experiencing a mental health emergency. Students can call CAPS and press 2 to speak with a crisis counselor anytime outside regular business hours.",
            "contact_email": "",
            "contact_phone": "(513) 556-0648",
            "contact_website": "https://www.uc.edu/campus-life/caps.html",
            "department": "Student Affairs",
            "office_hours": "24/7",
            "location": "",
            "freshman_notes": ""
        },
        {
            "service_name": "Bearcat Wellness",
            "description": "UC Wellness provides health promotion, peer education, and prevention programming focused on student mental health, stress management, substance use, and overall well-being.",
            "contact_email": "",
            "contact_phone": "",
            "contact_website": "https://www.uc.edu/campus-life/wellness.html",
            "department": "Student Affairs",
            "office_hours": "",
            "location": "Steger Student Life Center, University of Cincinnati",
            "freshman_notes": ""
        }
    ],
    "scraped_at": "2026-03-03T00:00:00.000000"
}

base = os.path.dirname(__file__)
for fname in ["starter_colleges_data.json", "scraped_colleges_data.json"]:
    path = os.path.join(base, fname)
    data = json.load(open(path, "r", encoding="utf-8"))

    # Remove any existing UC entry (thin scraped version)
    data = [c for c in data if c["name"] != "University of Cincinnati"]

    # Add the manual entry
    data.append(UC_ENTRY)

    # Sort alphabetically by name for consistency
    data.sort(key=lambda c: c["name"])

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    uc = [c for c in data if c["name"] == "University of Cincinnati"][0]
    print(f"{fname}: {len(data)} colleges, UC has {len(uc['resources'])} resources")

print("Done.")
