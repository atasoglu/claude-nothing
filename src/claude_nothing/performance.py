"""The performance itself: thinking, tool calls, diffs, agents. All fake.

Every function here is a coroutine that mutates the running App: it writes
rich-text lines to the conversation log and updates the spinner line. Since
each one awaits ``asyncio.sleep`` between steps, pressing escape cancels the
enclosing task cleanly at the next await point — that's the whole interrupt
mechanism.
"""

from __future__ import annotations

import asyncio
import random

from rich.text import Text

from . import content
from .styles import BORDER, CLAUDE, DIFF_ADD_BG, DIFF_DEL_BG, DIM, GREEN, RED


def fmt_tokens(n: int) -> str:
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


async def sleep(app, seconds: float) -> None:
    await asyncio.sleep(seconds * app.speed)


async def think(app, seconds: float, verb: str | None = None) -> None:
    verb = verb or random.choice(content.VERBS)
    duration = seconds * app.speed
    elapsed = 0.0
    frame = 0
    while elapsed < duration:
        app.tokens += random.randint(20, 90)
        spin = content.SPINNER_FRAMES[frame % len(content.SPINNER_FRAMES)]
        app.set_spinner(
            Text.from_markup(
                f" [{CLAUDE}]{spin} {verb}…[/] "
                f"[{DIM}]({int(elapsed)}s · ↑ {fmt_tokens(app.tokens)} tokens · esc to interrupt)[/]"
            )
        )
        app.update_context()
        frame += 1
        await asyncio.sleep(0.09)
        elapsed += 0.09
    app.clear_spinner()


async def thinking_block(app) -> None:
    """Extended thinking, with the internal monologue it deserves."""
    await think(app, random.uniform(1.0, 2.0), "Thinking")
    app.write(Text.from_markup(f"[italic {DIM}]✻ Thinking…[/]"))
    app.write("")
    app.write(Text.from_markup(f"  [italic {DIM}]{random.choice(content.THOUGHTS)}[/]"))
    app.write("")
    await sleep(app, 0.8)


async def say(app, text: str) -> None:
    await think(app, random.uniform(1.5, 3.5))
    app.write(Text.from_markup(f"⏺ {text}"))
    app.write("")
    await sleep(app, 0.3)


def show_user(app, text: str) -> None:
    app.write(Text.from_markup(f"[{DIM}]> {text}[/]"))
    app.write("")


async def tool_call(app, name: str, arg: str, result: str, error: bool = False) -> None:
    await think(app, random.uniform(0.8, 2.0))
    dot = RED if error else GREEN
    app.write(Text.from_markup(f"[{dot}]⏺[/] [bold]{name}[/]({arg})"))
    await sleep(app, random.uniform(0.2, 0.6))
    app.write(Text.from_markup(f"  [{BORDER}]⎿[/]  [{DIM}]{result}[/]"))
    app.write("")
    await sleep(app, 0.2)


async def bash_call(app, cmd: str, output_lines: list, error: bool = False) -> None:
    await think(app, random.uniform(0.8, 1.8))
    dot = RED if error else GREEN
    app.write(Text.from_markup(f"[{dot}]⏺[/] [bold]Bash[/]({cmd})"))
    await sleep(app, 0.3)
    for i, line in enumerate(output_lines):
        prefix = f"  [{BORDER}]⎿[/]  " if i == 0 else "     "
        app.write(Text.from_markup(f"{prefix}[{DIM}]{line}[/]"))
        await sleep(app, random.uniform(0.1, 0.4))
    app.write("")
    await sleep(app, 0.2)


async def update_tool(app, path: str) -> None:
    """An Edit with a proper colored diff, the way the real thing shows it."""
    hunk = random.choice(content.DIFF_HUNKS)
    adds = sum(1 for m, _ in hunk if m == "+")
    rems = sum(1 for m, _ in hunk if m == "-")
    await think(app, random.uniform(1.0, 2.5))
    app.write(Text.from_markup(f"[{GREEN}]⏺[/] [bold]Update[/]({path})"))
    await sleep(app, 0.4)
    app.write(
        Text.from_markup(
            f"  [{BORDER}]⎿[/]  [{DIM}]Updated {path} with {adds} addition{'s' if adds != 1 else ''}"
            f" and {rems} removal{'s' if rems != 1 else ''}[/]"
        )
    )
    ln = random.randint(18, 380)
    width = app.content_width()
    for marker, code in hunk:
        if marker == "-":
            line_text = Text(f"     {ln:>4} - {code}", style=f"{RED} on {DIFF_DEL_BG}")
        elif marker == "+":
            line_text = Text(f"     {ln:>4} + {code}", style=f"{GREEN} on {DIFF_ADD_BG}")
        else:
            line_text = Text(f"     {ln:>4}   {code}", style=DIM)
        if marker in ("-", "+") and line_text.cell_len < width:
            line_text.pad_right(width - line_text.cell_len)
        app.write(line_text)
        ln += 1
        await asyncio.sleep(0.08 * app.speed)
    app.write("")
    await sleep(app, 0.2)


