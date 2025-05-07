class BlockmindBrain:
    def __init__(self):
        self.memory = []
        self.current_goal = "explore"
        
    def decide_action(self, state):
        detections = state.get("detections", [])
        
        # Simple decision tree
        if self.current_goal == "gather_wood":
            if any(d["label"] == "tree" for d in detections):
                return {"type": "mine", "target": "tree"}
            return {"type": "explore"}
            
        elif self.current_goal == "mine_stone":
            if any(d["label"] == "stone" for d in detections):
                return {"type": "mine", "target": "stone"}
            return {"type": "explore"}
            
        return {"type": "explore"}
    
    def update_goal(self, new_goal):
        self.current_goal = new_goal