
import json
import os

# === SUGGESTION FUNCTION ===
def suggest_goal(scene_info):
    try:
        observations = []

        if "entities" in scene_info:
            observations += [f"I see {e['label']}" for e in scene_info["entities"]]

        if "items" in scene_info:
            observations += [f"I see item {i['label']}" for i in scene_info["items"]]

        if "blocks" in scene_info:
            observations += [f"Nearby block: {b['label']}" for b in scene_info["blocks"]]

        context = " ".join(observations)
        print(f"🧭 Scene Summary: {context}")

        return parse_tip_to_goal(context)

    except Exception as e:
        print(f"❌ Error suggesting goal: {e}")
        return None

# === PARSER ===
def parse_tip_to_goal(tip_text):
    if "wood" in tip_text.lower() or "tree" in tip_text.lower():
        return "gather_wood"
    elif "shelter" in tip_text.lower():
        return "build_shelter"
    elif "explore" in tip_text.lower():
        return "explore_area"
    elif "food" in tip_text.lower() or "animal" in tip_text.lower():
        return "collect_food"
    elif "craft" in tip_text.lower():
        return "craft_pickaxe"
    elif "furnace" in tip_text.lower():
        return "make_furnace"
    return None
