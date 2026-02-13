import subprocess, time, random, os, sys
from datetime import datetime

# ================= CONFIG =================
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
    "optimize structure"
]

SCAN_TEXT = [
    "scanning workspace",
    "checking changes",
    "verifying integrity",
    "analyzing repository",
    "preparing update"
]

# ================= COLORS =================
RESET="\033[0m"; DIM="\033[2m"; BOLD="\033[1m"
GREEN="\033[92m"; CYAN="\033[96m"; BLUE="\033[94m"
GRAY="\033[90m"; YELLOW="\033[93m"

history=[]

# ================= SYSTEM =================
def clear():
    os.system("cls" if os.name=="nt" else "clear")

def git(cmd):
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ================= ANIMATIONS =================
def typing(text, speed=0.04):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def scan_line(lines=6):
    for i in range(lines):
        print(GREEN + "│" + RESET + " scanning..." + " ░" * i)
        time.sleep(0.08)

def radar(duration=2):
    frames="◐◓◑◒"
    end=time.time()+duration
    i=0
    while time.time()<end:
        print(f"\r{CYAN}Scanning {frames[i%4]}{RESET}", end="")
        time.sleep(0.15)
        i+=1
    print("\r", end="")

# ================= UI =================
def header():
    print(CYAN+BOLD+"┌──────────────────────────────────────────────┐")
    print("│        SYSTEM AUTO COMMIT SCANNER            │")
    print("└──────────────────────────────────────────────┘"+RESET)
    print(GRAY+f"Branch: {BRANCH} | Delay: {DELAY_MIN}-{DELAY_MAX}s"+RESET+"\n")

def section(title):
    print(BLUE+BOLD+f"[ {title} ]"+RESET)
    print(GRAY+"────────────────────────────────"+RESET)

def history_panel():
    section("Commit History")
    for h in history[-HISTORY_LIMIT:]:
        print(GREEN+"●"+RESET, h)
    print()

# ================= SETUP =================
def setup():
    clear()
    header()
    typing(GREEN+"Initializing commit engine..."+RESET)
    scan_line()
    typing(YELLOW+"Press Y to start scanning & auto commit"+RESET)

    while True:
        c=input("Start now? [Y/N]: ").lower()
        if c=="y": return
        if c=="n": exit()

# ================= MAIN =================
def main():
    setup()

    while True:
        clear()
        header()

        msg=random.choice(COMMIT_MESSAGES)
        scan=random.choice(SCAN_TEXT)
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        section("System Scan")
        typing(f"> {scan}...")
        radar(2)

        typing(GRAY+"> staging changes"+RESET)
        git(["git","add","."])

        typing(GRAY+"> committing update"+RESET)
        git(["git","commit","-m",msg])

        typing(GRAY+"> pushing to remote"+RESET)
        git(["git","push","origin",BRANCH])

        history.append(f"{now} → {msg}")
        history_panel()

        delay=random.randint(DELAY_MIN,DELAY_MAX)
        section("Idle Mode")
        typing(GRAY+f"Next scan in {delay} seconds"+RESET)

        for _ in range(delay):
            time.sleep(1)

# ================= START =================
if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(GREEN+"System halted safely."+RESET)
