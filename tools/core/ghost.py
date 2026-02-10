import sys
import os
import time
import subprocess
import json
from guard_core import GuardCore

def play_sound(sound_name="Glass"):
    try:
        subprocess.run(["afplay", f"/System/Library/Sounds/{sound_name}.aiff"], check=False)
    except:
        pass

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
        
    service_name = sys.argv[1]
    guard = GuardCore(service_name)
    
    # Try to acquire lock - if fail, another ghost is working, so we exit
    if not guard.acquire_ghost_lock():
        sys.exit(0)
        
    try:
        while True:
            # 1. Check for jobs
            job_file = guard.get_next_job()
            if not job_file:
                break # Queue empty
                
            # 2. Check limits
            can_run, wait_time = guard.can_proceed()
            
            if not can_run:
                # Wait safely
                time.sleep(max(wait_time, 1))
                continue
                
            # 3. Process Job
            with open(job_file, "r") as f:
                job_data = json.load(f)
                
            cmd = job_data["command"]
            cwd = job_data["cwd"]
            
            # Execute
            # We assume the job will print output to stdout/stderr or files
            # Since this is detached, output might be lost unless redirected.
            # Ideally, tools should write to files (like transcripts).
            try:
                subprocess.run(cmd, cwd=cwd, check=True)
                
                # Success
                guard.register_run()
                play_sound("Glass")
                
                # Remove job file ONLY on success
                os.remove(job_file)
                
            except Exception as e:
                # Job failed. 
                # Strategy: For now, we keep it but maybe rename to .failed?
                # Or just keep trying? Endless loop risk.
                # Let's rename to .failed to unblock queue
                failed_path = str(job_file) + ".failed"
                os.rename(job_file, failed_path)
                
    finally:
        guard.release_ghost_lock()

if __name__ == "__main__":
    main()


