%%writefile route_finder1.pyimport sys
import pandas as pd
import networkx as nx

WALK_SPEED_M_PER_MIN = 80

EDGES_FILE = sys.argv[1] if len(sys.argv) > 1 else "edges.csv"
print("Loading", EDGES_FILE)                                       

nodes = pd.read_csv("nodes.csv")
edges = pd.read_csv(EDGES_FILE)                                   
ids = set(nodes["id"])

G = nx.Graph()
for _, row in nodes.iterrows():
    G.add_node(row["id"], name=row["name"])

for _, row in edges.iterrows():
    a, b = row["from"], row["to"]
    if a not in ids or b not in ids:
        print("Skipped edge with unknown ID:", a, b)
        continue
    if pd.isna(row["distance_m"]):
        print("Skipped edge without distance:", a, b)
        continue
    if float(row["distance_m"]) <= 0:
        print("Skipped edge with zero or negative distance:", a, b)
        continue
    if str(row["blocked"]).strip().lower() == "true":
        print("Skipped blocked edge:", a, b)
        continue
    if G.has_edge(a, b):
        print("Skipped duplicate edge:", a, b, "(kept", G[a][b]["weight"], "m)")
        continue
    G.add_edge(a, b, weight=float(row["distance_m"]))


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
