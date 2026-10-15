# integrity_monitor.py
# Detects files that were added, changed, or deleted in a folder.

import hashlib
import os

FOLDER = "watched_folder"   # the folder we are protecting
BASELINE = "baseline.txt"   # where the "known good" fingerprints are saved


# Turn a file's contents into a SHA-256 fingerprint (hash).
# If even one character in the file changes, the hash completely changes.
def hash_file(path):
    file = open(path, "rb")   # "rb" = read the raw bytes
    data = file.read()
    file.close()
    return hashlib.sha256(data).hexdigest()


# Build a dictionary of every file in the folder -> its hash
def get_hashes():
    hashes = {}
    for name in os.listdir(FOLDER):
        path = os.path.join(FOLDER, name)
        if os.path.isfile(path):
            hashes[name] = hash_file(path)
    return hashes


choice = input("Type 1 to create a baseline, or 2 to check for changes: ")

# Option 1: save the current fingerprints as the known-good baseline
if choice == "1":
    hashes = get_hashes()
    file = open(BASELINE, "w")
    for name in hashes:
        file.write(name + "," + hashes[name] + "\n")
    file.close()
    print("Baseline saved for", len(hashes), "files.")

# Option 2: compare the folder right now against the baseline
elif choice == "2":
    old = {}
    file = open(BASELINE, "r")
    for line in file:
        name, saved_hash = line.strip().split(",")
        old[name] = saved_hash
    file.close()

    new = get_hashes()
    changes = 0

    for name in new:
        if name not in old:
            print("NEW FILE:     ", name)
            changes = changes + 1
        elif new[name] != old[name]:
            print("MODIFIED:     ", name)
            changes = changes + 1

    for name in old:
        if name not in new:
            print("DELETED:      ", name)
            changes = changes + 1

    if changes == 0:
        print("No changes. All files match the baseline.")
    else:
        print(changes, "change(s) detected.")

else:
    print("Please type 1 or 2.")
