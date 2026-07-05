import urllib.request
import json

api_key = "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"
url = "https://api.tavily.com/search"

queries = [
    "\"Billy Don Hacker\" \"Melanie Slawson\"",
    "\"Lisa Hacker\" \"Wilson\" Oklahoma facebook",
]

for q in queries:
    print(f"=== {q} ===")
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
            print(res.get('answer', ''))
            for r in res.get("results", [])[:3]:
                print(r.get('url'))
    except Exception as e:
        print(f"Error for {q}: {e}")
