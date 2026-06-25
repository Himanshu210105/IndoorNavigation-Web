from collections import deque


def shortest_path(graph, start, goal):
    if start is None or goal is None:
        return None

    if start not in graph or goal not in graph:
        return None

    visited = set()
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)

            for neighbour in graph.get(node, []):
                if neighbour not in visited:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

    return None
