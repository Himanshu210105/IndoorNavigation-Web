from pathlib import Path
import os

import cv2
import torch
from ultralytics import YOLO

from config import MODEL_PATH, IMAGE_SIZE, CONFIDENCE, OUTPUT_FOLDER


_MODEL = None


def get_model():
    global _MODEL

    if _MODEL is None:
        model_path = Path(MODEL_PATH)
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found: {MODEL_PATH}"
            )
        _MODEL = YOLO(MODEL_PATH)

    return _MODEL


def detect_rooms(image_path):
    image_path = str(image_path)
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    device = 0 if torch.cuda.is_available() else "cpu"
    model = get_model()

    results = model.predict(
        source=image,
        imgsz=IMAGE_SIZE,
        conf=CONFIDENCE,
        device=device,
        verbose=False
    )

    names = model.names
    detections = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detections.append({
                "class": names[cls].lower(),
                "confidence": conf,
                "bbox": [x1, y1, x2, y2]
            })

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                image,
                f"{names[cls]} {conf:.2f}",
                (x1, max(20, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    stem = Path(image_path).stem
    output_filename = f"{stem}_prediction.png"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    cv2.imwrite(output_path, image)

    # Flask-friendly relative URL path
    output_url = f"static/results/{output_filename}"

    return detections, output_url


if __name__ == "__main__":
    import sys

    sample = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent / "static" / "uploads" / "test.png")
    dets, out = detect_rooms(sample)
    print("Detected:", len(dets))
    for d in dets:
        print(d)
    print("Saved:", out)
