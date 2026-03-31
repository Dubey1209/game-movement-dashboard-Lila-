# 🏗️ System Architecture — Game Movement Intelligence Dashboard

This document explains the architecture and data flow of the Game Movement Intelligence Dashboard.

---

## 📌 Overview

The system is a single-page interactive analytics dashboard built using Streamlit.

It processes game telemetry data and converts it into visual insights for game designers.

---

## 🔄 High-Level Flow

Telemetry Data → Data Processing → Feature Engineering → Visualization → Insights

---

## 📂 Data Layer

### Input
- Telemetry files (`.nakama-0`, parquet format)

### Stored in
- `/data` folder

### Contents
Each file contains:
- player ID  
- timestamp  
- map ID  
- x, z coordinates  
- event type (Kill, Loot, etc.)  

---

## ⚙️ Processing Layer

### Step 1 — Data Loading
- Multiple files loaded dynamically  
- Controlled via sidebar slider  

### Step 2 — Data Cleaning
- Decode event types  
- Convert timestamps  
- Remove invalid/null rows  

### Step 3 — Feature Engineering
- Player type classification (Bot vs Human)  
- Coordinate transformation (game → minimap)  
- Zone assignment (map divided into regions)  

---

## 🧠 Analysis Layer

### Movement Analysis
- Player movement paths  
- Heatmap for traffic density  

### Event Analysis
- Kill / Death / Loot mapping  
- Storm death detection  

### Behavioral Analysis
- Aggressive vs Passive classification  
- Bot vs Human comparison  

### Zone Analysis
- Engagement hotspots  
- High-risk (death) zones  
- Safe zones  

---

## 🎮 Replay System

- Timeline slider filters data by timestamp  
- Allows replay of player movement and events  
- Enables temporal analysis of gameplay  

---

## 🖥️ Presentation Layer (UI)

Built using Streamlit.

### Sidebar Controls
- File selection  
- Player selection  
- Map selection  
- Replay time  
- Event filters  
- Theme toggle (Light/Dark)  

### Main Dashboard Sections
1. Key Metrics  
2. Movement Map  
3. Heatmap  
4. Event Map  
5. Product Insights  
6. Zone Analysis  
7. Behavior Analysis  
8. Summary Tables  

---

## 📊 Visualization Layer

- Matplotlib used for:
  - movement plotting  
  - heatmaps  
  - event overlays  

- Minimap images used as background  

---

## ⚡ Performance Considerations

- File loading limited via slider  
- Data filtered before visualization  
- Only selected replay window processed  

---

## 📈 Scalability Considerations

Future improvements:
- Move data to cloud storage (S3)  
- Use database (BigQuery / Snowflake)  
- Real-time streaming pipeline  
- Replace matplotlib with faster rendering  

---

## 🧩 Design Philosophy

The system is designed to:

- Be simple and interactive  
- Provide insights, not just visuals  
- Support decision-making for game designers  
- Balance performance with usability  

---

## 📌 Summary

The architecture follows a clear pipeline:

Data → Processing → Analysis → Visualization → Insights

This ensures the dashboard remains:
- scalable  
- interpretable  
- useful for product and design teams  