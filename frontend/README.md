# Frontend – Streamlit interface

A simple web interface for the Campus Route Finder. The user chooses a start and a destination by name, and the app shows the route, distance and walking time for BFS, Dijkstra and A*, and draws the routes on the campus graph.

It uses the same graph, data checks and input validation as `route_finder1.py` in the main folder, so the search logic is not duplicated.

## Files
- `app.py` – the Streamlit app
- `requirements.txt` – Python packages needed

## Run
From the **main project folder** (not from inside `frontend/`):

```
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

On Windows, if `streamlit` is not recognised:

```
py -m streamlit run frontend/app.py
```

The app opens in the browser at `http://localhost:8501`.

To load the test data with the four data problems instead of the clean data:

```
streamlit run frontend/app.py -- edges_test.csv
```

The "Data loading log" at the bottom of the page shows which file was loaded and which edges were skipped.

## What to try
- 305 FCST → LH4: BFS 433 m, Dijkstra and A* 343 m (BFS is 90 m longer)
- Main entrance → Main entrance: warning "You are already there (0 m)."
