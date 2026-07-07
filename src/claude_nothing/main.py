"""CLI entry point: parses args and either runs the fullscreen app or,
when stdout isn't a terminal, a quick plain-text demo."""

from __future__ import annotations

import argparse
import asyncio
import random
import sys

from rich.console import Console

from . import content, performance
from .app import ClaudeNothingApp


class PlainRunner:
    """A headless stand-in for the App, used when there's no real terminal."""

    def __init__(self, fast: bool = False):
        self.speed = 0.12 if fast else 1.0
        self.tokens = 0
        self.console = Console()

    def write(self, renderable) -> None:
        self.console.print(renderable)

    def set_spinner(self, renderable) -> None:
        pass

    def clear_spinner(self) -> None:
        pass

    def update_context(self) -> None:
        pass

    def content_width(self) -> int:
        return self.console.width


def run_plain(task: str | None, loop_demo: bool, fast: bool) -> None:
    runner = PlainRunner(fast=fast)

    async def go() -> None:
        chosen = task or random.choice(content.TASKS)
        while True:
            performance.show_user(runner, chosen)
            await performance.respond(runner, chosen)
            if not loop_demo:
                break
            chosen = random.choice(content.TASKS)

    asyncio.run(go())


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="claude-nothing",
        description="A fake Claude Code session that looks incredibly productive but does absolutely nothing.",
    )
    parser.add_argument(
        "-t", "--task", help="run a scripted demo pretending to work on this task"
    )
    parser.add_argument("--fast", action="store_true", help="pretend faster")
    parser.add_argument(
        "--loop", action="store_true", help="run autonomously forever, no input needed"
    )
    parser.add_argument(
        "--seed", type=int, help="random seed, for reproducible nothing"
    )
    args = parser.parse_args()

    if not sys.stdout.isatty():
        run_plain(args.task, args.loop, args.fast)
        return

    if args.seed is not None:
        random.seed(args.seed)

    app = ClaudeNothingApp(
        task=args.task,
        loop_demo=args.loop,
        fast=args.fast,
        seed=args.seed,
    )
    app.run()


if __name__ == "__main__":
    main()
