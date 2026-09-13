# File_Integrity_Checker
A Python-based command-line tool that monitors files for unauthorized 
modifications using cryptographic hashing (SHA-256 and MD5).

## Overview

File Integrity Monitoring (FIM) is a security technique used to detect 
whether critical files have been altered, deleted, or tampered with. 
This tool implements the core logic behind real-world FIM systems like 
Wazuh, Tripwire, and AIDE.

## How It Works

1. **Baseline Creation** — The tool calculates the SHA-256 and MD5 hash 
   of a file and saves it in `baseline.json` along with a timestamp. 
   This becomes the "trusted" reference.

2. **Integrity Check** — On demand, the tool recalculates the file's 
   current hash and compares it against the saved baseline:
   - **Unchanged** → hashes match, file is safe
   - **Modified** → hashes differ, tampering detected
   - **Missing** → file no longer exists at its saved path

3. **Multiple File Support** — Several files can be added and monitored 
   at the same time.

## Features

- SHA-256 and MD5 hash calculation
- Persistent baseline storage (JSON)
- Colored terminal output for readability
- Detects modified, missing, and unchanged files
- Supports monitoring multiple files

## Tech Stack

- Python 3
- `hashlib` (hashing)
- `json` (baseline storage)
- `colorama` (colored CLI output)

## Installation

pip install colorama --break-system-packages


## Usage

python3 file_integrity_checker.py


## Setup

mkdir cybertask1
cd cybertask1

Place file_integrity_checker.py inside this folder.

## You'll see a menu:

Add file(s) to baseline (start monitoring)

Check integrity (compare current vs baseline)

View current baseline

Exit

## Testing — Modified File Scenario

In a new terminal tab, modify the monitored file:

echo "# test change" >> file_integrity_checker.py

Then run the tool again and select 
Option 2 — the tool will report MODIFIED and show both the original and current hash values.

## Testing — Missing File Scenario

mv file_integrity_checker.py file_integrity_checker_backup.py
python3 file_integrity_checker_backup.py

Select Option 2 — the tool will report MISSING.

## Restore the original filename afterward:

mv file_integrity_checker_backup.py file_integrity_checker

## Author

Bisma — Cybersecurity Intern at SAM AI Technologies
