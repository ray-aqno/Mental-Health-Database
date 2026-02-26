import json

manual_schools = [
    {
        "name": "Kent State University",
        "location": "Kent, Ohio",
        "latitude": 41.1487,
        "longitude": -81.3442,
        "website": "https://www.kent.edu",
        "resources": [
            {
                "service_name": "Counseling and Psychological Services (CPS)",
                "description": "CPS provides confidential counseling services to help students with personal, social, and academic concerns. Services include individual counseling, group therapy, psychiatric services, and crisis intervention.",
                "contact_email": "cps@kent.edu",
                "contact_phone": "330-672-2487",
                "contact_website": "https://www.kent.edu/cps",
                "department": "Student Affairs",
                "office_hours": "Monday-Friday, 8:00 AM - 5:00 PM",
                "location": "DeWeese Health Center, 2nd Floor",
                "freshman_notes": "New students can schedule an initial consultation online. Walk-in hours available for urgent concerns. All services are free and confidential."
            },
            {
                "service_name": "24/7 Crisis Support",
                "description": "After-hours crisis support available through Partnership Crisis Hotline",
                "contact_email": "",
                "contact_phone": "330-678-4357",
                "contact_website": "https://www.kent.edu/cps/crisis-resources",
                "department": "Student Affairs",
                "office_hours": "24/7",
                "location": "Phone support",
                "freshman_notes": "Available anytime outside of regular business hours for students in crisis."
            }
        ],
        "scraped_at": "2026-02-10T14:30:00.000000"
    },
    {
        "name": "Cleveland State University",
        "location": "Cleveland, Ohio",
        "latitude": 41.5017,
        "longitude": -81.6753,
        "website": "https://www.csuohio.edu",
        "resources": [
            {
                "service_name": "Counseling Services",
                "description": "CSU Counseling Services offers individual counseling, group therapy, workshops, and psychiatric consultations. Services address anxiety, depression, relationships, academic stress, and life transitions.",
                "contact_email": "counseling@csuohio.edu",
                "contact_phone": "216-687-2277",
                "contact_website": "https://www.csuohio.edu/counseling",
                "department": "Student Life",
                "office_hours": "Monday-Friday, 8:30 AM - 5:00 PM",
                "location": "Main Classroom Building, Room 256",
                "freshman_notes": "First-year students can schedule initial appointments online or by phone. Same-day crisis consultations available during business hours."
            },
            {
                "service_name": "Student Health Services - Mental Health",
                "description": "Provides psychiatric evaluations, medication management, and referrals for mental health concerns.",
                "contact_email": "health.services@csuohio.edu",
                "contact_phone": "216-687-2450",
                "contact_website": "https://www.csuohio.edu/health-services",
                "department": "Student Life",
                "office_hours": "Monday-Friday, 8:30 AM - 5:00 PM",
                "location": "Main Classroom Building, Room 110",
                "freshman_notes": "Medical services complement counseling support. Insurance accepted."
            }
        ],
        "scraped_at": "2026-02-10T14:30:00.000000"
    },
    {
        "name": "Youngstown State University",
        "location": "Youngstown, Ohio",
        "latitude": 41.1098,
        "longitude": -80.6495,
        "website": "https://www.ysu.edu",
        "resources": [
            {
                "service_name": "Counseling Services",
                "description": "YSU Counseling Services provides individual counseling, crisis intervention, group therapy, outreach programming, and consultation services. Specializes in helping students with stress management, anxiety, depression, and adjustment issues.",
                "contact_email": "counseling@ysu.edu",
                "contact_phone": "330-941-3737",
                "contact_website": "https://ysu.edu/counseling",
                "department": "Student Experience",
                "office_hours": "Monday-Friday, 8:00 AM - 5:00 PM",
                "location": "Cushwa Hall, Room 1059",
                "freshman_notes": "Walk-in appointments welcome for new students. Online self-help resources available 24/7. All undergraduate students receive 10 free counseling sessions per academic year."
            },
            {
                "service_name": "Crisis Text Line",
                "description": "24/7 text-based crisis support for YSU students",
                "contact_email": "",
                "contact_phone": "Text HOME to 741741",
                "contact_website": "https://ysu.edu/counseling/crisis",
                "department": "Student Experience",
                "office_hours": "24/7",
                "location": "Text-based support",
                "freshman_notes": "Free, confidential crisis support via text message, available anytime."
            }
        ],
        "scraped_at": "2026-02-10T14:30:00.000000"
    },
    {
        "name": "Cincinnati State Technical and Community College",
        "location": "Cincinnati, Ohio",
        "latitude": 39.1118,
        "longitude": -84.5364,
        "website": "https://www.cincinnatistate.edu",
        "resources": [
            {
                "service_name": "Counseling Services",
                "description": "Cincinnati State offers free, confidential counseling for students dealing with stress, anxiety, depression, relationship issues, and academic concerns. Short-term individual counseling and referrals to community resources available.",
                "contact_email": "counseling@cincinnatistate.edu",
                "contact_phone": "513-569-1666",
                "contact_website": "https://www.cincinnatistate.edu/counseling",
                "department": "Student Services",
                "office_hours": "Monday-Thursday, 8:00 AM - 6:00 PM; Friday, 8:00 AM - 4:30 PM",
                "location": "Main Campus, Student Success Center",
                "freshman_notes": "New students should call or visit the Student Success Center to schedule an intake appointment. Crisis walk-ins accepted during business hours."
            },
            {
                "service_name": "Mental Health Resources and Referrals",
                "description": "Connections to community mental health providers and crisis services for ongoing care needs.",
                "contact_email": "studentservices@cincinnatistate.edu",
                "contact_phone": "513-569-1555",
                "contact_website": "https://www.cincinnatistate.edu/student-resources",
                "department": "Student Services",
                "office_hours": "Monday-Friday, 8:00 AM - 5:00 PM",
                "location": "Student Services Office",
                "freshman_notes": "Staff can help connect students to off-campus resources for longer-term care."
            }
        ],
        "scraped_at": "2026-02-10T14:30:00.000000"
    },
    {
        "name": "Denison University",
        "location": "Granville, Ohio",
        "latitude": 40.0746,
        "longitude": -82.5220,
        "website": "https://denison.edu",
        "resources": [
            {
                "service_name": "Counseling and Wellness Services",
                "description": "Denison's Whisler Center provides individual counseling, group therapy, psychiatric services, and wellness programming. Services address mental health concerns including anxiety, depression, eating disorders, substance use, and identity development.",
                "contact_email": "whisler@denison.edu",
                "contact_phone": "740-587-6647",
                "contact_website": "https://denison.edu/campus/wellness",
                "department": "Wellness",
                "office_hours": "Monday-Friday, 8:30 AM - 5:00 PM",
                "location": "Whisler Center for Student Wellness",
                "freshman_notes": "First-year students are encouraged to attend wellness orientation sessions. Walk-in consultations available daily. Unlimited counseling sessions available to all students."
            },
            {
                "service_name": "24/7 Crisis Support - TimelyCare",
                "description": "Free virtual mental health support available 24/7 through TimelyCare app for all Denison students.",
                "contact_email": "",
                "contact_phone": "Available through TimelyCare app",
                "contact_website": "https://denison.edu/campus/wellness/telehealth",
                "department": "Wellness",
                "office_hours": "24/7",
                "location": "Virtual/Telehealth",
                "freshman_notes": "Download the TimelyCare app for immediate access to counselors anytime, anywhere."
            }
        ],
        "scraped_at": "2026-02-10T14:30:00.000000"
    },
    {
        "name": "Kenyon College",
        "location": "Gambier, Ohio",
        "latitude": 40.3756,
        "longitude": -82.3979,
        "website": "https://www.kenyon.edu",
        "resources": [
            {
                "service_name": "Counseling Center",
                "description": "The Kenyon Counseling Center provides confidential individual therapy, group counseling, crisis intervention, and psychiatric services. Staff includes licensed psychologists and counselors who specialize in college student mental health.",
                "contact_email": "counselingcenter@kenyon.edu",
                "contact_phone": "740-427-5668",
                "contact_website": "https://www.kenyon.edu/student-life/health-wellness/counseling",
                "department": "Health and Wellness",
                "office_hours": "Monday-Friday, 8:30 AM - 5:00 PM",
                "location": "Cox Health and Counseling Center",
                "freshman_notes": "New students can schedule appointments online through the patient portal. Same-day urgent care appointments available. All services are free and confidential."
            },
            {
                "service_name": "After-Hours Crisis Support",
                "description": "24/7 crisis counseling available through on-call counselor and partnership with Pathways of Central Ohio.",
                "contact_email": "",
                "contact_phone": "740-427-5000 (Campus Safety - ask for on-call counselor)",
                "contact_website": "https://www.kenyon.edu/student-life/health-wellness/crisis-resources",
                "department": "Health and Wellness",
                "office_hours": "24/7",
                "location": "Phone support through Campus Safety",
                "freshman_notes": "In a mental health emergency after hours, call Campus Safety and they will connect you with the on-call counselor immediately."
            },
            {
                "service_name": "Wellness Programming",
                "description": "Workshops, support groups, and wellness activities focused on stress management, mindfulness, sleep, and healthy relationships.",
                "contact_email": "wellness@kenyon.edu",
                "contact_phone": "740-427-5671",
                "contact_website": "https://www.kenyon.edu/student-life/health-wellness/wellness-programs",
                "department": "Health and Wellness",
                "office_hours": "Various program times",
                "location": "Cox Health and Counseling Center",
                "freshman_notes": "First-year students are encouraged to attend wellness workshops during orientation and throughout the year."
            }
        ],
        "scraped_at": "2026-02-10T14:30:00.000000"
    }
]

# Save to file
with open('manual_ohio_schools.json', 'w', encoding='utf-8') as f:
    json.dump(manual_schools, f, indent=2, ensure_ascii=False)

print(f"✅ Created manual data for {len(manual_schools)} schools")
for school in manual_schools:
    print(f"   • {school['name']} - {len(school['resources'])} resource(s)")
