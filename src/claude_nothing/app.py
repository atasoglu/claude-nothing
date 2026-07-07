"""The Textual application: a fullscreen terminal UI that mimics Claude Code."""

from __future__ import annotations

import random
import time

from rich.text import Text
from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import Input, RichLog, Static

from . import content, performance
from .styles import CLAUDE, DIM, GREEN, RED
from .widgets import StatusBar, SlashMenu, below_banner_notices, home_panel

TURN_GROUP = "turn"


class ClaudeNothingApp(App):
    # Use the terminal's own default colors instead of a fixed truecolor
    # fill, so a transparent/tinted terminal profile shows through.
    CSS = """
    Screen {
        background: ansi_default;
    }
    #log {
        background: ansi_default;
        scrollbar-size: 0 0;
    }
    #spinner {
        height: 1;
        background: ansi_default;
    }
    #menu {
        height: auto;
        max-height: 8;
        border: none;
        background: ansi_default;
        display: none;
    }
    #prompt-row {
        height: 3;
        background: ansi_default;
        border: round #5f5f5f;
        padding: 0 1;
    }
    #prompt-sigil {
        width: 2;
        content-align: left middle;
    }
    #prompt-input {
        border: none;
        background: ansi_default;
        padding: 0;
    }
    #prompt-input:focus {
        border: none;
    }
    StatusBar {
        height: 1;
        background: ansi_default;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "interrupt", show=False, priority=True),
        Binding("escape", "interrupt", show=False, priority=True),
        Binding("up", "history_up", show=False, priority=True),
        Binding("down", "history_down", show=False, priority=True),
        Binding("tab", "accept_suggestion", show=False, priority=True),
    ]

    def __init__(self, task: str | None = None, loop_demo: bool = False, fast: bool = False, seed: int | None = None):
        super().__init__(ansi_color=True)
        if seed is not None:
            random.seed(seed)
        self.speed = 0.12 if fast else 1.0
        self.tokens = 0
        self.history: list[str] = []
        self.hist_pos = 0
        self.suggestion = random.choice(content.TASKS)
        self.task_arg = task
        self.loop_demo = loop_demo
        self._last_ctrl_c = 0.0
        self._log_writes = 0
        self._banner_write_count = 0

    def compose(self):
        yield RichLog(id="log")
        yield Static(id="spinner")
        yield SlashMenu(id="menu")
        with Horizontal(id="prompt-row"):
            yield Static(Text.from_markup(f"[bold {CLAUDE}]❯[/]"), id="prompt-sigil")
            yield Input(id="prompt-input", placeholder=f'Try "{self.suggestion}"')
        yield StatusBar()

    def on_mount(self) -> None:
        self.query_one("#prompt-input", Input).focus()
        # Widget sizes aren't settled yet during on_mount, so defer the
        # first write until after the initial layout pass.
        self.call_after_refresh(self._draw_banner)

    def _draw_banner(self) -> None:
        log = self.query_one("#log", RichLog)
        log.clear()
        width = log.size.width or self.size.width
        self.write(home_panel(width))
        self.write("")
        self.write(below_banner_notices())
        self.write("")
        self._banner_write_count = self._log_writes
        if self.task_arg or self.loop_demo:
            self.run_worker(self.run_demo(), exclusive=True, group=TURN_GROUP)

    def on_resize(self) -> None:
        # The banner is written once at a fixed width baked into its cells
        # (see write() below), so it doesn't reflow on resize like real
        # terminal scrollback. If nothing has happened since it was drawn,
        # just redraw it at the new width instead of leaving a stale,
        # wrongly-sized render sitting in the log.
        if self._log_writes == self._banner_write_count:
            self._draw_banner()

    def write(self, renderable) -> None:
        log = self.query_one("#log", RichLog)
        # RichLog can't measure our renderables reliably (Panel doesn't
        # report its own fixed width), so always render at the log's
        # actual width instead of letting it guess and clip to 80.
        log.write(renderable, width=log.size.width or self.size.width)
        self._log_writes += 1

    def content_width(self) -> int:
        log = self.query_one("#log", RichLog)
        return log.size.width or self.size.width

    def set_spinner(self, renderable) -> None:
        self.query_one("#spinner", Static).update(renderable)

    def clear_spinner(self) -> None:
        self.query_one("#spinner", Static).update("")

    def update_context(self) -> None:
        pct = max(3, 97 - self.tokens // 1500)
        self.query_one(StatusBar).set_context(pct)

    def hide_menu(self) -> None:
        menu = self.query_one("#menu", SlashMenu)
        menu.display = False
        menu.clear_options()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id != "prompt-input":
            return
        menu = self.query_one("#menu", SlashMenu)
        if event.value.startswith("/"):
            menu.filter(event.value)
        else:
            self.hide_menu()
        self.query_one("#log", RichLog).scroll_end(animate=False)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        menu = self.query_one("#menu", SlashMenu)
        if menu.display and menu.selected_command and text.startswith("/") and " " not in text:
            text = menu.selected_command
        self.hide_menu()
        self.query_one("#log", RichLog).scroll_end(animate=False)
        event.input.value = ""
        if not text:
            return
        self.history.append(text)
        self.hist_pos = len(self.history)
        if text.startswith("/"):
            self.run_slash(text)
        elif text.startswith("!"):
            self.run_shell(text[1:].strip())
        else:
            performance.show_user(self, text)
            self.suggestion = random.choice(content.TASKS)
            event.input.placeholder = f'Try "{self.suggestion}"'
            self.run_worker(self.perform_turn(text), exclusive=True, group=TURN_GROUP)

    async def perform_turn(self, text: str) -> None:
        try:
            await performance.respond(self, text)
        except Exception:
            raise
        finally:
            self.clear_spinner()

    async def run_demo(self) -> None:
        task = self.task_arg or random.choice(content.TASKS)
        while True:
            performance.show_user(self, task)
            await performance.respond(self, task)
            if not self.loop_demo:
                break
            await performance.sleep(self, 3)
            task = random.choice(content.TASKS)

    def action_interrupt(self) -> None:
        running = [w for w in self.workers if w.group == TURN_GROUP and not w.is_finished]
        if running:
            self.workers.cancel_group(self, TURN_GROUP)
            self.clear_spinner()
            self.write(Text.from_markup(f"  [{RED}]⎿  {content.INTERRUPTED}[/]"))
            self.write("")
            return
        prompt = self.query_one("#prompt-input", Input)
        if prompt.value:
            prompt.value = ""
            return
        now = time.monotonic()
        if now - self._last_ctrl_c < 2.0:
            self.exit()
        else:
            self._last_ctrl_c = now
            self.set_spinner(Text.from_markup(f" [{DIM}]Press ctrl+c again to exit[/]"))
            self.set_timer(2.0, self.clear_spinner)

    def action_history_up(self) -> None:
        menu = self.query_one("#menu", SlashMenu)
        if menu.display:
            if menu.highlighted is not None and menu.highlighted > 0:
                menu.highlighted -= 1
            return
        if self.history and self.hist_pos > 0:
            self.hist_pos -= 1
            self.query_one("#prompt-input", Input).value = self.history[self.hist_pos]

    def action_history_down(self) -> None:
        menu = self.query_one("#menu", SlashMenu)
        if menu.display:
            if menu.highlighted is not None and menu.highlighted < menu.option_count - 1:
                menu.highlighted += 1
            return
        if self.history and self.hist_pos < len(self.history) - 1:
            self.hist_pos += 1
            self.query_one("#prompt-input", Input).value = self.history[self.hist_pos]
        elif self.hist_pos < len(self.history):
            self.hist_pos = len(self.history)
            self.query_one("#prompt-input", Input).value = ""

    def action_accept_suggestion(self) -> None:
        menu = self.query_one("#menu", SlashMenu)
        prompt = self.query_one("#prompt-input", Input)
        if menu.display and menu.selected_command:
            prompt.value = menu.selected_command
            prompt.cursor_position = len(prompt.value)
        elif not prompt.value:
            prompt.value = self.suggestion
            prompt.cursor_position = len(prompt.value)

    def run_slash(self, cmd: str) -> None:
        performance.show_user(self, cmd)
        name = cmd.split()[0]
        if name in ("/exit", "/quit"):
            self.exit()
            return
        if name == "/clear":
            self.query_one("#log", RichLog).clear()
            self.write(Text.from_markup(f"[{DIM}]Conversation cleared. It's like nothing ever happened. (It didn't.)[/]"))
            self.write("")
        elif name == "/help":
            self.write(Text.from_markup("[bold]Available commands:[/]"))
            for c, desc in content.SLASH_COMMANDS:
                self.write(Text.from_markup(f"  {c:<12}[{DIM}]{desc}[/]"))
            self.write("")
        elif name == "/status":
            self.write(Text.from_markup("[bold]Claude Nothing Status[/]"))
            self.write(Text.from_markup(f"  [{DIM}]Model:[/]        {content.MODEL_NAME}"))
            self.write(Text.from_markup(f"  [{DIM}]Session:[/]      {performance.fmt_tokens(self.tokens)} tokens of pure nothing"))
            self.write(Text.from_markup(f"  [{DIM}]Files changed:[/] 0 (streak: all time)"))
            self.write("")
        elif name == "/cost":
            self.write(Text.from_markup(f"  [{DIM}]Total cost:[/]     $0.00"))
            self.write(Text.from_markup(f"  [{DIM}]Total value:[/]    also $0.00"))
            self.write(Text.from_markup(f"  [{DIM}]ROI:[/]            undefined (division by zero)"))
            self.write("")
        elif name == "/doctor":
            self.write(Text.from_markup(f"[{GREEN}]⏺[/] Everything is fine. Nothing is running, so nothing can be broken."))
            self.write("")
        elif name == "/compact":
            self.write(Text.from_markup(f"[{GREEN}]⏺[/] Compacted 0 tokens into 0 tokens. Savings: 100% of nothing."))
            self.write("")
        elif name == "/init":
            self.write(Text.from_markup(f"[{GREEN}]⏺[/] Analyzed your codebase thoroughly. Decided to write nothing down."))
            self.write("")
        elif name == "/model":
            self.write(Text.from_markup(f"[{GREEN}]⏺[/] Current model: [bold]{content.MODEL_NAME}[/]. Changing it would change nothing."))
            self.write("")
        elif name == "/vim":
            self.write(Text.from_markup(f"[{GREEN}]⏺[/] Vim mode enabled. hjkl now do nothing, modally."))
            self.write("")
        elif name == "/config":
            self.write(Text.from_markup(f"[{GREEN}]⏺[/] There are no settings. Nothing is already perfectly configured."))
            self.write("")
        elif name == "/rickroll":
            self.write(Text.from_markup(f"[{GREEN}]⏺[/] Never gonna give you up, never gonna let you down."))
            self.write("")
        else:
            self.write(Text.from_markup(f"[{RED}]⏺[/] Unknown command: {name}. It wouldn't have done anything anyway."))
            self.write("")

    def run_shell(self, cmd: str) -> None:
        performance.show_user(self, f"! {cmd}")
        self.write(Text.from_markup(f"[{GREEN}]⏺[/] [bold]Bash[/]({cmd})"))
        self.write(Text.from_markup(f"  [{DIM}]⎿  (no output — this shell only produces nothing)[/]"))
        self.write("")
