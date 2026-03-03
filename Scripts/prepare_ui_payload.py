import json
from pathlib import Path

INPUT = Path(__file__).parent / 'scraped_colleges_data.json'
OUTPUT = Path(__file__).parent / 'ui_payload.json'


def build_card(resource):
    # Map normalized resource to UI card fields with safe defaults
    return {
        'title': resource.get('service_name') or 'Counseling & Mental Health',
        'subtitle': resource.get('department') or '',
        'description': resource.get('description') or 'No description available.',
        'contact': {
            'email': resource.get('contact_email') or '',
            'phone': resource.get('contact_phone') or '',
            'website': resource.get('contact_website') or ''
        },
        'meta': {
            'location': resource.get('location') or '',
            'office_hours': resource.get('office_hours') or '',
            'freshman_notes': resource.get('freshman_notes') or ''
        },
        'raw': resource.get('raw', '')
    }


def main():
    if not INPUT.exists():
        print('No scraped data found at', INPUT)
        return 1
    data = json.loads(INPUT.read_text(encoding='utf-8'))
    ui = []
    for college in data:
        college_entry = {
            'name': college.get('name'),
            'location': college.get('location'),
            'latitude': college.get('latitude'),
            'longitude': college.get('longitude'),
            'website': college.get('website'),
            'scraped_at': college.get('scraped_at'),
            'cards': [build_card(r) for r in college.get('resources', [])]
        }
        ui.append(college_entry)

    OUTPUT.write_text(json.dumps(ui, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Wrote UI payload to', OUTPUT)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
