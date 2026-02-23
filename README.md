The repository contains a single Python file, `read_so6.py`, which implements three core functions for handling SO6 flight traffic files to pandas for data analysis.

---

## Features

- Read raw SO6 files into structured data
- Group flight data by callsign
- Extract and clean waypoint-based routes
- Remove duplicate trajectory segments
- Prepare SO6 data for downstream processing or analysis

---

## Functions Overview

### `so6_to_df`

Reads a **raw SO6 file** and converts it into a structured data representation.

**Description**
- Parses the original SO6 file without altering its structure
- Serves as a base reader for further processing steps
- Redundadnt data, two waypoints in the same line of df
- File readed as the initial structure, raw, no filters or changes.

**Typical use cases**
- Initial inspection of SO6 data  
- Custom data pipelines built on top of raw SO6 inputs

---

### `so6_to_df_simple`

Processes SO6 data by **grouping records by callsign** and tracking changes in relevant variables.

**Description**
- Aggregates all records belonging to the same flight
- Stores variable changes in a list associated with each callsign

**Typical use cases**
- Flight-level trajectory analysis  
- Simplified representations of variable evolution along a route

---

### `so6_to_df_waypoints`

Reads the SO6 file in raw format and **splits multi-segment trajectories into individual waypoint lines**.

**Description**
- Divides complex trajectory segments into single-line waypoint entries
- Removes duplicate waypoints or repeated segments
- Produces a clean, waypoint-based representation of each route

**Typical use cases**
- Route reconstruction  
- Airspace and network analysis  
- Flight path visualization

---

## Route Extraction

All functions allow access to the **route information contained in the SO6 file**, enabling reconstruction of the complete flight trajectory based on waypoints and trajectory segments.

---

## Requirements

- Python 3.8 or newer
- Pandas no specific version
- No external dependencies (standard Python libraries only)
- No redundant data

---

## Usage Example 1

```python
from read_so6 import so6_to_df, so6_to_df_simple, so6_to_df_waypoints

# Read raw SO6 file
df_raw = so6_to_df("example.so6")

# Group SO6 data by callsign
df_simple = so6_to_df_simple("./route1/example.so6")

# Extract cleaned waypoint-based routes (Recommended)
df_waypoints = so6_to_df_waypoints("C:\Users\folder1\folder2\example.so6")
```
---

## Usage Example 2

```python
import read_so6

# Read raw SO6 file
df_raw = read_so6.so6_to_df("./route1/example.so6")

# Group SO6 data by callsign
```
df_simple = read_so6.so6_to_df_simple("C:\Users\folder1\folder2\example.so6")

# Extract cleaned waypoint-based routes (Recommended)
df_waypoints = read_so6.so6_to_df_waypoints("example.so6")
