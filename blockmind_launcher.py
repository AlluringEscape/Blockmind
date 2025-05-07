from blockmind_window_capture import capture_game_window
from blockmind_vision import detect_objects
from blockmind_brain import BlockmindBrain
from blockmind_actions import ActionHandler
from survival_brain import SurvivalPlanner
import time

class BlockmindCore:
    def __init__(self):
        self.brain = BlockmindBrain()
        self.actions = ActionHandler()
        self.survival = SurvivalPlanner()
        self.inventory = []
        
    def run(self):
        while True:
            # Capture game state
            frame, region = capture_game_window()
            if frame is None:
                time.sleep(1)
                continue
                
            # Analyze environment
            vision_data = detect_objects(frame)
            game_state = {
                "detections": vision_data["detections"],
                "inventory": self.inventory
            }
            
            # Make decisions
            goal = self.survival.choose_goal(game_state)
            self.brain.update_goal(goal)
            action = self.brain.decide_action(game_state)
            
            # Execute action
            result = self.actions.execute(action)
            print(f"Performed {action}: {result}")
            
            # Update inventory
            if result.get("item"):
                self.inventory.append(result["item"])
            
            time.sleep(0.5)

if __name__ == "__main__":
    bot = BlockmindCore()
    bot.run()