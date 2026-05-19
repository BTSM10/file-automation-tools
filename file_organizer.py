import os
import shutil
import sys

# ─── STEP 1: Get the target folder from the command line, or default to Downloads
if len(sys.argv) > 1:
    DOWNLOADS = os.path.expanduser(sys.argv[1])
else:
    DOWNLOADS = os.path.expanduser("~/Downloads")

# ─── STEP 2: Define categories and which extensions belong to each ────────────
CATEGORIES = {
    "Images":       [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "Documents":    [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".html"],
    "Videos":       [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
    "Audio":        [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Archives":     [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Installers":   [".dmg", ".pkg", ".exe", ".deb", ".iso"],
    "Code":         [".py", ".js", ".ts", ".html", ".css", ".json", ".sh"],
    "Network":      [".pkt", ".pcap", ".pcapng"],
    "Others":       [],   # catch-all for anything not matched above
}

# ─── STEP 3: Build a lookup table: extension → folder name ───────────────────
#   e.g. { ".pdf": "Documents", ".jpg": "Images", ... }
ext_to_folder = {}
for folder_name, extensions in CATEGORIES.items():
    for ext in extensions:
        ext_to_folder[ext] = folder_name

# ─── STEP 4: Scan the Downloads folder and move each file ────────────────────
moved = 0
skipped = 0

for filename in os.listdir(DOWNLOADS):
    full_path = os.path.join(DOWNLOADS, filename)

    # Skip folders — only process files
    if os.path.isdir(full_path):
        print(f"  [SKIP]  '{filename}' is a folder, leaving it alone.")
        skipped += 1
        continue

    # Skip hidden files (start with a dot, like .DS_Store)
    if filename.startswith("."):
        skipped += 1
        continue

    # Get the file extension in lowercase (e.g. ".PDF" → ".pdf")
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    # Look up which category this extension belongs to
    folder_name = ext_to_folder.get(ext, "Others")

    # Build the destination folder path and create it if it doesn't exist
    dest_folder = os.path.join(DOWNLOADS, folder_name)
    os.makedirs(dest_folder, exist_ok=True)

    # Move the file
    dest_path = os.path.join(dest_folder, filename)
    shutil.move(full_path, dest_path)

    print(f"  [MOVED] '{filename}'  →  {folder_name}/")
    moved += 1

# ─── STEP 5: Print a summary ─────────────────────────────────────────────────
print(f"\nDone! {moved} file(s) moved, {skipped} skipped.")
