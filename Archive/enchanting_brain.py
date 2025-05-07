import json

def load_enchantments(file_path="enchanting_options.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def get_enchantable_items(inventory, enchant_data):
    return [item for item in inventory if item in enchant_data]

def choose_enchantment(item, enchant_data):
    # Simple: pick best enchantment from list
    if item not in enchant_data:
        return None
    # Could be smarter later
    return enchant_data[item][0]  # highest priority enchant
