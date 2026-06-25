class Room:

    def __init__(self, id, name, bbox):

        self.id = id
        self.name = name
        self.bbox = bbox

        x1, y1, x2, y2 = bbox

        self.center = (
            (x1 + x2) / 2,
            (y1 + y2) / 2
        )

        self.neighbors = []

    def __str__(self):

        return f"{self.name} ({self.center})"