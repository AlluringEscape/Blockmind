import json
import random
import os
from survival_data import load_survival_guide

# === CONFIG ===
SURVIVAL_GUIDE_FILE = "data/survival_guide.json"

# === LOAD SURVIVAL GUIDE ===
def load_survival_tips():
    if os.path.exists(SURVIVAL_GUIDE_FILE):
        with open(SURVIVAL_GUIDE_FILE, 'r') as f:
            return json.load(f)
    return {}

survival_tips = load_survival_tips()

# === CONTEXT HANDLING ===
def match_context_to_tips(context):
    context_lower = context.lower()
    for tag, tips in survival_tips.items():
        if tag.lower() in context_lower:
            return tag, tips
    return None, []

def choose_best_tip(tips):
    return random.choice(tips) if tips else None

# === DECISION ENGINE ===
def get_survival_tip(context):
    tag, tips = match_context_to_tips(context)
    tip = choose_best_tip(tips)
    if tip:
        return tag, tip
    else:
        fallback_tip = random.choice([
            "Explore the surrounding area to collect information.",
            "Collect nearby resources like wood or stone.",
            "Find or build shelter before nightfall.",
            "Craft basic tools using available materials.",
            "Look for food sources such as animals or crops."
        ])
        return None, fallback_tip

# === MAIN DECISION FUNCTION ===
def decide_next_survival_action(observations, memory):
    context = " ".join(observations)
    tag, tip = get_survival_tip(context)
    return f"Survival Tip [{tag}]: {tip}", (tag, tip)

# === DEBUG USAGE ===
if __name__ == "__main__":
    test_context = ["It is getting dark", "I see zombies nearby", "I'm near a river"]
    memory = []
    result, detail = decide_next_survival_action(test_context, memory)
    print(result)
    print(detail)
