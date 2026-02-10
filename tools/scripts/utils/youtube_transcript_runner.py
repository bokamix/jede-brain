import os
import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime

def get_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_title(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            matches = re.findall(r'<title>(.*?)</title>', response.text)
            if matches:
                title = matches[0].replace(" - YouTube", "")
                return title
    except Exception as e:
        print(f"Warning: Could not fetch title: {e}")
    return video_id

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_")

def run_transcript_download(video_url, output_filepath=None):
    video_id = get_video_id(video_url)
    if not video_id:
        return f"Error: Could not extract video ID from URL: {video_url}"

    try:
        transcript_list = YouTubeTranscriptApi().list(video_id)
        
        generated_transcripts = [t for t in transcript_list if t.is_generated]
        manual_transcripts = [t for t in transcript_list if not t.is_generated]
        
        selected_transcript = None

        def find_by_lang(transcripts, lang_prefix):
            for t in transcripts:
                if t.language_code.lower().startswith(lang_prefix.lower()):
                    return t
            return None

        # 1. English Manual, 2. English Generated, 3. Audio Manual, 4. Audio Generated
        selected_transcript = find_by_lang(manual_transcripts, 'en') or \
                              find_by_lang(generated_transcripts, 'en')
        
        if not selected_transcript and generated_transcripts:
            audio_lang_code = generated_transcripts[0].language_code
            selected_transcript = find_by_lang(manual_transcripts, audio_lang_code) or \
                                  generated_transcripts[0]

        if not selected_transcript:
            if manual_transcripts: selected_transcript = manual_transcripts[0]
            elif generated_transcripts: selected_transcript = generated_transcripts[0]

        if not selected_transcript:
            return "Error: No transcripts available."

        transcript_data = selected_transcript.fetch()
        title = get_video_title(video_id)
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        output_lines = [
            "---",
            f"created: {now}",
            f"updated: {now}",
            "status: transcription",
            "tags: [youtube, transcript]",
            "---",
            "",
            f"# {title}",
            "",
            f"URL: https://www.youtube.com/watch?v={video_id}",
            f"Language: {selected_transcript.language} ({'Generated' if selected_transcript.is_generated else 'Manual'})",
            "",
            "---",
            ""
        ]
        
        for line in transcript_data:
            try:
                start_time = line['start']
                text = line['text']
            except (KeyError, TypeError):
                start_time = getattr(line, 'start', 0)
                text = getattr(line, 'text', "")

            minutes = int(start_time // 60)
            seconds = int(start_time % 60)
            output_lines.append(f"[{minutes:02d}:{seconds:02d}] {text}")

        content = "\n".join(output_lines)
        
        # Add Changelog
        content += "\n\n---\n## Changelog\n"
        content += f"- {now}: Transcript downloaded via youtube_transcript.py.\n"
        
        if not output_filepath:
            output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "05_Reading_Room")
            if not os.path.exists(output_dir):
                output_dir = os.path.join(os.path.dirname(__file__), "..", "transcriptions")
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            safe_title = sanitize_filename(title)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}_{safe_title}_{video_id}.md"
            output_filepath = os.path.join(output_dir, filename)
        
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Success! Transcript saved to: {output_filepath}"

    except Exception as e:
        return f"Error: {str(e)}"


