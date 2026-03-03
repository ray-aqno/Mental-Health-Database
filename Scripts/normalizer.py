import json


class Normalizer:
    def __init__(self, schema=None):
        self.schema = schema

    def normalize(self, raw_resource, source_url):
        # Minimal normalization: ensure keys exist and set website
        normalized = {
            'service_name': raw_resource.get('service_name', '').strip(),
            'description': raw_resource.get('description', '').strip(),
            'contact_email': raw_resource.get('contact_email', ''),
            'contact_phone': raw_resource.get('contact_phone', ''),
            'contact_website': raw_resource.get('contact_website', source_url),
            'department': raw_resource.get('department', 'Student Affairs'),
            'office_hours': raw_resource.get('office_hours', ''),
            'location': raw_resource.get('location', ''),
            'freshman_notes': raw_resource.get('freshman_notes', '')
        }
        normalized['raw'] = json.dumps(raw_resource, ensure_ascii=False)
        return normalized
