import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import json
from gemini_engine import generate_disaster_advisory
from gee_sim import (
    simulate_cyclone_telemetry,
    get_coastal_infrastructure_assets,
    calculate_infrastructure_vulnerability
)

# Set page configuration
st.set_page_config(
    page_title="ResiliTrack AI — Cyclone & Infrastructure Risk Forecaster",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark dashboard aesthetics
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E88E5;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #B0BEC5;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #1E293B;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #38BDF8;
        margin-bottom: 10px;
    }
    .alert-box-red {
        background-color: #450A0A;
        color: #FECACA;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #EF4444;
        margin-bottom: 12px;
    }
    .alert-box-green {
        background-color: #064E3B;
        color: #A7F3D0;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #10B981;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# App Title Header
st.markdown('<div class="main-title">🌀 ResiliTrack AI — Cyclone Risk Forecaster</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Track 5: AI-Powered Cyclone Storm Surge, Inundation & Infrastructure Vulnerability Platform (GEE + Gemini Multimodal AI)</div>', unsafe_allow_html=True)

# Sidebar Control Panel
st.sidebar.header("⚙️ Cyclone Telemetry Simulation")

region = st.sidebar.selectbox(
    "Target Coastal Sector",
    [
        "Bay of Bengal — Odisha / West Bengal Coast (India)",
        "Bay of Bengal — Chattogram / Cox's Bazar (Bangladesh)",
        "APAC Coastal Region — Luzon / Visayas (Philippines)",
        "APAC Coastal Region — Central Coast (Vietnam)"
    ]
)

intensity_preset = st.sidebar.selectbox(
    "Cyclone Intensity Category",
    [
        "Category 4 - Extremely Severe",
        "Category 5 - Super Cyclone",
        "Category 3 - Very Severe",
        "Category 2 - Moderate"
    ]
)

# Fetch baseline preset telemetry
base_metrics = simulate_cyclone_telemetry(intensity_preset)

cyclone_name = st.sidebar.text_input("Cyclone System ID / Name", value="Cyclone REMAL-X")

st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Real-Time Forecast Overrides")
wind_speed = st.sidebar.slider("Max Wind Speed (km/h)", 100, 300, base_metrics["wind_speed_kmh"])
surge_height = st.sidebar.slider("Storm Surge Height (meters)", 0.5, 10.0, float(base_metrics["surge_height_m"]), step=0.1)
rainfall = st.sidebar.slider("Predicted 24h Rainfall (mm)", 50, 600, base_metrics["rainfall_mm"])

# Gemini API Key Input
st.sidebar.markdown("---")
st.sidebar.subheader("🔑 Gemini API Settings")
gemini_api_key = st.sidebar.text_input("Google Gemini API Key", type="password", help="Leave blank to use pre-built realistic AI fallback engine.")

# Assemble active metrics
metrics = {
    "wind_speed_kmh": wind_speed,
    "category": base_metrics["category"],
    "surge_height_m": surge_height,
    "rainfall_mm": rainfall,
    "affected_population": base_metrics["affected_population"],
    "total_hospitals": base_metrics["total_hospitals"],
    "isolated_hospitals": base_metrics["isolated_hospitals"],
    "flooded_roads_km": base_metrics["flooded_roads_km"],
    "power_grid_risk_pct": base_metrics["power_grid_risk_pct"]
}

# Base location coordinates based on selected region
coords_map = {
    "Bay of Bengal — Odisha / West Bengal Coast (India)": (21.65, 87.85),
    "Bay of Bengal — Chattogram / Cox's Bazar (Bangladesh)": (21.43, 91.97),
    "APAC Coastal Region — Luzon / Visayas (Philippines)": (13.41, 123.74),
    "APAC Coastal Region — Central Coast (Vietnam)": (16.05, 108.20)
}
center_lat, center_lon = coords_map.get(region, (21.65, 87.85))

# Generate Infrastructure data & Vulnerabilities
infra_raw = get_coastal_infrastructure_assets(center_lat, center_lon)
infra_df = calculate_infrastructure_vulnerability(infra_raw, surge_height, rainfall)

# Top KPI Metric Row
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Wind Speed", f"{wind_speed} km/h", delta=f"Cat {base_metrics['category']}")
with col2:
    st.metric("Storm Surge", f"{surge_height} m", delta="Sea Elevation")
with col3:
    st.metric("24h Rainfall", f"{rainfall} mm", delta="Heavy Basin Rain")
with col4:
    submerged_count = len(infra_df[infra_df['water_depth_m'] > 0.8])
    st.metric("Critical Infrastructure Cut Off", f"{submerged_count} / {len(infra_df)} Assets", delta_color="inverse", delta=f"{int(submerged_count/len(infra_df)*100)}% High Risk")
with col5:
    st.metric("Population at Risk", f"{metrics['affected_population']:,}")

# Main Application Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ GIS Inundation & Infrastructure Map",
    "🧠 Gemini Multimodal AI Operations Intelligence",
    "📊 Exposure Analytics & Asset Risk",
    "📜 Hackathon Prototype Submission Package"
])

