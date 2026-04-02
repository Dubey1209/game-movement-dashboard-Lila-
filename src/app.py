import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(
    page_title="Game Movement Intelligence Dashboard",
    page_icon="🎮",
    layout="wide"
)

# -------------------------
# BASIC PATH CHECKS
# -------------------------
data_path = "data"
assets_path = "assets"

if not os.path.exists(data_path):
    st.error("The data folder was not found. Please make sure a folder named 'data' exists in the project root.")
    st.stop()

if not os.path.exists(assets_path):
    st.error("The assets folder was not found. Please make sure a folder named 'assets' exists in the project root.")
    st.stop()

files = os.listdir(data_path)
nakama_files = [f for f in files if f.endswith(".nakama-0")]

if len(nakama_files) == 0:
    st.error("No .nakama-0 telemetry files were found inside the data folder.")
    st.stop()

# -------------------------
# SIDEBAR CONTROLS
# -------------------------
st.sidebar.header("Dashboard Controls")
st.sidebar.write(f"Found {len(nakama_files)} telemetry files")

theme_mode = st.sidebar.radio("Theme", ["Light", "Dark"], index=0)

if theme_mode == "Dark":
    bg_color = "#0E1117"
    card_color = "#161B22"
    text_color = "#FAFAFA"
    border_color = "#30363D"
    muted_text = "#B8C0CC"
    accent_color = "#4F8CFF"
    hover_shadow = "0 10px 24px rgba(0, 0, 0, 0.28)"
else:
    bg_color = "#FFFFFF"
    card_color = "#F7F9FC"
    text_color = "#111111"
    border_color = "#D9E2EC"
    muted_text = "#5B6470"
    accent_color = "#2563EB"
    hover_shadow = "0 10px 24px rgba(37, 99, 235, 0.12)"

