import json
from collections import Counter

def load_trading_recipes(file_path="trading_recipes.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def can_trade(offer, inventory):
    inventory_count = Counter(inventory)
    cost = Counter(offer["give"])
    for item, amt in cost.items():
        if inventory_count[item] < amt:
            return False
    return True

def get_possible_trades(inventory, villager_type, trade_data):
    possible = []
    if villager_type not in trade_data:
        return []

    offers = trade_data[villager_type]["offers"]
    for offer in offers:
        if can_trade(offer, inventory):
            possible.append(offer)
    return possible