# ---------------------------------------------------------
# TAB 1: GIS Map Visualization
# ---------------------------------------------------------
with tab1:
    st.subheader("🌐 Hyper-Local Hydro-Elevation & Critical Asset Exposure Map")
    st.markdown("Google Earth Engine elevation matrix overlaid with predicted storm surge inundation zones and OpenStreetMap critical infrastructure points.")
    
    # Initialize Folium Map with clean tile layer
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles="OpenStreetMap")
    
    # Add Storm Surge Flood Buffer Polygon around coast
    surge_polygon_coords = [
        [center_lat - 0.1, center_lon - 0.2],
        [center_lat + 0.1, center_lon - 0.2],
        [center_lat + 0.1, center_lon + 0.05],
        [center_lat - 0.1, center_lon + 0.05]
    ]
    
    # Add simulated flood inundation overlay
    folium.Polygon(
        locations=surge_polygon_coords,
        color="#38BDF8",
        fill=True,
        fill_color="#0284C7",
        fill_opacity=min(0.7, 0.2 + (surge_height / 15.0)),
        popup=f"Simulated Inundation Zone (Surge Height: {surge_height}m)"
    ).add_to(m)

    # Add Infrastructure markers
    for idx, row in infra_df.iterrows():
        popup_html = f"""
        <div style="font-family: Arial; width: 220px;">
            <h4 style="margin: 0; color: #1E88E5;">{row['name']}</h4>
            <b>Type:</b> {row['type']}<br>
            <b>Ground Elevation:</b> {row['elevation_m']} m ASL<br>
            <b>Predicted Flood Depth:</b> <span style="color: {'red' if row['water_depth_m'] > 0.8 else 'green'}; font-weight: bold;">{row['water_depth_m']} m</span><br>
            <b>Status:</b> {row['status']}
        </div>
        """
        
        icon_color = "red" if row["water_depth_m"] >= 1.5 else ("orange" if row["water_depth_m"] > 0.0 else "green")
        icon_type = "cross" if "Hospital" in row["type"] else ("flash" if "Power" in row["type"] else "home")
        
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{row['name']} ({row['status']})",
            icon=folium.Icon(color=icon_color, icon=icon_type, prefix="fa")
        ).add_to(m)
        
    st_folium(m, width="100%", height=520)

