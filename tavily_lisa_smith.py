import urllib.request
import json

api_key = "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"
url = "https://api.tavily.com/search"

q = "\"Lisa Hacker Smith\" OR \"Lisa Smith\" \"Judy Hacker\" Wilson Oklahoma"

print(f"=== {q} ===")
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
        print("ANSWER:", res.get('answer', ''))
        for r in res.get("results", []):
            print(r.get('url'), "-", r.get('title'))
except Exception as e:
    print(f"Error for {q}: {e}")
