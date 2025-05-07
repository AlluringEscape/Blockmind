# === task_planner.py ===
class TaskPlanner:
    def __init__(self):
        self.goal = None
        self.task_list = []


    def choose_goal(self, scene):
        summary = scene.get("summary", {})
        if summary.get("tree"):
            return "gather_wood"
        elif summary.get("animal"):
            return "collect_food"
        elif summary.get("cave"):
            return "mine_stone"
        elif summary.get("sky"):
            return "survive_night"
        return None


    def set_goal(self, goal):
        self.goal = goal
        self.task_list = self.plan_steps(goal)

    def has_tasks(self):
        return bool(self.task_list)

    def next_task(self):
        return self.task_list.pop(0) if self.task_list else None

    def plan_steps(self, goal):
        if goal == "gather_wood":
            return ["walk_to_tree", "punch_tree", "collect_log"]
        elif goal == "build_shelter":
            return ["gather_wood", "craft_planks", "place_walls", "place_roof"]
        elif goal == "collect_food":
            return ["explore_area", "find_animals", "hunt_animal", "collect_meat"]
        elif goal == "mine_stone":
            return ["craft_pickaxe", "find_stone", "mine_stone", "collect_stone"]
        elif goal == "survive_night":
            return ["build_shelter", "craft_torch", "wait_till_morning"]
        else:
            return ["look_around", "gather_info"]
