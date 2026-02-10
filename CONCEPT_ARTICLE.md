---
created: 2025-12-20 12:00
updated: 2026-02-09 21:00
tags: [concept, productivity, ai, engineering, system, manifesto, agentic]
---

# Mental Refinery: Mind Engineering in the Age of AI
## Why Your "Second Brain" Is Broken and How to Fix It with Code

Most productivity systems (Notion, Obsidian, Evernote) share one critical flaw: **they treat your emotions and your tasks exactly the same.** They dump "depressive Tuesday entry" and "Q4 marketing strategy" into the same bucket.

The result? Cognitive noise. When you want to work, you stumble upon your fears. When you want to rest or process emotions, deadlines attack you.

The solution isn't another app with a pretty UI. The solution is **software engineering applied to psychology**.

Here is the concept of **Mental Refinery** – a system based on a development environment (Claude Code CLI) that radically separates "Fire" (emotions) from "Ice" (logic), using contextual Artificial Intelligence.

---

### 1. Philosophy: Fire and Ice

The system is based on the assumption that your brain operates in two conflicting modes that require two different environments and – crucially – two different AI assistants.

#### Hot Zone (Hot Storage) 🔥
*   **Goal:** Therapy, Brain Dump, dealing with chaos, uncensored creativity.
*   **Rule:** Here, you are allowed to complain, be afraid, and be unproductive.
*   **AI Persona:** "The Therapist." Empathetic, non-judgmental, asks questions in the CBT (Cognitive Behavioral Therapy) vein. It doesn't care about your deadlines.

#### Cold Zone (Cold Storage) 🧊
*   **Goal:** Execution, project management, hard knowledge, wiki.
*   **Rule:** Here, only facts, dates, "Definition of Done," and delivery matter.
*   **AI Persona:** "The Senior Manager." Ruthless, concrete, goal-oriented. It doesn't care about your feelings, only the task status.

---

### 2. System Architecture (Docs-as-Code)

Instead of a clickable app, we use a Markdown file structure with Claude Code (CLI). Why? Because it gives full control, versioning (Git), and scriptability.

#### Directory Structure
```text
/ (Root)
├── CLAUDE.md            <-- System Brain (Root instructions for AI)
├── 00_Stream/           <-- Hot Zone (Journal) + CLAUDE.md (Therapist persona)
├── 10_Projects/         <-- Cold Zone (Tasks) + CLAUDE.md (Manager persona)
├── 20_Knowledge/        <-- Library (Zettelkasten) + CLAUDE.md (Curator persona)
└── tools/               <-- The Arsenal + CLAUDE.md (Tool Operator persona)
```

---

### 3. "Ghost in the Shell": Contextual AI

This is the "Killer Feature" of this system. We use `CLAUDE.md` files (Claude Code's native configuration) in each directory to change the language model's behavior depending on which folder you are in.

**Scenario A: You are in the `00_Stream` folder**
You write: *"I don't feel like doing this project, I feel it's pointless."*
*   **Traditional AI:** "Maybe make a to-do list and use the Pomodoro technique?" (ERROR! This breeds frustration).
*   **Mental Refinery AI:** "Sounds like burnout. Do you think the project is objectively pointless, or is it your fatigue speaking? What exactly is triggering this resistance?" (Therapist Mode).

**Scenario B: You are in the `10_Projects` folder**
You write: *"I don't feel like doing this project, I feel it's pointless."*
*   **Mental Refinery AI:** "This is not a substantive update. Is the project blocked? If not, what is the ETA for the next milestone? If you are challenging the business case, update the `Strategy.md` file." (Manager Mode).

---

### 4. Crystallization Process (Workflow)

The system doesn't work if these two zones don't communicate. The connecting process is **Crystallization**.

1.  **Raw Input:** Every day, you dump unkempt thoughts into `00_Stream`.
2.  **Refinement:** Once a week (Weekly Review), you review these notes.
3.  **Crystallization:** You decide what is just an emotion (stays in the archive) and what is a real idea (moved to `10_Projects` and formatted as a task).

This way, your To-Do list isn't a graveyard of wishes, and your journal isn't a list of chores.

---

### 5. The Hands: Agentic Capabilities

A brain without hands is just a dreamer. Mental Refinery goes beyond text generation by giving the AI **tools** to interact with the outside world.

*   **The "Black Box" Protocol:** The AI operates under a strict "Run, Don't Read" policy. It doesn't waste tokens analyzing how a script works; it simply executes it like a CLI operator.
*   **Discovery First:** Before acting, the AI scans the available arsenal (`list_tools.py`) to understand its capabilities dynamically.
*   **Headless First:** Tools are designed to be run autonomously by the AI (passing file paths via CLI arguments), with GUI interfaces only as a fallback for human operators.
*   **Zero-Dependency Hell:** We use `uv` (by Astral) to manage Python tools. The system is self-bootstrapping. You don't install libraries; the tools install themselves in isolated environments when the AI calls them.

**Example Capabilities:**
*   *Research:* "Watch this YouTube video and extract mental models" (via `youtube_transcript.py`).
*   *Deployment:* "Upload this report to the cloud" (via `upload_to_firebase.py`).
*   *Market Analysis:* "Find trending topics in this niche" (via `trend_finder.py`).

This turns the IDE from a text editor into a **Command Center**.

---

### Summary

"Mental Refinery" is an attempt to tame human nature using developer tools. It is a system for people who understand that productivity doesn't come from a better calendar, but from better management of one's own psyche and separating the creative process (chaos) from the executive process (order).

---
## Changelog
- 2025-12-20 12:00: Created English translation of the concept for publication.
- 2025-12-20 16:30: Added Section 5 "The Hands" covering the Agentic Tools architecture (uv, black box protocol).
- 2025-12-20 17:00: Updated Section 5 with "Headless First" and "Discovery First" protocols.
- 2026-02-09 21:00: Migrated architecture from Cursor (.cursor/rules) to Claude Code (CLAUDE.md).
