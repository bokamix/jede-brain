---
created: 2025-12-20 18:30
updated: 2026-02-09 21:00
tags: [readme, documentation, infrastructure]
---
# Codebase Second Brain

Turn your terminal into a Personal Knowledge Management (PKM) system.
Stop switching between Notion, Obsidian, and VS Code. Keep everything where you code.

## Fast Start

1.  **Clone the Repo:**
    ```bash
    git clone https://github.com/bokamix/jede-brain.git
    cd jede-brain
    ```

2.  **Launch Claude Code:**
    ```bash
    claude
    ```

3.  **Initialize the Brain:**
    Type in the conversation:
    > **Co moge zrobić w tym projekcie? Jakie są założenia? Jak używać tools?**
    > *(English: "What can I do in this project? What are the assumptions? How to use tools?")*

    Claude Code will read the `CLAUDE.md` files and understand the full system.

## Philosophy

This system treats your life and knowledge like a software project.
- **00_Stream:** Your daily log / `console.log` for your brain.
- **10_Projects:** Where "features" are built.
- **20_Knowledge:** Your documentation / StackOverflow.
- **05_Reading_Room:** Your `Downloads` folder that actually gets cleaned up.

## Responsible Scraping (Iron Dome)

To avoid IP bans, we use a central interceptor called **Iron Dome**.
It automatically manages rate limits and queues tasks in the background without changing the tool's code.
Check `tools/policies.json` to see protected tools.

- **Safe Mode:** Scripts automatically queue tasks if they detect a risk of ban.
- **Asynchronous Processing:** Results might not be immediate. A sound will play when your data is ready.
- **Background Work:** A "ghost process" handles the queue in the background. Do not close your computer for continuous processing.

## Agents (The Team)

The repository uses `CLAUDE.md` files in each directory to give specific personalities to different zones:

*   **Morning Gardener (`00_Stream`)**: Helps you start the day, handles brain dumps, detects burnout patterns.
*   **Manager (`10_Projects`)**: Breaks down tasks, prevents scope creep, keeps you focused.
*   **Librarian (`05_Reading_Room`)**: Summarizes content, filters noise, demands "Zero Inbox".
*   **Curator (`20_Knowledge`)**: Connects dots between notes, quizzes you (Active Recall).
*   **Tool Operator (`tools/`)**: Automatically runs Python scripts for YouTube transcription and research.

## Tools Included

The `tools/` directory contains Python scripts powered by **uv**.
We provide a wrapper script `./tools/run` that handles installation automatically.

- **YouTube Transcriber**: `./tools/run run tools/scripts/youtube_transcript.py [URL]`
- **YouTube Finder**: `./tools/run run tools/scripts/yt_finder.py [QUERY]`

*You don't need to run them manually. Just ask Claude Code: "Transcribe this video..."*

### Configuration
If a tool needs API keys, look into `config/` folder. Copy `*.example.json` to `*.json` and fill your data.

## International Support

The core logic (CLAUDE.md files) is written in English for maximum compatibility, but the Agents are trained to **respond in your language**.
Configure your preferences in [ME.md](./ME.md).

---
## Changelog
- 2025-12-20 18:30: Added Scraping Guard documentation and metadata.
- 2026-02-09 21:00: Migrated from Cursor (.cursor/rules) to Claude Code (CLAUDE.md).

