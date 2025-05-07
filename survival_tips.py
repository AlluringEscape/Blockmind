def get_tip_for_block(label):
    tips = {
        "tree": "Trees give you wood. Punch them to gather logs.",
        "log": "Logs are used to craft planks. Punch to collect.",
        "wood": "Wood can be crafted into tools and shelter parts.",
        "stone": "Mine stone with a pickaxe to upgrade your tools.",
        "cobblestone": "Used to craft furnaces and stone tools.",
        "crafting_table": "Open it to craft better tools and items.",
        "chest": "Used to store items safely.",
        "dirt": "Good for quick shelter or scaffolding.",
        "sand": "Can be smelted into glass.",
        "zombie": "Avoid or attack zombies. They are hostile.",
        "skeleton": "Dangerous ranged mob. Block arrows or avoid.",
        "creeper": "Explodes. Back away and use ranged attacks."
    }
    return tips.get(label.lower(), f"No tip found for: {label}")
