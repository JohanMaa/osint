import subprocess
import time
import random
import os
from datetime import datetime

# ===================== CONFIG =====================
DELAY_MIN = 1
DELAY_MAX = 10
BRANCH = "main"
HISTORY_LIMIT = 6

COMMIT_MESSAGES = [
    "update internal notes",
    "minor cleanup",
    "adjust documentation",
    "sync changes",
    "small refactor",
    "improve readability",
    "organize project structure"
]

ACTIVITY_TEXT = [
    "Reviewing internal notes",
    "Checking documentation",
    "Organizing workspace",
    "Verifying references",
    "Preparing small update"
]

# ===================== COLORS =====================
RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"

WHITE = "\033[97m"
GRAY = "\033[90m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"

history = []

# ===================== SYSTEM =====================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def git(cmd):
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ===================== ANIMATION =====================
def progress_bar(duration):
    width = 30
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed >= duration:
            break
        filled = int((elapsed / duration) * width)
        bar = "█" * filled + "░" * (width - filled)
        print(f"\r{GRAY}Progress {bar}{RESET}", end="")
        time.sleep(0.05)
    print("\r", end="")

def pulse(text, cycles=3):
    for _ in range(cycles):
        print(f"\r{DIM}{text}{RESET}", end="")
        time.sleep(0.3)
        print(f"\r{text}", end="")
        time.sleep(0.3)
    print()

# ===================== UI =====================
def header():
    print(CYAN + BOLD + "┌──────────────────────────────────────────────┐")
    print("│        AUTO COMMIT CONTROL DASHBOARD          │")
    print("└──────────────────────────────────────────────┘" + RESET)
    print(f"{GRAY}Branch:{RESET} {BRANCH}")
    print(f"{GRAY}Delay :{RESET} {DELAY_MIN}s – {DELAY_MAX}s")
    print()

def section(title):
    print(BLUE + BOLD + title + RESET)
    print(GRAY + "────────────────────────────────" + RESET)

def history_panel():
    section("Commit History")
    for h in history[-HISTORY_LIMIT:]:
        print(f"{GREEN}●{RESET} {h}")
    print()

# ===================== SETUP =====================
def setup():
    clear()
    header()
    section("Setup")
    print("Dashboard ready.")
    print("Press Y to start auto commit loop")
    print("Press CTRL+C to stop safely\n")

    while True:
        c = input("Start now? [Y/N]: ").lower()
        if c == "y":
            return
        if c == "n":
            exit()

# ===================== MAIN LOOP =====================
def main():
    setup()

    while True:
        clear()
        header()

        msg = random.choice(COMMIT_MESSAGES)
        act = random.choice(ACTIVITY_TEXT)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        section("Current Task")
        print(f"{act}")
        pulse("Processing update")

        progress_bar(2)

        git(["git", "add", "."])
        git(["git", "commit", "-m", msg])
        git(["git", "push", "origin", BRANCH])

        history.append(f"{now} → {msg}")

        history_panel()

        delay = random.randint(DELAY_MIN, DELAY_MAX)
        section("Status")
        print(f"{GRAY}Next commit in {delay} seconds{RESET}")

        for i in range(delay):
            time.sleep(1)

# ===================== START =====================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(GREEN + "Stopped safely. Session ended." + RESET)
