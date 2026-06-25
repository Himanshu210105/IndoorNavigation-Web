from pathlib import Path
import os
import re
from functools import lru_cache

import cv2
import easyocr
import torch


PROJECT_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = PROJECT_DIR / "static" / "uploads" / "test.png"


@lru_cache(maxsize=1)
def get_reader():
    return easyocr.Reader(['en'], gpu=torch.cuda.is_available())


def read_texts(image_path):
    image_path = str(image_path)

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    if len(img.shape) == 3:
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    results = get_reader().readtext(img)

    texts = []
    for bbox, text, conf in results:
        clean = text.strip().upper()
        clean = re.sub(r"\s+", "", clean)
        clean = re.sub(r"[^A-Z0-9_/.-]", "", clean)

        if not clean:
            continue
        if len(clean) > 15:
            continue
        if not any(ch.isalpha() for ch in clean):
            continue

        texts.append({
            "text": clean,
            "confidence": float(conf),
            "bbox": bbox
        })

    return texts


if __name__ == "__main__":
    print("Reading:", IMAGE_PATH)
    print("Exists:", os.path.exists(str(IMAGE_PATH)))

    texts = read_texts(IMAGE_PATH)
    print("\nDetected Text:\n")
    for t in texts:
        print(t)
