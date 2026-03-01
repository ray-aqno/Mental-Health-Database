import json

with open('/mnt/c/Users/raygo/source/repos/Mental_Health_Database/Scripts/college_targets.json') as f:
    data = json.load(f)

# Fix URLs for failed schools and add missing Big Ten
updates = [
    # KY fixes
    {
        "name": "Northern Kentucky University",
        "state": "kentucky",
        "location": "Highland Heights, Kentucky",
        "latitude": 39.0325,
        "longitude": -84.4661,
        "website": "https://www.nku.edu",
        "mental_health_urls": [
            "https://www.nku.edu/studentaffairs/healthwellness.html",
            "https://nku.medicatconnect.com/"
        ],
        "source": "pending"
    },
    {
        "name": "Eastern Kentucky University",
        "state": "kentucky",
        "location": "Richmond, Kentucky",
        "latitude": 37.7486,
        "longitude": -84.3052,
        "website": "https://www.eku.edu",
        "mental_health_urls": [
            "https://www.eku.edu/counselingcenter/",
            "https://www.eku.edu/student-services/counseling/"
        ],
        "source": "pending"
    },
    # IN fixes
    {
        "name": "Indiana University Bloomington",
        "state": "indiana",
        "location": "Bloomington, Indiana",
        "latitude": 39.1682,
        "longitude": -86.523,
        "website": "https://www.iu.edu",
        "mental_health_urls": [
            "https://studentaffairs.iu.edu/counseling/",
            "https://healthcenter.iu.edu/counseling/index.html"
        ],
        "source": "pending"
    },
    {
        "name": "Ball State University",
        "state": "indiana",
        "location": "Muncie, Indiana",
        "latitude": 40.2044,
        "longitude": -85.4113,
        "website": "https://www.bsu.edu",
        "mental_health_urls": [
            "https://www.bsu.edu/counselingcenter",
            "https://www.bsu.edu/student-services/counseling"
        ],
        "source": "pending"
    },
    {
        "name": "University of Notre Dame",
        "state": "indiana",
        "location": "Notre Dame, Indiana",
        "latitude": 41.7055,
        "longitude": -86.2353,
        "website": "https://www.nd.edu",
        "mental_health_urls": [
            "https://counselingcenter.nd.edu/",
            "https://www.nd.edu/student-services/"
        ],
        "source": "pending"
    },
    # IL fix
    {
        "name": "Southern Illinois University Carbondale",
        "state": "illinois",
        "location": "Carbondale, Illinois",
        "latitude": 37.709,
        "longitude": -89.2172,
        "website": "https://siu.edu",
        "mental_health_urls": [
            "https://counseling.siu.edu/",
            "https://wellness.siu.edu/"
        ],
        "source": "pending"
    },
    # MI fixes
    {
        "name": "Michigan State University",
        "state": "michigan",
        "location": "East Lansing, Michigan",
        "latitude": 42.7018,
        "longitude": -84.4822,
        "website": "https://msu.edu",
        "mental_health_urls": [
            "https://counseling.msu.edu/",
            "https://msu.edu/counseling/"
        ],
        "source": "pending"
    },
    {
        "name": "Wayne State University",
        "state": "michigan",
        "location": "Detroit, Michigan",
        "latitude": 42.3591,
        "longitude": -83.0688,
        "website": "https://wayne.edu",
        "mental_health_urls": [
            "https://wayne.edu/counseling/",
            "https://wayne.edu/health/"
        ],
        "source": "pending"
    },
    {
        "name": "Central Michigan University",
        "state": "michigan",
        "location": "Mount Pleasant, Michigan",
        "latitude": 43.5887,
        "longitude": -84.775,
        "website": "https://cmich.edu",
        "mental_health_urls": [
            "https://www.cmich.edu/pages.aspx?cn=3440",
            "https://www.cmich.edu/student-affairs/counseling-center"
        ],
        "source": "pending"
    },
    {
        "name": "Western Michigan University",
        "state": "michigan",
        "location": "Kalamazoo, Michigan",
        "latitude": 42.2832,
        "longitude": -85.5796,
        "website": "https://wmich.edu",
        "mental_health_urls": [
            "https://wmich.edu/counseling/",
            "https://wmich.edu/health-services/counseling"
        ],
        "source": "pending"
    },
    # PA fixes
    {
        "name": "University of Pittsburgh",
        "state": "pennsylvania",
        "location": "Pittsburgh, Pennsylvania",
        "latitude": 40.4443,
        "longitude": -79.9608,
        "website": "https://pitt.edu",
        "mental_health_urls": [
            "https://www.counsel.pitt.edu/",
            "https://www.pitt.edu/counseling-services"
        ],
        "source": "pending"
    },
    {
        "name": "University of Pennsylvania",
        "state": "pennsylvania",
        "location": "Philadelphia, Pennsylvania",
        "latitude": 39.9526,
        "longitude": -75.1652,
        "website": "https://upenn.edu",
        "mental_health_urls": [
            "https://www.wellness.upenn.edu/",
            "https://www.counseling.studyabroad.pitt.edu/"
        ],
        "source": "pending"
    },
    # NY fixes
    {
        "name": "SUNY Buffalo",
        "state": "new york",
        "location": "Buffalo, New York",
        "latitude": 43.0008,
        "longitude": -78.789,
        "website": "https://buffalo.edu",
        "mental_health_urls": [
            "https://www.buffalo.edu/counseling.html",
            "https://student-affairs.buffalo.edu/counseling/"
        ],
        "source": "pending"
    },
    {
        "name": "Stony Brook University",
        "state": "new york",
        "location": "Stony Brook, New York",
        "latitude": 40.9176,
        "longitude": -73.1262,
        "website": "https://stonybrook.edu",
        "mental_health_urls": [
            "https://www.stonybrook.edu/counseling/",
            "https://stonybrook.edu/sb/counseling/"
        ],
        "source": "pending"
    },
    {
        "name": "University at Albany",
        "state": "new york",
        "location": "Albany, New York",
        "latitude": 42.6868,
        "longitude": -73.8291,
        "website": "https://albany.edu",
        "mental_health_urls": [
            "https://www.albany.edu/counseling/",
            "https://www.albany.edu/health-counseling/"
        ],
        "source": "pending"
    },
    {
        "name": "Syracuse University",
        "state": "new york",
        "location": "Syracuse, New York",
        "latitude": 43.0392,
        "longitude": -76.1351,
        "website": "https://syracuse.edu",
        "mental_health_urls": [
            "https://syracuse.edu/counseling/",
            "https://studentaffairs.syracuse.edu/counseling/"
        ],
        "source": "pending"
    },
    # Missing Big Ten
    {
        "name": "University of Wisconsin-Madison",
        "state": "wisconsin",
        "location": "Madison, Wisconsin",
        "latitude": 43.0766,
        "longitude": -89.4125,
        "website": "https://wisc.edu",
        "mental_health_urls": [
            "https://www.uhs.wisc.edu/counseling/",
            "https://www.wisc.edu/students/counseling/"
        ],
        "source": "pending"
    },
    {
        "name": "University of Minnesota",
        "state": "minnesota",
        "location": "Minneapolis, Minnesota",
        "latitude": 44.9740,
        "longitude": -93.2277,
        "website": "https://umn.edu",
        "mental_health_urls": [
            "https://counseling.umn.edu/",
            "https://www.mentalhealth.umn.edu/"
        ],
        "source": "pending"
    },
    {
        "name": "University of Iowa",
        "state": "iowa",
        "location": "Iowa City, Iowa",
        "latitude": 41.6611,
        "longitude": -91.5302,
        "website": "https://uiowa.edu",
        "mental_health_urls": [
            "https://counseling.uiowa.edu/",
            "https://studenthealth.iowa.uiowa.edu/counseling"
        ],
        "source": "pending"
    },
    {
        "name": "University of Nebraska-Lincoln",
        "state": "nebraska",
        "location": "Lincoln, Nebraska",
        "latitude": 40.8202,
        "longitude": -96.7005,
        "website": "https://unl.edu",
        "mental_health_urls": [
            "https://www.unl.edu/counseling/",
            "https://www.unl.edu/student-life/counseling"
        ],
        "source": "pending"
    },
    {
        "name": "University of Maryland",
        "state": "maryland",
        "location": "College Park, Maryland",
        "latitude": 38.9869,
        "longitude": -76.9426,
        "website": "https://umd.edu",
        "mental_health_urls": [
            "https://www.counseling.umd.edu/",
            "https://www.umd.edu/counseling-services"
        ],
        "source": "pending"
    },
    {
        "name": "Rutgers University",
        "state": "new jersey",
        "location": "New Brunswick, New Jersey",
        "latitude": 40.5008,
        "longitude": -74.4474,
        "website": "https://rutgers.edu",
        "mental_health_urls": [
            "https://health.rutgers.edu/counseling/",
            "https://www.rutgers.edu/counseling"
        ],
        "source": "pending"
    },
]

# Update existing or add new
for update in updates:
    found = False
    for i, college in enumerate(data['colleges']):
        if college['name'] == update['name']:
            data['colleges'][i] = update
            found = True
            break
    if not found:
        data['colleges'].append(update)

# Add new states if needed
new_states = ['wisconsin', 'minnesota', 'iowa', 'nebraska', 'maryland', 'new jersey']
for s in new_states:
    if s not in data['states']:
        data['states'].append(s)

with open('/mnt/c/Users/raygo/source/repos/Mental_Health_Database/Scripts/college_targets.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Updated! Total colleges: {len(data['colleges'])}")
print(f"States: {data['states']}")
