# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "elevenlabs",
#     "click",
# ]
# ///

"""
TOOL: ElevenLabs Transcriber
DESCRIPTION: Transcribes a selected audio file using ElevenLabs Scribe.
USAGE: ./tools/run run tools/scripts/transcribe_elevenlabs.py <file_path> OR leave blank for GUI
CONFIG: Requires 'config/elevenlabs.json' with {"api_key": "..."}.
"""

import os
import sys
import json
import click
import datetime
from pathlib import Path
from elevenlabs.client import ElevenLabs
import subprocess

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "../../config/elevenlabs.json")

def get_api_key():
    """Load API key from config."""
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ Config Error: File not found at {CONFIG_PATH}")
        print("💡 Fix: Copy 'config/elevenlabs.example.json' to 'config/elevenlabs.json' and add your API Key.")
        sys.exit(1)
    
    with open(CONFIG_PATH, 'r') as f:
        data = json.load(f)
        return data.get("api_key")

def pick_file_gui():
    """Open a native file picker dialog."""
    # macOS AppleScript
    if sys.platform == 'darwin':
        try:
            cmd = "osascript -e 'POSIX path of (choose file with prompt \"Select audio file to transcribe\")'"
            result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
            return result
        except subprocess.CalledProcessError:
            return None

    # Fallback: Tkinter
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.lift()
        root.attributes('-topmost',True)
        root.after_idle(root.attributes,'-topmost',False)
        file_path = filedialog.askopenfilename(title="Select audio file to transcribe")
        root.destroy()
        return file_path
    except Exception as e:
        print(f"❌ GUI Error: {e}")
        return None

@click.command()
@click.argument('file_path', required=False, type=click.Path(exists=True))
def main(file_path):
    api_key = get_api_key()
    if not api_key:
        print("❌ Error: 'api_key' missing in config/elevenlabs.json")
        sys.exit(1)

    if not file_path:
        print("📂 Opening file picker...")
        file_path = pick_file_gui()
    
    if not file_path:
        print("❌ No file selected.")
        sys.exit(0)

    print(f"🚀 Transcribing: {file_path}")
    
    client = ElevenLabs(api_key=api_key)
    
    try:
        # Note: model_id might default to scribe_v1, explicitly setting if known, 
        # otherwise letting library handle defaults. 
        # As of late 2024, speech_to_text.convert is the method.
        with open(file_path, "rb") as f:
            transcription = client.speech_to_text.convert(
                file=f,
                model_id="scribe_v1" 
            )
        
        # Save output to 05_Reading_Room
        reading_room_dir = os.path.join(BASE_DIR, "../../05_Reading_Room")
        if os.path.exists(reading_room_dir):
            output_dir = reading_room_dir
        else:
            output_dir = os.path.join(BASE_DIR, "transcriptions")

        os.makedirs(output_dir, exist_ok=True)
        
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        date_str = now.strftime("%Y-%m-%d %H:%M")

        original_name = Path(file_path).stem
        # Simple sanitize
        safe_name = "".join([c for c in original_name if c.isalnum() or c in (' ', '-', '_')]).strip()
        output_filename = f"{timestamp}_{safe_name}.md"
        
        output_path = os.path.join(output_dir, output_filename)
        
        # Format content
        content = f"""---
created: {date_str}
updated: {date_str}
status: transcription
tags: [elevenlabs, audio, transcription]
---

# {original_name}

{transcription.text}

---
## Changelog
- {date_str}: Audio transcribed via ElevenLabs.
"""
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"✅ Success! Transcription saved to:")
        print(f"📄 {output_path}")
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        print("Note: Ensure your API Key has Scribe access.")
        sys.exit(1)

if __name__ == "__main__":
    main()

