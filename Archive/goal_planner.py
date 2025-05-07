import json
import random

def load_goal_catalog(path="full_goal_catalog.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load goal catalog: {e}")
        return {}

def choose_goal(scene, goals):
    if not goals:
        return "wander"

    # Example: choose based on current biome or default to random
    biome = scene.get("biome", "unknown")
    biome_goals = [g for g in goals if biome in goals[g].get("biomes", [])]

    if biome_goals:
        return random.choice(biome_goals)
    else:
        return random.choice(list(goals.keys()))

def plan_steps_for_goal(goal, goals, scene):
    if goal not in goals:
        print(f"⚠️ Goal '{goal}' not found in catalog.")
        return []

    steps = goals[goal].get("steps", [])
    return steps
