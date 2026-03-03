import json, os

for fname in ["scraped_colleges_data.json", "starter_colleges_data.json"]:
    path = os.path.join(os.path.dirname(__file__), fname)
    if not os.path.exists(path):
        print(f"\n--- {fname}: NOT FOUND ---")
        continue
    data = json.load(open(path, "r", encoding="utf-8"))
    resources = [r for c in data for r in c.get("resources", [])]
    print(f"\n--- {fname} ---")
    print(f"Colleges: {len(data)}, Resources: {len(resources)}")
    for c in data:
        for r in c.get("resources", []):
            name = r.get("service_name", "???")
            desc = (r.get("description", "") or "")[:80]
            print(f"  [{c['name'][:30]}] {name} | {desc}")
