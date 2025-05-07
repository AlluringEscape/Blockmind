# desire_engine.py

def choose_goal(scene):
    entities = [e["label"] for e in scene.get("entities", [])]
    blocks = [b["label"] for b in scene.get("blocks", [])]
    biome = scene.get("biome", "unknown")

    # If it sees trees and doesn't have shelter, build a house
    if any("tree" in b for b in blocks):
        return {
            "goal": "build_house",
            "reason": "Trees detected for building materials"
        }

    # If it sees a village, maybe it wants to trade or loot
    if "village" in scene.get("structures", []):
        return {
            "goal": "explore_village",
            "reason": "Village detected"
        }

    # If it sees animals and no food, hunt
    if any(e in ["chicken", "pig", "cow"] for e in entities):
        return {
            "goal": "gather_food",
            "reason": "Food source detected"
        }

    # Fallback
    return {
        "goal": "explore",
        "reason": "No specific objective"
    }
