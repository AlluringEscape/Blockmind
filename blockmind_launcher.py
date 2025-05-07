from blockmind_window_capture import capture_game_window
from blockmind_vision import analyze_frame
from blockmind_brain import BlockmindBrain
from blockmind_actions import ActionHandler
from survival_brain import SurvivalPlanner
import time

def main():
    brain = BlockmindBrain()
    actions = ActionHandler()
    survival = SurvivalPlanner()
    
    while True:
        # Perception
        frame, region = capture_game_window()
        if frame is None:
            time.sleep(2)
            continue
            
        state = analyze_frame(frame)
        state.update({
            "region": region,
            "timestamp": time.time()
        })

        # Cognition
        goal = survival.choose_goal(state)
        possible_actions = self.get_possible_actions(goal)
        action = brain.choose_action(state, possible_actions)

        # Action
        result = actions.execute(action)
        
        # Learning
        next_state = analyze_frame(capture_game_window()[0])
        reward = self.calculate_reward(state, action, result)
        brain.update_q_values(state, action, reward, next_state)

        time.sleep(0.3)

if __name__ == "__main__":
    main()