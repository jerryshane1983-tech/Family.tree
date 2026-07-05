import urllib.request
import json
import time

api_key = "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"
url = "https://api.tavily.com/search"

queries = [
    "\"Randall Sanderson\" OR \"Bear Sanderson\" Wilson Oklahoma children descendants",
    "\"Donnie Hogan\" OR \"Judge Hogan\" Wilson Oklahoma children descendants",
    "\"Jennifer Beyer\" Wilson Oklahoma children descendants",
    "\"Stephanie VanCuren\" Wilson Oklahoma children descendants"
]

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
            print(f"AI Answer: {res.get('answer')}\n")
            for result in res.get("results", [])[:2]:
                print(f"Source: {result.get('url')}")
                print(f"Content: {result.get('content')[:300]}...")
                print("-" * 50)
    except Exception as e:
        print(f"Error for {q}: {e}")
    print("\n")
    time.sleep(1) # Prevent rate limiting
