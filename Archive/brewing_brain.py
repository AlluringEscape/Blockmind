import json
from collections import Counter

def load_brewing_recipes(file_path="brewing_recipes.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def can_brew(recipe_items, inventory):
    inventory_counts = Counter(inventory)
    for item in recipe_items:
        if inventory_counts[item] == 0:
            return False
        inventory_counts[item] -= 1
    return True

def get_brewable_potions(inventory, recipes):
    brewable = []
    for potion, data in recipes.items():
        if can_brew(data["requires"], inventory) and data["fuel"] in inventory:
            brewable.append(potion)
    return brewable