# -------------------------
# RESPONSIVE + ANIMATION STYLING
# -------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}

    .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 1450px;
        animation: pageFadeIn 0.6s ease-in-out;
    }}

    @keyframes pageFadeIn {{
        from {{
            opacity: 0;
            transform: translateY(8px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .hero-box {{
        background: linear-gradient(135deg, {card_color} 0%, {bg_color} 100%);
        padding: 22px;
        border-radius: 18px;
        border: 1px solid {border_color};
        margin-bottom: 18px;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }}

    .hero-box:hover {{
        transform: translateY(-3px);
        box-shadow: {hover_shadow};
        border-color: {accent_color};
    }}

    .hero-title {{
        margin: 0 0 8px 0;
        color: {text_color};
        font-size: 2.25rem;
        line-height: 1.15;
        font-weight: 800;
    }}

    .hero-subtitle {{
        margin: 0;
        color: {muted_text};
        font-size: 1rem;
        line-height: 1.6;
        max-width: 1000px;
    }}

    .metric-grid {{
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
        margin: 12px 0 20px 0;
    }}

    .metric-card {{
        flex: 1 1 180px;
        min-width: 180px;
        background-color: {card_color};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        animation: cardPopIn 0.45s ease;
    }}

    .metric-card:hover {{
        transform: translateY(-6px) scale(1.01);
        box-shadow: {hover_shadow};
        border-color: {accent_color};
    }}

    @keyframes cardPopIn {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .metric-accent {{
        height: 4px;
        width: 52px;
        border-radius: 999px;
        background-color: {accent_color};
        margin-bottom: 12px;
        transition: width 0.25s ease;
    }}

    .metric-card:hover .metric-accent {{
        width: 70px;
    }}

    .metric-label {{
        font-size: 0.9rem;
        color: {muted_text};
        margin-bottom: 8px;
    }}

    .metric-value {{
        font-size: 1.55rem;
        line-height: 1.2;
        font-weight: 750;
        color: {text_color};
        word-break: break-word;
    }}

    div[data-testid="stMetric"] {{
        background-color: {card_color};
        border: 1px solid {border_color};
        padding: 10px;
        border-radius: 12px;
        color: {text_color};
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }}

    div[data-testid="stMetric"]:hover {{
        transform: translateY(-4px);
        box-shadow: {hover_shadow};
        border-color: {accent_color};
    }}

    div[data-testid="stMetricLabel"] {{
        color: {text_color} !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: {text_color} !important;
    }}

    div[data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
        transition: box-shadow 0.25s ease, transform 0.25s ease;
    }}

    div[data-testid="stDataFrame"]:hover {{
        box-shadow: {hover_shadow};
        transform: translateY(-2px);
    }}

    .note-box {{
        background-color: {card_color};
        border: 1px solid {border_color};
        border-left: 5px solid {accent_color};
        border-radius: 14px;
        padding: 14px 16px;
        margin: 8px 0 18px 0;
        color: {muted_text};
        line-height: 1.55;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }}

    .note-box:hover {{
        transform: translateY(-3px);
        box-shadow: {hover_shadow};
        border-color: {accent_color};
    }}

    h2, h3 {{
        scroll-margin-top: 80px;
    }}

    @media (max-width: 1024px) {{
        .hero-title {{
            font-size: 2rem;
        }}

        .metric-card {{
            flex: 1 1 45%;
            min-width: 160px;
        }}
    }}

    @media (max-width: 640px) {{
        .block-container {{
            padding-top: 1rem;
            padding-left: 0.75rem;
            padding-right: 0.75rem;
        }}

        .hero-box {{
            padding: 18px;
            border-radius: 16px;
        }}

        .hero-title {{
            font-size: 1.7rem;
        }}

        .hero-subtitle {{
            font-size: 0.95rem;
        }}

        .metric-grid {{
            gap: 10px;
        }}

        .metric-card {{
            flex: 1 1 100%;
            min-width: 100%;
            padding: 14px;
        }}

        .metric-value {{
            font-size: 1.35rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# HERO SECTION
# -------------------------
st.markdown(
    f"""
    <div class="hero-box">
        <div class="hero-title">🎮 Game Movement Intelligence Dashboard</div>
        <div class="hero-subtitle">
            A browser-based telemetry exploration tool for Level Designers to understand player movement,
            combat zones, death clusters, loot activity, bot-vs-human patterns, and match progression over time.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="note-box">
        Use the controls in the sidebar to filter by player, map, date, match, replay time, and event visibility.
        This layout is responsive and now includes subtle hover effects and animation for a more polished experience.
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# FILE LOADING
# -------------------------
max_files = st.sidebar.slider(
    "Number of files to load",
    1,
    min(50, len(nakama_files)),
    min(10, len(nakama_files))
)
selected_files = nakama_files[:max_files]

df_list = []
for f in selected_files:
    file_path = os.path.join(data_path, f)
    try:
        temp_df = pd.read_parquet(file_path)
        df_list.append(temp_df)
    except Exception as e:
        st.warning(f"Skipping file {f} because it could not be read: {e}")

if len(df_list) == 0:
    st.error("No valid parquet telemetry files could be loaded.")
    st.stop()

df = pd.concat(df_list, ignore_index=True)

if df.empty:
    st.error("Loaded data is empty.")
    st.stop()

# -------------------------
# CLEAN DATA
# -------------------------
def decode_event(x):
    try:
        return x.decode("utf-8")
    except Exception:
        return str(x)

def detect_player_type(user_id):
    try:
        int(user_id)
        return "Bot"
    except Exception:
        return "Human"

df["event"] = df["event"].apply(decode_event)
df["player_type"] = df["user_id"].apply(detect_player_type)
df["ts"] = pd.to_numeric(df["ts"], errors="coerce")
df = df.dropna()

if df.empty:
    st.error("All rows were removed during cleaning. Please check the input data.")
    st.stop()

# -------------------------
# DATE PREPARATION
# -------------------------
df["datetime_utc"] = pd.to_datetime(df["ts"], unit="s", utc=True, errors="coerce")
df["event_date"] = df["datetime_utc"].dt.strftime("%Y-%m-%d")

# -------------------------
# FILTERS
# -------------------------
all_player_ids = sorted(df["user_id"].dropna().unique().tolist())
selected_player = st.sidebar.selectbox("Select Player", ["All"] + all_player_ids)

if selected_player != "All":
    df = df[df["user_id"] == selected_player]

if df.empty:
    st.warning("No data available for the selected player.")
    st.stop()

map_ids = sorted(df["map_id"].dropna().unique().tolist())
selected_map = st.sidebar.selectbox("Select Map", map_ids)
df = df[df["map_id"] == selected_map].copy()

if df.empty:
    st.warning("No data available for the selected map.")
    st.stop()

date_options = sorted([d for d in df["event_date"].dropna().unique().tolist() if d != "NaT"])
selected_date = st.sidebar.selectbox("Select Date", ["All"] + date_options)

if selected_date != "All":
    df = df[df["event_date"] == selected_date].copy()

if df.empty:
    st.warning("No data available for the selected date.")
    st.stop()

if "match_id" in df.columns:
    match_options = sorted(df["match_id"].dropna().astype(str).unique().tolist())
    selected_match = st.sidebar.selectbox("Select Match", ["All"] + match_options)
    if selected_match != "All":
        df = df[df["match_id"].astype(str) == selected_match].copy()
else:
    selected_match = "All"
    st.sidebar.info("match_id column not found in the dataset.")

if df.empty:
    st.warning("No data available for the selected match.")
    st.stop()

filtered_player_ids = sorted(df["user_id"].dropna().unique().tolist())

# -------------------------
# MAP CONFIG
# -------------------------
map_configs = {
    "AmbroseValley": {
        "scale": 900,
        "origin": (-370, -473),
        "image": "assets/AmbroseValley_Minimap.png"
    },
    "GrandRift": {
        "scale": 581,
        "origin": (-290, -290),
        "image": "assets/GrandRift_Minimap.png"
    },
    "Lockdown": {
        "scale": 1000,
        "origin": (-500, -500),
        "image": "assets/Lockdown_Minimap.jpg"
    },
}

if selected_map not in map_configs:
    st.error(f"No map configuration found for map_id: {selected_map}")
    st.stop()

config = map_configs[selected_map]
scale = config["scale"]
origin_x, origin_z = config["origin"]
image_path = config["image"]

if not os.path.exists(image_path):
    st.error(f"Map image not found: {image_path}")
    st.stop()

# -------------------------
# COORDINATE TRANSFORM
# -------------------------
def convert_coords(row):
    u = (row["x"] - origin_x) / scale
    v = (row["z"] - origin_z) / scale
    pixel_x = u * 1024
    pixel_y = (1 - v) * 1024
    return pd.Series([pixel_x, pixel_y])

df[["px", "py"]] = df.apply(convert_coords, axis=1)

df = df[
    (df["px"] >= 0) & (df["px"] <= 1024) &
    (df["py"] >= 0) & (df["py"] <= 1024)
].copy()

if df.empty:
    st.warning("After coordinate mapping, no points remained on the visible minimap.")
    st.stop()

# -------------------------
# ZONE ASSIGNMENT
# -------------------------
def assign_zone(px, py):
    if px < 512 and py < 512:
        return "North-West"
    elif px >= 512 and py < 512:
        return "North-East"
    elif px < 512 and py >= 512:
        return "South-West"
    else:
        return "South-East"

df["zone"] = df.apply(lambda row: assign_zone(row["px"], row["py"]), axis=1)

# -------------------------
# SPLIT DATA
# -------------------------
movement_df = df[df["event"].isin(["Position", "BotPosition"])].copy()
event_df = df[df["event"].isin([
    "Kill", "Killed", "BotKill", "BotKilled", "Loot", "KilledByStorm"
])].copy()

# -------------------------
# REPLAY / TIMELINE
# -------------------------
if df["ts"].isna().all():
    st.error("Timestamp column could not be parsed.")
    st.stop()

min_ts = int(df["ts"].min())
max_ts = int(df["ts"].max())

selected_ts = st.sidebar.slider(
    "Replay Time",
    min_value=min_ts,
    max_value=max_ts,
    value=max_ts
)

show_kills = st.sidebar.checkbox("Show Kills", value=True)
show_deaths = st.sidebar.checkbox("Show Deaths", value=True)
show_loot = st.sidebar.checkbox("Show Loot", value=True)
show_storm = st.sidebar.checkbox("Show Storm Deaths", value=True)

movement_replay_df = movement_df[movement_df["ts"] <= selected_ts].copy()
event_replay_df = event_df[event_df["ts"] <= selected_ts].copy()

human_replay_df = movement_replay_df[movement_replay_df["player_type"] == "Human"].copy()
bot_replay_df = movement_replay_df[movement_replay_df["player_type"] == "Bot"].copy()

# -------------------------
# LOAD MAP IMAGE
# -------------------------
try:
    img = Image.open(image_path)
except Exception as e:
    st.error(f"Could not open map image: {e}")
    st.stop()

# -------------------------
# METRICS
# -------------------------
total_movement = len(movement_replay_df)
total_events = len(event_replay_df)
total_kills = len(event_replay_df[event_replay_df["event"].isin(["Kill", "BotKill"])])
total_deaths = len(event_replay_df[event_replay_df["event"].isin(["Killed", "BotKilled"])])
total_loot = len(event_replay_df[event_replay_df["event"] == "Loot"])
total_storm = len(event_replay_df[event_replay_df["event"] == "KilledByStorm"])
human_points = len(human_replay_df)
bot_points = len(bot_replay_df)

display_match_value = selected_match if selected_match != "All" else str(df["match_id"].nunique()) + " matches"

metrics_html = f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-accent"></div>
        <div class="metric-label">Map</div>
        <div class="metric-value">{selected_map}</div>
    </div>
    <div class="metric-card">
        <div class="metric-accent"></div>
        <div class="metric-label">Date</div>
        <div class="metric-value">{selected_date if selected_date != "All" else "All Dates"}</div>
    </div>
    <div class="metric-card">
        <div class="metric-accent"></div>
        <div class="metric-label">Match</div>
        <div class="metric-value">{display_match_value}</div>
    </div>
    <div class="metric-card">
        <div class="metric-accent"></div>
        <div class="metric-label">Replay Time</div>
        <div class="metric-value">{selected_ts}</div>
    </div>
    <div class="metric-card">
        <div class="metric-accent"></div>
        <div class="metric-label">Movement Points</div>
        <div class="metric-value">{total_movement}</div>
    </div>
    <div class="metric-card">
        <div class="metric-accent"></div>
        <div class="metric-label">Events</div>
        <div class="metric-value">{total_events}</div>
    </div>
    <div class="metric-card">
        <div class="metric-accent"></div>
        <div class="metric-label">Players Loaded</div>
        <div class="metric-value">{len(filtered_player_ids)}</div>
    </div>
</div>
"""
st.markdown(metrics_html, unsafe_allow_html=True)

# -------------------------
# MOVEMENT + HEATMAP
# -------------------------
st.markdown("## 🗺️ Core Visualizations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Movement Path")

    fig1, ax1 = plt.subplots(figsize=(8, 8))
    ax1.imshow(img)

    if selected_player == "All":
        if len(human_replay_df) > 0:
            ax1.scatter(
                human_replay_df["px"],
                human_replay_df["py"],
                s=4,
                marker="o",
                label="Humans"
            )
        if len(bot_replay_df) > 0:
            ax1.scatter(
                bot_replay_df["px"],
                bot_replay_df["py"],
                s=8,
                marker="x",
                label="Bots"
            )
        if len(human_replay_df) > 0 or len(bot_replay_df) > 0:
            ax1.legend()
    else:
        if len(movement_replay_df) > 0:
            ordered_movement = movement_replay_df.sort_values("ts")
            ax1.plot(
                ordered_movement["px"],
                ordered_movement["py"],
                linewidth=1,
                label=str(selected_player)
            )
            ax1.legend()
        else:
            st.info("No movement points available for this replay window.")

    ax1.set_title("Player Movement Replay")
    ax1.axis("off")
    st.pyplot(fig1, use_container_width=True)

with col2:
    st.subheader("Traffic Heatmap")

    fig2, ax2 = plt.subplots(figsize=(8, 8))
    ax2.imshow(img)

    if len(movement_replay_df) > 0:
        ax2.hist2d(
            movement_replay_df["px"],
            movement_replay_df["py"],
            bins=60,
            range=[[0, 1024], [0, 1024]],
            alpha=0.5
        )
    else:
        st.info("No movement points available for heatmap in this replay window.")

    ax2.set_title("High-Traffic Zones")
    ax2.axis("off")
    st.pyplot(fig2, use_container_width=True)

# -------------------------
# EVENT MAP
# -------------------------
st.markdown("---")
st.markdown("## 🎯 Event Map")

fig3, ax3 = plt.subplots(figsize=(8, 8))
ax3.imshow(img)

legend_needed = False

if show_kills:
    kills_df = event_replay_df[event_replay_df["event"].isin(["Kill", "BotKill"])]
    if len(kills_df) > 0:
        ax3.scatter(kills_df["px"], kills_df["py"], marker="x", s=40, label="Kills")
        legend_needed = True

if show_deaths:
    deaths_df = event_replay_df[event_replay_df["event"].isin(["Killed", "BotKilled"])]
    if len(deaths_df) > 0:
        ax3.scatter(deaths_df["px"], deaths_df["py"], marker="o", s=30, label="Deaths")
        legend_needed = True

if show_loot:
    loot_df = event_replay_df[event_replay_df["event"] == "Loot"]
    if len(loot_df) > 0:
        ax3.scatter(loot_df["px"], loot_df["py"], marker="s", s=30, label="Loot")
        legend_needed = True

if show_storm:
    storm_df = event_replay_df[event_replay_df["event"] == "KilledByStorm"]
    if len(storm_df) > 0:
        ax3.scatter(storm_df["px"], storm_df["py"], marker="^", s=50, label="Storm Deaths")
        legend_needed = True

ax3.set_title("Event Replay")
ax3.axis("off")
if legend_needed:
    ax3.legend()

st.pyplot(fig3, use_container_width=True)

if len(event_replay_df) == 0:
    st.info("No event markers are available in the current replay window.")

# -------------------------
# PRODUCT INSIGHTS
# -------------------------
st.markdown("---")
st.markdown("## 🧠 Product Insights")

bot_share = (bot_points / total_movement) if total_movement > 0 else 0

top_traffic_zone = (
    movement_replay_df["zone"].value_counts().idxmax()
    if len(movement_replay_df) > 0 else "No movement data"
)

death_zone_df = event_replay_df[event_replay_df["event"].isin(["Killed", "BotKilled", "KilledByStorm"])]
top_death_zone = (
    death_zone_df["zone"].value_counts().idxmax()
    if len(death_zone_df) > 0 else "No death data"
)

if total_kills + total_deaths > 10:
    play_style = "Aggressive"
elif total_loot > total_kills and total_loot > total_deaths:
    play_style = "Loot-focused / passive"
else:
    play_style = "Balanced / exploratory"

insight_lines = [
    f"1. The most active area in the current view is **{top_traffic_zone}**.",
    f"2. The highest-risk area appears to be **{top_death_zone}**.",
    f"3. The current behavior pattern looks **{play_style}**."
]

if bot_share > 0.4:
    insight_lines.append("4. Bot activity is relatively high, so this view should not be treated as purely human behavior.")
else:
    insight_lines.append("4. Human activity dominates this view, so this pattern is more likely to reflect real player behavior.")

if total_storm > 0:
    insight_lines.append("5. Storm deaths are visible here, suggesting possible rotation pressure or weak route readability.")
else:
    insight_lines.append("5. No storm deaths are visible in the current replay window.")

for line in insight_lines:
    st.write(line)

# -------------------------
# ADVANCED ZONE ANALYSIS
# -------------------------
st.markdown("---")
st.markdown("## 📊 Advanced Zone Analysis")

zone_order = ["North-West", "North-East", "South-West", "South-East"]
zone_summary = pd.DataFrame({"zone": zone_order})

movement_zone_counts = movement_replay_df["zone"].value_counts().rename("movement_points")
event_zone_counts = event_replay_df["zone"].value_counts().rename("event_points")
kill_zone_counts = event_replay_df[event_replay_df["event"].isin(["Kill", "BotKill"])]["zone"].value_counts().rename("kills")
death_zone_counts = event_replay_df[event_replay_df["event"].isin(["Killed", "BotKilled", "KilledByStorm"])]["zone"].value_counts().rename("deaths")
loot_zone_counts = event_replay_df[event_replay_df["event"] == "Loot"]["zone"].value_counts().rename("loot")

zone_summary = zone_summary.merge(movement_zone_counts, on="zone", how="left")
zone_summary = zone_summary.merge(event_zone_counts, on="zone", how="left")
zone_summary = zone_summary.merge(kill_zone_counts, on="zone", how="left")
zone_summary = zone_summary.merge(death_zone_counts, on="zone", how="left")
zone_summary = zone_summary.merge(loot_zone_counts, on="zone", how="left")
zone_summary = zone_summary.fillna(0)

hottest_engagement_zone = zone_summary.sort_values(["kills", "event_points"], ascending=False).iloc[0]["zone"]
highest_risk_zone = zone_summary.sort_values(["deaths", "event_points"], ascending=False).iloc[0]["zone"]
safest_zone = zone_summary.sort_values(["deaths", "movement_points"], ascending=True).iloc[0]["zone"]
most_loot_active_zone = zone_summary.sort_values(["loot", "movement_points"], ascending=False).iloc[0]["zone"]

zone_metrics_html = f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-accent"></div>
        <div class="metric-label">Engagement Hotspot</div>
        <div class="metric-value">{hottest_engagement_zone}</div>
    </div>
    <div class="metric-card">
        <div class="metric-accent"></div>
        <div class="metric-label">High-Risk Zone</div>
        <div class="metric-value">{highest_risk_zone}</div>
    </div>
    <div class="metric-card">
        <div class="metric-accent"></div>
        <div class="metric-label">Safe Zone</div>
        <div class="metric-value">{safest_zone}</div>
    </div>
    <div class="metric-card">
        <div class="metric-accent"></div>
        <div class="metric-label">Loot Activity Zone</div>
        <div class="metric-value">{most_loot_active_zone}</div>
    </div>
</div>
"""
st.markdown(zone_metrics_html, unsafe_allow_html=True)
st.dataframe(zone_summary, use_container_width=True)

# -------------------------
# BEHAVIOR + JOURNEY
# -------------------------
st.markdown("---")
st.markdown("## 🧭 Behavior and Journey Analysis")

tab_a, tab_b = st.tabs(["Behavior Pattern Detection", "Player Journey Analysis"])

with tab_a:
    loot_ratio = (total_loot / total_movement) if total_movement > 0 else 0
    combat_ratio = ((total_kills + total_deaths) / total_movement) if total_movement > 0 else 0

    if combat_ratio > 0.20:
        behavior_pattern = "Aggressive / combat-seeking"
    elif loot_ratio > 0.20 and combat_ratio < 0.10:
        behavior_pattern = "Passive / loot-oriented"
    else:
        behavior_pattern = "Balanced / exploratory"

    st.write(f"**Detected Pattern:** {behavior_pattern}")
    st.write(f"- Loot events: {total_loot}")
    st.write(f"- Combat events: {total_kills + total_deaths}")
    st.write(f"- Human movement points: {human_points}")
    st.write(f"- Bot movement points: {bot_points}")

with tab_b:
    journey_text = []

    if len(movement_replay_df) > 0:
        ordered_movement = movement_replay_df.sort_values("ts")
        first_zone = ordered_movement.iloc[0]["zone"]
        last_zone = ordered_movement.iloc[-1]["zone"]

        journey_text.append(f"The current replay window begins in **{first_zone}** and ends in **{last_zone}**.")

        if first_zone != last_zone:
            journey_text.append("This suggests players are rotating across the map instead of staying in one area.")
        else:
            journey_text.append("This suggests players are spending most of their time in a concentrated area.")
    else:
        journey_text.append("No movement data is available for journey analysis.")

    if highest_risk_zone == hottest_engagement_zone:
        journey_text.append(
            f"Combat and deaths are clustering in **{highest_risk_zone}**, which may indicate a choke point or over-contested area."
        )
    else:
        journey_text.append(
            f"Combat is strongest in **{hottest_engagement_zone}**, while deaths cluster in **{highest_risk_zone}**."
        )

    journey_text.append(
        f"From a level design perspective, **{safest_zone}** appears under-utilized and may need stronger incentives or better routing."
    )

    for line in journey_text:
        st.write(line)

# -------------------------
# SUMMARY TABLES
# -------------------------
st.markdown("---")
st.markdown("## 📋 Summary Tables")

summary_tab1, summary_tab2 = st.tabs(["Player Type Counts", "Event Counts in Replay Window"])

with summary_tab1:
    st.dataframe(
        df["player_type"].value_counts().reset_index(name="count"),
        use_container_width=True
    )

with summary_tab2:
    if len(event_replay_df) > 0:
        st.dataframe(
            event_replay_df["event"].value_counts().reset_index(name="count"),
            use_container_width=True
        )
    else:
        st.write("No events yet in the current replay window.")