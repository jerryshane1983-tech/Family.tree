import urllib.request
import json

api_key = "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"
url = "https://api.tavily.com/search"

queries = [
    "\"Robert Powell\" born 1845 father of \"L. Otto Oliver Powell\" genealogy parents",
    "\"Robert Darrell Hall\" born 1890 died 1959 married \"Verna Mae Branch\" genealogy parents"
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
            for result in res.get("results", [])[:5]:
                print(f"Source: {result.get('url')}")
                print(f"Title: {result.get('title')}")
                print(f"Content: {result.get('content')}")
                print("-" * 50)
    except Exception as e:
        print(f"Error for {q}: {e}")
    print("\n")
