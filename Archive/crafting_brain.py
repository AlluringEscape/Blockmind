import json
from collections import Counter

def load_recipes(file_path="crafting_recipes.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def can_craft(recipe_items, inventory_items):
    inventory_counts = Counter(inventory_items)
    recipe_counts = Counter(recipe_items)

    for item, count in recipe_counts.items():
        if inventory_counts[item] < count:
            return False
    return True

def get_craftable_items(inventory_items, recipes, allow_station="none"):
    craftable = []
    for item, recipe in recipes.items():
        if recipe["station"] != allow_station and recipe["station"] != "none":
            continue
        if can_craft(recipe["requires"], inventory_items):
            craftable.append(item)
    return craftable
