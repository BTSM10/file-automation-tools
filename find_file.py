import sys
import subprocess
import os

# ─── STEP 1: Make sure the user provided a search term ───────────────────────
if len(sys.argv) < 2:
    print("Usage: python3 find_file.py <filename or partial name>")
    print("Example: python3 find_file.py photo")
    sys.exit(1)

search_term = " ".join(sys.argv[1:])
print(f"Searching for '{search_term}'...")

# ─── STEP 2: Use Spotlight to search ─────────────────────────────────────────
result = subprocess.run(
    ["mdfind", "-name", search_term],
    capture_output=True,
    text=True
)

matches = [line for line in result.stdout.strip().split("\n") if line]

# ─── STEP 3: Handle no results ────────────────────────────────────────────────
if not matches:
    print(f"No files matching '{search_term}' found on your Mac.")
    sys.exit(0)

# ─── STEP 4: Show the list ────────────────────────────────────────────────────
print(f"\nFound {len(matches)} match(es):\n")
for i, path in enumerate(matches):
    filename = os.path.basename(path)   # just the filename, not the full path
    print(f"  [{i + 1}] {filename}")
    print(f"       {path}")             # full path shown below in gray indent

# ─── STEP 5: Ask user to pick by number or by typing the exact filename ───────
print("\nEnter a number or type the exact filename to open in Finder (or press Enter to cancel): ", end="")
choice = input().strip()

if not choice:
    print("Cancelled.")
    sys.exit(0)

# Check if they typed a number
if choice.isdigit():
    index = int(choice) - 1
    if 0 <= index < len(matches):
        selected = matches[index]
    else:
        print("Invalid number.")
        sys.exit(1)

# Check if they typed an exact filename
else:
    selected = None
    for path in matches:
        if os.path.basename(path) == choice:
            selected = path
            break

    if not selected:
        print(f"No match found for '{choice}' in the results.")
        sys.exit(1)

# ─── STEP 6: Open in Finder ───────────────────────────────────────────────────
subprocess.run(["open", "-R", selected])
print(f"Opened in Finder: {selected}")
