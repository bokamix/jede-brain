# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "duckduckgo-search",
# ]
# ///

"""
TOOL: Trend Finder
DESCRIPTION: Finds trending news articles using DuckDuckGo.
USAGE: ./tools/run run tools/scripts/trend_finder.py "<query>" [limit]
"""

import sys
from duckduckgo_search import DDGS

def main():
    query = "trending"
    limit = 10

    if len(sys.argv) > 1:
        query = sys.argv[1]
    
    if len(sys.argv) > 2:
        try:
            limit = int(sys.argv[2])
        except ValueError:
            pass

    print(f"Szukam popularnych artykułów dla hasła: '{query}' (ostatni tydzień)...")
    
    try:
        # region="wt-wt" (World), timelimit="w" (Week)
        results = DDGS().news(
            keywords=query, 
            region="wt-wt", 
            safesearch="off", 
            timelimit="w", 
            max_results=limit
        )
        
        if not results:
             print("Brak wyników.")
             return

        for r in results:
            print(f"- {r['title']}")
            print(f"  Link: {r['url']}")
            print(f"  Source: {r['source']} | Date: {r['date']}")
            print("")
            
    except Exception as e:
        print(f"Błąd podczas wyszukiwania: {e}")
        print("Upewnij się, że masz połączenie z internetem.")

if __name__ == "__main__":
    main()

