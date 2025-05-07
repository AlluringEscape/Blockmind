
import os
import subprocess

LABEL_DIR = "datasets/unknown_screenshots"
LABEL_THRESHOLD = 100
TRAIN_CMD = [
    "yolo",
    "task=detect",
    "mode=train",
    "model=yolov8n.pt",
    "data=minecraft.yaml",
    "epochs=20",
    "imgsz=640"
]

def count_label_files():
    return len([f for f in os.listdir(LABEL_DIR) if f.endswith(".txt")])

def run_training():
    print("⚙️ Starting YOLOv8 training...")
    subprocess.run(TRAIN_CMD)
    print("✅ Training complete!")

def main():
    label_count = count_label_files()
    print(f"📦 Found {label_count} labeled files.")

    if label_count >= LABEL_THRESHOLD:
        run_training()
    else:
        print(f"⏳ Not enough data yet. Need {LABEL_THRESHOLD - label_count} more.")

if __name__ == "__main__":
    main()
