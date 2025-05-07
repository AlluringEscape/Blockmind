import multiprocessing
from blockmind_brain import BlockmindBrain
from overlay_window import run_overlay

if __name__ == "__main__":
    overlay_proc = multiprocessing.Process(target=run_overlay)
    overlay_proc.start()

    brain = BlockmindBrain("andy")
    brain.start(init_message="Let's begin survival.")
