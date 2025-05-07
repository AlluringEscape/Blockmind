
# Blockmind's knowledge of possible actions in the world (simplified starter set)
# This should be expanded from Minecraft wiki pages eventually

knowledge_base = [
    {
        "name": "Punch a tree",
        "goal": "Obtain wood",
        "requirements": [],
        "steps": ["Find a tree", "Move to the tree", "Punch until log breaks", "Collect the log"]
    },
    {
        "name": "Make wooden planks",
        "goal": "Create crafting material",
        "requirements": ["Have: Oak Log"],
        "steps": ["Open inventory", "Craft planks from Oak Log"]
    },
    {
        "name": "Make crafting table",
        "goal": "Enable more crafting",
        "requirements": ["Have: Oak Plank x4"],
        "steps": ["Open inventory", "Craft crafting table"]
    },
    {
        "name": "Explore",
        "goal": "Discover new areas",
        "requirements": [],
        "steps": ["Pick a direction", "Walk forward", "Look around"]
    },
    {
        "name": "Eat food",
        "goal": "Regain health or hunger",
        "requirements": ["Have: Edible item"],
        "steps": ["Select food item", "Right-click to eat"]
    },
    {
        "name": "Build shelter",
        "goal": "Stay safe at night",
        "requirements": ["Have: blocks to place"],
        "steps": ["Find location", "Place blocks to form a box"]
    }
]
