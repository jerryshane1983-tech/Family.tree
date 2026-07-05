import urllib.request
import urllib.parse
import json
import base64

def search_okcountyrecords(api_key, name, county="carter"):
    url = f"https://okcountyrecords.com/api/v1/search?county={county}&name={urllib.parse.quote(name)}"
    
    # Create the Basic Auth header
    auth_string = f"{api_key}:"
    base64_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    
    req = urllib.request.Request(url, headers={
        'Authorization': f'Basic {base64_auth}',
        'Accept': 'application/json'
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        return None
    except Exception as e:
        print(f"Error connecting: {e}")
        return None

if __name__ == "__main__":
    API_KEY = "79561136fdfb120122a22263fe4eed38"
    
    targets = [
        "Powell, Josh",
        "Powell, Becky",
        "Powell, Carrie Dawn"
    ]
    
    for target in targets:
        print(f"\n--- Searching OKCountyRecords API for: {target} ---")
        results = search_okcountyrecords(API_KEY, target)
        
        if results and 'results' in results:
            print(f"Found {results.get('total', 0)} matches.")
            # Print the first few results to find spouses/deeds
            for r in results['results'][:5]:
                print(f"Instrument: {r.get('instrument_type')} - Date: {r.get('date_filed')}")
                parties = [p.get('name') for p in r.get('parties', [])]
                print(f"Parties: {', '.join(parties)}")
        else:
            print("No data returned or error occurred.")
