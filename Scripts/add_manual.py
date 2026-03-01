import json

# Manual entries for schools that don't scrape well
manual_entries = [
    {
        "name": "Northern Kentucky University",
        "state": "kentucky",
        "location": "Highland Heights, Kentucky",
        "latitude": 39.0325,
        "longitude": -84.4661,
        "website": "https://www.nku.edu",
        "resources": [
            {
                "service_name": "Counseling and Student Development",
                "description": "NKU offers counseling services including individual therapy, group counseling, crisis intervention, and psychiatric consultations. Services address anxiety, depression, academic stress, and personal concerns.",
                "contact_email": "counseling@nku.edu",
                "contact_phone": "859-572-5650",
                "contact_website": "https://www.nku.edu/studentaffairs/counseling.html",
                "department": "Student Affairs",
                "office_hours": "Monday-Friday, 8:00 AM - 5:00 PM",
                "location": "University Center 440",
                "freshman_notes": "First-year students can access counseling services immediately. Walk-in hours available for urgent concerns."
            },
            {
                "service_name": "24/7 Crisis Support",
                "description": "After-hours crisis support available through the NKU Police Department",
                "contact_email": "",
                "contact_phone": "859-572-7777",
                "contact_website": "https://www.nku.edu/counseling/crisis",
                "department": "Student Affairs",
                "office_hours": "24/7",
                "location": "Emergency: Call 911 or NKU Police",
                "freshman_notes": "In case of mental health emergency after hours, call NKU Police."
            }
        ],
        "scraped_at": "2026-03-01T00:00:00.000000"
    },
    {
        "name": "Indiana University Bloomington",
        "state": "indiana",
        "location": "Bloomington, Indiana",
        "latitude": 39.1682,
        "longitude": -86.523,
        "website": "https://www.iu.edu",
        "resources": [
            {
                "service_name": "Counseling and Psychological Services (CAPS)",
                "description": "IU Bloomington offers comprehensive mental health services including individual counseling, group therapy, psychiatric services, crisis intervention, and outreach programs. Specializes in helping students with anxiety, depression, relationships, and academic stress.",
                "contact_email": "caps@iu.edu",
                "contact_phone": "812-855-5711",
                "contact_website": "https://studentaffairs.iu.edu/counseling/",
                "department": "Student Affairs",
                "office_hours": "Monday-Friday, 8:00 AM - 5:00 PM",
                "location": "Student Health Center, 3rd Floor",
                "freshman_notes": "All students receive free counseling sessions. Initial appointment available within 1-2 weeks. Crisis services available same-day."
            },
            {
                "service_name": "24/7 Crisis Line",
                "description": "24/7 crisis support for students in distress",
                "contact_email": "",
                "contact_phone": "812-855-5711",
                "contact_website": "https://studentaffairs.iu.edu/counseling/crisis.html",
                "department": "Student Affairs",
                "office_hours": "24/7",
                "location": "Phone support",
                "freshman_notes": "Press 1 after calling for immediate crisis support."
            }
        ],
        "scraped_at": "2026-03-01T00:00:00.000000"
    },
    {
        "name": "Michigan State University",
        "state": "michigan",
        "location": "East Lansing, Michigan",
        "latitude": 42.7018,
        "longitude": -84.4822,
        "website": "https://msu.edu",
        "resources": [
            {
                "service_name": "Counseling and Psychiatric Services (CAPS)",
                "description": "MSU Counseling Center provides individual counseling, group therapy, psychiatric services, crisis intervention, and outreach. Services address mental health concerns including anxiety, depression, stress, and relationship issues.",
                "contact_email": "caps@msu.edu",
                "contact_phone": "517-355-8270",
                "contact_website": "https://counseling.msu.edu/",
                "department": "Student Health and Wellness",
                "office_hours": "Monday-Friday, 8:00 AM - 5:00 PM",
                "location": "Olin Health Center",
                "freshman_notes": "First-year students priority scheduling available. Unlimited free sessions for enrolled students."
            },
            {
                "service_name": "After-Hours Crisis Support",
                "description": "24/7 crisis support through ProtoCall",
                "contact_email": "",
                "contact_phone": "517-355-8270",
                "contact_website": "https://counseling.msu.edu/crisis/",
                "department": "Student Health and Wellness",
                "office_hours": "24/7",
                "location": "Phone support",
                "freshman_notes": "Call the main number and select option 1 for after-hours crisis support."
            }
        ],
        "scraped_at": "2026-03-01T00:00:00.000000"
    },
    {
        "name": "University of Wisconsin-Madison",
        "state": "wisconsin",
        "location": "Madison, Wisconsin",
        "latitude": 43.0766,
        "longitude": -89.4125,
        "website": "https://wisc.edu",
        "resources": [
            {
                "service_name": "University Health and Counseling Services",
                "description": "UW-Madison offers comprehensive counseling services including individual therapy, group counseling, psychiatric services, and crisis intervention. Services address anxiety, depression, academic stress, and personal concerns.",
                "contact_email": "uhs@wisc.edu",
                "contact_phone": "608-265-5600",
                "contact_website": "https://www.uhs.wisc.edu/counseling/",
                "department": "University Health Services",
                "office_hours": "Monday-Friday, 8:30 AM - 5:00 PM",
                "location": "333 East Campus Mall",
                "freshman_notes": "All students can access counseling services. Same-day appointments available for urgent concerns."
            },
            {
                "service_name": "24/7 Crisis Support",
                "description": "After-hours crisis counseling available 24/7",
                "contact_email": "",
                "contact_phone": "608-265-5600",
                "contact_website": "https://www.uhs.wisc.edu/counseling/crisis/",
                "department": "University Health Services",
                "office_hours": "24/7",
                "location": "Phone support",
                "freshman_notes": "Press option 8 for after-hours crisis support."
            }
        ],
        "scraped_at": "2026-03-01T00:00:00.000000"
    },
    {
        "name": "University of Pittsburgh",
        "state": "pennsylvania",
        "location": "Pittsburgh, Pennsylvania",
        "latitude": 40.4443,
        "longitude": -79.9608,
        "website": "https://pitt.edu",
        "resources": [
            {
                "service_name": "University Counseling Center",
                "description": "Pitt offers comprehensive mental health services including individual counseling, group therapy, psychiatric services, and crisis intervention. Services address anxiety, depression, relationships, and academic stress.",
                "contact_email": "counsel@pitt.edu",
                "contact_phone": "412-648-7930",
                "contact_website": "https://www.counsel.pitt.edu/",
                "department": "Student Affairs",
                "office_hours": "Monday-Friday, 8:30 AM - 5:00 PM",
                "location": "3340 O'Hara Student Center",
                "freshman_notes": "Free counseling services for all enrolled students. Initial appointment within 1 week."
            },
            {
                "service_name": "24/7 Crisis Services",
                "description": "After-hours crisis support available 24/7",
                "contact_email": "",
                "contact_phone": "412-648-7930",
                "contact_website": "https://www.counsel.pitt.edu/crisis",
                "department": "Student Affairs",
                "office_hours": "24/7",
                "location": "Phone support",
                "freshman_notes": "Press 2 for crisis services when calling."
            }
        ],
        "scraped_at": "2026-03-01T00:00:00.000000"
    }
]

# Load existing manual file
with open('/mnt/c/Users/raygo/source/repos/Mental_Health_Database/Scripts/manual_ohio_schools.json') as f:
    manual_data = json.load(f)

# Add new entries (avoid duplicates)
existing_names = {c['name'] for c in manual_data}
for entry in manual_entries:
    if entry['name'] not in existing_names:
        manual_data.append(entry)

# Save
with open('/mnt/c/Users/raygo/source/repos/Mental_Health_Database/Scripts/manual_ohio_schools.json', 'w') as f:
    json.dump(manual_data, f, indent=2)

print(f"Added {len(manual_entries)} manual entries")
print(f"Total manual entries: {len(manual_data)}")
