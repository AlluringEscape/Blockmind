class BlockmindBrain:
    def __init__(self):
        self.current_goal = "gather_wood"
        self.inventory = []
        
    def decide_action(self, state):
        detections = state.get("detections", [])
        target = None
        
        # Filter relevant targets
        targets = [d for d in detections if (
            (self.current_goal == "gather_wood" and d["label"] == "tree") or
            (self.current_goal == "mine_stone" and d["label"] == "stone")
        )]
        
        if targets:
            # Select highest confidence target
            target = max(targets, key=lambda x: x["confidence"])
            return {
                "type": "mine",
                "target": target["label"],
                "center": target["center"]
            }
            
        return {"type": "explore"}
    
    def update_inventory(self, item):
        self.inventory.append(item)
        if self.current_goal == "gather_wood" and len([i for i in self.inventory if i == "tree"]) >= 5:
            self.current_goal = "mine_stone"