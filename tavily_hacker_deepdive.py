import urllib.request
import json

api_key = "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"
url = "https://api.tavily.com/search"

queries = [
    "\"Judy Hacker\" OR \"Judy M. Hacker\" \"Billy Floyd\" Wilson Oklahoma obituary",
    "\"Billy Floyd Hacker\" Wilson Oklahoma obituary",
    "\"Lisa Hacker\" \"Judy Hacker\" Wilson Oklahoma",
    "\"Billy Don Hacker\" \"Judy Hacker\" Wilson Oklahoma",
    "\"Mary Hacker\" \"Judy Hacker\" Wilson Oklahoma",
    "\"Rachel Hacker\" \"Judy Hacker\" Wilson Oklahoma",
]

report = "# 🦅 KRAKEN OSINT: JUDY HACKER BRANCH DEEP DIVE\n\n"

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
            sources = [r.get('url') for r in res.get("results", [])[:5]]
            
            report += f"## Query: {q}\n"
            report += f"### Intelligence Summary\n{answer}\n\n"
            report += f"### Top Leads\n"
            for src in sources:
                report += f"- {src}\n"
            report += "\n---\n\n"
    except Exception as e:
        print(f"Error for {q}: {e}")
        report += f"## Query: {q}\n*Search failed.*\n\n---\n\n"

with open('kraken_hacker_deepdive.md', 'w') as f:
    f.write(report)

print("Report saved to kraken_hacker_deepdive.md")
