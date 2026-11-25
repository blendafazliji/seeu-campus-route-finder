import pandas as pd
import networkx as nx

WALK_SPEED_M_PER_MIN = 80

nodes = pd.read_csv("nodes.csv")
edges = pd.read_csv("edges.csv")
ids = set(nodes["id"])

G = nx.Graph()
for _, row in nodes.iterrows():
    G.add_node(row["id"], name=row["name"])

for _, row in edges.iterrows():
    if row["from"] not in ids or row["to"] not in ids:
        print("Skipped edge with unknown ID:", row["from"], row["to"])
        continue
    if pd.isna(row["distance_m"]):
        print("Skipped edge without distance:", row["from"], row["to"])
        continue
    if str(row["blocked"]).strip().lower() != "true":
        G.add_edge(row["from"], row["to"], weight=float(row["distance_m"]))


def check_input(start, goal):
    """Return an error message, or None if the input is valid."""
    if start not in G or goal not in G:
        return "Error: location not found."
    if start == goal:
        return "You are already there (0 m)."
    if not nx.has_path(G, start, goal):
        return "No route found."
    return None


def run_all(start, goal):
    message = check_input(start, goal)
    if message:
        print(start, "->", goal, ":", message, "\n")
        return
    paths = [
        ("BFS", nx.shortest_path(G, start, goal)),
        ("Dijkstra", nx.dijkstra_path(G, start, goal, weight="weight")),
        ("A*", nx.astar_path(G, start, goal, heuristic=lambda a, b: 0, weight="weight")),
    ]
    for name, path in paths:
        distance = nx.path_weight(G, path, weight="weight")
        print(name)
        print("Route:", " -> ".join(G.nodes[n]["name"] for n in path))
        print("Distance:", distance, "m")
        print("Walking:", round(distance / WALK_SPEED_M_PER_MIN, 1), "min")
        print()


run_all("J01", "N05")
