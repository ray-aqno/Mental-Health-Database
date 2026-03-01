import json

# Read the scraped data
with open('scraped_colleges_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get unique schools
unique_schools = {}
for college in data:
    name = college['name']
    if name not in unique_schools:
        unique_schools[name] = {
            'location': college['location'],
            'resources': college.get('resources', [])
        }
    else:
        # Merge resources
        unique_schools[name]['resources'].extend(college.get('resources', []))

# Print summary
print(f"Total entries: {len(data)}")
print(f"Unique schools: {len(unique_schools)}")
print("\n" + "="*70)
print("SCHOOLS SCRAPED:")
print("="*70)

ohio_schools = []
other_schools = []

for name, info in sorted(unique_schools.items()):
    resource_count = len(info['resources'])
    school_info = f"{name} ({info['location']}) - {resource_count} resources"
    
    if 'Ohio' in info['location']:
        ohio_schools.append(school_info)
    else:
        other_schools.append(school_info)

print("\n🔵 Ohio Schools:")
for school in ohio_schools:
    print(f"  ✓ {school}")

print(f"\n🟢 Other Schools:")
for school in other_schools:
    print(f"  ✓ {school}")

print(f"\n{'='*70}")
print(f"SUMMARY: {len(ohio_schools)} Ohio schools + {len(other_schools)} other schools = {len(unique_schools)} total")
print("="*70)
