# Data Dictionary – Campus Route Finder

The campus is stored as an undirected weighted graph in two CSV files:
**locations** are nodes (`nodes.csv`) and **walkways** are edges (`edges.csv`).
The dataset is hand-made from a campus map photo, distances are estimates, and it contains no personal data.

## Schema

```
Location (nodes.csv)                Connection (edges.csv)
+-----------+                       +-------------+
| id   PK   |<----------------------| from   FK   |
| name      |<----------------------| to     FK   |
| type      |                       | distance_m  |
| notes     |                       | blocked     |
+-----------+                       +-------------+
```

Each connection links two locations by their IDs and can be walked in both directions.

## nodes.csv – locations

| Field | Type | Meaning | Example | Constraint |
|---|---|---|---|---|
| `id` | text | Unique location ID (N = building, J = junction, P = parking) | `N05` | Unique, required |
| `name` | text | Name shown in the route output | `305 Faculty of Contemporary Sciences and Technologies (FCST)` | Required |
| `type` | text | Kind of location | `building` | `building`, `junction` or `parking` |
| `notes` | text | Optional comment | *(empty)* | Optional |

## edges.csv – walkways

| Field | Type | Meaning | Example | Constraint |
|---|---|---|---|---|
| `from` | text | ID of the first location of the walkway | `J01` | Must exist in `nodes.csv` |
| `to` | text | ID of the second location of the walkway | `N03` | Must exist in `nodes.csv` |
| `distance_m` | number | Walking distance of the walkway in meters | `100` | Required, greater than 0 |
| `blocked` | boolean | `True` if the walkway is closed and must not be used | `False` | `True` or `False` |

## Data rules (preprocessing)

When `edges.csv` is loaded, each row is checked in this order and skipped with a printed message if it fails:

1. Both IDs exist in `nodes.csv` → otherwise `Skipped edge with unknown ID`
2. `distance_m` is not empty → otherwise `Skipped edge without distance`
3. `distance_m` is greater than 0 → otherwise `Skipped edge with zero or negative distance`
4. `blocked` is not `True` (spaces and capital letters ignored) → otherwise `Skipped blocked edge`
5. The walkway is not already in the graph, in either direction → otherwise `Skipped duplicate edge` (the first row is kept)

## Current size

- 20 locations: 15 buildings, 2 junctions, 3 parking areas
- 23 walkways
