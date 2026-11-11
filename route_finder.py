"""SEEU Campus Route Finder: compare BFS, Dijkstra, and A* on CSV campus data.

A* uses a zero heuristic (equivalent to Dijkstra) because no geographic
coordinates are stored. BFS minimizes hops, not distance.
"""
import csv
import heapq
from collections import deque

NODES_FILE = "nodes.csv"
EDGES_FILE = "edges.csv"
WALK_SPEED_M_PER_MIN = 80
START = "J01"
GOAL = "N05"


def to_bool(value):
    return (value or "").strip().lower() == "true"


def load_graph():
    nodes = {}
    with open(NODES_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            node_id = row["id"].strip()
            if not node_id:
                continue
            nodes[node_id] = row["name"].strip()

    graph = {node_id: [] for node_id in nodes}
    with open(EDGES_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            a, b = row["from"].strip(), row["to"].strip()
            if a not in nodes or b not in nodes:
                print(f"Warning: unknown node in edge {a} - {b}; skipped.")
                continue
            try:
                distance = float(row["distance_m"])
            except (ValueError, TypeError):
                print(f"Warning: missing/invalid distance for {a} - {b}; skipped.")
                continue
            if distance < 0:
                raise ValueError(f"Negative distance for edge {a} - {b}")
            blocked = to_bool(row["blocked"])
            graph[a].append((b, distance, blocked))
            graph[b].append((a, distance, blocked))
    return nodes, graph


def rebuild(came_from, goal):
    path = [goal]
    while path[-1] in came_from:
        path.append(came_from[path[-1]])
    return path[::-1]


def path_length(path, graph):
    return sum(
        min(d for nxt, d, blocked in graph[a] if nxt == b and not blocked)
        for a, b in zip(path, path[1:])
    )


def bfs(graph, start, goal):
    queue = deque([start])
    came_from, seen, expanded = {}, {start}, 0
    while queue:
        node = queue.popleft()
        expanded += 1
        if node == goal:
            return rebuild(came_from, goal), expanded
        for nxt, _, blocked in graph[node]:
            if not blocked and nxt not in seen:
                seen.add(nxt)
                came_from[nxt] = node
                queue.append(nxt)
    return None, expanded


def best_first(graph, start, goal, heuristic):
    heap = [(heuristic(start), 0, start)]
    counter, g = 0, {start: 0.0}
    came_from, closed, expanded = {}, set(), 0
    while heap:
        _, _, node = heapq.heappop(heap)
        if node in closed:
            continue
        closed.add(node)
        expanded += 1
        if node == goal:
            return rebuild(came_from, goal), expanded
        for nxt, distance, blocked in graph[node]:
            if blocked or nxt in closed:
                continue
            new_g = g[node] + distance
            if new_g < g.get(nxt, float("inf")):
                g[nxt] = new_g
                came_from[nxt] = node
                counter += 1
                heapq.heappush(heap, (new_g + heuristic(nxt), counter, nxt))
    return None, expanded


def main():
    nodes, graph = load_graph()
    if START not in nodes or GOAL not in nodes:
        raise ValueError("START or GOAL is not present in nodes.csv")

    print(f"Route: {nodes[START]} -> {nodes[GOAL]}\n")
    for label in ("BFS", "Dijkstra", "A*"):
        if label == "BFS":
            path, expanded = bfs(graph, START, GOAL)
        else:
            path, expanded = best_first(graph, START, GOAL, lambda _: 0.0)
        if path is None:
            print(f"{label}: no route found (nodes expanded: {expanded})\n")
            continue
        distance = path_length(path, graph)
        print(label)
        print("  Route:    " + " -> ".join(nodes[node] for node in path))
        print(f"  Distance: {distance:.0f} m")
        print(f"  Walking:  {distance / WALK_SPEED_M_PER_MIN:.1f} min")
        print(f"  Nodes expanded: {expanded}\n")


if __name__ == "__main__":
    main()
