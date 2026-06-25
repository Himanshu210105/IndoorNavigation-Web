from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent

MODEL_PATH = str(PROJECT_DIR / "best.pt")
UPLOAD_FOLDER = str(PROJECT_DIR / "static" / "uploads")
OUTPUT_FOLDER = str(PROJECT_DIR / "static" / "results")

IMAGE_SIZE = 640
CONFIDENCE = 0.35
