class SurvivalPlanner:
    def __init__(self):
        self.stage = 1  # 1: Wood, 2: Stone
        
    def choose_goal(self, state):
        wood_count = len([i for i in state.get("inventory", []) if i == "tree"])
        if self.stage == 1 and wood_count < 5:
            return "gather_wood"
        return "mine_stone"