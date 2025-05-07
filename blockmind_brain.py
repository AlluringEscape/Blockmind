import requests
import json
import os
import time
import pyautogui
import cv2
import numpy as np
import importlib
import traceback
import pygetwindow as gw
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
        self.last_scene = None
        if self.load_memory:
            self.load_from_disk()

    def capture_game_window(self):
        try:
            win = gw.getWindowsWithTitle("Minecraft")[0]
            x, y, w, h = win.left, win.top, win.width, win.height
            full = pyautogui.screenshot()
            cropped = full.crop((x, y, x + w, y + h))
            return cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"⚠️ Could not find Minecraft window: {e}")
            return cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)

    def start(self, init_message=None):
        print(f"🧠 {self.name} is ready.")
        if init_message:
            self.loop(init_message)

    def loop(self, first_message):
        prompt = first_message
        stuck_counter = 0

        while True:
            img = self.capture_game_window()
            self.last_scene = analyze_frame(img)

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
                        pass
                else:
                    stuck_counter = 0
                time.sleep(2)
                prompt = f"What will you do after {task.replace('_', ' ')}?"

    def suggest_survival_goal(self):
        if self.last_scene is not None:
            scene = self.last_scene
        else:
            img = self.capture_game_window()
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
            func(**{k: dummy_args[k] for k in params if k in dummy_args})

    def perform_action(self, action_name):
        if not blockmind_actions:
            print("❌ No actions module loaded.")
            return False

        try:
            func = getattr(blockmind_actions, action_name)
            self.call_action_function(func)
            return True
        except AttributeError:
            print(f"🆕 Missing action: {action_name}. Attempting to create it...")
            success = self_updater.create_new_function(action_name, f"Define an action for {action_name} in Minecraft survival gameplay")
            if success:
                importlib.reload(importlib.import_module("blockmind_actions"))
                try:
                    func = getattr(blockmind_actions, action_name)
                    self.call_action_function(func)
                    return True
                except Exception as e:
                    print(f"❌ Error after injecting {action_name}: {e}")
                    return False
            return False
        except Exception as e:
            print(f"❌ Action error: {e}")
            traceback.print_exc()
            return False

    def save_to_disk(self):
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"⚠️ Memory save failed: {e}")

    
    def load_from_disk(self):
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, "r") as f:
                    self.memory = json.load(f)
            else:
                self.memory = []
        except Exception as e:
            print(f"⚠️ Failed to load memory: {e}")
            self.memory = []

    def think_and_act(self, frame):
        try:
            print("🧠 Analyzing scene...")
            scene = analyze_frame(frame)
            print(f"🌍 Scene detected: {scene}")

            goal = self.task_planner.choose_goal(scene)
            if not goal:
                print("❌ No valid goal found.")
                return

            print(f"🎯 Chosen goal: {goal}")
            actions = self.task_planner.plan(goal)
            print(f"🪛 Planned actions: {actions}")

            for action in actions:
                result = blockmind_actions.perform_action(action)
                print(f"✅ Action result: {result}")
                # You can add memory logging here if desired

        except Exception as e:
            print(f"❗ Error in think_and_act: {e}")

def load_from_disk(self):
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, "r") as f:
                    self.memory = json.load(f)
        except Exception as e:
            print(f"⚠️ Memory load failed: {e}")
