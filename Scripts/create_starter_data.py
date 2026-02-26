"""
Create starter college data for testing
Run this to generate sample data before web scraping
"""

import json

STARTER_DATA = [
    {
        "name": "University of Cincinnati",
        "location": "Cincinnati, Ohio",
        "latitude": 39.1329,
        "longitude": -84.5150,
        "website": "https://www.uc.edu",
        "resources": [
            {
                "service_name": "Counseling and Psychological Services (CAPS)",
                "description": "CAPS provides free, confidential counseling services to all UC students. Services include individual counseling, group therapy, crisis intervention, and psychiatric consultation.",
                "contact_email": "caps@uc.edu",
                "contact_phone": "(513) 556-0648",
                "contact_website": "https://www.uc.edu/campus-life/caps.html",
                "department": "Division of Student Affairs",
                "office_hours": "Monday-Friday, 8:00 AM - 5:00 PM",
                "location": "Clifton Court Hall, 5th Floor, Suite 530",
                "freshman_notes": "Walk-in hours available Monday-Thursday 1-4 PM for urgent concerns. New students can schedule an intake appointment by calling or using the online portal."
            },
            {
                "service_name": "Student Wellness Center",
                "description": "Comprehensive wellness services including mental health support, stress management workshops, and mindfulness programs.",
                "contact_email": "wellness@uc.edu",
                "contact_phone": "(513) 556-0000",
                "contact_website": "https://www.uc.edu/wellness",
                "department": "Student Health Services",
                "office_hours": "Monday-Friday, 8:00 AM - 6:00 PM",
                "location": "University Hall, Room 210",
                "freshman_notes": "Freshmen can attend free wellness workshops throughout the year. Check website for schedule."
            }
        ]
    },
    {
        "name": "The Ohio State University",
        "location": "Columbus, Ohio",
        "latitude": 40.0067,
        "longitude": -83.0305,
        "website": "https://www.osu.edu",
        "resources": [
            {
                "service_name": "Counseling and Consultation Service (CCS)",
                "description": "Free counseling services for Ohio State students including individual therapy, couples counseling, group therapy, and crisis services available 24/7.",
                "contact_email": "ccs@osu.edu",
                "contact_phone": "(614) 292-5766",
                "contact_website": "https://ccs.osu.edu",
                "department": "Student Life",
                "office_hours": "Monday-Friday, 8:00 AM - 5:00 PM; 24/7 Crisis Line",
                "location": "Younkin Success Center, 4th Floor",
                "freshman_notes": "First-year students can schedule Let's Talk drop-in consultations at various locations across campus. No appointment needed."
            },
            {
                "service_name": "Student Wellness Center",
                "description": "Holistic wellness programs including mental health resources, substance abuse prevention, and peer education programs.",
                "contact_email": "swc@osu.edu",
                "contact_phone": "(614) 292-4527",
                "contact_website": "https://swc.osu.edu",
                "department": "Student Life",
                "office_hours": "Monday-Friday, 8:00 AM - 6:00 PM",
                "location": "1739 N High St, Columbus, OH 43210",
                "freshman_notes": "New students receive wellness orientation during Welcome Week. Peer educators available for questions."
            }
        ]
    },
    {
        "name": "Miami University",
        "location": "Oxford, Ohio",
        "latitude": 39.5097,
        "longitude": -84.7330,
        "website": "https://www.miamioh.edu",
        "resources": [
            {
                "service_name": "Student Counseling Service",
                "description": "Professional counseling for personal, academic, and career concerns. Services include individual counseling, group therapy, and crisis intervention.",
                "contact_email": "scs@miamioh.edu",
                "contact_phone": "(513) 529-4634",
                "contact_website": "https://miamioh.edu/student-life/student-counseling-service",
                "department": "Division of Student Life",
                "office_hours": "Monday-Friday, 8:00 AM - 5:00 PM",
                "location": "35 Peabody Hall, Oxford, OH 45056",
                "freshman_notes": "First-year students can access TimelyCare for 24/7 virtual counseling. Download the app with your Miami ID."
            }
        ]
    },
    {
        "name": "Xavier University",
        "location": "Cincinnati, Ohio",
        "latitude": 39.1484,
        "longitude": -84.4745,
        "website": "https://www.xavier.edu",
        "resources": [
            {
                "service_name": "Counseling & Psychological Services",
                "description": "Free, confidential counseling for Xavier students. Services include individual therapy, group counseling, and psychiatric services.",
                "contact_email": "counselingservices@xavier.edu",
                "contact_phone": "(513) 745-3531",
                "contact_website": "https://www.xavier.edu/counseling",
                "department": "Division of Student Affairs",
                "office_hours": "Monday-Friday, 8:30 AM - 5:00 PM",
                "location": "Conaton Learning Commons, Room 311",
                "freshman_notes": "Drop-in consultations available for urgent concerns. First appointment includes assessment and goal-setting for freshmen."
            }
        ]
    },
    {
        "name": "University of Dayton",
        "location": "Dayton, Ohio",
        "latitude": 39.7400,
        "longitude": -84.1800,
        "website": "https://www.udayton.edu",
        "resources": [
            {
                "service_name": "Counseling Center",
                "description": "Comprehensive mental health services including individual counseling, group therapy, workshops, and outreach programs.",
                "contact_email": "counselingcenter@udayton.edu",
                "contact_phone": "(937) 229-3141",
                "contact_website": "https://www.udayton.edu/studev/counselingcenter",
                "department": "Division of Student Development",
                "office_hours": "Monday-Friday, 8:30 AM - 5:00 PM",
                "location": "St. Joseph Hall, Ground Floor",
                "freshman_notes": "Freshmen can attend stress management workshops designed specifically for first-year students. Register online."
            }
        ]
    },
    {
        "name": "Ohio University",
        "location": "Athens, Ohio",
        "latitude": 39.3292,
        "longitude": -82.1013,
        "website": "https://www.ohio.edu",
        "resources": [
            {
                "service_name": "Counseling & Psychological Services",
                "description": "Professional counseling services including individual therapy, group counseling, crisis intervention, and consultation.",
                "contact_email": "counseling@ohio.edu",
                "contact_phone": "(740) 593-1616",
                "contact_website": "https://www.ohio.edu/student-affairs/counseling",
                "department": "Division of Student Affairs",
                "office_hours": "Monday-Friday, 8:00 AM - 5:00 PM; After-hours crisis line available",
                "location": "Hudson Health Center, 2nd Floor",
                "freshman_notes": "Let's Talk drop-in hours available in residence halls for first-year students. Check schedule on website."
            }
        ]
    },
    {
        "name": "Northern Kentucky University",
        "location": "Highland Heights, Kentucky",
        "latitude": 39.0325,
        "longitude": -84.4661,
        "website": "https://www.nku.edu",
        "resources": [
            {
                "service_name": "Counseling & Wellness Services",
                "description": "Mental health counseling, crisis intervention, and wellness programs for NKU students.",
                "contact_email": "wellness@nku.edu",
                "contact_phone": "(859) 572-5650",
                "contact_website": "https://inside.nku.edu/healthwellness",
                "department": "Division of Student Affairs",
                "office_hours": "Monday-Friday, 8:00 AM - 4:30 PM",
                "location": "University Center, Suite 300",
                "freshman_notes": "Freshmen can schedule same-day appointments for urgent concerns. Call in the morning for availability."
            }
        ]
    },
    {
        "name": "Wright State University",
        "location": "Dayton, Ohio",
        "latitude": 39.7806,
        "longitude": -84.0533,
        "website": "https://www.wright.edu",
        "resources": [
            {
                "service_name": "Student Counseling and Wellness Services",
                "description": "Free counseling and wellness services for Wright State students including therapy, psychiatric consultation, and wellness coaching.",
                "contact_email": "counseling@wright.edu",
                "contact_phone": "(937) 775-3407",
                "contact_website": "https://www.wright.edu/student-affairs/student-counseling-and-wellness",
                "department": "Student Affairs",
                "office_hours": "Monday-Friday, 8:30 AM - 5:00 PM",
                "location": "Frederick White Health Center",
                "freshman_notes": "New student orientation includes wellness fair. First-year students can access telehealth counseling through TimelyCare app."
            }
        ]
    },
    {
        "name": "Purdue University",
        "location": "West Lafayette, Indiana",
        "latitude": 40.4237,
        "longitude": -86.9212,
        "website": "https://www.purdue.edu",
        "resources": [
            {
                "service_name": "Counseling and Psychological Services (CAPS)",
                "description": "Comprehensive mental health services including individual counseling, group therapy, psychiatric services, and crisis intervention available 24/7.",
                "contact_email": "caps@purdue.edu",
                "contact_phone": "(765) 494-6995",
                "contact_website": "https://www.purdue.edu/caps",
                "department": "Division of Student Life",
                "office_hours": "Monday-Friday, 8:00 AM - 5:00 PM; 24/7 Crisis Line: (765) 494-6995",
                "location": "Young Hall, 601 Stadium Mall Drive",
                "freshman_notes": "BoilerConnect online screening available for all students. First-year students can attend anxiety management workshops specifically designed for freshmen."
            }
        ]
    },
    {
        "name": "Case Western Reserve University",
        "location": "Cleveland, Ohio",
        "latitude": 41.5045,
        "longitude": -81.6081,
        "website": "https://www.case.edu",
        "resources": [
            {
                "service_name": "University Counseling Services",
                "description": "Professional mental health counseling including individual therapy, group counseling, couples therapy, and psychiatric services.",
                "contact_email": "counseling@case.edu",
                "contact_phone": "(216) 368-5872",
                "contact_website": "https://case.edu/studentlife/healthcounseling/counseling-services",
                "department": "Division of Student Affairs",
                "office_hours": "Monday-Friday, 8:30 AM - 5:00 PM; 24/7 Crisis Line available",
                "location": "Adelbert Hall, 2nd Floor",
                "freshman_notes": "Freshmen can access Let's Talk informal consultations in residence halls. No appointment needed. Also available via telehealth."
            }
        ]
    }
]


if __name__ == "__main__":
    output_file = "starter_colleges_data.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(STARTER_DATA, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created {output_file} with {len(STARTER_DATA)} colleges")
    print(f"   Total resources: {sum(len(c['resources']) for c in STARTER_DATA)}")
    print("\nTo import this data:")
    print("   1. Start your ASP.NET backend (dotnet run)")
    print("   2. Run: python data_importer.py")
