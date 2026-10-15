# File Integrity Monitor

A Python script that detects when files in a folder are added, changed, or deleted, using SHA-256 hashes.

## Why I built this

When attackers break into a system, they often change important files: adding a user account, editing a config file, or dropping in a malicious script. Security tools like Tripwire and Wazuh catch this with **file integrity monitoring (FIM)**. I built a simple version to understand how it works.

## How it works

The script uses **hashes**, which are unique "fingerprints" of a file's contents. If even one character in a file changes, its hash changes completely.

1. **Baseline (option 1):** the script hashes every file in `watched_folder` and saves the results to `baseline.txt`. This is the "known good" state.
2. **Check (option 2):** the script hashes every file again and compares the results to the baseline:
   - A file that isn't in the baseline is reported as **NEW FILE**
   - A file whose hash changed is reported as **MODIFIED**
   - A file in the baseline that's now missing is reported as **DELETED**

### The core logic

```python
for name in new:
    if name not in old:
        print("NEW FILE:     ", name)
    elif new[name] != old[name]:
        print("MODIFIED:     ", name)

for name in old:
    if name not in new:
        print("DELETED:      ", name)
```

Both the baseline and the current scan are stored in dictionaries (`file name -> hash`), so comparing them only takes a few `if` checks.

See the full script here: [integrity_monitor.py](integrity_monitor.py)

## How to run it

Put `integrity_monitor.py` and the `watched_folder` folder in the same place, then run:

```
python integrity_monitor.py
```

Type `1` to save a baseline, make some changes to the files, then run it again and type `2` to check. No extra libraries are needed. It only uses built-in Python.

## Results

### 1. Baseline created, no changes

![Baseline and clean check](screenshot-baseline.png)

### 2. After simulating an attacker

To test it, I made three changes like an attacker might:

- Added a fake `hacker` account to `users.txt`
- Deleted `budget.txt`
- Created a new file, `suspicious_file.txt`

![Tampering detected](screenshot-tampered.png)

```
MODIFIED:      users.txt
DELETED:       budget.txt
NEW FILE:      suspicious_file.txt
3 change(s) detected.
```

All three changes were caught.

## Limitations and next steps

- **Manual checks:** the script only checks when I run it. Next I want it to re-check automatically every few minutes.
- **Doesn't say what changed:** it reports *that* a file changed, not *which lines*. A future version could show the exact differences.
- **Baseline isn't protected:** an attacker who can edit `baseline.txt` could hide their changes. Real tools store the baseline somewhere the attacker can't reach.
- **One folder only:** it doesn't scan subfolders yet.

## What I learned

- How hashing works and why it's used to verify file integrity
- How to use Python's `hashlib` and `os` modules
- How to compare two sets of data using dictionaries
- How file integrity monitoring helps detect attackers after a break-in
