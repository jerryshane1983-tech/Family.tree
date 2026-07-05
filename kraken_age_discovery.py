import urllib.request
import json
import time
import sys
import re

API_KEY = "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"
URL = "https://api.tavily.com/search"

def load_tree():
    with open('sanderson_tree.json', 'r') as f:
        return json.load(f)

def save_tree(data):
    with open('sanderson_tree.json', 'w') as f:
        json.dump(data, f, indent=2)

def run_age_discovery(limit=5):
    data = load_tree()
    
    # Find targets who lack a birth_date
    targets = [p for p in data['people'] if 'birth_date' not in p and 'estimated_birth_year' not in p]
    print(f"[*] Found {len(targets)} people missing birth dates. Running Age-Discovery on the first {limit}...")
    
    report = "## 🦅 KRAKEN AGE DISCOVERY REPORT\n\n"
    
    for i, person in enumerate(targets[:limit]):
        name = person['name']
        print(f"[{i+1}/{limit}] Scanning public records and obituaries for {name}...")
        
        # We phrase the query as a question so Tavily's AI tries to extract the exact answer
        q = f'What is the age or birth year of "{name}" from "Wilson, Oklahoma"?'
        
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
                answer = res.get('answer', '')
                snippets = " ".join([r.get('content', '') for r in res.get('results', [])[:3]])
                
                # Simple regex to look for age patterns like "Age 45" or "born in 1980"
                # This is just a backup if the AI answer doesn't explicitly state it
                age_match = re.search(r'(?i)age[\s:]*(\d{1,3})', snippets)
                born_match = re.search(r'(?i)born\s*(?:in\s*)?(19\d{2}|20\d{2})', snippets)
                
                report += f"### Target: {name} (ID: {person['id']})\n"
                
                found_intel = False
                if answer:
                    report += f"**AI Extraction:** {answer}\n"
                    found_intel = True
                
                if age_match:
                    report += f"**Raw Data Match:** Age {age_match.group(1)}\n"
                    person['estimated_birth_year'] = f"Estimated based on age {age_match.group(1)}"
                    found_intel = True
                elif born_match:
                    report += f"**Raw Data Match:** Born {born_match.group(1)}\n"
                    person['estimated_birth_year'] = born_match.group(1)
                    found_intel = True
                
                if not found_intel:
                    report += "*No definitive age or birth date found in the first pass.*\n"
                else:
                    # Append a note in the JSON so we don't scan them endlessly
                    current_note = person.get('note', '')
                    intel_note = f"| AGE OSINT: {answer[:100]}..."
                    person['note'] = current_note + intel_note if current_note else intel_note
                
                report += "\n"
                
        except Exception as e:
            print(f"    [!] Error scanning {name}: {e}")
            report += f"### Target: {name}\n*Error during scan.*\n\n"
        
        time.sleep(1) # Rate limiting
        
    save_tree(data)
    
    with open('kraken_age_report.md', 'w') as f:
        f.write(report)
        
    print("[+] Age Discovery Module Complete! Check kraken_age_report.md for findings.")

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    run_age_discovery(limit)
