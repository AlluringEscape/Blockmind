import os
import json
import datetime

BACKUP_DIR = "memory_backups"

def find_latest_memory_file():
    files = [f for f in os.listdir() if f.startswith("memory_") and f.endswith(".json")]
    if not files:
        return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def backup_memory():
    memory_file = find_latest_memory_file()
    if not memory_file:
        print("❌ No memory file found.")
        return
    ensure_backup_dir()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"{memory_file}_backup_{timestamp}.json")
    os.rename(memory_file, backup_path)
    print(f"💾 Memory backed up to {backup_path}")

def reset_memory():
    memory_file = find_latest_memory_file()
    if memory_file:
        os.remove(memory_file)
        print(f"🧠 Memory file '{memory_file}' has been deleted.")
    else:
        print("🧠 No memory file to delete.")

def trim_memory(keep_last=10):
    memory_file = find_latest_memory_file()
    if not memory_file:
        print("❌ No memory file to trim.")
        return

    with open(memory_file, "r") as f:
        memory = json.load(f)

    trimmed = memory[-keep_last:]
    with open(memory_file, "w") as f:
        json.dump(trimmed, f, indent=2)

    print(f"✂️ Trimmed '{memory_file}' to last {keep_last} messages.")

def view_memory():
    memory_file = find_latest_memory_file()
    if not memory_file:
        print("❌ No memory file found.")
        return
    with open(memory_file, "r") as f:
        memory = json.load(f)
    for i, entry in enumerate(memory[-10:], 1):
        print(f"{i}. [{entry['role']}] {entry['content'][:100]}...")

# === Manual usage ===
if __name__ == "__main__":
    print("Memory Manager Options:\n1. Backup\n2. Reset\n3. Trim\n4. View")
    choice = input("Choose (1-4): ")
    if choice == "1":
        backup_memory()
    elif choice == "2":
        reset_memory()
    elif choice == "3":
        trim_memory()
    elif choice == "4":
        view_memory()
    else:
        print("❌ Invalid choice.")
