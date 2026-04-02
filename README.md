# 🎮 Game Movement Intelligence Dashboard

A data-driven analytics dashboard built using Python and Streamlit to analyze player movement patterns, engagement zones, and gameplay behavior in a battle royale-style environment.

---

## 🌐 Live Demo

👉 https://kpf8ophsvvgazhhnnlepcm.streamlit.app/

---

## 📌 Problem Statement

Game designers often lack visibility into how players actually move through maps, where combat happens, and which zones are overused or ignored.

Without this insight, it becomes difficult to:

- balance maps  
- improve player experience  
- optimize engagement zones  
- reduce frustration (e.g., unfair death zones)  

---

## 👤 Who Is This For?

This tool is designed for **Level Designers** and **Game Product Teams** to:

- understand player behavior visually  
- identify map design issues  
- make data-driven design decisions  

---

## 💡 Solution

This dashboard transforms raw game telemetry into actionable insights by:

- Visualizing player movement paths  
- Identifying high-traffic and low-activity zones  
- Mapping combat, loot, and death events  
- Differentiating bot vs human behavior  
- Providing replay-based timeline analysis  
- Generating product-level insights for designers  

---

## 🚀 Features

### Core Features
- 📂 Process telemetry data (.nakama / parquet)  
- 🧹 Data cleaning and preprocessing  
- 🗺️ Player movement path visualization  
- 🔥 Traffic heatmap (hot zones)  
- 👤 Player filtering  
- 🎯 Event mapping (Kills, Deaths, Loot, Storm)  

### Advanced Features
- 🤖 Bot vs Human detection  
- ⏱️ Replay system with timeline slider  
- 📊 Engagement hotspot detection  
- ⚠️ High-risk (death) zone identification  
- 🟢 Safe zone detection  
- 🧠 Behavior pattern detection (Aggressive vs Passive)  
- 🧭 Player journey analysis  

---

## 🧠 Product Thinking

This is not just a visualization tool.

It is designed to help Level Designers:
- identify choke points and unfair zones  
- detect underutilized map areas  
- understand player behavior patterns  
- make actionable decisions to improve gameplay  

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Pandas  
- NumPy  
- Matplotlib  
- PyArrow  

---

## ▶️ How to Run Locally

```bash
git clone https://github.com/Dubey1209/game-movement-dashboard-Lila-.git
cd game-movement-dashboard-Lila-
pip install -r requirements.txt
python -m streamlit run src/app.py
