import json
import os
import subprocess
import time
import sys
from datetime import datetime

# ============== CONFIG ==============
JSON_FILE = "commit.json"
BRANCH_NAME = "main"
DEFAULT_DELAY = 60
# ====================================

# ===== ANSI COLORS =====
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RED = "\033[91m"
CYAN = "\033[96m"
GRAY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"
# =======================

SPINNER = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    print(BOLD + BLUE + "AUTO GITHUB COMMIT DASHBOARD" + RESET)
    print(CYAN + "──────────────────────────────────────────────" + RESET)


def load_json():
    if not os.path.exists(JSON_FILE):
        return {"angka": 0}
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {"angka": 0}
    if "angka" not in data:
        data["angka"] = 0
    return data


def save_json(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)


def run_git(cmd):
    subprocess.run(
        cmd,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def spinner_run(text, seconds=1.2):
    start = time.time()
    i = 0
    while time.time() - start < seconds:
        sys.stdout.write(f"\r{CYAN}{SPINNER[i % len(SPINNER)]}{RESET} {text}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 50 + "\r")


def commit_and_push(number):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"auto commit #{number} - {now}"

    spinner_run("Running git add")
    run_git(["git", "add", "."])

    spinner_run("Running git commit")
    run_git(["git", "commit", "-m", msg])

    spinner_run("Pushing to GitHub")
    run_git(["git", "push", "origin", BRANCH_NAME])

    return msg, now


def progress_bar(seconds):
    width = 30
    for s in range(seconds, 0, -1):
        filled = int(width * (seconds - s) / seconds)
        bar = "█" * filled + "░" * (width - filled)
        sys.stdout.write(
            f"\r{GRAY}Next commit in {s:>3}s {BLUE}[{bar}]{RESET}"
        )
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 80 + "\r")


def setup():
    clear_screen()
    header()

    data = load_json()
    print(f"{GREEN}Last commit number :{RESET} {data['angka']}")
    print(f"{GREEN}Branch             :{RESET} {BRANCH_NAME}\n")

    delay = input(f"{YELLOW}Delay commit (detik) [{DEFAULT_DELAY}]: {RESET}")
    delay = int(delay) if delay.strip() else DEFAULT_DELAY

    start = input(f"\n{CYAN}Mulai auto commit loop? (Y/N): {RESET}").lower()
    if start != "y":
        print(RED + "Dibatalkan." + RESET)
        exit()

    return delay


def render_dashboard(data, msg, time_now, delay, status):
    clear_screen()
    header()
    print(f"{GREEN}Status              :{RESET} {status}")
    print(f"{GREEN}Total Commit        :{RESET} {data['angka']}")
    print(f"{GREEN}Last Commit Time    :{RESET} {time_now}")
    print(f"{GREEN}Last Commit Message :{RESET} {msg}")
    print(f"{GREEN}Delay               :{RESET} {delay} detik")
    print(CYAN + "──────────────────────────────────────────────" + RESET)
    print(GRAY + "CTRL + C untuk menghentikan" + RESET)


def main():
    delay = setup()

    while True:
        try:
            data = load_json()
            data["angka"] += 1
            save_json(data)

            render_dashboard(data, "-", "-", delay, "COMMITTING")
            msg, time_now = commit_and_push(data["angka"])

            render_dashboard(data, msg, time_now, delay, "IDLE")
            progress_bar(delay)

        except KeyboardInterrupt:
            clear_screen()
            header()
            print(RED + "Auto commit dihentikan." + RESET)
            break

        except Exception as e:
            clear_screen()
            header()
            print(RED + "ERROR:" + RESET, e)
            print(YELLOW + "Retry dalam 30 detik..." + RESET)
            time.sleep(30)


if __name__ == "__main__":
    main()
