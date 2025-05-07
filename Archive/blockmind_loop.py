import time
import random
import hashlib
from collections import defaultdict
import traceback

from blockmind_window_capture import capture_game_window_image as grab_game_window
from blockmind_vision import analyze_frame
import controls
from memory import log_memory
from navigation_memory import load_navigation_memory, save_navigation_memory
from scene_builder import build_scene_model
from scene_decider import decide_action_from_scene
from survival_brain import SurvivalBrain
from goal_planner import choose_goal, plan_steps_for_goal, load_goal_catalog

# === MEMORY ===
scene_history = load_navigation_memory()
survival = SurvivalBrain()
behavior_log = []
current_goal = None
current_plan = []
goals = load_goal_catalog("full_goal_catalog.json")

# === UTILS ===
def frame_hash(frame):
    return hashlib.md5(frame.tobytes()).hexdigest()

# === MAIN LOOP ===
def blockmind_autopilot_loop(should_continue=lambda: True):
    print("🧠 Blockmind Autopilot: Navigation + Smart Punching + Survival Brain")

    day_counter = 1
    survival.set_day(day_counter)

    while should_continue():
        frame_before = grab_game_window()
        if frame_before is None:
            print("❌ Could not capture game window.")
            time.sleep(1)
            continue

        try:
            vision_data = analyze_frame(frame_before)
        except Exception:
            print("❌ Error in analyze_frame:")
            traceback.print_exc()
            continue

        scene = build_scene_model(frame_before)
        print("🌍 Scene Model:")
        for e in scene["entities"]:
            print(f" - Entity: {e['label']} at {e['bbox']}")
        for b in scene["blocks"]:
            print(f" - Block: {b['label']} at {b['bbox']}")

        frame_id = frame_hash(frame_before)
        scene_history[frame_id] += 1
        visits = scene_history[frame_id]

        # === GOAL + PLAN ===
        global current_goal, current_plan
        if not current_goal or not current_plan:
            current_goal = choose_goal(scene, goals)
            current_plan = plan_steps_for_goal(current_goal, goals, scene)
            print(f"🔢 New Goal: {current_goal}")
            print(f"🔮 Plan: {current_plan}")

        if current_plan:
            action = current_plan.pop(0)
        else:
            action = decide_action_from_scene(scene)

        print(f"🤖 Blockmind Chose: {action}")
        behavior_log.append(action)

        result = "fail"

        # === Execute Action ===
        try:
            action_type = action.get("type")
            if action_type == "move":
                direction = action.get("direction", "forward")
                if direction == "forward":
                    controls.move_forward(duration=random.uniform(0.5, 1.2))
                elif direction == "strafe_left":
                    controls.strafe_left()
                elif direction == "strafe_right":
                    controls.strafe_right()
                elif direction == "turn":
                    angle = action.get("angle", 15)
                    controls.turn_right(angle)
                elif direction == "jump":
                    controls.jump()
                result = "success"

            elif action_type == "punch":
                initial_hash = frame_hash(frame_before)

                def block_changed():
                    frame_now = grab_game_window()
                    return frame_now is not None and frame_hash(frame_now) != initial_hash

                controls.punch(max_duration=5.0, observe_fn=block_changed)
                result = "success" if block_changed() else "fail"

            elif action_type == "look":
                direction = action.get("direction", "around")
                if direction == "left":
                    controls.look_left()
                elif direction == "right":
                    controls.look_right()
                elif direction == "around":
                    controls.look_around()
                elif direction == "down":
                    controls.look_down()
                result = "success"

            elif action_type == "craft":
                print(f"🛠️ Crafting: {action.get('item')}")
                result = "success"

            elif action_type == "activate":
                print(f"✨ Trying to activate {action.get('target')}")
                controls.right_click()
                result = "success"

            elif action_type == "enter":
                print(f"🚪 Trying to enter {action.get('target')}")
                controls.move_forward(duration=1.5)
                result = "success"

            elif action_type == "plant":
                print(f"🌱 Planting {action.get('item')}")
                controls.right_click()
                result = "success"

            elif action_type == "till":
                print("🌾 Tilling soil...")
                controls.right_click()
                result = "success"

            else:
                print(f"⚠️ Unknown action type: {action_type}")
                result = "fail"

        except Exception as e:
            print(f"❌ Error performing action: {e}")
            traceback.print_exc()

        log_memory(vision_data, action, result)
        print(f"🧠 Action result: {result}")

        # === Survival Advice ===
        print("📘 Survival Goals & Advice:")
        survival.set_day(day_counter)
        raw_hunger = scene["player"].get("food", 20)
        try:
            hunger_level = int(raw_hunger)
        except:
            hunger_level = 20

        tips = survival.suggest_next_action(
            behavior_log=behavior_log[-10:],
            hunger_level=hunger_level
        )

        for tip in tips:
            print("🧠", tip)

        time.sleep(random.uniform(0.6, 1.2))

    save_navigation_memory(scene_history)
    print("🚓 Blockmind Autopilot stopped. Navigation memory saved.")

