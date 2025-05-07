
def get_tip_for_block(block_label):
    tips = {
        "oak_log": "Punch it until it drops wood, then craft planks.",
        "stone": "Mine with pickaxe to gather cobblestone.",
        "dirt": "Use shovel to collect or move.",
        "Block_001": "Try punching longer. Watch for cracks, then collect drop.",
        "Block_002": "Punch until it breaks, check if it drops anything useful."
    }
    return tips.get(block_label, "No known tip for this block yet.")
