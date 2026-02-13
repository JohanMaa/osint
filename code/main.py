import json
import os
import subprocess
import time
from datetime import datetime

JSON_FILE = "commit.json"
BRANCH_NAME = "main"
DELAY_SECONDS = 1  # commit setiap 60 detik (ubah sesuka kamu)

def load_json():
    if not os.path.exists(JSON_FILE):
        return {"angka": 0}

    with open(JSON_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {"angka": 0}

    if "angka" not in data or not isinstance(data["angka"], int):
        data["angka"] = 0

    return data


def save_json(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)


def run_git(cmd):
    subprocess.run(cmd, check=True)


def commit_and_push(number):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"auto commit #{number} - {now}"

    run_git(["git", "add", "."])
    run_git(["git", "commit", "-m", message])
    run_git(["git", "push", "origin", BRANCH_NAME])

    print(f"✅ Commit #{number} berhasil dikirim ke GitHub")


def main():
    print("🚀 AUTO COMMIT LOOP DIMULAI (CTRL+C untuk berhenti)")

    while True:
        try:
            data = load_json()
            data["angka"] += 1
            save_json(data)

            commit_and_push(data["angka"])

            print(f"⏳ Tunggu {DELAY_SECONDS} detik...\n")
            time.sleep(DELAY_SECONDS)

        except KeyboardInterrupt:
            print("\n🛑 Auto commit dihentikan manual")
            break
        except Exception as e:
            print("❌ Error:", e)
            print("⏳ Coba lagi 30 detik...\n")
            time.sleep(30)


if __name__ == "__main__":
    main()
