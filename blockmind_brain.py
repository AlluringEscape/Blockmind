import random
import json
import os
import numpy as np
from config_loader import config

class BlockmindBrain:
    def __init__(self, profile):
        self.name = profile.get("name", "Blockmind")
        self.model = profile.get("model", "meta-llama/meta-llama-3-8b-instruct")
        self.provider = profile.get("llm_provider", "llama3")
        self.api_url = profile.get("llm_url", "http://127.0.0.1:1234/v1/chat/completions")
        self.memory_file = f"memory_{self.name}.json"
        self.load_memory = profile.get("load_memory", True)
        self.memory = []
        self.q_table = {}  
        self.epsilon = 0.1 
        # Add other initializations if needed


    def get_state_key(self, detections):
        """Create state signature from environment"""
        if not detections:
            return "empty"
            
        objects = sorted(set([d["label"] for d in detections]))
        return "_".join(objects)

    def choose_action(self, state_key):
        """Epsilon-greedy action selection"""
        if random.random() < self.epsilon or state_key not in self.q_table:
            return random.choice(["mine", "explore", "craft"])
            
        return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def update_model(self, state, action, reward, next_state):
        """Q-learning update with exploration decay"""
        # Initialize state if new
        if state not in self.q_table:
            self.q_table[state] = {
                "mine": 1.0, 
                "explore": 1.0, 
                "craft": 1.0
            }
            
        # Q-value calculation
        old_value = self.q_table[state].get(action, 1.0)
        next_max = max(self.q_table.get(next_state, self.q_table[state]).values())
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        
        # Update values
        self.q_table[state][action] = new_value
        self.epsilon = max(self.min_epsilon, self.epsilon * self.decay)
        self.action_count += 1
        
        # Periodic save
        if self.action_count % config.model["save_interval"] == 0:
            self.save_model()

    def calculate_reward(self, result):
        """Dynamic reward calculation"""
        reward = 0
        rewards = config.rewards
        
        # Positive rewards
        if result.get("wood"):
            reward += rewards["wood_collected"]
        if result.get("stone"):
            reward += rewards["stone_collected"]
        if result.get("successful_craft"):
            reward += rewards["successful_craft"]
            
        # Negative rewards
        if result.get("damage"):
            reward += rewards["damage_taken"]
        if result.get("death"):
            reward += rewards["death"]
            
        # Exploration bonus
        if result.get("exploration"):
            reward += rewards["exploration_step"]
            
        return reward

    def save_model(self):
        with open(self.model_file, 'w') as f:
            json.dump(self.q_table, f)

    def load_model(self):
        if os.path.exists(self.model_file):
            with open(self.model_file, 'r') as f:
                self.q_table = json.load(f)

    def think(self, context):
        """Process the vision context and decide on next action."""
        blocks = context.get("blocks", [])
        entities = context.get("entities", [])
        items = context.get("items", [])

        # Merge all observations
        all_detections = blocks + entities
        if isinstance(items, list):
            all_detections += items

        state_key = self.get_state_key(all_detections)
        action = self.choose_action(state_key)
        return {"state": state_key, "action": action}
