"""SEEU Campus Route Finder - loads nodes.csv and edges.csv and compares
BFS, Dijkstra and A* (route, distance, walking time, nodes expanded)."""
import csv
import heapq
import math
from collections import deque

NODES_FILE = "nodes.csv"
EDGES_FILE = "edges.csv"

# Meters per pixel on your screenshot. Measure one real distance in Google Maps,
# measure the same distance in pixels on the screenshot, then divide.
# Example: 100 m on the ground = 250 px on the screenshot -> 0.4
METERS_PER_PIXEL = 0.25

WALK_SPEED_M_PER_MIN = 80  # about 4.8 km/h

START = "J01"  # Main entrance
GOAL = "N05"   # 305


def to_float(value):
    value = (value or "").strip()
    return float(value) if value else None


def to_bool(value):
    return (value or "").strip().lower() == "true"


def pixel_to_meters(a, b, nodes):
    """Straight-line distance in meters between two nodes, from their x,y."""
    na, nb = nodes[a], nodes[b]
    if None in (na["x"], na["y"], nb["x"], nb["y"]) or METERS_PER_PIXEL is None:
        return None
    return math.hypot(na["x"] - nb["x"], na["y"] - nb["y"]) * METERS_PER_PIXEL


def load_graph():
    nodes = {}
    with open(NODES_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            nid = row["id"].strip()
            if not nid:
                print("Warning: a row in nodes.csv has no ID and was skipped.")
                continue
            nodes[nid] = {"name": row["name"].strip(), "x": to_float(row["x"]), "y": to_float(row["y"])}

    graph = {nid: [] for nid in nodes}
    with open(EDGES_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            a, b = row["from"].strip(), row["to"].strip()
            if not a and not b:
                continue
            if a not in nodes or b not in nodes:
                print(f"Warning: edge {a} - {b} uses an unknown node ID and was skipped.")
                continue
            dist = to_float(row["distance_m"])
            if dist is None:
                dist = pixel_to_meters(a, b, nodes)
            if dist is None:
                raise ValueError(
                    f"Edge {a} - {b} has no distance_m, and no x/y positions + METERS_PER_PIXEL to estimate it.")
            blocked = to_bool(row["blocked"])
            graph[a].append((b, dist, blocked))
            graph[b].append((a, dist, blocked))
    return nodes, graph


def rebuild(came_from, goal):
    path = [goal]
    while path[-1] in came_from:
        path.append(came_from[path[-1]])
    return path[::-1]


def path_length(path, graph):
    total = 0
    for u, v in zip(path, path[1:]):
        total += min(d for (n, d, blocked) in graph[u] if n == v and not blocked)
    return total


def bfs(graph, start, goal):
    """Plain BFS: fewest hops, ignores distance."""
    queue, came_from, seen, expanded = deque([start]), {}, {start}, 0
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
    """Dijkstra when heuristic returns 0; A* otherwise."""
    heap, counter = [(heuristic(start), 0, start)], 0
    g, came_from, closed, expanded = {start: 0.0}, {}, set(), 0
    while heap:
        _, _, node = heapq.heappop(heap)
        if node in closed:
            continue
        closed.add(node)
        expanded += 1
        if node == goal:
            return rebuild(came_from, goal), expanded
        for nxt, d, blocked in graph[node]:
            if blocked:
                continue
            new_g = g[node] + d
            if new_g < g.get(nxt, float("inf")):
                g[nxt] = new_g
                came_from[nxt] = node
                counter += 1
                heapq.heappush(heap, (new_g + heuristic(nxt), counter, nxt))
    return None, expanded


def main():
    nodes, graph = load_graph()

    def zero(_):
        return 0.0

    def euclid_to_goal(n):
        d = pixel_to_meters(n, GOAL, nodes)
        return d if d is not None else 0.0  # falls back to Dijkstra if no positions

    print(f"Route: {nodes[START]['name']}  ->  {nodes[GOAL]['name']}\n")
    for label, fn in [("BFS", None), ("Dijkstra", zero), ("A*", euclid_to_goal)]:
        path, expanded = bfs(graph, START, GOAL) if fn is None else best_first(graph, START, GOAL, fn)
        if path is None:
            print(f"{label}: no route found (nodes expanded: {expanded})\n")
            continue
        dist = path_length(path, graph)
        print(f"{label}")
        print("  Route:    " + " -> ".join(nodes[n]["name"] for n in path))
        print(f"  Distance: {dist:.0f} m")
        print(f"  Walking:  {dist / WALK_SPEED_M_PER_MIN:.1f} min")
        print(f"  Nodes expanded: {expanded}\n")


if __name__ == "__main__":
    main()
