import os, subprocess, time, sys, threading, random
from datetime import datetime
from collections import deque

# ================= CONFIG =================
ACTIVITY_FILE = "activity.log"
HISTORY_FILE = "history.log"
BRANCH_NAME = "main"
DEFAULT_DELAY = 1   # 5 menit (AMAN)
MAX_HISTORY = 5
# =========================================

# ================= THEMES =================
THEMES = {
    "dark": {
        "title": "\033[1;94m",
        "line": "\033[96m",
        "ok": "\033[92m",
        "warn": "\033[93m",
        "err": "\033[91m",
        "muted": "\033[90m",
        "reset": "\033[0m",
    }
}
# =========================================

# ================= IP UTIL =================
def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def masked_ip():
    ip = random_ip().split(".")
    return f"{ip[0]}.{ip[1]}.x.{ip[3]}"

# ================= DATA ====================
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

state = {
    "paused": False,
    "quit": False,
    "status": "IDLE",
    "delay": DEFAULT_DELAY,
    "page": 1,
    "start_time": time.time()
}

history = deque(maxlen=MAX_HISTORY)

# ================= UTIL ===================
def clear(): os.system("cls" if os.name=="nt" else "clear")
def C(k): return THEMES["dark"][k]

def run_git(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def spinner(text, sec=1):
    t,i=time.time(),0
    while time.time()-t<sec:
        sys.stdout.write(f"\r{SPINNER[i%10]} {text}")
        sys.stdout.flush()
        time.sleep(0.1); i+=1
    sys.stdout.write("\r"+" "*60+"\r")

# ================= UI =====================
def header():
    print(C("title")+"AUTO COMMIT SCANNER DASHBOARD"+C("reset"))
    print(C("line")+"────────────────────────────────────────────"+C("reset"))

def render_dashboard(last_msg="-", last_time="-"):
    clear(); header()
    uptime=int(time.time()-state["start_time"])
    print(f"{C('ok')}Status{C('reset')}        : {state['status']}")
    print(f"{C('ok')}Uptime{C('reset')}       : {uptime}s")
    print(f"{C('ok')}Delay{C('reset')}        : {state['delay']}s (randomized)")
    print(f"{C('ok')}Last Scan{C('reset')}   : {last_msg}")
    print(f"{C('ok')}Last Time{C('reset')}   : {last_time}")
    print(C("line")+"────────────────────────────────────────────"+C("reset"))
    print(C("muted")+"[1]Dashboard [2]History  P Pause  Q Quit"+C("reset"))

def render_history():
    clear(); header()
    print(f"{C('ok')}SCAN HISTORY{C('reset')}\n")
    if not history:
        print(C("muted")+"No scan history."+C("reset"))
    else:
        for h in history:
            print(C("ok")+"• "+C("reset")+h)
    print("\n"+C("line")+"────────────────────────────────────────────"+C("reset"))
    print(C("muted")+"[1]Dashboard  [2]History  Q Quit"+C("reset"))

# ================= CORE ===================
def write_activity(ip):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    action = random.choice(SCAN_ACTIONS)
    with open(ACTIVITY_FILE,"a",encoding="utf-8") as f:
        f.write(f"[{now}] {action} {ip}\n")

def commit_and_push():
    ip = masked_ip()
    action = random.choice(SCAN_ACTIONS)
    msg = f"{action} {ip}"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state["status"]="SCANNING"

    write_activity(ip)

    spinner(f"scanning {ip}")
    run_git(["git","add","."])

    spinner("writing snapshot")
    run_git(["git","commit","-m",msg])

    spinner("syncing remote")
    run_git(["git","push","origin",BRANCH_NAME])

    state["status"]="IDLE"
    history.appendleft(f"[{now}] {msg}")

    with open(HISTORY_FILE,"a",encoding="utf-8") as f:
        f.write(f"[{now}] {msg}\n")

    return msg, now

# ================= INPUT ==================
def key_listener():
    while not state["quit"]:
        k=sys.stdin.read(1).lower()
        if k=="1": state["page"]=1
        elif k=="2": state["page"]=2
        elif k=="p": state["paused"]=not state["paused"]
        elif k=="q": state["quit"]=True

# ================= MAIN ===================
def main():
    clear(); header()
    if input("Start scanning & auto commit? (Y/N): ").lower()!="y":
        return

    threading.Thread(target=key_listener,daemon=True).start()

    last_msg,last_tm="-","-"

    while not state["quit"]:
        while state["paused"]:
            time.sleep(0.5)

        last_msg,last_tm=commit_and_push()

        if state["page"]==1:
            render_dashboard(last_msg,last_tm)
        else:
            render_history()

        delay=random.randint(int(state["delay"]*0.8),int(state["delay"]*1.4))
        time.sleep(delay)

    clear(); header()
    print(C("warn")+"Scanner stopped safely."+C("reset"))

if __name__=="__main__":
    main()
