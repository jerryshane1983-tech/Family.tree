import urllib.request
import json
import time

api_key = "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"
url = "https://api.tavily.com/search"

with open('sanderson_tree.json', 'r') as f:
    data = json.load(f)

people = {p['id']: p for p in data['people']}

def get_children(person_id):
    children_ids = set()
    person = people.get(person_id)
    if not person: return []
    if 'children' in person:
        for c in person['children']:
            children_ids.add(c)
    for pid, p in people.items():
        if 'parents' in p and person_id in p['parents']:
            children_ids.add(pid)
    return list(children_ids)

garland_id = next(pid for pid, p in people.items() if 'Garland' in p['name'])
kids_ids = get_children(garland_id)

cousins = []
for kid_id in kids_ids:
    kid = people[kid_id]
    kid_children_ids = get_children(kid_id)
    for cid in kid_children_ids:
        c = people[cid]
        # Ignore unnamed people
        if "Unknown Daughter" in c['name'] or "?" in c['name']: continue
        cousins.append((c['name'], kid['name']))

results_markdown = "# 🦅 KRAKEN OSINT: GENERATION SUMMARY\n\nThis report contains automated OSINT dossiers for the grandchildren of Garland Thomas Powell and Pearl Edith Marshall.\n\n"

for name, parent in cousins:
    # Build query
    clean_name = name.split('[')[0].strip()
    clean_parent = parent.split('[')[0].strip()
    q = f'"{clean_name}" "{clean_parent}" Wilson Oklahoma OR Oklahoma genealogy OR family'
    
    print(f"=== Searching: {clean_name} ===")
    
    data = json.dumps({
        "query": q,
        "api_key": api_key,
        "search_depth": "basic",
        "include_answer": True
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            ai_answer = res.get('answer', 'No summary available.')
            sources = [r.get('url') for r in res.get("results", [])[:3]]
            
            results_markdown += f"## 🎯 Target: {clean_name}\n"
            results_markdown += f"**Lineage:** Child of {clean_parent}\n\n"
            results_markdown += f"### Intelligence Summary\n{ai_answer}\n\n"
            results_markdown += f"### Top Leads\n"
            for src in sources:
                results_markdown += f"- {src}\n"
            results_markdown += "\n---\n\n"
    except Exception as e:
        print(f"Error for {q}: {e}")
        results_markdown += f"## 🎯 Target: {clean_name}\n**Lineage:** Child of {clean_parent}\n\n*Search failed or timed out.*\n\n---\n\n"
        
    time.sleep(2) # Prevent rate limit

with open('generation_osint_report.md', 'w') as f:
    f.write(results_markdown)

print("Report saved to generation_osint_report.md")
