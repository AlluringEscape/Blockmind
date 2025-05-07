import random

def decide_action_from_scene(scene):
    """
    Decide what action to take based on the scene model.
    Returns an action dict like: { "type": "move", "direction": "forward", "duration": 1.0 }
    """
    entities = scene.get("entities", [])
    blocks = scene.get("blocks", [])

    if any(e["label"] == "cow" for e in entities):
        print("🐄 Cow spotted! Walking toward it.")
        return {"type": "move", "direction": "forward", "duration": 1.5}

    if any(b["label"] in ["tree", "log"] for b in blocks):
        print("🌲 Tree detected. Punching it.")
        return {"type": "punch"}

    if any(b["label"] == "grass" for b in blocks):
        print("🌱 Just grass here. Walk around.")
        return {"type": "move", "direction": "turn", "angle": 15}

    print("🤔 Nothing interesting. Random walk.")
    return {"type": "move", "direction": "forward", "duration": 0.5}
