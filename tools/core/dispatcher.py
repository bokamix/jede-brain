import sys
import os
import json
import subprocess
import time
import random
from pathlib import Path
from guard_core import GuardCore

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
POLICIES_PATH = BASE_DIR / "tools" / "policies.json"

def load_policies():
    if not POLICIES_PATH.exists():
        return {}
    with open(POLICIES_PATH, "r") as f:
        return json.load(f)

def spawn_ghost(service_name):
    """Spawns the background processor (detached)."""
    script_path = Path(__file__).parent / "ghost.py"
    # Use sys.executable to ensure we use the same python (uv environment)
    subprocess.Popen(
        [sys.executable, str(script_path), service_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

def main():
    # Args from ./tools/run: [dispatcher.py, script_path, arg1, arg2...]
    if len(sys.argv) < 2:
        print("Usage: dispatcher.py <script_path> [args...]")
        sys.exit(1)

    script_path_raw = sys.argv[1]
    script_args = sys.argv[2:]
    
    # Normalize path relative to repo root for policy matching
    # script_path might be absolute or relative
    try:
        abs_script = Path(script_path_raw).resolve()
        abs_root = BASE_DIR.resolve()
        rel_path = abs_script.relative_to(abs_root)
        policy_key = str(rel_path)
        # Fix: if run via "tools/scripts/..." vs "scripts/..."
        # We try to match end of string in policies if exact match fails
    except ValueError:
        # Script is outside repo? Unlikely but fallback
        policy_key = script_path_raw

    policies = load_policies()
    
    # Find policy
    policy = policies.get(policy_key)
    if not policy:
        # Try matching by suffix (e.g. "scripts/yt_finder.py")
        for k, v in policies.items():
            if policy_key.endswith(k):
                policy = v
                break
    
    if not policy:
        policy = policies.get("default", {"guard": "none"})

    guard_service = policy.get("guard", "none")
    
    # --- EXECUTION LOGIC ---
    
    if guard_service == "none":
        # Direct execution via uv to ensure dependencies are handled
        # We need to find the 'uv' command. Since we are running inside uv, 
        # we can assume 'uv' is in PATH or use the one from tools/run wrapper if passed via env
        uv_cmd = os.environ.get("UV_CMD", "uv")
        cmd = [uv_cmd, "run", script_path_raw] + script_args
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            sys.exit(e.returncode)
            
    else:
        # Guarded execution
        print(f"[Iron Dome] Policy active: Guard '{guard_service}'")
        guard = GuardCore(guard_service)
        
        can_run, wait_time = guard.can_proceed()
        
        if can_run:
            print("[Iron Dome] Access granted. Executing...")
            uv_cmd = os.environ.get("UV_CMD", "uv")
            cmd = [uv_cmd, "run", script_path_raw] + script_args
            try:
                subprocess.run(cmd, check=True)
                guard.register_run() # Success! Update limits
                
                # Check if there is a queue (maybe we jumped ahead?)
                # If so, spawn ghost to clean up
                if guard.get_next_job():
                    spawn_ghost(guard_service)
                    
            except subprocess.CalledProcessError as e:
                print(f"[Iron Dome] Script failed with code {e.returncode}")
                sys.exit(e.returncode)
        else:
            print(f"[Iron Dome] Access denied (Rate Limit / Cooldown).")
            print(f"            Wait time: {int(wait_time)}s")
            
            # Queue it
            cwd = os.getcwd()
            # We store the command to run with UV
            uv_cmd = os.environ.get("UV_CMD", "uv")
            full_cmd = [uv_cmd, "run", str(abs_script)] + script_args
            
            job_file = guard.enqueue_command(full_cmd, cwd)
            
            print(f"[Iron Dome] 🛡️ Job queued safely.")
            print(f"            ID: {job_file.name}")
            print(f"            Status: Background process will execute this shortly.")
            
            # Trigger ghost
            spawn_ghost(guard_service)

if __name__ == "__main__":
    main()

