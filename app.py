"""Campus Route Finder - Streamlit interface.

Run with:  streamlit run app.py
Uses the graph, rules and input check from route_finder1.py.
"""
import contextlib
import io

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

# Import the route finder quietly (it prints a demo route when loaded).
with contextlib.redirect_stdout(io.StringIO()) as load_log:
    import route_finder1 as rf

G = rf.G
SPEED = rf.WALK_SPEED_M_PER_MIN

st.set_page_config(page_title="Campus Route Finder", page_icon="🧭", layout="wide")
st.title("🧭 SEEU Campus Route Finder")
st.caption("Find a walking route between two places on the SEEU Tetovo campus. "
           f"Walking time = distance ÷ {SPEED} m per minute.")

# ---------- Input ----------
names = {n: G.nodes[n]["name"] for n in G.nodes}
options = sorted(G.nodes, key=lambda n: names[n].lower())
label = lambda n: f"{names[n]}  ({n})"

col1, col2 = st.columns(2)
start = col1.selectbox("Start", options, index=options.index("J01"), format_func=label)
goal = col2.selectbox("Destination", options, index=options.index("N05"), format_func=label)
algos = st.multiselect("Algorithms", ["BFS", "Dijkstra", "A*"], default=["BFS", "Dijkstra", "A*"])

def short(n):
    """Short label for the map: building number, or the full short name."""
    first = names[n].split(" ")[0]
    return first if first[0].isdigit() else names[n]

# ---------- Search ----------
def find(name):
    if name == "BFS":
        return nx.shortest_path(G, start, goal)
    if name == "Dijkstra":
        return nx.dijkstra_path(G, start, goal, weight="weight")
    return nx.astar_path(G, start, goal, heuristic=lambda a, b: 0, weight="weight")

if st.button("Find route", type="primary"):
    message = rf.check_input(start, goal)
    if message:
        st.warning(message)
    elif not algos:
        st.warning("Choose at least one algorithm.")
    else:
        results = []
        for name in algos:
            path = find(name)
            dist = nx.path_weight(G, path, weight="weight")
            results.append((name, path, dist))
        best = min(r[2] for r in results)

        cols = st.columns(len(results))
        for col, (name, path, dist) in zip(cols, results):
            with col:
                st.subheader(name)
                st.metric("Distance", f"{dist:.0f} m",
                          delta=None if dist == best else f"+{dist - best:.0f} m",
                          delta_color="inverse")
                st.metric("Walking time", f"{round(dist / SPEED, 1)} min")
                st.write(f"**{len(path) - 1} walkways**")
                st.markdown("\n".join(f"{i + 1}. {names[n]}" for i, n in enumerate(path)))

        # ---------- Map of the graph ----------
        st.subheader("Route on the campus graph")
        st.caption("Layout is schematic (positions are not real map positions yet).")
        pos = nx.kamada_kawai_layout(G, weight=None)
        fig, ax = plt.subplots(figsize=(10, 6))
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#c8d3d6", width=1.5)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color="#e6f0ef", edgecolors="#1e4e5c", node_size=350)
        colors = {"BFS": "#e07b39", "Dijkstra": "#1e4e5c", "A*": "#5aa469"}
        for k, (name, path, _) in enumerate(results):
            edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=edges, ax=ax, edge_color=colors[name],
                                   width=6 - 2 * k, label=name)
        nx.draw_networkx_nodes(G, pos, nodelist=[start, goal], ax=ax, node_color="#f4c542",
                               edgecolors="#1e4e5c", node_size=500)
        nx.draw_networkx_labels(G, pos, labels={n: short(n) for n in G}, ax=ax, font_size=8)
        ax.legend(loc="lower left")
        ax.axis("off")
        st.pyplot(fig)

with st.expander("Data loading log"):
    st.code(load_log.getvalue() or "No messages.")