import cv2

def visualize_rooms(image_path, rooms, output_path):

    image = cv2.imread(image_path)

    for room in rooms:

        x1, y1, x2, y2 = room["bbox"]

        cx = int((x1+x2)/2)
        cy = int((y1+y2)/2)

        cv2.rectangle(
            image,
            (x1,y1),
            (x2,y2),
            (0,255,0),
            2
        )

        cv2.circle(
            image,
            (cx,cy),
            5,
            (0,0,255),
            -1
        )

        cv2.putText(
            image,
            room["room"],
            (x1,y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,0,0),
            2
        )

    cv2.imwrite(output_path,image)

    print("Saved:",output_path)