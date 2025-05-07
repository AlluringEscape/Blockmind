
from perception import observe_environment
from break_detector import block_was_broken
from controls import punch
from narrator import narrate
import time

def punch_until_broken(max_attempts=10, delay=0.3):
    before = observe_environment()['full']
    punches = 0

    for i in range(max_attempts):
        punch()
        punches += 1
        time.sleep(delay)
        after = observe_environment()['full']
        if block_was_broken(before, after):
            narrate(f"✅ Block broke after {punches} punches.")
            return True, punches
        else:
            narrate(f"👊 Punch {punches} — still hitting...")
    narrate("❌ Gave up — block never broke.")
    return False, punches
