import urllib.request
import json
import time
import sys

API_KEY = "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"
URL = "https://api.tavily.com/search"

def load_tree():
    with open('sanderson_tree.json', 'r') as f:
        return json.load(f)

def save_tree(data):
    with open('sanderson_tree.json', 'w') as f:
        json.dump(data, f, indent=2)

def get_person(data, name):
    # Try exact match first
    for p in data['people']:
        if name.lower() == p['name'].lower():
            return p
    # Try partial match
    for p in data['people']:
        if name.lower() in p['name'].lower():
            return p
    return None

def get_relatives(data, person):
    relatives = []
    def extract_name(name):
        parts = name.replace('.', '').split()
        for p in parts:
            if len(p) > 2: return p
        return parts[0] if parts else ""

    # parents
    for pid in person.get('parents', []):
        parent = next((p for p in data['people'] if p['id'] == pid), None)
        if parent: relatives.append(extract_name(parent['name']))
    # spouse
    if person.get('spouse'):
        relatives.append(extract_name(person['spouse']))
    # kids
    for cid in person.get('children', []):
        child = next((p for p in data['people'] if p['id'] == cid), None)
        if child: relatives.append(extract_name(child['name']))
    return relatives

def run_osint(target_name):
    data = load_tree()
    person = get_person(data, target_name)
    if not person:
        print(f"Could not find {target_name} in the family tree.")
        return
    
    print(f"[*] 🦅 INITIALIZING KRAKEN ON TARGET: {person['name']}...")
    relatives = get_relatives(data, person)
    rel_str = " OR ".join([f'"{r}"' for r in set(relatives)]) if relatives else ""
    
    # Construct advanced queries
    queries = {
        "Deep Web & Obituaries": f'"{person["name"]}" obituary "Wilson" "Oklahoma"',
        "Spouse/Parent Cross-Reference": f'"{person["name"]}" "Wilson" "Oklahoma" AND ({rel_str})' if rel_str else f'"{person["name"]}" "Wilson" "Oklahoma"',
        "Facebook Dorking": f'site:facebook.com "{person["name"]}" "Wilson" "Oklahoma"'
    }
    
    intel_snippets = []
    leads = set()
    
    for method, q in queries.items():
        print(f"    -> Executing {method} Protocol...")
        req_data = json.dumps({
            "query": q,
            "api_key": API_KEY,
            "search_depth": "advanced",
            "include_answer": True
        }).encode("utf-8")
        
        req = urllib.request.Request(URL, data=req_data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode("utf-8"))
                if res.get('answer'):
                    intel_snippets.append(res['answer'])
                for result in res.get("results", [])[:3]:
                    leads.add(result['url'])
        except Exception as e:
            print(f"    [!] Target evasion detected on {method}: {e}")
        time.sleep(1)
        
    full_intel = "\n\n".join(intel_snippets)
    
    # Append to Master Dossier
    try:
        with open('KRAKEN_MASTER_DOSSIER.md', 'a') as f:
            f.write(f"## 🦅 TARGET: {person['name']}\n")
            f.write(f"**ID:** {person['id']} | **Gender:** {person.get('gender', 'Unknown')}\n")
            if relatives:
                f.write(f"**Known Relatives Used in Pivot:** {', '.join(set(relatives))}\n")
            f.write(f"### Intelligence Summary\n{full_intel if full_intel else 'No significant data uncovered.'}\n\n")
            f.write("### Digital Leads\n")
            for l in leads:
                f.write(f"- {l}\n")
            f.write("\n---\n\n")
    except Exception as e:
        pass
        
    # Update JSON Tree
    current_note = person.get('note', '')
    if full_intel and "KRAKEN INTEL:" not in current_note:
        # Keep it brief for the JSON file to prevent bloat
        brief_intel = (full_intel[:150] + '...') if len(full_intel) > 150 else full_intel
        brief_intel = brief_intel.replace("\n", " ")
        if current_note:
            person['note'] = current_note + f" | KRAKEN INTEL: {brief_intel}"
        else:
            person['note'] = f"KRAKEN INTEL: {brief_intel}"
        save_tree(data)
        print(f"    [+] Injected intelligence into sanderson_tree.json")
    
    print(f"[*] 🦅 KRAKEN DEEP DIVE COMPLETE. Dossier Updated.\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = " ".join(sys.argv[1:])
        run_osint(target)
    else:
        print("Usage: python kraken_engine.py <Target Name>")
