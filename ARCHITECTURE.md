#  System Architecture — Game Movement Intelligence Dashboard

This document explains the architecture, data flow, coordinate mapping logic, assumptions, and trade-offs of the Game Movement Intelligence Dashboard.

---

## 📌 Overview

The system is a single-page interactive analytics dashboard built using Streamlit.

Its purpose is to transform raw gameplay telemetry into visual and actionable insights for Level Designers. The tool helps analyze player movement, events, hotspots, pacing, and zone usage using a browser-based interface.

---

## 🔄 High-Level Flow

Telemetry Data → Data Cleaning → Feature Engineering → Coordinate Mapping → Visualization → Product Insights

---

## 📂 Data Layer

### Input
- Telemetry files (`.nakama-0`, parquet format)
- Minimap image assets for each map

### Stored in
- `/data` folder for telemetry files
- `/assets` folder for minimap images

### Contents
Each telemetry file contains:
- player ID
- timestamp
- match ID
- map ID
- x and z world coordinates
- event type (movement, kills, deaths, loot, storm deaths, etc.)

---

## ⚙️ Processing Layer

### Step 1 — Data Loading
- Multiple parquet files are loaded dynamically
- Number of files loaded is controlled by a sidebar slider
- All selected files are concatenated into one dataframe

### Step 2 — Data Cleaning
- Event values are decoded from bytes into readable text
- Timestamps are converted into numeric and datetime values
- Invalid / null rows are removed
- Data is filtered to keep only usable records

### Step 3 — Feature Engineering
- Player type is classified as Bot or Human
- Event date is derived from timestamp for date filtering
- Match ID is used for match-level filtering
- Map zones are derived by dividing the minimap into four high-level regions:
  - North-West
  - North-East
  - South-West
  - South-East

---

## 🧭 Coordinate Mapping Approach

This is the most important transformation in the tool.

Gameplay telemetry provides positions in world coordinates (`x`, `z`), but the dashboard must display them correctly on a 2D minimap image.

### Mapping logic
For each map:
- A fixed `origin` is defined
- A fixed `scale` is defined
- World coordinates are normalized relative to this origin
- Normalized values are scaled into minimap pixel coordinates
- The vertical axis is inverted to match image coordinate orientation

### Simplified formula
- `u = (x - origin_x) / scale`
- `v = (z - origin_z) / scale`
- `pixel_x = u * image_width`
- `pixel_y = (1 - v) * image_height`

### Why this works
This approach converts positions from game-space to image-space in a way that keeps movement, events, and heatmaps aligned with the minimap.

### Assumptions in mapping
- Map bounds are stable for each map
- The provided minimap images align consistently with the telemetry coordinate system
- Linear scaling is sufficient for representing player movement at the dashboard level

---

## 🧠 Analysis Layer

### Movement Analysis
- Player movement paths plotted on minimap
- Human and bot movement shown separately
- Replay-based movement progression using timeline slider

### Event Analysis
- Kill markers
- Death markers
- Loot markers
- Storm death markers

### Heatmap Analysis
- High-traffic area detection
- Zone-level movement density

### Behavioral Analysis
- Aggressive vs passive play classification
- Human vs bot activity comparison

### Zone Analysis
- Engagement hotspots
- High-risk (death) zones
- Safe zones
- Loot-heavy zones

### Product Insights Layer
A rule-based insights layer translates telemetry into human-readable conclusions for Level Designers. This makes the dashboard useful not just for observing data, but for supporting design decisions.

---

## 🎮 Replay System

The replay system is built using timestamp filtering.

### How it works
- A replay slider selects a time threshold
- Only movement and events with timestamp ≤ selected replay time are shown
- This allows the match to be explored progressively instead of only as a final aggregate state

### Why it matters
Designers can observe how player flow and combat evolve over time, rather than only looking at static heatmaps.

---

## 🖥️ Presentation Layer (UI)

Built using Streamlit.

### Sidebar Controls
- Theme toggle (Light / Dark)
- File count selector
- Player filter
- Map filter
- Date filter
- Match filter
- Replay time slider
- Event visibility toggles

### Main Dashboard Sections
1. Overview / Hero section
2. Metric cards
3. Movement Path
4. Traffic Heatmap
5. Event Map
6. Product Insights
7. Advanced Zone Analysis
8. Behavior and Journey Analysis
9. Summary Tables

### UI Design Goal
The dashboard is designed for Level Designers, not data scientists. Therefore:
- visuals are prioritized over raw tables
- interaction is simple and browser-friendly
- insights are written in plain English
- responsive styling improves readability across devices

---

## 📊 Visualization Layer

Matplotlib is used for:
- movement plotting
- heatmap rendering
- event overlay rendering

Minimap images are used as background layers for all spatial visualizations.

---

## ⚡ Performance Considerations

- Number of loaded files is limited by a slider
- Filters reduce data before visualization
- Replay view only processes the selected time window
- Visualizations are generated only for currently filtered slices

This keeps the dashboard usable without requiring a complex backend.

---

## ⚖️ Major Trade-offs

| Decision | Benefit | Trade-off |
|---------|---------|-----------|
| Streamlit for UI | Fast development and deployment | Less frontend flexibility than a custom React app |
| Matplotlib for visuals | Simple and reliable plotting | Not ideal for highly interactive or very large-scale rendering |
| Local parquet processing | Easy to implement and review | Not scalable for very large production datasets |
| Linear coordinate mapping | Easy to interpret and maintain | Less precise than advanced projection-based methods |
| Rule-based insights | Explainable and stable | Less adaptive than ML-based insight generation |

---

## 📝 Assumptions Made

- Telemetry files contain reliable map, timestamp, and event information
- Coordinate mapping can be handled using map-specific origin and scale values
- Bots can be distinguished using ID-based classification logic
- A browser-based dashboard is the fastest and most practical format for this assignment
- A simple zone grid is sufficient for decision support in this version of the tool

---

## 📈 What I Would Do Differently With More Time

- Add finer-grained zone segmentation instead of four broad quadrants
- Add real-time or near-real-time telemetry ingestion
- Support richer session-level replay controls
- Build stronger statistical summaries per match and per date
- Separate human-only and bot-only analytical views more deeply
- Replace static plotting with more interactive rendering for large datasets

---

## 📌 Summary

The architecture follows a clear and interpretable pipeline:

**Data → Cleaning → Feature Engineering → Coordinate Mapping → Visualization → Insights**

This makes the dashboard:
- usable for Level Designers
- understandable for reviewers
- scalable in concept
- strong enough to support product and map design decisions