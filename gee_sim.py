"""
Google Earth Engine (GEE) & Hydro-Dynamic Inundation Simulation Engine
Provides elevation-aware storm surge modeling, satellite SAR flood overlays,
and critical infrastructure exposure analysis for coastal regions (Bay of Bengal / APAC).
"""

import numpy as np
import pandas as pd

def simulate_cyclone_telemetry(intensity_preset="Category 4 - Severe Severe"):
    """
    Returns realistic cyclone meteorological parameters.
    """
    presets = {
        "Category 2 - Moderate": {
            "wind_speed_kmh": 140,
            "category": 2,
            "surge_height_m": 2.2,
            "rainfall_mm": 180,
            "pressure_mb": 975,
            "affected_population": 125000,
            "total_hospitals": 12,
            "isolated_hospitals": 2,
            "flooded_roads_km": 34.5,
            "power_grid_risk_pct": 45
        },
        "Category 3 - Very Severe": {
            "wind_speed_kmh": 175,
            "category": 3,
            "surge_height_m": 3.8,
            "rainfall_mm": 260,
            "pressure_mb": 950,
            "affected_population": 310000,
            "total_hospitals": 15,
            "isolated_hospitals": 5,
            "flooded_roads_km": 78.2,
            "power_grid_risk_pct": 72
        },
        "Category 4 - Extremely Severe": {
            "wind_speed_kmh": 220,
            "category": 4,
            "surge_height_m": 5.4,
            "rainfall_mm": 380,
            "pressure_mb": 925,
            "affected_population": 540000,
            "total_hospitals": 18,
            "isolated_hospitals": 9,
            "flooded_roads_km": 142.0,
            "power_grid_risk_pct": 88
        },
        "Category 5 - Super Cyclone": {
            "wind_speed_kmh": 265,
            "category": 5,
            "surge_height_m": 7.2,
            "rainfall_mm": 510,
            "pressure_mb": 895,
            "affected_population": 890000,
            "total_hospitals": 22,
            "isolated_hospitals": 16,
            "flooded_roads_km": 245.5,
            "power_grid_risk_pct": 96
        }
    }
    return presets.get(intensity_preset, presets["Category 4 - Extremely Severe"])

def get_coastal_infrastructure_assets(center_lat=21.65, center_lon=87.85):
    """
    Generates coastal critical infrastructure nodes (Hospitals, Power Sub-stations, Evacuation Shelters, Bridges)
    along with their elevation above sea level (meters) and calculated inundation status.
    """
    np.random.seed(42)
    
    # 20 infrastructure locations around coastal Bay of Bengal region (e.g. Digha / Sundarbans / Paradeep region)
    lats = center_lat + np.random.uniform(-0.15, 0.15, 20)
    lons = center_lon + np.random.uniform(-0.15, 0.15, 20)
    
    types = [
        "Hospital / Trauma Center", "Power Sub-station", "Cyclone Evacuation Shelter", 
        "Water Treatment Plant", "Arterial Bridge / Causeway", "Telecom Tower"
    ]
    
    names = [
        "District General Hospital", "Coastal Power Grid Sub-station 1", "Central Multi-purpose Shelter",
        "Municipal Water Works", "Estuary Highway Bridge", "Telecom Node Alpha",
        "Sub-divisional Medical Unit", "Primary Sub-station B", "Community Relief Center 4",
        "Emergency Fuel Storage Depot", "Coastal Access Bridge West", "Regional Trauma Care",
        "Shelter 8 - High School Ground", "Water Purification Facility 2", "Grid Junction 4",
        "Mobile Command Outpost", "District Red Cross Shelter", "Port Authority Dispatch",
        "Sub-station C (Low-lying)", "Coastal Highway Toll Plaza"
    ]
    
    # Distance from coast determines approximate ground elevation (0.5m to 12.0m)
    elevations = np.round(np.random.uniform(0.8, 8.5, 20), 1)
    
    df = pd.DataFrame({
        "name": names,
        "type": np.random.choice(types, 20),
        "lat": lats,
        "lon": lons,
        "elevation_m": elevations,
        "capacity_people": np.random.randint(200, 2500, 20)
    })
    return df

def calculate_infrastructure_vulnerability(infra_df, surge_height_m, rainfall_mm):
    """
    Computes flood risk score and accessibility status for each asset based on elevation,
    storm surge height, and rainfall accumulation pathways.
    """
    # Inundation risk formula: (Surge Height + Rain Accumulation Factor) - Elevation
    rain_factor = rainfall_mm / 150.0  # Approx added water level in low-lying basins
    water_level = surge_height_m + rain_factor
    
    infra_df["water_depth_m"] = np.maximum(0.0, np.round(water_level - infra_df["elevation_m"], 2))
    
    def classify_status(depth):
        if depth == 0.0:
            return "SAFE / OPERATIONAL", "green"
        elif depth < 0.8:
            return "MODERATE RISK (SLIGHT FLOOD)", "orange"
        elif depth < 1.8:
            return "SEVERE INUNDATION (ACCESS CUT)", "red"
        else:
            return "CRITICAL / SUBMERGED", "darkred"

    results = [classify_status(d) for d in infra_df["water_depth_m"]]
    infra_df["status"] = [r[0] for r in results]
    infra_df["color"] = [r[1] for r in results]
    
    return infra_df