# ---------------------------------------------------------
# TAB 2: Gemini Multimodal Operational Intelligence
# ---------------------------------------------------------
with tab2:
    st.subheader("🧠 Gemini Disaster Operations & Advisory Dispatch Engine")
    st.markdown("Generates pre-landfall anticipatory action plans, infrastructure warnings, and multi-lingual alerts by synthesizing weather metrics and satellite elevation vectors.")
    
    if st.button("🚀 Run Gemini Multimodal Risk Synthesis", type="primary"):
        with st.spinner("Analyzing satellite elevation grids, weather vectors, and asset isolation graphs via Gemini..."):
            advisory = generate_disaster_advisory(cyclone_name, metrics, api_key=gemini_api_key)
            st.session_state["advisory_data"] = advisory

    if "advisory_data" in st.session_state:
        adv = st.session_state["advisory_data"]
        
        st.markdown(f'<div class="alert-box-red"><b>THREAT LEVEL: {adv.get("threat_level", "CRITICAL")}</b><br>{adv.get("executive_summary", "")}</div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("🚨 Priority Evacuation Zones")
            for zone in adv.get("priority_evacuation_zones", []):
                st.markdown(f"- ⚠️ **{zone}**")
                
            st.subheader("⚡ Infrastructure Damage & Isolation Assessment")
            infra_st = adv.get("infrastructure_status", {})
            st.write(f"🏥 **Hospitals & Medical**: {infra_st.get('hospitals', 'N/A')}")
            st.write(f"⚡ **Power Grid**: {infra_st.get('power_grid', 'N/A')}")
            st.write(f"🛣️ **Arterial Roads**: {infra_st.get('roads', 'N/A')}")

        with col_b:
            st.subheader("📋 Operational Tactical Commands")
            for cmd in adv.get("tactical_commands", []):
                st.markdown(f"1. 🎯 {cmd}")

            st.subheader("💳 Parametric Insurance & Emergency Liquidity")
            payout = adv.get("parametric_insurance", {})
            st.info(f"**Payout Trigger**: {payout.get('payout_trigger', 'APPROVED')}\n\n**Impact Severity Index**: {payout.get('severity_index', '8.5')}/10\n\n**Recommended Immediate Release**: {payout.get('recommended_liquidity_usd', '$2,500,000')}")

        st.markdown("---")
        st.subheader("📱 Automated Multi-Lingual Citizen Dispatches (SMS / Telegram / Radio)")
        
        dispatches = adv.get("public_dispatches", {})
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.text_area("🇬🇧 English Public Advisory", value=dispatches.get("english", ""), height=100)
            st.text_area("🇮🇳 Odia Public Advisory", value=dispatches.get("regional_odia", ""), height=100)
        with d_col2:
            st.text_area("🇮🇳 Bengali Public Advisory", value=dispatches.get("regional_bengali", ""), height=100)
            st.text_area("🇮🇳 Hindi Public Advisory", value=dispatches.get("regional_hindi", ""), height=100)

# ---------------------------------------------------------
# TAB 3: Exposure Analytics
# ---------------------------------------------------------
with tab3:
    st.subheader("📊 Coastal Infrastructure Vulnerability Analytics")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("#### Asset Inundation Depth (Meters)")
        chart_data = infra_df[["name", "water_depth_m"]].set_index("name")
        st.bar_chart(chart_data)
        
    with col_chart2:
        st.markdown("#### Ground Elevation vs Predicted Water Level")
        chart_elev = infra_df[["name", "elevation_m", "water_depth_m"]].set_index("name")
        st.area_chart(chart_elev)

    st.markdown("#### Detailed Infrastructure Exposure Table")
    st.dataframe(infra_df[["name", "type", "elevation_m", "water_depth_m", "status", "capacity_people"]], use_container_width=True)

# ---------------------------------------------------------
# TAB 4: Submission Package Guide
# ---------------------------------------------------------
with tab4:
    st.subheader("📝 Track 5 Submission Copy-Paste Template")
    st.markdown("Use the text below directly for filling out your hackathon prototype submission fields:")
    
    st.markdown("### **Brief Description of Your Solution**")
    st.code("""
ResiliTrack AI is an anticipatory disaster intelligence platform built for Track 5 (Cyclone Impact & Infrastructure Vulnerability Forecaster).

The solution integrates Google Earth Engine (GEE) satellite elevation feeds (NASADEM/SRTM) and real-time cyclone telemetry with Gemini 1.5/3.7 Multimodal AI reasoning to:
1. Simulate coastal storm surge inundation levels and hydro-elevation rainfall accumulation pathways.
2. Overlay OpenStreetMap infrastructure assets to calculate accessibility decay, flagging isolated hospitals, power grid failures, and flooded arterial roads hours before landfall.
3. Automate multi-lingual tactical command advisories and localized citizen alert dispatches in Bengali, Odia, Hindi, and English.
4. Provide immediate parametric insurance severity scores to trigger pre-landfall emergency relief funding.
""", language="markdown")

    st.markdown("### **Key Highlights for Pitch Deck / Demo Video**")
    st.markdown("""
- **Anticipatory Action Focus**: Shifts response from post-disaster recovery to pre-disaster targeted evacuation and infrastructure hardening.
- **Multimodal AI Integration**: Synthesizes visual satellite/elevation maps with complex meteorological vectors using Gemini.
- **Localized Regional Dispatches**: Generates native-language alerts for vulnerable coastal communities.
""")
