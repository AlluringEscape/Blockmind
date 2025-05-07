import json
import os
import time

DEFAULT_MEMORY_FILE = "memory_log.txt"

# === CONVERSATIONAL MEMORY ===

class MemoryManager:
    def __init__(self, name="Blockmind", file_path=None):
        self.name = name
        self.memory_file = file_path or f"memory_{name}.json"
        self.memory = []
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    self.memory = json.load(f)
                print(f"📥 Loaded memory for {self.name} ({len(self.memory)} messages)")
            except Exception as e:
                print(f"⚠️ Failed to load memory: {e}")

    def save_memory(self):
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.memory, f, indent=2)
            print(f"💾 Saved memory for {self.name}")
        except Exception as e:
            print(f"⚠️ Failed to save memory: {e}")

    def add_message(self, role, content):
        self.memory.append({"role": role, "content": content})
        self.save_memory()

    def get_memory(self):
        return self.memory

# === SURVIVAL TASK MEMORY ===

def remember(task, result, memory_log=DEFAULT_MEMORY_FILE):
    entry = {
        "task": task,
        "result": result,
        "timestamp": time.time()
    }
    try:
        with open(memory_log, "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"🧠 Remembered task: {task}")
    except Exception as e:
        print(f"⚠️ Failed to remember task: {e}")

def recall_last_result(memory_log=DEFAULT_MEMORY_FILE):
    if not os.path.exists(memory_log):
        return None
    try:
        with open(memory_log, "r") as f:
            lines = f.readlines()
        if not lines:
            return None
        return json.loads(lines[-1])
    except Exception as e:
        print(f"⚠️ Failed to recall last result: {e}")
        return None
