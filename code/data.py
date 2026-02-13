import json, os, subprocess, time, sys, threading, random
from datetime import datetime

# ================= CONFIG FILES =================
JSON_FILE = "commit.json"
CONFIG_FILE = "config.json"
BRANCH_NAME = "main"
DEFAULT_DELAY = 5
# ===============================================

# ================== THEMES ======================
THEMES = {
    "dark": {
        "title": "\033[1;94m",
        "line": "\033[96m",
        "ok": "\033[92m",
        "warn": "\033[93m",
        "err": "\033[91m",
        "muted": "\033[90m",
        "reset": "\033[0m",
    },
    "light": {
        "title": "\033[1;34m",
        "line": "\033[36m",
        "ok": "\033[32m",
        "warn": "\033[33m",
        "err": "\033[31m",
        "muted": "\033[90m",
        "reset": "\033[0m",
    }
}
# ===============================================

SPINNER = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

state = {
    "paused": False,
    "quit": False,
    "status": "IDLE",
    "delay": DEFAULT_DELAY,
    "theme": "dark",
    "random_delay": False,
    "session_commits": 0,
    "start_time": time.time()
}

# ----------------- UTIL -----------------
def clear(): os.system("cls" if os.name == "nt" else "clear")

def load_json(path, default):
    if not os.path.exists(path): return default
    try:
        with open(path) as f: return json.load(f)
    except: return default

def save_json(path, data):
    with open(path, "w") as f: json.dump(data, f, indent=2)

def run_git(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# --------------- DATA -------------------
def load_counter():
    data = load_json(JSON_FILE, {"angka": 0})
    if "angka" not in data: data["angka"] = 0
    return data

def save_counter(n):
    save_json(JSON_FILE, {"angka": n})

def load_config():
    cfg = load_json(CONFIG_FILE, {})
    state["delay"] = cfg.get("delay", DEFAULT_DELAY)
    state["theme"] = cfg.get("theme", "dark")
    state["random_delay"] = cfg.get("random_delay", False)

def save_config():
    save_json(CONFIG_FILE, {
        "delay": state["delay"],
        "theme": state["theme"],
        "random_delay": state["random_delay"]
    })

# -------------- UI ----------------------
def C(k): return THEMES[state["theme"]][k]
def header():
    print(C("title")+"AUTO GITHUB COMMIT DASHBOARD"+C("reset"))
    print(C("line")+"────────────────────────────────────────────────"+C("reset"))

def spinner(text, seconds=1.0):
    t0, i = time.time(), 0
    while time.time()-t0 < seconds:
        sys.stdout.write(f"\r{SPINNER[i%len(SPINNER)]} {text}")
        sys.stdout.flush()
        time.sleep(0.1); i+=1
    sys.stdout.write("\r"+" "*50+"\r")

def render(data, last_msg="-", last_time="-"):
    clear(); header()
    dur = int(time.time()-state["start_time"])
    print(f"{C('ok')}Status{C('reset')}        : {state['status']}")
    print(f"{C('ok')}Total Commit{C('reset')} : {data['angka']}")
    print(f"{C('ok')}Session Commit{C('reset')}: {state['session_commits']}")
    print(f"{C('ok')}Uptime{C('reset')}       : {dur}s")
    print(f"{C('ok')}Delay{C('reset')}        : {state['delay']}s ({'RANDOM' if state['random_delay'] else 'FIXED'})")
    print(f"{C('ok')}Theme{C('reset')}        : {state['theme']}")
    print(f"{C('ok')}Last Time{C('reset')}    : {last_time}")
    print(f"{C('ok')}Last Msg{C('reset')}     : {last_msg}")
    print(C("line")+"────────────────────────────────────────────────"+C("reset"))
    print(C("muted")+"Hotkeys: P=Pause  +=Delay  -=Delay  R=Random  T=Theme  Q=Quit"+C("reset"))

def progress(seconds):
    for s in range(seconds,0,-1):
        if state["quit"]: return
        while state["paused"]: time.sleep(0.2)
        bar = int(30*(seconds-s)/seconds)
        sys.stdout.write(f"\rNext in {s:>3}s ["+"█"*bar+"░"*(30-bar)+"]")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r"+" "*5+"\r")

# ------------- GIT ----------------------
def commit_and_push(n):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"auto commit #{n} - {now}"

    state["status"]="COMMITTING"; spinner("git add")
    run_git(["git","add","."])

    spinner("git commit"); run_git(["git","commit","-m",msg])
    state["status"]="PUSHING"; spinner("git push")
    run_git(["git","push","origin",BRANCH_NAME])

    state["status"]="IDLE"
    state["session_commits"]+=1
    return msg, now

# ----------- INPUT THREAD ---------------
def key_listener():
    while not state["quit"]:
        k = sys.stdin.read(1).lower()
        if k=="p": state["paused"]=not state["paused"]
        elif k=="+": state["delay"]+=5; save_config()
        elif k=="-" and state["delay"]>5: state["delay"]-=5; save_config()
        elif k=="r": state["random_delay"]=not state["random_delay"]; save_config()
        elif k=="t": state["theme"]="light" if state["theme"]=="dark" else "dark"; save_config()
        elif k=="q": state["quit"]=True

# --------------- MAIN -------------------
def main():
    load_config()
    data = load_counter()

    clear(); header()
    start = input("Mulai auto commit? (Y/N): ").lower()
    if start!="y": return

    threading.Thread(target=key_listener, daemon=True).start()

    while not state["quit"]:
        while state["paused"]: time.sleep(0.2)

        data["angka"]+=1
        save_counter(data["angka"])

        render(data)
        msg, tm = commit_and_push(data["angka"])
        render(data, msg, tm)

        d = random.randint(int(state["delay"]*0.7), int(state["delay"]*1.3)) if state["random_delay"] else state["delay"]
        progress(d)

    clear(); header()
    print(C("warn")+"Stopped safely."+C("reset"))

if __name__=="__main__":
    main()
