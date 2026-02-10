# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "youtube-search",
# ]
# ///

"""
TOOL: YouTube Finder
DESCRIPTION: Searches for YouTube videos by query and returns IDs/URLs.
USAGE: ./tools/run run tools/scripts/yt_finder.py "<query>" [limit]
"""

import sys
import json
from youtube_search import YoutubeSearch

def parse_views(view_str):
    """Konwertuje string z liczbą wyświetleń na int."""
    if not view_str:
        return 0
    # Usuń wszystko co nie jest cyfrą (w tym spacje, 'wyświetleń' itp.)
    clean_str = ''.join(c for c in view_str if c.isdigit())
    try:
        return int(clean_str)
    except ValueError:
        return 0

def search_videos(query, max_results=5):
    """Szuka filmów i zwraca ID."""
    print(f"Szukam: '{query}'...")
    results = YoutubeSearch(query, max_results=max_results).to_dict()
    
    # Sortowanie po wyświetleniach
    for video in results:
        video['view_count_int'] = parse_views(video.get('views', ''))
    
    # Sortuj malejąco (najwięcej wyświetleń na górze)
    results.sort(key=lambda x: x['view_count_int'], reverse=True)
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Użycie: python tools/yt_finder.py 'zapytanie' [liczba_wynikow]")
        sys.exit(1)

    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    videos = search_videos(query, limit)
    
    print(f"\nZnaleziono {len(videos)} filmów:\n")
    for v in videos:
        url = f"https://www.youtube.com/watch?v={v['id']}"
        print(f"- [{v['duration']}] {v['title']}")
        print(f"  Link: {url}")
        print(f"  Views: {v['views']}")
        
        # Opcjonalnie: Tu można wywołać pobieranie transkrypcji
        # import subprocess
        # subprocess.run(["python", "tools/youtube_transcript.py", url])
        
    print("\nAby pobrać transkrypcję, uruchom: python tools/youtube_transcript.py <URL>")

if __name__ == "__main__":
    main()
