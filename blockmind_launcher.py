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
