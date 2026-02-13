import json
import os
import subprocess
from datetime import datetime

JSON_FILE = "commit.json"
BRANCH_NAME = "main"   # ganti kalau branch kamu bukan main

def load_json():
    # Jika file belum ada, buat data default
    if not os.path.exists(JSON_FILE):
        return {"angka": []}

    with open(JSON_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {"angka": []}

    if "angka" not in data or not isinstance(data["angka"], list):
        data["angka"] = []

    return data


def save_json(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)


def run_git_command(command):
    subprocess.run(command, check=True)


def git_commit_and_push(commit_message):
    try:
        run_git_command(["git", "add", "."])
        run_git_command(["git", "commit", "-m", commit_message])
        run_git_command(["git", "push", "origin", BRANCH_NAME])
    except subprocess.CalledProcessError as e:
        print("❌ Git command gagal")
        print(e)


def main():
    data = load_json()

    # Tentukan angka selanjutnya
    if len(data["angka"]) == 0:
        next_number = 1
    else:
        next_number = data["angka"][-1] + 1

    data["angka"].append(next_number)
    save_json(data)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"auto commit #{next_number} - {now}"

    git_commit_and_push(commit_message)

    print("✅ AUTO COMMIT & PUSH BERHASIL")
    print("   Angka sekarang :", next_number)
    print("   Commit message :", commit_message)


if __name__ == "__main__":
    main()
