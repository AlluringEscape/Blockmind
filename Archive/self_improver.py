# self_improver.py
import os
import requests

SELF_IMPROVEMENT_LOG = "self_improvement_log.json"
LLM_ENDPOINT = "http://127.0.0.1:1234/v1/chat/completions"

def log_issue(issue, context=None):
    print(f"🛠️ Self-Improvement Triggered: {issue}")
    with open(SELF_IMPROVEMENT_LOG, "a") as f:
        f.write(f"\nISSUE: {issue}\nCONTEXT:\n{context}\n")

def request_fix(issue, context, file_to_modify):
    prompt = f"""
You are Blockmind, an autonomous AI playing Minecraft. You encountered an issue:

ISSUE: {issue}

CONTEXT:
{context}

Fix this by generating a working Python function and updating the relevant file: {file_to_modify}.
Return ONLY valid Python code (no comments, no explanation).
"""

    response = requests.post(LLM_ENDPOINT, json={
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    })

    result = response.json()
    code = result["choices"][0]["message"]["content"]
    print("🧠 AI Code Suggestion:\n", code)
    return code

def apply_fix_to_file(file_path, new_code):
    with open(file_path, "a") as f:
        f.write("\n\n# === Auto-added by Blockmind ===\n")
        f.write(new_code + "\n")
    print(f"✅ Code applied to {file_path}")

def fix_self(issue, context, file_to_patch="blockmind_brain.py"):
    log_issue(issue, context)
    new_code = request_fix(issue, context, file_to_patch)
    apply_fix_to_file(file_to_patch, new_code)
