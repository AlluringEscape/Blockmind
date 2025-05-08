import os
import importlib
import traceback
from datetime import datetime
import openai
import shutil
import json
import re

ACTIONS_FILE = "blockmind_actions.py"
BACKUP_DIR = "backups"
LOG_FILE = "memory/self_learn_log.json"
RESULTS_FILE = "memory/action_results.json"

openai.api_base = "http://127.0.0.1:1234/v1"
openai.api_key = "local"

def backup_actions_file():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy(ACTIONS_FILE, f"{BACKUP_DIR}/blockmind_actions_{timestamp}.py")

def request_code_from_llm(function_name, goal_description):
    prompt = f"""Write a valid Python function named {function_name} to perform the following Minecraft bot task: {goal_description}.
    Only return the Python code. Do not wrap it in triple backticks or markdown. Use pyautogui for inputs if needed."""

    response = openai.ChatCompletion.create(
        model="meta-llama/meta-llama-3-8b-instruct",
        messages=[
            {"role": "system", "content": "You are a Python coding assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
    )

    code = response.choices[0].message.content.strip()

    # Extract valid code only (strip markdown formatting)
    if code.startswith("```python") or code.startswith("```"):
        code = re.sub(r"```[a-z]*", "", code).strip()
        code = re.sub(r"```", "", code).strip()

    # Basic filter: must include def and match function name
    if "def " not in code or function_name not in code:
        log_failure(function_name, goal_description, code)
        return None

    return code

def rewrite_function(function_name, new_code):
    try:
        with open(ACTIONS_FILE, "r") as f:
            lines = f.readlines()

        backup_actions_file()

        with open(ACTIONS_FILE, "w") as f:
            inside = False
            for line in lines:
                if line.strip().startswith(f"def {function_name}("):
                    inside = True
                    f.write(new_code + "\n\n")  # write replacement code
                    continue
                if inside and line.strip().startswith("def "):
                    inside = False
                if not inside:
                    f.write(line)

        importlib.reload(importlib.import_module("blockmind_actions"))
        return True
    except Exception as e:
        print(f"❌ Rewrite error: {e}")
        traceback.print_exc()
        return False

def log_failure(func, goal, raw_output):
    log = {
        "function": func,
        "goal": goal,
        "bad_response": raw_output,
        "timestamp": datetime.now().isoformat()
    }
    os.makedirs("memory", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log, indent=2) + "\n")

def create_new_function(function_name, goal_description):
    print(f"📥 Creating missing function: {function_name}")
    code = request_code_from_llm(function_name, goal_description)
    if not code:
        print(f"❌ LLM failed to generate code for {function_name}")
        return False
    return inject_function(function_name, code)

def inject_function(function_name, code):
    try:
        backup_actions_file()
        with open(ACTIONS_FILE, "a") as f:
            f.write("\n\n" + code.strip() + "\n")
        importlib.reload(importlib.import_module("blockmind_actions"))
        print(f"✅ Injected new function: {function_name}")
        return True
    except Exception as e:
        print(f"❌ Injection error: {e}")
        traceback.print_exc()
        return False