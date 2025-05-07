import json

PROFILE_FILE = "entity_profiles.json"

def rename_label(old_label, new_label):
    with open(PROFILE_FILE, "r") as f:
        profiles = json.load(f)

    if old_label not in profiles:
        print(f"❌ Label '{old_label}' not found.")
        return

    # Merge if the new label already exists
    if new_label in profiles:
        profiles[new_label].extend(profiles[old_label])
    else:
        profiles[new_label] = profiles[old_label]

    del profiles[old_label]

    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=2)

    print(f"✅ Renamed '{old_label}' → '{new_label}'")

def list_labels():
    with open(PROFILE_FILE, "r") as f:
        profiles = json.load(f)
    for label in profiles:
        print(f"- {label} ({len(profiles[label])} samples)")

if __name__ == "__main__":
    print("📘 Known Labels:")
    list_labels()
    old_label = input("Which label do you want to rename? ").strip()
    new_label = input(f"What is the correct name for '{old_label}'? ").strip()
    rename_label(old_label, new_label)
