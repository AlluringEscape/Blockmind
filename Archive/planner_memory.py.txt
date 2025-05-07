# === planner_memory.py ===
import json
import os
from datetime import datetime

MEMORY_FILE = "memory/planner_memory.json"

class PlannerMemory:
    def __init__(self):
        self.plans = []
        self.load()

    def load(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    self.plans = json.load(f)
            except:
                self.plans = []

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.plans, f, indent=2)

    def record_plan(self, goal, steps):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "goal": goal,
            "steps": steps,
            "results": {s: None for s in steps}
        }
        self.plans.append(entry)
        self.save()

    def record_result(self, step, success):
        if not self.plans:
            return
        last = self.plans[-1]
        if step in last["results"]:
            last["results"][step] = success
        self.save()

    def get_last_successful_plan(self):
        for plan in reversed(self.plans):
            if all(v is True for v in plan["results"].values()):
                return plan
        return None

    def summarize(self):
        print("📘 === Stored Plans ===")
        for plan in self.plans[-5:]:
            print(f"Goal: {plan['goal']}")
            for step, result in plan["results"].items():
                icon = "✅" if result else "❌" if result is False else "⭕"
                print(f"  {icon} {step}")
            print("---")
