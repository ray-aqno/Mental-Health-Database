import json
from simple_scraper import CollegeScraper
from pathlib import Path


def load_targets(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['colleges']


def run_sample(n=3):
    scraper = CollegeScraper()
    targets = load_targets(Path(__file__).parent / 'college_targets.json')
    selected = [c for c in targets if c.get('source') != 'manual'][:n]
    results = []
    for c in selected:
        print(f"Scraping: {c['name']} -> {c.get('mental_health_urls', [])}")
        res = scraper.scrape_college(c)
        results.append((c['name'], res))
    for name, res in results:
        print(f"\n{name}: {len(res)} resource(s)")
        for r in res:
            print(' -', r.get('service_name')[:80])


if __name__ == '__main__':
    run_sample(3)
