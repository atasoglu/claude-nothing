"""Custom widgets: the home banner, the status bar, and the slash-command menu."""

from __future__ import annotations

import getpass
import os

from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual.containers import Horizontal
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from . import content
from .styles import BLUE, BORDER, CLAUDE, DIM


def home_panel(width: int) -> Panel:
    """The startup banner: a rounded box with the version in its top border,
    two columns inside separated by a vertical rule, matching the real
    Claude Code home screen."""
    user = getpass.getuser()
    cwd = os.getcwd().replace(os.path.expanduser("~"), "~")
    box_w = max(width - 2, 40)
    two_cols = box_w >= 80

    def line(text: str, style: str = "") -> Text:
        return Text(text, style=style, no_wrap=True, overflow="ellipsis")

    left_w = 34

    def centered(text: str, style: str = "") -> Text:
        # Rich's own justify="center" ignores trailing whitespace when
        # measuring width, which throws off already-padded strings like the
        # logo rows. Center manually so left/right padding stays exact.
        return line(text.center(left_w)[:left_w], style)

    right_w = box_w - left_w - 7  # border + panel padding + divider column + cell padding

    left_lines = [
        centered(f"Welcome back {user.capitalize()}!", "bold"),
        centered(""),
    ]
    for logo_line in content.LOGO:
        left_lines.append(centered(logo_line, CLAUDE))
    left_lines.append(centered(""))
    left_lines.append(
        centered(f"{content.MODEL_DISPLAY} with medium effort · {user}@nothing.dev's Organization", DIM)
    )
    left_lines.append(centered(cwd, DIM))

    right_lines = [
        line("Tips for getting started", f"bold {CLAUDE}"),
        line("Run /init to analyze your codebase and write nothing down"),
        line(""),
        Text("─" * right_w, style=BORDER),
        line("What's new", f"bold {CLAUDE}"),
    ]
    for whats_new_line in content.WHATS_NEW:
        right_lines.append(line(whats_new_line))
    right_lines.append(line("/release-notes for more (there are none)", f"italic {DIM}"))

    height = max(len(left_lines), len(right_lines))
    left_lines += [line("")] * (height - len(left_lines))
    right_lines += [line("")] * (height - len(right_lines))

    if two_cols:
        grid = Table.grid(padding=(0, 1))
        grid.add_column(width=left_w)
        grid.add_column(width=1)
        grid.add_column(width=right_w)
        for left_line, right_line in zip(left_lines, right_lines):
            grid.add_row(left_line, Text("│", style=BORDER), right_line)
        body = grid
    else:
        left = Table.grid(padding=0)
        left.add_column(width=left_w)
        for left_line in left_lines:
            left.add_row(left_line)
        body = left

    return Panel(
        body,
        title=f"Claude Code {content.VERSION}",
        title_align="left",
        border_style=CLAUDE,
        box=box.ROUNDED,
        width=box_w,
        padding=(0, 1),
    )


def below_banner_notices() -> Text:
    """The MCP warning and usage-limit notice that sit under the home panel."""
    t = Text()
    t.append("⚠ 0 MCP servers need authentication", style=CLAUDE)
    t.append(" · there is nothing to connect to\n", style=DIM)
    t.append("\n")
    t.append("▏", style=CLAUDE)
    t.append("Extended: doing nothing is included in your weekly limit\n", style="bold")
    t.append("▏", style=CLAUDE)
    t.append("You can use up to 100% of your weekly limit doing nothing. If you hit\n")
    t.append("▏", style=CLAUDE)
    t.append("your limit, don't worry — nothing will happen. ")
    t.append("Learn more", style=f"underline {BLUE}")
    return t


class StatusBar(Horizontal):
    """The bottom-most line: permission mode on the left, model/context on the right."""

    def compose(self):
        yield Static(id="status-left")
        yield Static(id="status-right")

    def on_mount(self) -> None:
        self.set_mode("bypass")
        self.set_context(97)

    def set_mode(self, mode: str) -> None:
        left = self.query_one("#status-left", Static)
        if mode == "plan":
            text = Text.from_markup(
                f"  [bold {CLAUDE}]⏸ plan mode on[/] [{DIM}](shift+tab to cycle) · ← for agents[/]"
            )
        else:
            text = Text.from_markup(
                f"  [bold {CLAUDE}]⏵⏵[/] [{DIM}]bypass permissions on (shift+tab to cycle) · ← for agents[/]"
            )
        left.update(text)

    def set_context(self, pct: int) -> None:
        right = self.query_one("#status-right", Static)
        right.update(Text.from_markup(f"[{DIM}]◐ medium · /effort · {pct}% context left[/]  "))


class SlashMenu(OptionList):
    """Dropdown of fake slash commands, filtered as the user types."""

    def filter(self, prefix: str) -> None:
        self.clear_options()
        matches = [c for c in content.SLASH_COMMANDS if c[0].startswith(prefix)]
        for cmd, desc in matches:
            label = Text.from_markup(f"[bold]{cmd:<12}[/] [{DIM}]{desc}[/]")
            self.add_option(Option(label, id=cmd))
        if matches:
            self.highlighted = 0
        self.display = bool(matches)

    @property
    def selected_command(self) -> str | None:
        if self.highlighted is None:
            return None
        option = self.get_option_at_index(self.highlighted)
        return option.id
