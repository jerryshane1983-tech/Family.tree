import urllib.request
import json

api_key = "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"
url = "https://api.tavily.com/search"

queries = [
    "(\"Summer Hacker\" OR \"Summer Fisher\" OR \"Summer Drinnon\" OR \"Summer Canales\" OR \"Summer Slawson\") Wilson Oklahoma",
    "(\"Amber Hacker\" OR \"Amber Fisher\" OR \"Amber Drinnon\" OR \"Amber Canales\" OR \"Amber Slawson\") Wilson Oklahoma",
    "(\"Desiree Hacker\" OR \"Desiree Fisher\" OR \"Desiree Drinnon\" OR \"Desiree Canales\" OR \"Desiree Slawson\") Wilson Oklahoma",
    "(\"Katelynn Hacker\" OR \"Katelynn Fisher\" OR \"Katelynn Drinnon\" OR \"Katelynn Canales\" OR \"Katelynn Slawson\") Wilson Oklahoma",
    "(\"Elizabeth Hacker\" OR \"Elizabeth Fisher\" OR \"Elizabeth Drinnon\" OR \"Elizabeth Canales\" OR \"Elizabeth Slawson\") Wilson Oklahoma",
    "(\"Autumn Hacker\" OR \"Autumn Fisher\" OR \"Autumn Drinnon\" OR \"Autumn Canales\" OR \"Autumn Slawson\") Wilson Oklahoma",
]

report = "# 🦅 KRAKEN OSINT: HACKER GRANDDAUGHTERS DEEP DIVE\n\n"

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

with open('kraken_hacker_granddaughters.md', 'w') as f:
    f.write(report)
