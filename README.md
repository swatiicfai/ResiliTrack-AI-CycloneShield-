# 🌀 ResiliTrack AI — Cyclone Impact & Infrastructure Vulnerability Forecaster

> **Hackathon Submission**: Track 5 — Cyclone Impact & Infrastructure Vulnerability Forecaster  
> **Tech Stack**: Python, Streamlit, Folium, Google Earth Engine (GEE), Gemini Multimodal AI.

---

## 📌 Project Overview
**ResiliTrack AI** is an AI-powered predictive risk and vulnerability modeling platform. It synthesizes Google Earth Engine satellite elevation feeds (NASADEM/SRTM), real-time cyclone telemetry, and Gemini Multimodal AI reasoning to:
- Simulate **coastal storm surge inundation levels** and rainfall flood accumulation pathways.
- Map **critical infrastructure exposure** (hospitals, power grid sub-stations, arterial roads, evacuation shelters).
- Calculate **accessibility decay** and flag geographically isolated trauma centers before landfall occurs.
- Automate **multi-lingual emergency advisories** (English, Odia, Bengali, Hindi) for municipal authorities and local communities.
- Compute **parametric insurance severity scores** for rapid pre-landfall liquidity release.

---

## ⚡ Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch Dashboard
```bash
streamlit run app.py
```

### 3. Open in Browser
Navigate to `http://localhost:8501` to view the interactive disaster control room dashboard.

---

## 📁 Repository Structure
```
cyclone_shield_ai/
├── app.py              # Streamlit interactive dashboard UI
├── gemini_engine.py    # Gemini Multimodal AI disaster advisory generator
├── gee_sim.py          # Hydro-elevation simulation & infrastructure risk engine
├── requirements.txt    # Python dependencies
└── README.md           # Documentation & pitch guide
```
