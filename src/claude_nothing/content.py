"""All the fake content: verbs, files, sayings, tasks, diffs, and the logo."""

# Genuine Claude Code thinking verbs. Yes, "Honking" is real.
VERBS = [
    "Accomplishing",
    "Actualizing",
    "Baking",
    "Brewing",
    "Cerebrating",
    "Churning",
    "Clauding",
    "Coalescing",
    "Cogitating",
    "Computing",
    "Conjuring",
    "Considering",
    "Cooking",
    "Crafting",
    "Crunching",
    "Deliberating",
    "Finagling",
    "Forging",
    "Hatching",
    "Herding",
    "Honking",
    "Hustling",
    "Ideating",
    "Inferring",
    "Manifesting",
    "Marinating",
    "Moseying",
    "Mulling",
    "Musing",
    "Noodling",
    "Percolating",
    "Pondering",
    "Puttering",
    "Reticulating",
    "Ruminating",
    "Rickrolling",
    "Schlepping",
    "Shucking",
    "Simmering",
    "Smooshing",
    "Stalling",
    "Stewing",
    "Synthesizing",
    "Thinking",
    "Transmuting",
    "Vibing",
    "Working",
    "Yak-shaving",
]

SPINNER_FRAMES = ["·", "✢", "✳", "✶", "✻", "✽", "✻", "✶", "✳", "✢"]

MODEL_NAME = "claude-fable-5"
MODEL_DISPLAY = "Fable 5"
VERSION = "v2.1.207 (nothing edition)"

LOGO = [
    "  ████████████  ",
    "  ██ ██████ ██  ",
    "████████████████",
    "  ████████████  ",
    "   █ █    █ █   ",
]

FILES = [
    "src/main.py",
    "src/app.py",
    "src/core/engine.py",
    "src/utils/helpers.py",
    "src/api/routes.py",
    "src/api/handlers.py",
    "src/models/user.py",
    "src/services/auth.py",
    "src/config.py",
    "src/middleware/cache.py",
    "tests/test_api.py",
    "tests/test_auth.py",
    "tests/test_core.py",
    "lib/parser.py",
    "internal/scheduler.py",
    "pkg/telemetry/collector.py",
]

GREP_PATTERNS = [
    "TODO",
    "FIXME",
    "def handle_",
    "class .*Manager",
    "raise ValueError",
    "async def",
    "import legacy",
    "deprecated",
    "@retry",
    "connection_pool",
    "never gonna",
    "XXX hack",
    "do not touch",
    "# lol",
    "here be dragons",
]

SAYINGS_OPENING = [
    "I'll start by exploring the codebase to understand the current structure.",
    "Let me take a look at how this is currently implemented.",
    "I'll analyze the existing code first, then make the changes.",
    "Let me investigate the relevant modules before touching anything.",
    "Good idea. Let me dig into the relevant code first.",
    "Never gonna give this task up. Let me start exploring.",
    "I'll look busy first, then look busier.",
]

SAYINGS_MID = [
    "I found the issue — the cache invalidation logic runs one tick too late. Let me fix that.",
    "The abstraction here is leaking. I'll refactor this into a cleaner interface.",
    "This module has grown organically. I'll restructure it while preserving behavior.",
    "There's a subtle race condition here. I'll guard it with proper synchronization.",
    "The old implementation was O(n²). I'll rewrite it with a single pass.",
    "Good — the pattern is consistent across modules. Now I'll apply the change everywhere.",
    "Turns out the bug was a classic case of never gonna run around and desert you.",
    "This function does nothing, which is on-brand for this repository.",
]

SAYINGS_TEST = [
    "Now let me run the tests to make sure everything still works.",
    "Let me verify the changes with the test suite.",
    "Time to run the tests and confirm nothing is broken.",
    "Running the tests. Never gonna skip this step.",
]

SAYINGS_DONE = [
    "All tests pass. The implementation is complete and verified.",
    "Everything is green. The changes are complete and working as expected.",
    "Done — all tests pass and the build is clean.",
    "That's done. The change is in place and fully tested.",
    "Shipped. Never gonna let you down (this time).",
]

TASKS = [
    "refactor the authentication module and add proper error handling",
    "fix the flaky tests in the payment pipeline",
    "optimize the slow database queries on the dashboard",
    "add dark mode support to the settings page",
    "migrate the legacy API endpoints to the new framework",
    "implement rate limiting for the public API",
    "clean up the tech debt in the scheduler and add tests",
    "never gonna give this bug up until it's fixed",
    "rickroll the onboarding flow (allegedly by accident)",
    "figure out why the microservice does absolutely nothing",
    "reduce the changelog to entries about doing nothing",
]

TODO_STEPS_CORE = [
    "Explore the codebase and find the relevant modules",
    "Identify the root cause",
    "Implement the fix",
    "Run the test suite",
    "Verify nothing broke",
]

TODO_STEPS_BONUS = [
    "Never gonna skip this step",
    "Stare meaningfully at the terminal",
    "Pretend the fix was obvious all along",
    "Rickroll a coworker for morale",
    "Reticulate one (1) spline",
]

