---
created: 2025-12-20 18:31
updated: 2025-12-20 18:31
tags: [tools, setup, guard]
---
# Mental Refinery Tools Setup Guide

We use **uv** to manage tools. To make it easy, we include a wrapper script `./tools/run`.

## 1. Zero Setup Usage

You don't need to install anything. Just run the wrapper. It will download what it needs locally.

**Find Videos:**
```bash
./tools/run run tools/scripts/yt_finder.py "Topic"
```

**Transcribe Video:**
```bash
./tools/run run tools/scripts/youtube_transcript.py URL
```

## 2. Configuration (Secrets)

Some tools (like Firebase uploader) require keys.
We keep them in the `config/` folder.

**How to configure a tool:**
1. Look for an example file in `config/` (e.g., `firebase.example.json`).
2. Duplicate it and remove `.example`.
3. Fill in your real keys.
4. **Git ignores these files automatically.** You are safe.

## 3. Iron Dome (Protection System)

We use a central interceptor managed by `tools/core/dispatcher.py`.
You don't need to modify your scripts to add protection.

**To protect a tool:**
1. Open `tools/policies.json`.
2. Add your script path and assign a guard profile:
   ```json
   "scripts/my_tool.py": { "guard": "youtube", "log": true }
   ```

**Available Guards:**
*   `youtube`: Strict rate limits for YouTube API.
*   `default`: Generic protection.
*   `none`: No protection (direct execution).

## Troubleshooting

*   **"Permission denied":** Run `chmod +x tools/run`.

---
## Changelog
- 2025-12-20 18:32: Added Scraping Guard documentation.
