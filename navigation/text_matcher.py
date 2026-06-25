import re


def point_inside(point, box):
    x, y = point
    x1, y1, x2, y2 = box
    return x1 <= x <= x2 and y1 <= y <= y2


def normalize_text(text):
    text = text.strip().upper()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^A-Z0-9_/.-]", "", text)
    return text


def looks_like_room_label(text):
    s = normalize_text(text)

    if not s or len(s) > 15:
        return False

    if not any(ch.isalpha() for ch in s):
        return False

    return True


def match_text_to_rooms(detections, texts):
    matched = []

    room_detections = [
        d for d in detections
        if d["class"].lower() == "room"
    ]

    for det in room_detections:
        x1, y1, x2, y2 = det["bbox"]
        room_name = "Unknown"
        best_conf = -1.0

        for t in texts:
            if not looks_like_room_label(t["text"]):
                continue

            pts = t["bbox"]
            cx = sum(p[0] for p in pts) / len(pts)
            cy = sum(p[1] for p in pts) / len(pts)

            if point_inside((cx, cy), (x1, y1, x2, y2)):
                if t["confidence"] > best_conf:
                    room_name = normalize_text(t["text"])
                    best_conf = t["confidence"]

        if best_conf < 0.35:
            room_name = "Unknown"

        matched.append({
            "room": room_name,
            "confidence": max(best_conf, 0.0),
            "bbox": det["bbox"],
            "center": (
                int((x1 + x2) / 2),
                int((y1 + y2) / 2)
            )
        })

    return matched
