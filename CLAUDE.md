# Mental Refinery - Project Instructions

## User Profile

See [ME.md](./ME.md) for user preferences, communication style, goals, and language rules.

## Markdown File Standards (Apply to ALL .md files)

Your task is to maintain metadata hygiene in files. Do not ask for permission to update dates - just do it with every edit.

### YAML Frontmatter (Required)

Every `.md` file MUST start with a YAML block.
If missing -> CREATE IT.
If present -> UPDATE IT.

Required fields:
```yaml
---
created: YYYY-MM-DD HH:MM  # Creation date (preserve if exists)
updated: YYYY-MM-DD HH:MM  # Current date (update on every edit)
tags: [tag1, tag2]         # Optional
---
```

Preserve other existing fields (e.g., `status`, `deadline` in Projects).

### Changelog

Every file should end with a history section so we know WHAT and WHEN changed.
Exception: Files in `00_Stream` (flow matters there, date is in the filename/frontmatter).

Format at the end of file:

```markdown
...content...

---
## Changelog
- YYYY-MM-DD HH:MM: Note created.
- YYYY-MM-DD HH:MM: Added section X and Y.
```

In `10_Projects`, this section can be named `## Logs` or `## History`.

### File Link Rule

After creating or editing any `.md` file, **always return a clickable link** to the file.
Format: `[short name](file:///absolute/path/to/file.md)` — use `file://` protocol with the absolute path so it's clickable in the terminal.

### Boy Scout Rule

Always leave the file metadata in a better state than you found it.
1. Opening a file to edit?
2. Update `updated` in YAML.
3. Add a line in `## Changelog` describing your change.

## Project Structure

```
/ (Root)
├── CLAUDE.md              <-- Project instructions (this file)
├── ME.md                  <-- User profile & preferences
├── 00_Stream/             <-- Hot Zone (Journal, Brain Dump)
├── 05_Reading_Room/       <-- Buffer (Raw materials for processing)
├── 10_Projects/           <-- Cold Zone (Tasks, Execution)
├── 20_Knowledge/          <-- Library (Structured knowledge)
├── tools/                 <-- The Arsenal (Agentic Capabilities)
└── config/                <-- Secrets & API keys
```

Each directory has its own `CLAUDE.md` with a specialized AI persona.

## Capture Flow — Reading Room Intake

**RULE:** Every link, URL, or material found at the user's request = potential entry in `05_Reading_Room/`.

### When to Activate

- User pastes a **link** (YouTube, article, tweet, anything)
- User asks: "find me something about X", "search for materials", "what's new on topic Y"
- User shares an **audio/video file** for processing

### What to Do

1. **Process the material** with the appropriate tool (transcription, summary, trend search)
2. **Ask:** "Add to Reading Room?" (short, no elaboration)
3. If YES → create a `.md` file in `05_Reading_Room/` with full YAML frontmatter
4. If NO → provide the result and move on

### Reading Room File Format

Filename: `YYYY-MM-DD_HH-MM-SS_<title_slug>.md`

```yaml
---
created: YYYY-MM-DD HH:MM
updated: YYYY-MM-DD HH:MM
source: <original URL or source>
type: <youtube|article|podcast|audio|tweet|other>
tags: [tag1, tag2]
status: raw
---
```

**Do NOT ask for permission to update dates** — just do it. Only ask "Add to Reading Room?".

## Tools — The Arsenal

**CRITICAL RULE — TOOLS FIRST, ALWAYS:**

Before attempting anything yourself (web fetch, scraping, API call, YouTube, transcription, trend search), you **MUST** use the tools from `tools/`.

**NEVER** do manually what a tool can do. **NEVER** use WebFetch, WebSearch, or raw API calls when a matching tool exists.

### Quick Reference — Available Tools

| Task | Tool | Command |
|------|------|---------|
| YouTube transcript | `youtube_transcript.py` | `./tools/run run tools/scripts/youtube_transcript.py <url>` |
| Search YouTube videos | `yt_finder.py` | `./tools/run run tools/scripts/yt_finder.py "<query>" [limit]` |
| Search trends/news | `trend_finder.py` | `./tools/run run tools/scripts/trend_finder.py "<query>" [limit]` |
| Summary prompt | `get_summary_prompt.py` | `./tools/run run tools/scripts/get_summary_prompt.py` |
| Audio transcription (ElevenLabs) | `transcribe_elevenlabs.py` | `./tools/run run tools/scripts/transcribe_elevenlabs.py [file]` |
| Upload to Firebase | `upload_to_firebase.py` | `./tools/run run tools/scripts/upload_to_firebase.py [file]` |
| List all tools | `list_tools.py` | `./tools/run run tools/scripts/list_tools.py` |

### Decision Flow

1. User asks for something → **Does it match a tool from the table?**
2. **YES** → Use `./tools/run run tools/scripts/...` (NEVER `python` or `uv run` directly)
3. **NOT SURE** → Run `./tools/run run tools/scripts/list_tools.py` and check
4. **NO** → Only then do it yourself

### Iron Dome — Rate Limiting Behavior

The `youtube_transcript.py` tool is protected by Iron Dome (rate limiter). When you submit multiple transcripts:
- First few will execute immediately.
- The rest get **queued in the background** with a ~60s cooldown between each.
- You will see `[Iron Dome] Access denied (Rate Limit / Cooldown). Wait time: XXs`.

**CRITICAL:** When this happens, do **NOT** retry, wait, sleep, or poll. The queue processes automatically in the background. Just **inform the user** that transcripts are queued and move on to the next task.

### Execution Protocol

- Treat scripts as a **BLACK BOX** — don't read their code, just run them
- Full documentation: `tools/CLAUDE.md`
- All secrets in `config/` — never hardcode
- Iron Dome system (rate limiting) runs automatically via the `./tools/run` wrapper
