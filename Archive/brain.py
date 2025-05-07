import random
import cv2
from memory import recall_similar

def decide_action(vision_data):
    pixel = vision_data.get("center_pixel", (0, 0, 0))
    r, g, b = pixel[:3]
    brightness = (r + g + b) / 3

    # Extract vision
    entities = vision_data.get("entities_visible", 0)
    health = vision_data.get("health_avg_brightness", 100)
    food = vision_data.get("food_avg_brightness", 100)
    cross_rgb = vision_data.get("crosshair_rgb", [0, 0, 0])
    biome = vision_data.get("biome", "unknown")
    time_of_day = vision_data.get("time_of_day", "day")
    sky = vision_data.get("sky_visible", False)
    cross_target = vision_data.get("crosshair_target", "unknown")
    clutter = vision_data.get("structure_clutter", "low")

    # === Memory Recall ===
    recent_actions = recall_similar(vision_data)
    if recent_actions:
        print(f"🧠 Memory match: {recent_actions}")
        return random.choice(recent_actions)

    # === Vision Debug Console ===
    print("\n--- Blockmind Vision Debug ---")
    print(f"Biome: {biome} | Time: {time_of_day} | Sky: {sky}")
    print(f"Crosshair: {cross_target} | Clutter: {clutter}")
    print(f"Center Pixel RGB: {pixel}")
    print(f"Brightness: {brightness:.2f}")
    print(f"Entities Detected: {entities}")
    print(f"Health Brightness: {health}")
    print(f"Food Brightness: {food}")
    print(f"Crosshair RGB: {cross_rgb}")

    # === Behavior Tree ===

    # Emergency survival
    if health < 30 or food < 30:
        return random.choice(["strafe_left", "strafe_right", "look_around"])

    # Enemies or mobs
    if entities >= 3:
        return random.choice(["punch", "jump", "move_forward"])

    # Safe walkable area
    if cross_target == "air":
        return "move_forward"

    # Confined space
    if clutter == "high":
        return random.choice(["look_right", "look_left", "jump"])

    # Sky visible = likely looking up
    if sky:
        return random.choice(["look_down", "strafe_left", "strafe_right"])

    # Environment: biome reaction
    if biome == "grass":
        return random.choices(["move_forward", "jump", "look_around"], weights=[4, 1, 1])[0]

    if biome == "water":
        return random.choices(["jump", "strafe_left", "strafe_right"], weights=[3, 1, 1])[0]

    if time_of_day == "night":
        return random.choices(["look_around", "look_left", "strafe_right"], weights=[2, 1, 1])[0]

    # Default fallback
    return random.choices(
        ["move_forward", "jump", "look_right", "look_left", "look_around"],
        weights=[4, 2, 1, 1, 1]
    )[0]

# Compatibility alias
analyze_game_scene = decide_action
