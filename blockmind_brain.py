
class BlockmindBrain:
    def __init__(self, profile):
        # Ensure profile is a dictionary, even if something else is passed by mistake
        if not isinstance(profile, dict):
            print("⚠️ Warning: profile is not a dict. Defaulting to empty profile.")
            profile = {}
        self.profile = profile
        print(f"🔧 Initialized BlockmindBrain for {self.profile.get('name', 'Unknown')}")

    def think(self):
        print("🧠 Blockmind is thinking...")
        # Add your AI decision-making logic here
