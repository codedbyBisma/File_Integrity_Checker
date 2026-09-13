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

You'll see a menu:

Add file(s) to baseline (start monitoring)
Check integrity (compare current vs baseline)
View current baseline
Exit


## Example Output

### Unchanged File

[OK] UNCHANGED : /home/kali/cybertask1/test.txt
[INFO] Summary → Unchanged: 1 | Modified: 0 | Missing: 0

### Modified File

[ALERT] MODIFIED : /home/kali/cybertask1/test.txt
[WARNING] Original SHA-256: 3ecca8724b9bf412fd136cac17b4e7b6ed8d88016d7141d0b124579a9f733a3f
[WARNING] Current SHA-256: d09aa86320400a7fb4fac0ebc425bd89d11e52c7ec0d6cbd797d3edfe469725d
[INFO] Summary → Unchanged: 0 | Modified: 1 | Missing: 0

### Missing File

[ALERT] MISSING : /home/kali/cybertask1/test.txt
[INFO] Summary → Unchanged: 0 | Modified: 0 | Missing: 1

## Author

Bisma — Cybersecurity Intern at SAM AI Technologies
