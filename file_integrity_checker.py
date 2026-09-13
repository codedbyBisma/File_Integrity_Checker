import hashlib
import json
import os
import sys
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLOR = True
except ImportError:
    COLOR = False

BASELINE_FILE = "baseline.json"


# ---------- Helper functions for colored output ----------

def info(msg):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}" if COLOR else f"[INFO] {msg}")

def success(msg):
    print(f"{Fore.GREEN}[OK]{Style.RESET_ALL} {msg}" if COLOR else f"[OK] {msg}")

def warning(msg):
    print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {msg}" if COLOR else f"[WARNING] {msg}")

def error(msg):
    print(f"{Fore.RED}[ALERT]{Style.RESET_ALL} {msg}" if COLOR else f"[ALERT] {msg}")

def banner():
    line = "=" * 55
    title = "   FILE INTEGRITY CHECKER"
    if COLOR:
        print(Fore.MAGENTA + line)
        print(Fore.MAGENTA + Style.BRIGHT + title)
        print(Fore.MAGENTA + line)
    else:
        print(line)
        print(title)
        print(line)


# ---------- Core hashing logic ----------

def calculate_hashes(file_path):
    """Return (sha256, md5) hex digests for a given file."""
    sha256_hash = hashlib.sha256()
    md5_hash = hashlib.md5()

    with open(file_path, "rb") as f:
        # Read in chunks so large files don't eat up memory
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
            md5_hash.update(chunk)

    return sha256_hash.hexdigest(), md5_hash.hexdigest()


def load_baseline():
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_baseline(baseline):
    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)


# ---------- Main actions ----------

def add_files_to_baseline():
    baseline = load_baseline()
    paths_input = input(
        "Enter file path(s) to monitor (separate multiple paths with a comma):\n> "
    )
    paths = [p.strip() for p in paths_input.split(",") if p.strip()]

    if not paths:
        warning("No file paths entered.")
        return

    for path in paths:
        if not os.path.isfile(path):
            error(f"File not found, skipped: {path}")
            continue

        sha256_val, md5_val = calculate_hashes(path)
        baseline[os.path.abspath(path)] = {
            "sha256": sha256_val,
            "md5": md5_val,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        success(f"Added to baseline: {path}")

    save_baseline(baseline)
    info(f"Baseline saved to '{BASELINE_FILE}'.\n")


def check_integrity():
    baseline = load_baseline()

    if not baseline:
        warning("No baseline found. Add files first (Option 1).\n")
        return

    print()
    banner_line = "-" * 55
    print(banner_line)
    modified_count = 0
    missing_count = 0
    ok_count = 0

    for path, saved_data in baseline.items():
        if not os.path.exists(path):
            error(f"MISSING   : {path}")
            missing_count += 1
            continue

        current_sha256, current_md5 = calculate_hashes(path)

        if current_sha256 == saved_data["sha256"] and current_md5 == saved_data["md5"]:
            success(f"UNCHANGED : {path}")
            ok_count += 1
        else:
            error(f"MODIFIED  : {path}")
            warning(f"           Original SHA-256: {saved_data['sha256']}")
            warning(f"           Current  SHA-256: {current_sha256}")
            modified_count += 1

    print(banner_line)
    info(
        f"Summary -> Unchanged: {ok_count} | "
        f"Modified: {modified_count} | Missing: {missing_count}\n"
    )


def view_baseline():
    baseline = load_baseline()
    if not baseline:
        warning("Baseline is empty.\n")
        return

    print()
    for path, data in baseline.items():
        print(f"File     : {path}")
        print(f"  SHA-256: {data['sha256']}")
        print(f"  MD5     : {data['md5']}")
        print(f"  Added   : {data['added_on']}\n")


def main_menu():
    banner()
    while True:
        print("\n1. Add file(s) to baseline (start monitoring)")
        print("2. Check integrity (compare current vs baseline)")
        print("3. View current baseline")
        print("4. Exit")
        choice = input("\nSelect an option (1-4): ").strip()

        if choice == "1":
            add_files_to_baseline()
        elif choice == "2":
            check_integrity()
        elif choice == "3":
            view_baseline()
        elif choice == "4":
            info("Exiting. Stay secure!")
            sys.exit(0)
        else:
            warning("Invalid option, please choose 1-4.")


if __name__ == "__main__":
    main_menu()
