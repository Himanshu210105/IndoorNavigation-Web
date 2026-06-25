from navigation.geometry import rooms_adjacent


def build_graph(rooms):
    graph = {}
    room_counter = {}

    for room in rooms:
        name = room["room"]
        room_counter[name] = room_counter.get(name, 0) + 1
        room["node"] = f"{name}_{room_counter[name]}"
        graph[room["node"]] = []

    for i in range(len(rooms)):
        for j in range(i + 1, len(rooms)):
            r1 = rooms[i]
            r2 = rooms[j]

            if rooms_adjacent(r1["bbox"], r2["bbox"]):
                graph[r1["node"]].append(r2["node"])
                graph[r2["node"]].append(r1["node"])

    return graph
