import urllib.request
import json

api_key = "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"
url = "https://api.tavily.com/search"

queries = [
    "\"Brodey Canales\" Wilson Oklahoma",
    "\"Mason Salsbury\" Wilson Oklahoma",
    "\"Jerry Wayne Hacker\" Wilson Oklahoma",
    "\"Billy Jack Drinnon\" Wilson Oklahoma",
]

report = "# 🦅 KRAKEN OSINT: HACKER GRANDCHILDREN DEEP DIVE\n\n"

for q in queries:
    print(f"=== Searching: {q} ===")
    data = json.dumps({
        "query": q,
        "api_key": api_key,
        "search_depth": "advanced",
        "include_answer": True
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            answer = res.get('answer', 'No summary available.')
            sources = [r.get('url') for r in res.get("results", [])[:3]]
            
            report += f"## Query: {q}\n"
            report += f"### Intelligence Summary\n{answer}\n\n"
            report += f"### Top Leads\n"
            for src in sources:
                report += f"- {src}\n"
            report += "\n---\n\n"
    except Exception as e:
        print(f"Error for {q}: {e}")

with open('kraken_hacker_grandkids.md', 'w') as f:
    f.write(report)
