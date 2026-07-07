# claude-nothing

A fake Claude Code session that looks incredibly productive but does **absolutely nothing**.

Inspired by [install-nothing](https://github.com/buyukakyuz/install-nothing).

It's a real fullscreen terminal chat, styled after the actual Claude Code UI: the welcome banner, the todo checklist, the extended-thinking block, colored diffs, subagents, slash commands, `!shell` mode — all of it. Type any task and it thinks hard (`✻ Reticulating…`), reads files that don't exist, edits code that isn't there, spins up subagents to look extra busy, watches a test fail dramatically, fixes it heroically, and finishes with all tests green — while touching exactly zero bytes on your disk.

Perfect for:

- Looking busy on a screen share
- Impressing people walking past your desk
- Feeling productive without the burden of producing anything

## Usage

Run it instantly, no install required:

```sh
uvx claude-nothing
```

Or install it as a tool:

```sh
uv tool install claude-nothing
claude-nothing
```

Working from a local checkout of this repo instead:

```sh
uv run claude-nothing
```

Type anything and press enter. Real slash commands work too: `/help`, `/status`, `/cost`, `/clear`, `/compact`... none of them do anything either. `!command` runs a fake shell command. `Esc` interrupts mid-turn, `Ctrl+C` twice exits.

### Options

| Flag | What it pretends to do |
| --- | --- |
| `-t, --task "..."` | run one scripted demo turn for this task, then exit |
| `--fast` | pretend faster |
| `--loop` | run autonomously forever, no input needed, until you exit |
| `--seed N` | reproducible nothing |

### Examples

```sh
# Watch one demo turn play out, then exit
claude-nothing -t "rewrite the billing system in Rust"

# Infinite productivity, unattended — never waits for input
claude-nothing --loop

# The exact same nothing, every time
claude-nothing --seed 42
```

Piped into a file or another program (no real terminal attached), it falls back to printing one plain-text demo turn instead of the fullscreen UI.

## What it actually does

```
0 files changed, 0 insertions(+), 0 deletions(-)
```

Exactly as planned.
