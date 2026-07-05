import urllib.request
import urllib.parse
from html.parser import HTMLParser

class TaxRollParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_row = False
        self.in_cell = False
        self.current_cell = 0
        self.current_data = []
        self.results = []

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.in_row = True
            self.current_data = []
            self.current_cell = 0
        elif tag == "td" and self.in_row:
            self.in_cell = True

    def handle_endtag(self, tag):
        if tag == "td":
            self.in_cell = False
            self.current_cell += 1
        elif tag == "tr":
            self.in_row = False
            if self.current_data:
                self.results.append(self.current_data)

    def handle_data(self, data):
        if self.in_cell:
            text = data.strip()
            if text:
                self.current_data.append(text)

def search_assessor(county, name):
    print(f"Scraping OKTaxRolls for {name} in {county} County...")
    
    # Try different search URLs
    encoded_name = urllib.parse.quote_plus(name)
    url = f"https://oktaxrolls.com/county/{county}/search/{encoded_name}"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            parser = TaxRollParser()
            parser.feed(html)
            
            print(f"Found {len(parser.results)} potential records.")
            for row in parser.results:
                # Typically format is [Owner Name, Account, Address, etc]
                print(" | ".join(row))
                
    except Exception as e:
        print(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    search_assessor("Carter", "Powell")
