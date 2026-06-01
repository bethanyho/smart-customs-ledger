import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import datetime

# Import core backend elements from your existing ledger engine
import ledger_engine
from ledger_engine import (
    blockchain_ledger, 
    create_transit_block, 
    run_system_integrity_audit, 
    load_system_keys,
    ENVIRONMENT_SETTINGS
)

# =====================================================================
# --- INITIALIZATION & LAYOUT CONFIGURATION ---
# =====================================================================
st.set_page_config(
    page_title="HK Customs Smart Port Clearance Interface",
    page_icon="🛂",
    layout="wide"
)

# Day 102: Title Header Initialization
st.title("🛂 HK Customs Smart Port Clearance Interface")
st.markdown("---")

# Setup state persistency for our live demo ledger simulation
if "live_ledger" not in st.session_state:
    # Initialize keys and pre-populate with mock logistics checkpoints
    priv_key, pub_key = load_system_keys()
    st.session_state.priv_key = priv_key
    st.session_state.pub_key = pub_key
    
    # Build standard clean validation track
    b0 = create_transit_block("Guangdong Manufacturing Hub", 15000, "Electronics", "MSKU-991", "0", 22.5431, 114.0579, private_key=priv_key)
    b1 = create_transit_block("Port of Shenzhen (Yantian)", 15000, "Electronics", "MSKU-991", b0["block_hash"], 22.5752, 114.2792, private_key=priv_key)
    b2 = create_transit_block("Kwai Tsing Terminal 4, HK", 15000, "Electronics", "MSKU-991", b1["block_hash"], 22.3347, 114.1241, private_key=priv_key)
    
    # Build a compromised/quarantined vessel tracking link (Lantau Island Illegal Anchorage)
    b3 = create_transit_block("Lamma Channel Lane", 22000, "Apparel", "MSKU-X8", "0", 22.2100, 114.0700, speed=15.5, private_key=priv_key)
    b4 = create_transit_block("Unapproved Lantau Incursion", 22000, "Apparel", "MSKU-X8", b3["block_hash"], 22.2500, 113.8500, speed=0.5, station_hours=5.0, private_key=priv_key)
    
    st.session_state.live_ledger = [b0, b1, b2, b3, b4]
    st.session_state.quarantine_log = []

# =====================================================================
# --- DAY 103: SIDEBAR CONTROL NAVIGATION PANEL ---
# =====================================================================
st.sidebar.header("🛠️ System Mission Controls")

# Day 91 & 103: Typhoon Environment Switch Toggle
typhoon_toggle = st.sidebar.toggle("Simulate Typhoon Toggle (x2.5 Time Buffer)", value=ENVIRONMENT_SETTINGS["typhoon_active"])
ENVIRONMENT_SETTINGS["typhoon_active"] = typhoon_toggle

# Control Operational Executions
run_audit_clicked = st.sidebar.button("🔍 Run System Audit", use_container_width=True)

# Add dummy manifest manual ingestion tool to sidebar to show reactive map generation
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Quick Ingest Block")
input_loc = st.sidebar.text_input("Checkpoint Location", "Tuen Mun Terminal")
input_wt = st.sidebar.number_input("Cargo Weight (KG)", value=18500)
input_lat = st.sidebar.number_input("Latitude Coords", value=22.3700, format="%.4f")
input_lon = st.sidebar.number_input("Longitude Coords", value=113.9100, format="%.4f")

if st.sidebar.button("Mint & Append Block"):
    prev_hash = st.session_state.live_ledger[-1]["block_hash"] if st.session_state.live_ledger else "0"
    new_b = create_transit_block(input_loc, input_wt, "General Merch", "MSKU-NEW", prev_hash, input_lat, input_lon, private_key=st.session_state.priv_key)
    st.session_state.live_ledger.append(new_b)
    st.toast("New block appended successfully!", icon="✅")

# =====================================================================
# --- DAY 104: REAL-TIME METRIC STREAM TICKERS ---
# =====================================================================
total_blocks = len(st.session_state.live_ledger)
# Calculate totals dynamically based on compliance flags
quarantined_count = sum(1 for b in st.session_state.live_ledger if b.get("hours_stationary", 0) > 3.0 and b.get("vessel_speed_knots", 12.0) <= 2.0)
cleared_count = total_blocks - quarantined_count

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Ledger Block Height", value=total_blocks)
with col2:
    st.metric(label="Total Cleared Manifests", value=cleared_count)
with col3:
    st.metric(label="High-Risk Flagged Devices", value=quarantined_count, delta=f"+{quarantined_count}" if quarantined_count > 0 else 0, delta_color="inverse")
with col4:
    weather_status = "TYPHOON WARNING" if ENVIRONMENT_SETTINGS["typhoon_active"] else "CLEAR / NORMAL"
    st.metric(label="Contextual Atmospheric Status", value=weather_status)

