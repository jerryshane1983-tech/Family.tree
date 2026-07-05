import urllib.request
import json
import time

api_key = "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"
url = "https://api.tavily.com/search"

target = "James Powell"
relatives = ["Christina", "Rahnessa", "Bailey", "Austin"]
rel_str = " OR ".join([f'"{r}"' for r in relatives])

queries = [
    f'"{target}" AND ("Christina" OR "Rahnessa" OR "Bailey" OR "Austin") "Wilson" "Oklahoma"',
    f'site:facebook.com "{target}" "Wilson" "Oklahoma" AND ("Christina" OR "Rahnessa" OR "Bailey" OR "Austin")',
    f'"Rahnessa Powell" OR "Bailey Powell" OR "Austin Powell" "Wilson" "Oklahoma"'
]

report = f"## 🦅 TARGET: {target}\n"
for q in queries:
    print(f"=== Searching: {q} ===")
    req_data = json.dumps({
        "query": q,
        "api_key": api_key,
        "search_depth": "advanced",
        "include_answer": True
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=req_data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            if res.get('answer'):
                report += f"**Query ({q}):** {res['answer']}\n\n"
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(1)

with open('kraken_james_powell.md', 'w') as f:
    f.write(report)
print("Finished. Saved to kraken_james_powell.md")
