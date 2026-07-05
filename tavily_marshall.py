import urllib.request
import json

api_key = "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"
url = "https://api.tavily.com/search"

queries = [
    "\"William Henry Marshall\" born 1871 married \"Salina Annie Palmer\" Atoka Oklahoma parents genealogy",
    "\"William Henry Marshall\" Choctaw Nation Dawes Roll parents Atoka Oklahoma"
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
            for result in res.get("results", [])[:3]:
                print(f"Source: {result.get('url')}")
                print(f"Content: {result.get('content')[:500]}...")
                print("-" * 50)
    except Exception as e:
        print(f"Error for {q}: {e}")
    print("\n")