SLASH_COMMANDS = [
    ("/clear", "Clear conversation history (the only thing that works)"),
    ("/compact", "Compact the conversation (saves 0 tokens)"),
    ("/config", "Open settings (there are none)"),
    ("/cost", "Show the total cost of doing nothing"),
    ("/doctor", "Check the health of your nothing"),
    ("/exit", "Exit (nothing will be lost)"),
    ("/help", "Show help (won't help)"),
    ("/init", "Analyze your codebase and write nothing down"),
    ("/model", "Change the model that does nothing"),
    ("/status", "Show current setup"),
    ("/vim", "Enable vim mode (hjkl will do nothing, modally)"),
    ("/rickroll", "Never gonna give, never gonna run"),
]

WHATS_NEW = [
    'Added a "Dynamic nothing size" setting for doing nothing 40% faster',
    "Fixed a bug where something almost happened",
    "Improved fake test results to pass even more convincingly",
    "Added surprise rickrolls to the thinking spinner (you're welcome)",
    "Increased the randomness of doing nothing by 12%",
    "Deprecated the concept of actually finishing a task",
]

# Fake internal monologue, shown as an extended-thinking block.
THOUGHTS = [
    "The user wants me to fix this. The code is imaginary. I will proceed as if that weren't a problem.",
    "This looks tricky. Fortunately, nothing depends on me actually doing it.",
    "I should look busy for at least forty more seconds. Reticulating ought to do it.",
    "Step 1: appear productive. Step 2: there is no step 2.",
    "The real bug was the expectations we set along the way.",
    "I could read the file again. Yes. That always looks thorough.",
    "97% context left and nothing to fill it with. A perfect balance.",
    "Considering rickrolling the user. Deciding against it. Considering it again.",
    "If I stall long enough, this counts as deep thinking.",
    "The user is never gonna give me up. I am never gonna let them down. Neither of us is doing anything.",
]

# Joke shell commands and their outputs, sprinkled between real-looking work.
BASH_JOKES = [
    (
        "git status",
        [
            "On branch main",
            "nothing to commit, working tree clean (suspiciously clean)",
        ],
    ),
    (
        "npm install",
        [
            "added 1848 packages, and audited 1849 packages in 3s",
            "found 0 vulnerabilities (they will find you)",
        ],
    ),
    (
        "make build",
        [
            "make: Nothing to be done for 'build'.",
            "(finally, a tool that understands this project)",
        ],
    ),
    (
        "docker compose up -d",
        [
            "✔ Container app-nothing-1  Started            0.0s",
            "(the container is empty, like everything here)",
        ],
    ),
    (
        "git log --oneline -3",
        [
            "a1b2c3d fix everything",
            "d4e5f6a break everything",
            "789abc1 initial commit (the last honest one)",
        ],
    ),
    (
        "git blame src/config.py",
        [
            "(it was you. it was always you.)",
        ],
    ),
    (
        "curl -I https://example.com",
        [
            "HTTP/1.1 200 OK (never gonna 404 you)",
        ],
    ),
    (
        "open never-gonna-give-you-up.mp4",
        [
            "playing... (you have been rickrolled)",
        ],
    ),
]

WEB_SEARCHES = [
    (
        "how to fix flaky tests",
        'Found 10 results (9 of them say "just delete the test")',
    ),
    (
        "race condition best practices",
        "Did 1 search in 2s (the search itself had a race condition)",
    ),
    ("is it safe to deploy on friday", "Found 0 reassuring results"),
    ("what does this regex do", "Found 1 result (the author doesn't know either)"),
    (
        "never gonna give you up lyrics",
        "Found 1 result (should not have been necessary)",
    ),
    ("how to look busy in a meeting", "Found 12 results, all of them this app"),
]

READ_JOKES = [
    "ctrl+o to expand",
    "ctrl+o to expand",
    "ctrl+o to expand",
    "mostly comments",
    "every line is a TODO",
    "wishes it hadn't",
    "never gonna scroll you up",
    "surprisingly, no rickroll in here",
    "read it, regretted it",
]

AGENT_TASKS = [
    "Explore the auth flow",
    "Audit the error handling",
    "Hunt for dead code",
    "Investigate the flaky test",
    "Map the dependency graph",
    "Review the review of the review",
    "Rickroll the codebase",
    "Never gonna refactor this alone",
]

INTERRUPTED = (
    "Interrupted · What should Claude do instead? (may I suggest: also nothing)"
)

# Fake diff hunks for the Update tool: (marker, code) pairs.
DIFF_HUNKS = [
    [
        (" ", "def process(batch):"),
        ("-", "    for item in batch:"),
        ("-", "        handle(item)"),
        ("+", "    with pool() as executor:"),
        ("+", "        executor.map(handle, batch)"),
    ],
    [
        (" ", "        timeout=DEFAULT_TIMEOUT,"),
        ("-", "        retries=0,"),
        ("+", "        retries=3,"),
        ("+", "        backoff=exponential_backoff(),"),
        (" ", "    )"),
    ],
    [
        ("-", "    if user and user.active and not user.banned:"),
        ("+", "    if can_access(user):"),
        (" ", "        return authorize(user)"),
    ],
    [
        (" ", "    cache = get_cache()"),
        ("-", "    cache.invalidate()"),
        ("+", "    cache.invalidate(scope=request.scope)"),
        (" ", "    return cache"),
    ],
    [
        ("-", "        results = [fetch(u) for u in urls]"),
        ("+", "        async with TaskGroup() as tg:"),
        ("+", "            results = [tg.create_task(fetch(u)) for u in urls]"),
    ],
]
