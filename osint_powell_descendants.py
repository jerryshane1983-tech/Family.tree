import urllib.request
import urllib.parse

def search_ddg(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            results = []
            for part in html.split('class="result__snippet"'):
                if '</a>' in part:
                    snippet = part.split('>')[1].split('<')[0]
                    results.append(snippet)
            return results
    except Exception as e:
        return [str(e)]

targets = [
    '"Josh Powell" "Wilson" "Oklahoma" married',
    '"Josh Powell" "Wilson" "Oklahoma" wife',
    '"Becky Powell" "Wilson" "Oklahoma" husband',
    '"Carrie Dawn Powell" "Wilson" "Oklahoma"'
]

for q in targets:
    print(f"--- Searching for {q} ---")
    results = search_ddg(q)
    for r in results[:5]:
        print(r)
    print()
