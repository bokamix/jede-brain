import os
import time
import json
import random
import fcntl
from pathlib import Path
from datetime import datetime

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
TOOLS_DIR = BASE_DIR / "tools"
GUARD_DIR = TOOLS_DIR / ".guard"
QUEUE_DIR = GUARD_DIR / "queues"
LOCK_DIR = GUARD_DIR / "locks"
GUARD_STATE_PATH = GUARD_DIR / "state.json"

# Legacy path for migration
OLD_CONFIG_PATH = BASE_DIR / "config" / "scraping_guard.json"

DEFAULT_GUARD_CONFIG = {
    "services": {
        "youtube": {
            "min_delay": 60,
            "max_delay": 180,
            "max_per_hour": 10
        },
        "default": {
            "min_delay": 5,
            "max_delay": 15,
            "max_per_hour": 100
        }
    },
    "state": {}
}

class GuardCore:
    def __init__(self, service_name):
        self.service_name = service_name
        self._ensure_infrastructure()
        self.config = self._load_config()
        self.service_config = self.config["services"].get(service_name, self.config["services"]["default"])
        self.queue_path = QUEUE_DIR / service_name
        self.queue_path.mkdir(parents=True, exist_ok=True)
        self.lock_file = LOCK_DIR / f"guard_{service_name}.lock"
        
        # Ensure state entry
        if service_name not in self.config["state"]:
            self.config["state"][service_name] = {"last_run": 0, "history": []}
            self._save_config()

    def _ensure_infrastructure(self):
        GUARD_DIR.mkdir(parents=True, exist_ok=True)
        QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        LOCK_DIR.mkdir(parents=True, exist_ok=True)
        
        # Migration from legacy config
        if OLD_CONFIG_PATH.exists() and not GUARD_STATE_PATH.exists():
            try:
                with open(OLD_CONFIG_PATH, "r") as f:
                    old_data = json.load(f)
                # We only want to migrate 'services' config and 'state'
                # We do NOT migrate 'queues' as they were in the JSON structure before, 
                # but now we use file-based queues. Old pending jobs in JSON will be lost/ignored.
                new_data = DEFAULT_GUARD_CONFIG.copy()
                if "services" in old_data:
                    new_data["services"] = old_data["services"]
                if "state" in old_data:
                    new_data["state"] = old_data["state"]
                    
                with open(GUARD_STATE_PATH, "w") as f:
                    json.dump(new_data, f, indent=4)
                    
                # Rename old file to avoid confusion (or delete?)
                os.rename(OLD_CONFIG_PATH, str(OLD_CONFIG_PATH) + ".migrated")
            except Exception:
                pass # Fail silently and use default
        
        if not GUARD_STATE_PATH.exists():
            with open(GUARD_STATE_PATH, "w") as f:
                json.dump(DEFAULT_GUARD_CONFIG, f, indent=4)

    def _load_config(self):
        # Simple read, atomic write is handled in save
        with open(GUARD_STATE_PATH, "r") as f:
            return json.load(f)

    def _save_config(self):
        # Atomic write to avoid corruption
        temp_path = str(GUARD_STATE_PATH) + ".tmp"
        with open(temp_path, "w") as f:
            json.dump(self.config, f, indent=4)
        os.replace(temp_path, GUARD_STATE_PATH)

    def can_proceed(self):
        """Checks rules (delay + rate limit). Returns (bool, wait_time)."""
        # Reload config to get latest state
        self.config = self._load_config()
        state = self.config["state"][self.service_name]
        
        last_run = state["last_run"]
        now = time.time()
        
        # 1. Jitter Delay
        # Note: In a real persistent system, we might want to store the target 'next_run' time
        # instead of calculating random delay every time, but for now this is safe enough.
        min_d = self.service_config.get("min_delay", 0)
        max_d = self.service_config.get("max_delay", 0)
        # We use min_delay for checking "can I run NOW", assuming randomization happens during wait
        required_delay = min_d 
        
        if now - last_run < required_delay:
            return False, required_delay - (now - last_run)

        # 2. Hourly Limit
        history = [t for t in state["history"] if now - t < 3600]
        if len(history) >= self.service_config.get("max_per_hour", 9999):
            # Calculate when the oldest slot frees up
            if history:
                oldest = min(history)
                wait_until = oldest + 3601
                return False, max(0, wait_until - now)
            return False, 60 # Fallback

        return True, 0

    def register_run(self):
        """Log a successful run to state."""
        self.config = self._load_config() # Reload first
        now = time.time()
        state = self.config["state"][self.service_name]
        
        state["last_run"] = now
        # Clean history
        state["history"] = [t for t in state["history"] if now - t < 3600]
        state["history"].append(now)
        
        self.config["state"][self.service_name] = state
        self._save_config()

    def enqueue_command(self, command_args, cwd):
        """Creates a job file in the file-based queue."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        job_id = f"job_{timestamp}"
        job_file = self.queue_path / f"{job_id}.json"
        
        job_data = {
            "id": job_id,
            "created_at": time.time(),
            "command": command_args,
            "cwd": cwd,
            "status": "pending"
        }
        
        with open(job_file, "w") as f:
            json.dump(job_data, f, indent=4)
            
        return job_file

    def get_next_job(self):
        """Returns the path to the oldest job file, or None."""
        files = sorted(list(self.queue_path.glob("job_*.json")))
        if files:
            return files[0]
        return None

    def acquire_ghost_lock(self):
        """Tries to acquire the lock for the background processor."""
        # Using the same logic as before: flock
        self.f_lock = open(self.lock_file, "a+")
        try:
            fcntl.flock(self.f_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # Write PID
            self.f_lock.truncate(0)
            self.f_lock.write(str(os.getpid()))
            self.f_lock.flush()
            return True
        except IOError:
            self.f_lock.close()
            return False

    def release_ghost_lock(self):
        if hasattr(self, 'f_lock') and self.f_lock:
            fcntl.flock(self.f_lock, fcntl.LOCK_UN)
            self.f_lock.close()
            try:
                os.remove(self.lock_file)
            except:
                pass

