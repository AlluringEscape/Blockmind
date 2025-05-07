class SurvivalPlanner:
    NEEDS_HIERARCHY = [
        "evade_threats",
        "acquire_food",
        "secure_shelter",
        "mine_resources",
        "explore_environment"
    ]

    def __init__(self):
        self.last_health = 20
        self.last_hunger = 20

    def choose_goal(self, state):
        # Threat detection
        threats = ["creeper", "zombie", "skeleton", "spider"]
        if any(d["label"] in threats for d in state.get("detections", [])):
            return "evade_threats"

        # Health priority
        if state.get("health", 20) < 10:
            return "heal"

        # Hunger management
        if state.get("hunger", 20) < 8:
            return "acquire_food"

        # Progressive goals
        inventory = state.get("inventory", [])
        if "wood" not in inventory:
            return "mine_resources"
        if "bed" not in inventory:
            return "secure_shelter"
            
        return "explore_environment"