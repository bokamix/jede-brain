# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "youtube-transcript-api",
#     "requests",
# ]
# ///

"""
TOOL: YouTube Transcript Downloader
DESCRIPTION: Downloads transcripts from YouTube videos.
USAGE: ./tools/run run tools/scripts/youtube_transcript.py <youtube_url>
NOTE: This tool is managed by Iron Dome (tools/core/dispatcher.py). Do not use ScrapingGuard manually here.
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add the current script's directory to sys.path to allow importing from utils
current_dir = Path(__file__).parent.absolute()
sys.path.append(str(current_dir))

from utils.youtube_transcript_runner import run_transcript_download, get_video_id, get_video_title, sanitize_filename

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/youtube_transcript.py <youtube_url>")
        sys.exit(1)

    video_url = sys.argv[1]
    video_id = get_video_id(video_url)

    if not video_id:
        print(f"Error: Could not extract video ID from URL: {video_url}")
        sys.exit(1)

    # Prepare output directory and filename
    # Save to 05_Reading_Room
    output_dir = current_dir.parent.parent / "05_Reading_Room"
    if not output_dir.exists():
        # Fallback if 05_Reading_Room doesn't exist
        output_dir = current_dir / "transcriptions"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    title = get_video_title(video_id)
    safe_title = sanitize_filename(title)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{safe_title}_{video_id}.md"
    filepath = output_dir / filename

    print(f"Downloading transcript for: {title}...")
    result = run_transcript_download(video_url, str(filepath))
    print(result)

if __name__ == "__main__":
    main()
