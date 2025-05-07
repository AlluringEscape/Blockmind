# goal_engine.py

import random
from world_model import analyze_environment

# === Supported Goals ===
GOALS = {
    "build_shelter": ["collect_wood", "craft_planks", "place_walls", "place_roof"],
    "craft_tools": ["collect_wood", "mine_stone", "craft_tools"],
    "explore": ["walk_forward", "look_around", "record_area"],
    "eat_food": ["collect_berries", "eat_food"],
    "mine_resources": ["mine_stone", "collect_item"],
}

# === GOAL SELECTOR ===
def determine_goal(scene):
    env = analyze_environment(scene)

    if env["danger_nearby"]:
        return "eat_food" if env["hunger_low"] else "explore"

    if env["shelter_needed"]:
        return "build_shelter"

    if env["has_wood"] and not env["has_tools"]:
        return "craft_tools"

    return random.choice(list(GOALS.keys()))

# === SUBGOAL PLANNER ===
def get_subgoals_for(goal):
    return GOALS.get(goal, ["explore"])
