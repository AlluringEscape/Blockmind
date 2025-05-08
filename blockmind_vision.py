import cv2
from block_learner import detect_blocks, load_block_profiles
from entity_learner import detect_entities, load_profiles as load_entity_profiles
from item_learner import predict_item, load_item_profiles


def analyze_frame(frame):
    block_profiles = load_block_profiles()
    entity_profiles = load_entity_profiles()
    item_profiles = load_item_profiles()

    results = {
        "blocks": detect_blocks(frame, block_profiles),
        "entities": detect_entities(frame, entity_profiles),
        "items": predict_item(frame, item_profiles),
    }

    # Optional debug visualization
    debug_frame = frame.copy()
    for b in results["blocks"]:
        if "box" in b and "label" in b:
            cv2.rectangle(debug_frame, b["box"][:2], b["box"][2:], (0, 255, 0), 2)
            cv2.putText(debug_frame, b["label"], (b["box"][0], b["box"][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    for e in results["entities"]:
        if "box" in e and "label" in e:
            cv2.rectangle(debug_frame, e["box"][:2], e["box"][2:], (255, 0, 0), 2)
            cv2.putText(debug_frame, e["label"], (e["box"][0], e["box"][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    for i in results["items"]:
        if "box" in i and "label" in i:
            cv2.rectangle(debug_frame, i["box"][:2], i["box"][2:], (0, 0, 255), 2)
            cv2.putText(debug_frame, i["label"], (i["box"][0], i["box"][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)


    return results, debug_frame