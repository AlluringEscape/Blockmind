import json
import os
import random
import numpy as np

class BlockmindBrain:
    def __init__(self):
        self.q_table = {}
        self.epsilon = 0.3  # Exploration rate
        self.learning_rate = 0.1
        self.discount_factor = 0.9

    def get_state_hash(self, state):
        simplified_state = (
            tuple(sorted([d["label"] for d in state["detections"]])),
            state.get("health", 20),
            state.get("hunger", 20)
        )
        return hash(simplified_state)

    def choose_action(self, state, possible_actions):
        state_key = self.get_state_hash(state)
        
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(possible_actions)
            
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 1.0 for action in possible_actions}
            
        return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def update_q_values(self, state, action, reward, next_state):
        state_key = self.get_state_hash(state)
        next_state_key = self.get_state_hash(next_state)
        
        old_value = self.q_table.get(state_key, {}).get(action, 1.0)
        next_max = max(self.q_table.get(next_state_key, {}).values(), default=1.0)
        
        new_value = (1 - self.learning_rate) * old_value + \
                    self.learning_rate * (reward + self.discount_factor * next_max)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        self.q_table[state_key][action] = new_value