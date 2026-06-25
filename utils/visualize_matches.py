import cv2


def visualize_matches(image_path, rooms, output_path):

    img = cv2.imread(image_path)

    for room in rooms:

        x1, y1, x2, y2 = room["bbox"]

        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)

        cx = (x1+x2)//2
        cy = (y1+y2)//2

        cv2.circle(img, (cx,cy), 5, (0,0,255), -1)

        cv2.putText(
            img,
            room["room"],
            (x1, y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,0,0),
            2
        )

    cv2.imwrite(output_path, img)

    print("Saved:", output_path)