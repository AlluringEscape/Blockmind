import json

def load_smelting_recipes(file_path="smelting_recipes.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def get_smeltable_items(inventory, smelt_recipes):
    smeltable = []
    for item in inventory:
        if item in smelt_recipes:
            smeltable.append(item)
    return smeltable

def get_valid_fuel(inventory):
    valid_fuel = ["coal", "charcoal", "wood", "planks", "stick"]
    for item in inventory:
        if item in valid_fuel:
            return item
    return None
