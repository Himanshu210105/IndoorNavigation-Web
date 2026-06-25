import os
import cv2

def crop_rooms(image_path, detections, output_dir="outputs/crops"):

    os.makedirs(output_dir, exist_ok=True)

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Cannot read image: {image_path}")

    H, W = image.shape[:2]

    crops = []
    room_id = 1

    for det in detections:

        if det["class"] != "room":
            continue

        x1, y1, x2, y2 = map(int, det["bbox"])

        # Clamp coordinates to image boundaries
        x1 = max(0, min(x1, W - 1))
        y1 = max(0, min(y1, H - 1))
        x2 = max(0, min(x2, W))
        y2 = max(0, min(y2, H))

        if x2 <= x1 or y2 <= y1:
            print(f"Skipping invalid bbox: {det['bbox']}")
            continue

        crop = image[y1:y2, x1:x2]

        if crop.size == 0:
            print(f"Skipping empty crop: {det['bbox']}")
            continue

        filename = f"room_{room_id}.png"
        filepath = os.path.join(output_dir, filename)

        cv2.imwrite(filepath, crop)

        crops.append({
            "id": room_id,
            "image": filepath,
            "bbox": [x1, y1, x2, y2]
        })

        room_id += 1

    return crops