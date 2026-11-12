import pandas as pd
import networkx as nx

nodes = pd.read_csv("nodes.csv")
edges = pd.read_csv("edges.csv")

G = nx.Graph()

for _, row in nodes.iterrows():
    G.add_node(row["id"], name=row["name"])

for _, row in edges.iterrows():
    if str(row["blocked"]).strip().lower() != "true":
        G.add_edge(
            row["from"],
            row["to"],
            weight=float(row["distance_m"])
        )

start = "J01"
goal = "N05"

# BFS: fewest connections
bfs_path = nx.shortest_path(G, start, goal)

# Dijkstra: shortest distance
dijkstra_path = nx.dijkstra_path(G, start, goal, weight="weight")

# A*: zero heuristic
astar_path = nx.astar_path(
    G, start, goal,
    heuristic=lambda a, b: 0,
    weight="weight"
)

for name, path in [
    ("BFS", bfs_path),
    ("Dijkstra", dijkstra_path),
    ("A*", astar_path)
]:
    distance = nx.path_weight(G, path, weight="weight")

    print(name)
    print("Route:", " -> ".join(G.nodes[n]["name"] for n in path))
    print("Distance:", distance, "m")
    print("Walking:", round(distance / 80, 1), "min")
    print()
