import requests
import urllib3

urllib3.disable_warnings()

# Get all colleges
response = requests.get('http://localhost:58346/api/colleges', verify=False)
colleges = response.json()

print(f"{'='*70}")
print(f"DATABASE IMPORT STATUS")
print(f"{'='*70}\n")

print(f"Total Colleges in Database: {len(colleges)}")

# Count Ohio schools
ohio_schools = [c for c in colleges if 'Ohio' in c.get('location', '')]
print(f"Ohio Schools: {len(ohio_schools)}")

# Count total resources
total_resources = sum(len(c.get('resources', [])) for c in colleges)
print(f"Total Resources: {total_resources}\n")

# Show recent Ohio schools (likely our imports)
print(f"{'='*70}")
print("OHIO SCHOOLS WITH RESOURCES:")
print(f"{'='*70}\n")

for college in sorted(ohio_schools, key=lambda x: x.get('name', '')):
    resources = college.get('resources', [])
    name = college['name']
    location = college.get('location', '')
    resource_count = len(resources)
    
    status = "✓" if resource_count > 0 else "⚠"
    print(f"{status} {name} ({location})")
    print(f"   Resources: {resource_count}")
    
    if resources:
        for r in resources:
            service = r.get('serviceName', 'Unknown')
            phone = r.get('contactPhone', '')
            email = r.get('contactEmail', '')
            print(f"     • {service}")
            if phone:
                print(f"       Phone: {phone}")
            if email:
                print(f"       Email: {email}")
    print()

print(f"{'='*70}")
print(f"SUMMARY: {len(ohio_schools)} Ohio schools, {sum(len(c.get('resources', [])) for c in ohio_schools)} resources")
print(f"{'='*70}")
