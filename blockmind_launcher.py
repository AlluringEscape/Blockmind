# blockmind_launcher.py
import time
import cv2
from blockmind_window_capture import capture_game_window
from blockmind_vision import analyze_frame
from config_loader import load_profile
from blockmind_brain import BlockmindBrain
from blockmind_actions import ActionHandler

print("🧠 Blockmind Autopilot: Vision + Brain Debug Mode")

profile = load_profile("profile.yaml") or {}
brain = BlockmindBrain(profile)
actions = ActionHandler()

try:
    while True:
        try:
            result = capture_game_window()

            if isinstance(result, tuple) and len(result) >= 2:
                frame, window_region = result[0], result[1]
            else:
                frame, window_region = result, None

            context, processed_frame = analyze_frame(frame)
            print("👁️ Vision Context:", context)

            actions.set_window_region(window_region)
            thought = brain.think(context)
            print("🧠 Thought:", thought)

            # Execute the action (safely handles missing fields)
            target_block = context.get("blocks", [{}])[0]
            result = actions.execute({
                "type": thought.get("action", "explore"),
                "target": target_block.get("label"),
                "center": target_block.get("center")
            })

            # Show what the bot sees
            cv2.imshow("Blockmind Vision", processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.2)

        except Exception as e:
            print("❌ ERROR:", e)
            time.sleep(1)

finally:
    cv2.destroyAllWindows()

