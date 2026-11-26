# SEEU Campus Route Finder

Finds a walking route between two locations on the SEEU Tetovo campus and shows its distance in meters and walking time (distance ÷ 80 m per minute). BFS is the non-AI baseline; Dijkstra and A* are compared with it.

ECS-609 Introduction to Artificial Intelligence · individual project · Blenda Fazliji

## Structure
```
route_finder1.py      loads the data, builds the graph, runs BFS, Dijkstra and A*
nodes.csv             locations (id, name, type, notes)
edges.csv             walkways (from, to, distance_m, blocked)
edges_test.csv        copy of edges.csv with four data problems, for testing
DATA_DICTIONARY.md    meaning and rules for every field
frontend/             Streamlit web interface (see frontend/README.md)
docs/                 weekly reports, test logs and the architecture diagram
```

## Run in Google Colab
1. Clone the repository:
   ```
   !git clone https://github.com/blendafazliji/seeu-campus-route-finder
   %cd seeu-campus-route-finder
   ```
2. Run the script. It prints any skipped edges and the route from Main entrance (J01) to 305 FCST (N05):
   ```
   %run route_finder1.py
   ```
3. Find another route with two IDs from `nodes.csv`:
   ```
   run_all("N05", "N15")
   ```
4. Run with the test data instead of the clean data:
   ```
   %run route_finder1.py edges_test.csv
   ```

## Run locally
```
pip install pandas networkx
python route_finder1.py
```

## Web interface
```
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```
See `frontend/README.md` for details.

## Data rules
Edges are skipped with a printed message if an ID is unknown, the distance is empty, zero or negative, the walkway is blocked, or the walkway is a duplicate (the first row is kept).
