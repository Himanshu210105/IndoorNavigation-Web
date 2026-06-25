from flask import Flask, render_template, request
from pathlib import Path
from uuid import uuid4
from werkzeug.utils import secure_filename

from detect import detect_rooms
from ocr.room_reader import read_texts
from navigation.text_matcher import match_text_to_rooms
from navigation.graph_builder import build_graph
from navigation.astar import shortest_path
from navigation.draw_path import draw_navigation

app = Flask(__name__)

# Maximum upload size (16 MB)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_FOLDER_FS = BASE_DIR / "static" / "uploads"
RESULT_FOLDER_FS = BASE_DIR / "static" / "results"

UPLOAD_FOLDER_FS.mkdir(parents=True, exist_ok=True)
RESULT_FOLDER_FS.mkdir(parents=True, exist_ok=True)

rooms_data = []
graph_data = {}

current_image_fs_path = ""
current_image_url = ""
current_prediction_url = ""


def _display_label(node_name: str) -> str:
    if "_" in node_name:
        return node_name.rsplit("_", 1)[0]
    return node_name


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    global rooms_data
    global graph_data
    global current_image_fs_path
    global current_image_url
    global current_prediction_url

    file = request.files.get("image")

    if file is None or file.filename.strip() == "":
        return "No file selected.", 400

    filename = secure_filename(file.filename)

    if filename == "":
        filename = "floorplan.png"

    unique_name = f"{uuid4().hex}_{filename}"

    current_image_fs_path = str(
        UPLOAD_FOLDER_FS / unique_name
    )

    current_image_url = f"static/uploads/{unique_name}"

    file.save(current_image_fs_path)

    detections, prediction_path = detect_rooms(
        current_image_fs_path
    )

    current_prediction_url = "/" + prediction_path.replace("\\", "/")

    texts = read_texts(current_image_fs_path)

    all_rooms = match_text_to_rooms(
        detections,
        texts
    )

    rooms_data = [
        room
        for room in all_rooms
        if room["room"] != "Unknown"
    ]

    if len(rooms_data) == 0:
        rooms_data = all_rooms

    graph_data = build_graph(rooms_data)

    room_names = [
        room["node"]
        for room in rooms_data
    ]

    if len(room_names) == 0:

        return render_template(

            "result.html",

            image="",

            original="/" + current_image_url,

            prediction=current_prediction_url,

            path=[],

            path_found=False,

            navigation_steps=[],

            rooms=[],

            stats={
                "rooms": 0,
                "nodes": 0,
                "edges": 0,
                "path_length": 0
            },

            start=None,

            goal=None,

            message="No readable room labels were found."

        )

    return render_template(
        "select_rooms.html",
        rooms=room_names
    )


@app.route("/navigate", methods=["POST"])
def navigate():

    global rooms_data
    global graph_data
    global current_image_fs_path
    global current_image_url
    global current_prediction_url

    if len(rooms_data) == 0 or len(graph_data) == 0:
        return "Upload a floor plan first.", 400

    start = request.form.get("start")

    goal = request.form.get("goal")

    path = shortest_path(
        graph_data,
        start,
        goal
    )

    stem = Path(current_image_fs_path).stem

    output_fs = RESULT_FOLDER_FS / f"{stem}_navigation.png"

    output_url = f"/static/results/{stem}_navigation.png"

    if path:

        draw_navigation(

            current_image_fs_path,

            rooms_data,

            path,

            str(output_fs),

            start=start,

            goal=goal

        )

    edges = sum(
        len(v)
        for v in graph_data.values()
    ) // 2

    stats = {

        "rooms": len(rooms_data),

        "nodes": len(graph_data),

        "edges": edges,

        "path_length": len(path) if path else 0

    }

    navigation_steps = []

    if path:

        for i, node in enumerate(path):

            label = _display_label(node)

            if i == 0:

                navigation_steps.append(
                    f"Start from {label}"
                )

            elif i == len(path) - 1:

                navigation_steps.append(
                    f"Reach destination {label}"
                )

            else:

                navigation_steps.append(
                    f"Move to {label}"
                )

    return render_template(

        "result.html",

        image=output_url,

        original="/" + current_image_url,

        prediction=current_prediction_url,

        path=path if path else [],

        path_found=bool(path),

        navigation_steps=navigation_steps,

        rooms=rooms_data,

        stats=stats,

        start=start,

        goal=goal,

        message=""
        if path
        else f"No valid path found between {start} and {goal}."

    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )