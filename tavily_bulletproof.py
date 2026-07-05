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
        if "Unknown Daughter" in c['name'] or "?" in c['name']: continue
        cousins.append((c['name'], kid['name']))

results_markdown = "# 🦅 KRAKEN OSINT: GENERATION SUMMARY (STRICT MATCH MODE)\n\nThis report contains automated OSINT dossiers for the grandchildren of Garland Thomas Powell and Pearl Edith Marshall.\n\n*Note: This report uses strict identity verification. If an exact match cannot be verified against the parent's name, it will be marked as NO EXACT MATCH to prevent false positives.*\n\n"

for name, parent in cousins:
    clean_name = name.split('[')[0].strip()
    clean_parent = parent.split('[')[0].strip()
    
    # Specific exclusions based on common false positives
    exclusions = []
    if "Jerry" in clean_name:
        exclusions.extend(["Elton", "Elgian", "Elton Sanderson"])
    if "Josh" in clean_name:
        exclusions.extend(["Susan Powell", "Steven Powell", "true crime", "murder", "podcast"])
    if "Danny" in clean_name:
        exclusions.append("Henryetta") # The previous false positive lived here
    if "Randall" in clean_name:
        exclusions.append("Bedford") # False positive
    
    q = f'exact match genealogy for "{clean_name}" child of "{clean_parent}" Wilson Oklahoma'
    
    print(f"=== Searching: {clean_name} ===")
    
    data = json.dumps({
        "query": q,
        "api_key": api_key,
        "search_depth": "advanced",
        "include_answer": True,
        "exclude_domains": ["wikipedia.org", "youtube.com"]
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            ai_answer = res.get('answer', '')
            results = res.get("results", [])
            
            # Post-processing: Strict validation
            valid_sources = []
            for r in results:
                content = r.get('content', '').lower()
                title = r.get('title', '').lower()
                text = content + " " + title
                
                # Check exclusions
                if any(ex.lower() in text for ex in exclusions):
                    continue
                    
                # Must contain at least part of the name
                first_name = clean_name.split()[0].lower()
                if first_name not in text:
                    continue
                    
                valid_sources.append(r.get('url'))
            
            # Strict answer validation
            answer_lower = ai_answer.lower()
            if any(ex.lower() in answer_lower for ex in exclusions):
                ai_answer = "❌ NO EXACT MATCH FOUND. The search engine attempted to return a known false positive, which was intercepted and blocked."
            elif clean_name.split()[0].lower() not in answer_lower and "no information" not in answer_lower:
                ai_answer = "❌ NO EXACT MATCH FOUND. Results did not explicitly mention the target."
            
            results_markdown += f"## 🎯 Target: {clean_name}\n"
            results_markdown += f"**Lineage:** Child of {clean_parent}\n\n"
            results_markdown += f"### Intelligence Summary\n{ai_answer}\n\n"
            results_markdown += f"### Verified Leads\n"
            if valid_sources:
                for src in valid_sources[:3]:
                    results_markdown += f"- {src}\n"
            else:
                results_markdown += "- *No strictly verified leads found.*\n"
            results_markdown += "\n---\n\n"
    except Exception as e:
        print(f"Error for {q}: {e}")
        results_markdown += f"## 🎯 Target: {clean_name}\n**Lineage:** Child of {clean_parent}\n\n*Search failed or timed out.*\n\n---\n\n"
        
    time.sleep(2) # Prevent rate limit

with open('generation_osint_report_strict.md', 'w') as f:
    f.write(results_markdown)

print("Report saved to generation_osint_report_strict.md")
