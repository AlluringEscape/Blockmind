# task_planner.py

def plan(goal, scene):
    goal_type = goal["goal"]

    if goal_type == "build_house":
        return [
            {"type": "collect", "target": "wood"},
            {"type": "craft", "recipe": "planks"},
            {"type": "craft", "recipe": "crafting_table"},
            {"type": "build", "structure": "basic_shelter"}
        ]

    elif goal_type == "gather_food":
        return [
            {"type": "hunt", "target": "chicken"},
            {"type": "collect", "target": "meat"},
            {"type": "cook", "method": "furnace"}
        ]

    elif goal_type == "explore_village":
        return [
            {"type": "navigate", "target": "village"},
            {"type": "search", "target": "chests"},
            {"type": "loot", "target": "useful_items"}
        ]

    elif goal_type == "explore":
        return [
            {"type": "move", "direction": "forward", "duration": 1.0},
            {"type": "look", "direction": "around"}
        ]

    return []
