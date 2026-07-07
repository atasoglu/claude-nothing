# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A joke Textual TUI app that mimics a Claude Code session's UI and produces entirely scripted, randomized fake output — no real file access, no real tool execution, no real LLM calls. All "thinking," "tool calls," and "diffs" are canned strings from `content.py` played back with fake timing by `performance.py`.

## Commands

```sh
uv sync                     # install dependencies
uv run claude-nothing        # run the fullscreen TUI
uv run claude-nothing -t "some task" --fast --seed 42   # scripted single demo turn, fast, reproducible
python -m py_compile src/claude_nothing/*.py             # quick syntax check (no test suite exists)
```

There is no test suite, linter, or build step configured beyond the `uv_build` backend in `pyproject.toml`.

## Architecture

- `main.py` — argument parsing and entry point. If stdout isn't a TTY (e.g. piped output), it runs `run_plain()`, a headless `PlainRunner` that prints one plain-text demo turn via `rich.Console` instead of launching the Textual app. Otherwise it constructs and runs `ClaudeNothingApp`.
- `app.py` — the Textual `App` subclass (`ClaudeNothingApp`). Owns the log widget, spinner, input box, slash-command menu, and history/interrupt handling. Slash commands (`/help`, `/status`, `/clear`, etc.) are handled directly in `run_slash()`; `!cmd` triggers `run_shell()` (also fake).
- `performance.py` — the "performance" itself: a set of async functions (`thinking_block`, `explore_phase`, `work_phase`, `test_phase`, `subagent_phase`, `todo_update`, etc.) that write rich-text lines to the app's log with `asyncio.sleep` delays between steps. `respond()` composes these phases into one full randomized turn. Both `ClaudeNothingApp` and `PlainRunner` are duck-typed targets for these functions — they just need `write()`, `set_spinner()`, `clear_spinner()`, `update_context()`, `content_width()`, `tokens`, and `speed`.
- `content.py` — all fake data: thinking verbs, file lists, grep patterns, sayings, diff hunks, todo steps, agent task names, spinner frames, model name/version strings.
- `widgets.py` — `home_panel()` (startup banner matching the real Claude Code welcome screen), `StatusBar`, `SlashMenu`, `below_banner_notices()`.
- `styles.py` — color constants matched to the real Claude Code palette (used as `[color]` markup tags via `rich.text.Text.from_markup`).

## Key conventions

- Every "action" (tool call, diff, bash output) is a coroutine in `performance.py` that takes the app instance as its first argument and calls `app.write(...)` / `await sleep(app, seconds)`. New fake behaviors should follow this same pattern rather than writing to widgets directly.
- Timing always goes through `sleep(app, seconds)` / `think(app, seconds, verb)`, which scale by `app.speed` (set via `--fast`) — never call `asyncio.sleep` with a raw literal for user-visible pacing.
- `Text.from_markup` with the color constants from `styles.py` is the standard way to build colored output lines, matching the real CLI's visual style.
- Interrupts (Esc/Ctrl+C) work by cancelling the Textual worker running the current turn; since each phase function awaits between every line, cancellation lands cleanly at the next `await`.
