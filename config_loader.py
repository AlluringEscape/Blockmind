import yaml
import os

DEFAULT_PROFILE_PATH = "self_learning.yaml"

def load_profile(profile_path=DEFAULT_PROFILE_PATH):
    if os.path.exists(profile_path):
        with open(profile_path, "r") as f:
            return yaml.safe_load(f)
    else:
        print(f"⚠️ Profile not found at {profile_path}, loading empty profile.")
        return {}

class Config:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance
    
    def load_config(self):
        with open("self_learning.yaml", "r") as f:
            self.data = yaml.safe_load(f)
            
    @property
    def learning(self):
        return self.data.get("learning", {})
    
    @property
    def rewards(self):
        return self.data.get("rewards", {})
    
    @property 
    def vision(self):
        return self.data.get("vision", {})
    
    @property
    def model(self):
        return self.data.get("model", {})

    
    # Add other sections as needed

# Singleton access
config = Config()