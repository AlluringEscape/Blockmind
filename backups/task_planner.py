
class TaskPlanner:
    def __init__(self):
        self.task_memory = []

    def plan_task(self, scene_info):
        if not scene_info:
            return "scan_area"

        if scene_info.get("summary", {}).get("tree"):
            return "gather_wood"
        if scene_info.get("summary", {}).get("animal"):
            return "hunt_animal"
        if scene_info.get("summary", {}).get("cave"):
            return "explore_cave"
        return "wander"