st.markdown("---")

# =====================================================================
# --- DAY 107 - 109: INTERACTIVE MAP & THREAT PANEL FUSION ---
# =====================================================================
st.subheader("🌐 Real-Time Spatial/Temporal Tracking Corridor Map")

# Day 107: Initialize standard Folium map canvas focused around Hong Kong waters
m = folium.Map(location=[22.3800, 114.1000], zoom_start=10, tiles="CartoDB positron")

# Group blocks by serial markers to construct historical trajectory trace lines
trajectories = {}
for block in st.session_state.live_ledger:
    serial = block["container_serial"]
    if serial not in trajectories:
        trajectories[serial] = []
    trajectories[serial].append(block)

# Day 108 & 109: Structural Mapping Vector Rules
st.session_state.quarantine_log = [] # Reset log to build clean presentation view
for serial, blocks in trajectories.items():
    points = [[b["current_lat"], b["current_lon"]] for b in blocks]
    
    # Assess if any node in this container path triggers an illegal anchor or geofence deviation
    is_compromised_path = False
    fail_reason = ""
    for b in blocks:
        # Cross-reference Week 20 Anchor rule directly
        if b.get("hours_stationary", 0) > 3.0 and b.get("vessel_speed_knots", 12.0) <= 2.0:
            is_compromised_path = True
            fail_reason = "CRITICAL: PROBABLE OFFSHORE CONTRABAND TRANSFER (Stationary > 3h in unapproved grid)"
            if b not in st.session_state.quarantine_log:
                st.session_state.quarantine_log.append({"block_id": b["block_id"], "serial": serial, "reason": fail_reason, "location": b["location"]})

    # Day 108/109: Assign Line Colors based on validation audit status
    line_color = "#E74C3C" if is_compromised_path else "#2ECC71"  # Glowing Red vs Crisp Emerald Green
    
    # Draw vector line path trace
    folium.PolyLine(
        locations=points,
        color=line_color,
        weight=4,
        opacity=0.85,
        popup=f"Container Route: {serial}"
    ).add_to(m)

    # Add custom geographic drop pin anchors for individual checkpoints
    for b in blocks:
        icon_color = "red" if is_compromised_path else "green"
        folium.Marker(
            location=[b["current_lat"], b["current_lon"]],
            popup=f"Node {b['block_id']}: {b['location']}<br>Speed: {b['vessel_speed_knots']} kts",
            icon=folium.Icon(color=icon_color, icon="ship", prefix="fa")
        ).add_to(m)

# Render native interactive map frame widget
st_folium(m, width=1400, height=500, key="customs_map")

st.markdown("---")

# Layout Splitting: Ledger View vs Priority Threat Dashboard Sidebar Container
main_col, side_col = st.columns([2, 1])

with main_col:
    # Day 105: Active Interactive Blockchain Array View Data Frame
    st.subheader("📦 Master Supply Chain Ledger Frame")
    df_ledger = pd.DataFrame(st.session_state.live_ledger)
    
    # Dropping bytes/objects that don't serialize easily to standard text data tables
    clean_df = df_ledger.drop(columns=["digital_signature", "block_hash", "previous_hash"], errors="ignore")
    st.dataframe(clean_df, use_container_width=True)

with side_col:
    # Day 110: Frontline Interception Priorities Threat Panel Widget
    st.subheader("🚨 Frontline Interception Priorities")
    
    if not st.session_state.quarantine_log:
        st.success("✅ No current intercepts active. Port clearing channels clear.")
    else:
        for alert in st.session_state.quarantine_log:
            with st.container(border=True):
                st.markdown(f"### 🛑 CONTAINER: **{alert['serial']}**")
                st.markdown(f"**Target Node ID:** `{alert['block_id']}`")
                st.markdown(f"**Intercept Zone:** *{alert['location']}*")
                st.markdown(f"<span style='color:#E74C3C; font-weight:bold;'>Reason: {alert['reason']}</span>", unsafe_allowed_html=True)

# =====================================================================
# --- RUNTIME AUDIT TRIGGER DIALOGUE HOOKS ---
# =====================================================================
# =====================================================================
# --- RUNTIME AUDIT TRIGGER DIALOGUE HOOKS ---
# =====================================================================
if run_audit_clicked:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎛️ Audit Output Console")
    with st.sidebar.spinner("Scanning chain integrity layers..."):
        is_tampered = run_system_integrity_audit(st.session_state.live_ledger, st.session_state.pub_key)
        if is_tampered:
            st.sidebar.error("❌ Integrity Check FAILED! Anomalous records isolated.")
        else:
            st.sidebar.success("✅ System Audit SUCCESS! All nodes validated.")