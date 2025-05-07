
# blockmind_launcher.py
import time
from blockmind_vision import analyze_frame
from blockmind_brain import BlockmindBrain
from blockmind_actions import ActionHandler
from blockmind_memory import BlockmindMemory
from blockmind_survival_brain import SurvivalPlanner
from blockmind_self_improve import SelfImprover

print("🧠 Blockmind Autopilot: Full Autonomy Mode")

profile = {"name": "Blockmind"}
brain = BlockmindBrain(profile)
actions = ActionHandler()
memory = BlockmindMemory()
survival = SurvivalPlanner()
self_ai = SelfImprover()

try:
    while True:
        # === SEE ===
        state = analyze_frame()
        memory.save_state(state)

        # === THINK ===
        goal = survival.choose_goal(state)
        decision = brain.perform_action(state, goal)

        # === ACT ===
        result = actions.execute(decision)
        memory.log_result(state, decision, result)

        # === LEARN ===
        brain.learn_from_result(state, decision, result)

        # === SELF-IMPROVE ===
        self_ai.check_and_evolve(memory)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("🛑 Blockmind shutdown requested by user.")


# blockmind_brain.py
import random
import json
import os

class BlockmindBrain:
    def __init__(self, profile):
        self.name = profile.get("name", "Blockmind")
        self.memory_file = f"memory_{self.name}.json"
        self.memory = []
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                self.memory = json.load(f)

    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=2)

    def perform_action(self, state, goal):
        if goal == "explore":
            actions = [
                {"type": "move", "direction": "forward"},
                {"type": "look", "direction": "left"},
                {"type": "look", "direction": "right"},
                {"type": "jump"}
            ]
        elif goal == "collect_wood":
            actions = [
                {"type": "punch"},
                {"type": "mine"},
                {"type": "look", "direction": "down"},
                {"type": "move", "direction": "forward"}
            ]
        else:
            actions = [
                {"type": "move", "direction": "backward"},
                {"type": "jump"}
            ]

        action = random.choice(actions)
        self.memory.append({"state": state, "goal": goal, "action": action})
        self.save_memory()
        return action

    def learn_from_result(self, state, action, result):
        # Future: log success/failure and adjust behavior
        pass