async def todo_update(app, steps: list, done: int) -> None:
    """The famous checklist. Progress you can see, on work that isn't there."""
    await think(app, random.uniform(0.5, 1.2))
    app.write(Text.from_markup(f"[{GREEN}]⏺[/] [bold]Update Todos[/]"))
    for i, step in enumerate(steps):
        prefix = f"  [{BORDER}]⎿[/]  " if i == 0 else "     "
        if i < done:
            app.write(Text.from_markup(f"{prefix}[{DIM}]☒ {step}[/]", justify="left"))
        elif i == done:
            app.write(Text.from_markup(f"{prefix}[bold]☐ {step}[/]"))
        else:
            app.write(Text.from_markup(f"{prefix}☐ {step}"))
    app.write("")
    await sleep(app, 0.3)


async def subagent_phase(app) -> None:
    """Delegate the nothing. Management experience."""
    await say(app, "This is a big task — let me spin up a few agents to cover more ground.")
    tasks = random.sample(content.AGENT_TASKS, k=random.randint(2, 3))
    for t in tasks:
        app.write(Text.from_markup(f"[{GREEN}]⏺[/] [bold]Task[/]({t})"))
        app.write(Text.from_markup(f"  [{BORDER}]⎿[/]  [{DIM}]Initializing…[/]"))
        app.write("")
        await sleep(app, random.uniform(0.3, 0.7))
    await think(app, random.uniform(3.0, 5.0), "Herding")
    for t in tasks:
        uses = random.randint(6, 34)
        toks = random.randint(8, 60)
        secs = random.randint(35, 200)
        app.write(Text.from_markup(f"[{GREEN}]⏺[/] [bold]Task[/]({t})"))
        app.write(
            Text.from_markup(
                f"  [{BORDER}]⎿[/]  [{DIM}]Done ({uses} tool uses · {toks}.{random.randint(0, 9)}k tokens · "
                f"{secs // 60}m {secs % 60}s) — found nothing, which was the goal[/]"
            )
        )
        app.write("")
        await sleep(app, random.uniform(0.2, 0.5))
    await say(app, "The agents confirmed my suspicion. Proceeding with the fix.")


async def explore_phase(app) -> None:
    await say(app, random.choice(content.SAYINGS_OPENING))
    await tool_call(app, "Glob", "**/*.py", f"Found {random.randint(23, 187)} files")
    for f in random.sample(content.FILES, k=random.randint(2, 3)):
        await tool_call(app, "Read", f, f"Read {random.randint(40, 480)} lines ({random.choice(content.READ_JOKES)})")
    await tool_call(
        app,
        "Search",
        f'pattern: "{random.choice(content.GREP_PATTERNS)}"',
        f"Found {random.randint(3, 31)} matches in {random.randint(2, 9)} files",
    )
    if random.random() < 0.4:
        q, result = random.choice(content.WEB_SEARCHES)
        await tool_call(app, "WebSearch", f'"{q}"', result)


async def work_phase(app) -> None:
    for _ in range(random.randint(1, 2)):
        await say(app, random.choice(content.SAYINGS_MID))
        await update_tool(app, random.choice(content.FILES))
        if random.random() < 0.5:
            await bash_call(app, *random.choice(content.BASH_JOKES))
        if random.random() < 0.4:
            f = random.choice(content.FILES)
            await tool_call(app, "Write", f, f"Wrote {random.randint(18, 240)} lines to {f}")


async def test_phase(app) -> None:
    await say(app, random.choice(content.SAYINGS_TEST))
    total = random.randint(40, 220)
    failed = random.randint(1, 3)
    fail_file = f"tests/{random.choice(['test_api', 'test_auth', 'test_core'])}.py"
    fail_test = random.choice(
        ["test_edge_case", "test_timeout_retry", "test_invalid_token", "test_nothing_happens"]
    )
    await bash_call(
        app,
        "uv run pytest",
        [
            f"collected {total} items",
            "",
            f"[{RED}]FAILED[/][{DIM}] {fail_file}::{fail_test} - AssertionError",
            f"[{RED}]{total - failed} passed, {failed} failed[/][{DIM}] in {random.uniform(2, 14):.2f}s",
            f"… +{random.randint(12, 96)} lines (ctrl+o to expand)",
        ],
        error=True,
    )
    await say(app, "Ah, I see the problem — the mock wasn't accounting for the new retry logic. Easy fix.")
    await update_tool(app, fail_file)
    await bash_call(
        app,
        "uv run pytest",
        [
            f"collected {total} items",
            "",
            f"[{GREEN}]{total} passed[/][{DIM}] in {random.uniform(2, 14):.2f}s",
        ],
    )


async def respond(app, task: str) -> None:
    """One full turn of very convincing nothing."""
    steps = content.TODO_STEPS_CORE + random.sample(
        content.TODO_STEPS_BONUS, k=random.randint(0, 2)
    )
    if random.random() < 0.6:
        await thinking_block(app)
    await todo_update(app, steps, 0)
    await explore_phase(app)
    await todo_update(app, steps, 2)
    await work_phase(app)
    if random.random() < 0.35:
        await subagent_phase(app)
    await todo_update(app, steps, 3)
    if random.random() < 0.75:
        await test_phase(app)
    await todo_update(app, steps, len(steps))
    await say(app, random.choice(content.SAYINGS_DONE))
