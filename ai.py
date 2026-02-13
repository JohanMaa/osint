import os, subprocess, time, threading, random, sys
from datetime import datetime
from collections import deque

# ================= CONFIG =================
BRANCH = "main"
DEFAULT_DELAY_MIN = 
DEFAULT_DELAY_MAX = 10
MAX_HISTORY = 6
LOG_FILE = "data.log"

MESSAGES = [
    "update internal notes",
    "adjust documentation",
    "minor cleanup",
    "sync changes",
    "small refactor",
    "maintenance update",
    "improve readability"
]

SCAN_ACTIONS = [
    "scanning node",
    "probing endpoint",
    "verifying packet",
    "analyzing traffic",
    "checking response",
    "syncing metadata",
    "validating route"
]

SPINNER = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

# ================= COLORS =================
RESET="\033[0m"
BOLD="\033[1m"
DIM="\033[2m"
WHITE="\033[97m"
GRAY="\033[90m"
GREEN="\033[92m"
CYAN="\033[96m"
YELLOW="\033[93m"
RED="\033[91m"
MAGENTA="\033[95m"

# ================= STATE =================
state = {
    "running": False,
    "quit": False,
    "delay_min": DEFAULT_DELAY_MIN,
    "delay_max": DEFAULT_DELAY_MAX,
    "last_commit": "-",
    "start_time": time.time(),
    "page": 1
}

history = deque(maxlen=MAX_HISTORY)

# ================= UTILS =================
def clear(): os.system("cls" if os.name=="nt" else "clear")

def random_ip():
    return ".".join(str(random.randint(1,254)) for _ in range(4))

def masked_ip():
    ip = random_ip().split(".")
    return f"{ip[0]}.{ip[1]}.x.{ip[3]}"

def random_delay():
    return random.randint(state["delay_min"], state["delay_max"])

def run_git(cmd):
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def log_commit(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {msg}\n")

# ================= ANIMATIONS =================
def spinner_animation(text, duration=1.5):
    start = time.time()
    i = 0
    while time.time() - start < duration:
        sys.stdout.write(f"\r{SPINNER[i%len(SPINNER)]} {text}...{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " "*60 + "\r")

# ================= DASHBOARD =================
def header():
    print(CYAN+BOLD+"┌──────────────────────────────────────────────┐"+RESET)
    print(CYAN+BOLD+"│          AI AUTO COMMIT DASHBOARD            │"+RESET)
    print(CYAN+BOLD+"└──────────────────────────────────────────────┘"+RESET)
    uptime = int(time.time()-state["start_time"])
    print(f"{GRAY}Uptime     :{RESET} {uptime}s")
    print(f"{GRAY}Branch     :{RESET} {BRANCH}")
    print(f"{GRAY}Delay      :{RESET} {state['delay_min']} - {state['delay_max']}s\n")

def render_dashboard():
    clear()
    header()
    print(f"{GREEN}Status        :{RESET} {'RUNNING' if state['running'] else 'STOPPED'}")
    print(f"{GREEN}Last Commit   :{RESET} {state['last_commit']}")
    print(CYAN+"────────────────────────────────────────────"+RESET)
    print(f"{GRAY}[1]Dashboard [2]History  P Pause  Q Quit"+RESET)

def render_history():
    clear()
    header()
    print(f"{MAGENTA}Commit & Scan History{RESET}\n")
    if not history:
        print(GRAY+"No history yet."+RESET)
    else:
        for h in history:
            print(GREEN+"• "+RESET+h)
    print(CYAN+"────────────────────────────────────────────"+RESET)
    print(GRAY+"[1]Dashboard [2]History  Q Quit"+RESET)

# ================= CORE =================
def commit_cycle():
    while not state["quit"]:
        if not state["running"]:
            time.sleep(0.5)
            continue

        ip = masked_ip()
        action = random.choice(SCAN_ACTIONS)
        msg = f"{action} {ip}"
        state["last_commit"] = msg

        spinner_animation(f"Processing {ip}")

        run_git(["git","add","."])
        spinner_animation("Staging changes")
        run_git(["git","commit","-m",msg])
        spinner_animation("Pushing to remote")
        run_git(["git","push","origin",BRANCH])

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.appendleft(f"[{now}] {msg}")
        log_commit(f"[{now}] {msg}")

        # Render dashboard
        if state["page"]==1:
            render_dashboard()
        else:
            render_history()

        delay = random_delay()
        for _ in range(delay):
            if not state["running"] or state["quit"]:
                break
            time.sleep(1)

# ================= INPUT =================
def key_listener():
    while not state["quit"]:
        k = sys.stdin.read(1).lower()
        if k=="1": state["page"]=1
        elif k=="2": state["page"]=2
        elif k=="p": state["running"] = not state["running"]
        elif k=="q": state["quit"]=True

# ================= COMMAND MODE =================
def command_mode():
    print(CYAN+"AI Commit Assistant Interactive Mode"+RESET)
    print("Type 'help' to see commands.\n")
    threading.Thread(target=commit_cycle, daemon=True).start()
    threading.Thread(target=key_listener, daemon=True).start()

    while not state["quit"]:
        try:
            cmd = input("you > ").strip().lower()
            if not cmd: continue
            parts = cmd.split()

            if parts[0]=="start":
                state["running"]=True
                print(GREEN+"✅ Auto commit started"+RESET)
            elif parts[0]=="stop":
                state["running"]=False
                print(YELLOW+"⛔ Auto commit stopped"+RESET)
            elif parts[0]=="delay" and len(parts)==2:
                val = int(parts[1])
                state["delay_min"]=state["delay_max"]=val
                print(GREEN+f"⏱ Delay set to {val}s"+RESET)
            elif parts[0]=="range" and len(parts)==3:
                state["delay_min"]=int(parts[1])
                state["delay_max"]=int(parts[2])
                print(GREEN+f"⏱ Delay range {parts[1]}-{parts[2]}s"+RESET)
            elif parts[0]=="status":
                render_dashboard()
            elif parts[0]=="help":
                print("""
Commands:
start           → start auto commit
stop            → stop auto commit
delay <sec>     → set fixed delay
range <min> <max> → set delay range
status          → show dashboard
help            → show commands
exit            → quit safely
""")
            elif parts[0]=="exit":
                state["quit"]=True
            else:
                print(RED+"❌ Unknown command. Type 'help'"+RESET)

        except KeyboardInterrupt:
            state["quit"]=True

# ================= MAIN =================
def main():
    clear()
    command_mode()
    clear()
    print(YELLOW+"✅ Shutting down safely"+RESET)

if __name__=="__main__":
    main()
