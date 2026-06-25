import cv2


def center(box):
    x1, y1, x2, y2 = box
    return (
        int((x1 + x2) / 2),
        int((y1 + y2) / 2)
    )


def draw_navigation(image_path, rooms, path, output, start=None, goal=None):
    img = cv2.imread(image_path)

    if img is None:
        raise FileNotFoundError(image_path)

    room_dict = {room["node"]: room for room in rooms if "node" in room}

    points = []
    for node in path:
        if node in room_dict:
            points.append(center(room_dict[node]["bbox"]))

    for i in range(len(points) - 1):
        cv2.line(img, points[i], points[i + 1], (255, 0, 0), 5)

    for node in path:
        if node not in room_dict:
            continue

        x, y = center(room_dict[node]["bbox"])

        if node == start:
            color = (0, 180, 0)      # green
        elif node == goal:
            color = (0, 0, 255)      # red
        else:
            color = (255, 0, 0)      # blue

        cv2.circle(img, (x, y), 8, color, -1)

        label = node
        cv2.putText(
            img,
            label,
            (x + 8, y - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2
        )

    cv2.imwrite(output, img)
    print("Navigation image saved:", output)
