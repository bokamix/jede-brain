# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "firebase-admin",
#     "click",
#     "pyperclip",
# ]
# ///

"""
TOOL: File Uploader
DESCRIPTION: Uploads a selected file to Firebase Storage and generates a public URL.
USAGE: ./tools/run run tools/scripts/upload_to_firebase.py <file_path> OR leave blank for GUI
CONFIG: Requires 'config/firebase.json' (Service Account Key)
"""

import os
import sys
import click
import firebase_admin
from firebase_admin import credentials, storage
from pathlib import Path
import subprocess
import pyperclip

# --- Configuration Management ---
# Define paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "../../config")
DEFAULT_KEY_PATH = os.path.join(CONFIG_DIR, "firebase.json")
DEFAULT_BUCKET_ENV = "superfunction-c5136.appspot.com"

def pick_file_gui():
    """Open a native file picker dialog (macOS/Linux/Windows)."""
    # 1. macOS (AppleScript) - Best integration
    if sys.platform == 'darwin':
        try:
            cmd = "osascript -e 'POSIX path of (choose file with prompt \"Select file to upload to Firebase\")'"
            result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
            return result
        except subprocess.CalledProcessError:
            return None # Cancelled
            
    # 2. Linux (Zenity) - Common on Linux desktops
    try:
        if subprocess.call(["which", "zenity"], stdout=subprocess.DEVNULL) == 0:
            cmd = ["zenity", "--file-selection", "--title=Select file to upload"]
            return subprocess.check_output(cmd).decode('utf-8').strip()
    except:
        pass

    # 3. Fallback: Python Tkinter (Universal but ugly)
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        # Bring to front hack
        root.lift()
        root.attributes('-topmost',True)
        root.after_idle(root.attributes,'-topmost',False)
        
        file_path = filedialog.askopenfilename(title="Select file to upload to Firebase")
        root.destroy()
        return file_path if file_path else None
    except Exception as e:
        click.echo(f"❌ GUI Error: {e}", err=True)
        return None

def get_config():
    """Load config with error handling compliant with Mental Refinery rules."""
    
    # 1. Check Key
    key_path = os.environ.get("FIREBASE_CREDENTIALS", DEFAULT_KEY_PATH)
    if not os.path.exists(key_path):
        click.echo(f"❌ Config Error: Credential file not found at: {key_path}", err=True)
        click.echo(f"💡 Fix: Copy 'config/firebase.example.json' to '{key_path}' and fill it.")
        sys.exit(1)
        
    # 2. Check Bucket (inside JSON or Env)
    # We load it later when initing app, or from ENV
    # Fixed: Treat DEFAULT_BUCKET_ENV as the value itself if env var not found
    bucket_name = os.environ.get("FIREBASE_BUCKET", DEFAULT_BUCKET_ENV)
    
    return key_path, bucket_name

@click.command()
@click.argument('file_path', required=False, type=click.Path(exists=True))
@click.option('--bucket', help='Override bucket name')
def main(file_path, bucket):
    """
    GUI or CLI based file uploader for Firebase.
    If file_path is provided, uploads it directly.
    Otherwise, opens a system file picker.
    """
    # 1. Get Config
    key_path, env_bucket = get_config()
    final_bucket = bucket or env_bucket
    
    if not final_bucket:
        click.echo("❌ Config Error: Bucket name missing.", err=True)
        click.echo(f"💡 Fix: Set {DEFAULT_BUCKET_ENV} in .env or pass --bucket.")
        sys.exit(1)

    # 2. Pick File (CLI or GUI)
    if not file_path:
        print("📂 No file argument provided. Opening file picker...")
        file_path = pick_file_gui()
    
    if not file_path:
        print("❌ No file selected.")
        return

    path = Path(file_path)
    print(f"🚀 Preparing to upload: {path.name}")

    try:
        # 3. Init Firebase
        cred = credentials.Certificate(key_path)
        try:
            app = firebase_admin.get_app()
        except ValueError:
            app = firebase_admin.initialize_app(cred, {
                'storageBucket': final_bucket
            })
            
        # 4. Upload
        bucket_obj = storage.bucket()
        blob = bucket_obj.blob(path.name)
        
        print(f"⏳ Uploading ({path.stat().st_size / 1024:.2f} KB)...")
        blob.upload_from_filename(file_path)
        blob.make_public()
        
        url = blob.public_url
        
        # 5. Success
        print("\n" + "="*50)
        print(f"✅ UPLOAD SUCCESS")
        print(f"🔗 URL: {url}")
        print("="*50)
        
        # Copy to clipboard
        try:
            pyperclip.copy(url)
            print("📋 Copied to clipboard!")
        except:
            pass
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
