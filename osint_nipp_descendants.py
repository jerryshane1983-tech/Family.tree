import urllib.request
import urllib.parse
import json

def search_obituary(name, year=None):
    query = f"{name} Nipp obituary Oklahoma"
    if year:
        query += f" {year}"
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # Extract basic snippets
            results = []
            for part in html.split('class="result__snippet"'):
                if '</a>' in part:
                    snippet = part.split('>')[1].split('<')[0]
                    results.append(snippet)
            return results
    except Exception as e:
        return [str(e)]

targets = [
    ("Claud William Nipp", 1990),
    ("Oleta Pearl Nipp", 2010),
    ("Lorene Montgomery", None),
    ("Linda Sue Williams", None),
    ("Donnie Nipp", None),
    ("Curtiss Nipp", None)
]

for name, year in targets:
    print(f"--- Searching for {name} ({year}) ---")
    results = search_obituary(name, year)
    for r in results[:3]:
        print(r)
    print()
