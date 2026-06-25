def overlap(a1, a2, b1, b2):
    return max(a1, b1) <= min(a2, b2)


def rooms_adjacent(box1, box2, margin=35):
    x1, y1, x2, y2 = box1
    a1, b1, a2, b2 = box2

    # Vertical neighbours
    if abs(x2 - a1) <= margin or abs(a2 - x1) <= margin:
        if overlap(y1, y2, b1, b2):
            return True

    # Horizontal neighbours
    if abs(y2 - b1) <= margin or abs(b2 - y1) <= margin:
        if overlap(x1, x2, a1, a2):
            return True

    return False
