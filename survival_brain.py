class SurvivalPlanner:
    def __init__(self):
        self.current_stage = 1  # 1: Wood, 2: Stone, 3: Shelter
        
    def choose_goal(self, state):
        inventory = state.get("inventory", [])
        
        # Progressive survival stages
        if self.current_stage == 1 and "wood" not in inventory:
            return "gather_wood"
        elif self.current_stage == 2 and "stone" not in inventory:
            return "mine_stone"
        return "explore"
    
    def update_stage(self, new_stage):
        self.current_stage = new_stage