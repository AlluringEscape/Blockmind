import requests
import json
import os
import time
import pyautogui
import cv2
import numpy as np
import importlib
import traceback
from blockmind_vision import analyze_frame
from task_planner import TaskPlanner
from planner_memory import PlannerMemory
import self_updater

blockmind_actions = None
try:
    import blockmind_actions as actions
    blockmind_actions = actions
except Exception as e:
    print(f"⚠️ Failed to import blockmind_actions: {e}")

WOOD_ALIASES = ["log", "wood", "oak_log", "tree"]
STONE_ALIASES = ["stone", "cobblestone", "rock"]
FOOD_ALIASES = ["apple", "bread", "cooked_porkchop"]

class BlockmindBrain:
    def __init__(self, profile):
        self.name = profile.get("name", "Blockmind")
        self.model = profile.get("model", "meta-llama/meta-llama-3-8b-instruct")
        self.provider = profile.get("llm_provider", "llama3")
        self.api_url = profile.get("llm_url", "http://127.0.0.1:1234/v1/chat/completions")
        self.memory_file = f"memory_{self.name}.json"
        self.load_memory = profile.get("load_memory", True)
        self.memory = []
        self.task_planner = TaskPlanner()
        self.planner_memory = PlannerMemory()
        self.last_scene = None  # ✅ THIS IS REQUIRED
        if self.load_memory:
            self.load_from_disk()

    def start(self, init_message=None):
        print(f"🧠 {self.name} is ready.")
        if init_message:
            self.loop(init_message)

    def loop(self, first_message):
        prompt = first_message
        stuck_counter = 0

        while True:
            if not self.task_planner.has_tasks():
                suggested_goal = self.suggest_survival_goal()
                if suggested_goal:
                    plan_steps = self.task_planner.plan_steps(suggested_goal)
                    self.planner_memory.record_plan(suggested_goal, plan_steps)
                    self.task_planner.set_goal(suggested_goal)
                    prompt = f"I'm starting to {suggested_goal.replace('_', ' ')}."
                else:
                    print("⚠️ No survival goal determined.")
                    stuck_counter += 1
                    if stuck_counter > 2:
                        print("🧠 I feel stuck. Let me think how to improve...")
                        self.self_improve("No survival goal detected. Need better scene understanding or fallback logic.")
                    prompt = "What should I do now?"
                    continue

            task = self.task_planner.next_task()
            if task:
                print(f"➡️ Executing subtask: {task}")
                success = self.perform_action(task)
                self.planner_memory.record_result(task, success)
                if not success:
                    stuck_counter += 1
                    print(f"⚠️ Action failed: {task}")
                    if stuck_counter > 2:
                        pass  # originally self-improvement logic was here
                else:
                    stuck_counter = 0
                time.sleep(2)
                prompt = f"What will you do after {task.replace('_', ' ')}?"

    def suggest_survival_goal(self):
        if self.last_scene is not None:
            scene = self.last_scene
        else:
            screenshot = pyautogui.screenshot()
            screenshot.save("vision_debug.png")
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            scene = analyze_frame(img)

        print("👁️ Scene Info:", scene)
        advice = "Try gathering wood to begin."
        print(f"🧭 Memory Tip: {advice}")

        from survival_brain import suggest_goal
        return suggest_goal(scene)


    def think(self, message):
        messages = [
            {"role": "system", "content": "You are a Minecraft survival expert AI."}
        ] + self.memory + [
            {"role": "user", "content": message}
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }

        try:
            print(f"📡 Sending to {self.api_url} ...")
            res = requests.post(self.api_url, json=payload)
            res.raise_for_status()
            data = res.json()

            reply = data["choices"][0]["message"]["content"]
            self.memory.append({"role": "user", "content": message})
            self.memory.append({"role": "assistant", "content": reply})
            self.save_to_disk()
            return reply
        except Exception as e:
            print(f"❌ LLM error: {e}")
            return "I'm having trouble thinking right now."

    def self_improve(self, problem_description):
        tip = self.think(f"I am a Minecraft AI. Problem: {problem_description}. What new code or logic should I add to fix this?")
        print(f"💡 AI Suggestion: {tip}")
        with open("improvement_log.txt", "a") as f:
            f.write(f"\n[PROBLEM]: {problem_description}\n[SOLUTION]: {tip}\n")

    def log_action_result(self, action, success):
        path = "memory/action_results.json"
        if not os.path.exists("memory"):
            os.makedirs("memory")
        try:
            if os.path.exists(path):
                with open(path, "r") as f:
                    data = json.load(f)
            else:
                data = {}

            if action not in data:
                data[action] = {"success": 0, "fail": 0}

            if success:
                data[action]["success"] += 1
            else:
                data[action]["fail"] += 1

            with open(path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to log action result: {e}")

    def call_action_function(self, func):
        import inspect
        sig = inspect.signature(func)
        params = sig.parameters

        if len(params) == 0:
            func()
        else:
            dummy_args = {
                'world': None,
                'x_range': (0, 5),
                'y_range': (0, 5),
                'z_range': (0, 5)
            }
            args = [dummy_args.get(name, None) for name in params]
            func(*args)

    def perform_action(self, action):
        print(f"🎮 Performing action: {action}")
        success = False

        try:
            if hasattr(blockmind_actions, action):
                import inspect
                func = getattr(blockmind_actions, action)
                sig = inspect.signature(func)
                params = sig.parameters

                dummy_args = {
                    'world': None,
                    'x_range': (0, 5),
                    'y_range': (0, 5),
                    'z_range': (0, 5)
                }
                args = [dummy_args.get(name, None) for name in params]
                result = func(*args) if args else func()
                success = bool(result)

                if not success and self_updater.should_rewrite(action):
                    print(f"🔁 Detected failure — rewriting skill: {action}")
                    if self_updater.rewrite_broken_function(action, f"Fix skill: {action}"):
                        importlib.reload(blockmind_actions)
                        return self.perform_action(action)
            else:
                print(f"🧠 I don't know how to '{action}' yet.")
                if self_updater.try_to_learn_skill(action, f"Perform the Minecraft task: {action.replace('_', ' ')}"):
                    importlib.reload(blockmind_actions)
                    return self.perform_action(action)

        except Exception as e:
            print("❌ Error in perform_action:", e)
            traceback.print_exc()

        self.log_action_result(action, success)
        return success

    def load_from_disk(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    self.memory = json.load(f)
                print(f"💾 Memory loaded ({len(self.memory)} messages)")
            except Exception as e:
                print(f"⚠️ Failed to load memory: {e}")

    def save_to_disk(self):
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.memory, f, indent=2)
            print("💾 Memory saved")
        except Exception as e:
            print(f"⚠️ Failed to save memory: {e}")

    def shutdown(self):
        print("📥 Shutting down...")
        self.save_to_disk()
