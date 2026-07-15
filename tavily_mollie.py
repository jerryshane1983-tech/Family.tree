import urllib.request
import json

api_key = "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"
url = "https://api.tavily.com/search"

queries = [
    "\"Mary Elizabeth Riley\" Sanderson 1861 1941",
    "\"Mollie Riley\" Sanderson 1861 1941 genealogy",
    "\"James Milton Sanderson\" \"Mary Elizabeth\" 1854 1934"
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
            result = json.loads(response.read().decode("utf-8"))
            print("Answer:", result.get("answer", "No answer provided"))
            print("Sources:")
            for res in result.get("results", [])[:3]:
                print(f"- {res.get('title')}: {res.get('url')}")
            print("\n")
    except Exception as e:
        print("Error:", e)
