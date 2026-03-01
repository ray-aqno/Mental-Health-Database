import json

with open('scraped_colleges_data.json') as f:
    scraped = json.load(f)

print('SCRAPED (' + str(len(scraped)) + '):')
print('='*60)
for c in scraped:
    r = len(c.get('resources', []))
    print(f'{r:2} | {c["name"]}')

print()
print('FAILED TO SCRAPE:')
print('='*60)
with open('college_targets.json') as f:
    targets = json.load(f)

scraped_names = {c['name'] for c in scraped}
for t in targets['colleges']:
    if t['name'] not in scraped_names and t.get('source') != 'manual':
        print(f'{t["name"]} ({t["state"]})')
