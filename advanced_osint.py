import urllib.request
import json
import time

api_key = "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"
url = "https://api.tavily.com/search"

queries = {
    "Method 2 (OSCN Court Records)": [
        "site:oscn.net \"Summer Hacker\" Carter",
        "site:oscn.net \"Amber Hacker\" Carter",
        "site:oscn.net \"Desiree Hacker\" Carter",
        "site:oscn.net \"Elizabeth Hacker\" Carter",
        "site:oscn.net \"Autumn Hacker\" Carter"
    ],
    "Method 3 (Spouse Pivot)": [
        "\"Melanie Slawson\" \"Billy Don\" Hacker Wilson Oklahoma"
    ],
    "Method 5 (Facebook Dorking)": [
        "site:facebook.com \"Summer\" \"Wilson\" \"Oklahoma\" AND (\"Hacker\" OR \"Canales\" OR \"Fisher\" OR \"Drinnon\")",
        "site:facebook.com \"Amber\" \"Wilson\" \"Oklahoma\" AND (\"Hacker\" OR \"Canales\" OR \"Fisher\" OR \"Drinnon\")",
        "site:facebook.com \"Desiree\" \"Wilson\" \"Oklahoma\" AND (\"Hacker\" OR \"Canales\" OR \"Fisher\" OR \"Drinnon\")",
        "site:facebook.com \"Autumn\" \"Wilson\" \"Oklahoma\" AND (\"Hacker\" OR \"Canales\" OR \"Fisher\" OR \"Drinnon\")"
    ]
}

report = "# 🦅 KRAKEN OSINT: ADVANCED TACTICS DEEP DIVE\n\n"

for method, qs in queries.items():
    report += f"## {method}\n\n"
    for q in qs:
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
                results = res.get("results", [])
                
                report += f"### Target Query: `{q}`\n"
                report += f"**AI Analysis:** {answer}\n\n"
                
                if results:
                    report += "**Raw Hits:**\n"
                    for r in results[:3]:
                        report += f"- [{r.get('title')}]({r.get('url')})\n"
                else:
                    report += "*No direct hits found.*\n"
                report += "\n---\n\n"
        except Exception as e:
            print(f"Error for {q}: {e}")
        time.sleep(1)

with open('kraken_advanced_osint.md', 'w') as f:
    f.write(report)
print("Finished. Saved to kraken_advanced_osint.md")
