import os
import json

def generate_disaster_advisory(cyclone_name, metrics, api_key=None):
    """
    Calls Google Gemini API to produce executive disaster command advisories,
    infrastructure vulnerability warnings, multi-lingual emergency dispatches,
    and parametric insurance liquidity scores.
    """
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    
    prompt = f"""
You are the Chief Emergency Operations Intelligence AI for coastal disaster response.
Analyze the following real-time cyclone hazard simulation telemetry and infrastructure exposure data:

- **Cyclone Name**: {cyclone_name}
- **Maximum Wind Speed**: {metrics['wind_speed_kmh']} km/h (Category {metrics['category']})
- **Estimated Storm Surge Height**: {metrics['surge_height_m']} meters
- **Predicted 24h Rainfall**: {metrics['rainfall_mm']} mm
- **High-Risk Flood Zone Population**: {metrics['affected_population']:,}
- **Compromised/Isolated Hospitals**: {metrics['isolated_hospitals']} out of {metrics['total_hospitals']}
- **Submerged Arterial Road Segments**: {metrics['flooded_roads_km']} km
- **Power Sub-station Failure Risk**: {metrics['power_grid_risk_pct']}%

SYSTEM INSTRUCTIONS (EDGE CASE HANDLING):
1. If the metrics indicate a minor storm (e.g., wind speed < 119 km/h, surge < 1.0m, or low infrastructure risk), scale down the threat level to "MODERATE" or "LOW", and focus tactical commands on basic preparedness rather than mass evacuation. Do NOT trigger panic for minor events.
2. If the infrastructure damage risk is negligible (e.g., 0 isolated hospitals, 0 flooded roads), clearly state that critical infrastructure is secure and expected to remain operational.
3. If the event severity does not meet the threshold for catastrophic damage, set the parametric insurance payout trigger to "PENDING" or "NOT MET". Only trigger "APPROVED" for Category 3+ cyclones or significant surge risk.

Based on this telemetry, generate a structured emergency response report with the following EXACT JSON structure (return ONLY raw valid JSON without markdown formatting):

{{
  "threat_level": "CRITICAL / SEVERE / MODERATE / LOW",
  "executive_summary": "Concise 2-sentence overview of landfall impact and critical threats (proportional to the actual data).",
  "priority_evacuation_zones": [
    "Sub-district A (Low-lying coastal belt)",
    "Sub-district B (Estuary river basin)"
  ],
  "infrastructure_status": {{
    "hospitals": "Detailed status of medical access and isolated emergency rooms.",
    "power_grid": "Grid failure projection and backup generator requirement.",
    "roads": "Primary evacuation route blockage and amphibious vehicle requirements."
  }},
  "tactical_commands": [
    "Command action 1",
    "Command action 2",
    "Command action 3"
  ],
  "public_dispatches": {{
    "english": "Urgent SMS warning for citizens in affected coastal districts.",
    "regional_bengali": "জরুরি নির্দেশিকা: উপকূলীয় বাসিন্দাদের অবিলম্বে ঘূর্ণিঝড় আশ্রয়কেন্দ্রে আশ্রয় নেওয়ার জন্য অনুরোধ করা হচ্ছে।",
    "regional_odia": "ଜରୁରୀ ସୂଚନା: ଉପକୂଳବର୍ତ୍ତୀ ଅଞ୍ଚଳର ଲୋକମାନଙ୍କୁ ତୁରନ୍ତ ବାତ୍ୟା ଆଶ୍ରୟସ୍ଥଳକୁ ଯିବାକୁ ପରାମର୍ଶ ଦିଆଯାଉଛି।",
    "regional_hindi": "आपातकालीन चेतावनी: तटीय क्षेत्रों के निवासी तुरंत निकटतम चक्रवात राहत शिविर में जाएं।"
  }},
  "parametric_insurance": {{
    "payout_trigger": "APPROVED / PENDING / NOT MET",
    "severity_index": 8.7,
    "recommended_liquidity_usd": "$2,500,000 for immediate pre-landfall relief (or $0 if not met)"
  }}
}}
"""

    if not api_key:
        # Structured realistic fallback for demo when API key is not yet set
        return {
            "threat_level": "CRITICAL (CATEGORY 4 CYCLONE)",
            "executive_summary": f"{cyclone_name} is advancing with {metrics['wind_speed_kmh']} km/h winds and a {metrics['surge_height_m']}m storm surge. Extreme inundation threatens {metrics['affected_population']:,} residents across low-lying coastal sectors.",
            "priority_evacuation_zones": [
                "Zone 1: Coastal Estuary (Sector 4 & 5)",
                "Zone 2: Low-Lying Fishing Hamlets (Bhadrak / South 24 Parganas)",
                "Zone 3: Riverine Delta Islands"
            ],
            "infrastructure_status": {
                "hospitals": f"{metrics['isolated_hospitals']} regional medical centers isolated due to flooded feeder roads. Amphibious transport required.",
                "power_grid": f"{metrics['power_grid_risk_pct']}% substation flooding risk. High probability of grid shutdown within 6 hours.",
                "roads": f"{metrics['flooded_roads_km']} km of primary coastal arterial highways under >1.0m inundation."
            },
            "tactical_commands": [
                "Deploy NDRF / Marine Rescue teams to Sector 4 coastal embankment breaches.",
                "Pre-position mobile diesel generators at Trauma Care Unit 2.",
                "Reroute emergency medical evacuation via Elevated Expressway 1."
            ],
            "public_dispatches": {
                "english": f"EMERGENCY ALERT: Cyclone {cyclone_name} landfall imminent. Evacuate low-lying areas immediately. Move to designated storm shelters.",
                "regional_bengali": f"জরুরি সতর্কবার্তা: ঘূর্ণিঝড় {cyclone_name} দ্রুত এগিয়ে আসছে। নিম্নাঞ্চলের বাসিন্দারা অবিলম্বে নিকটবর্তী ঘূর্ণিঝড় আশ্রয়কেন্দ্রে চলে যান।",
                "regional_odia": f"ଜରୁରୀ ସୂଚନା: ସାମୁଦ୍ରିକ ଝଡ଼ {cyclone_name} ପାଇଁ ତୁରନ୍ତ ଉପକୂଳବର୍ତ୍ତୀ ଅଞ୍ଚଳ ଖାଲି କରନ୍ତୁ ଏବଂ ନିକଟସ୍ଥ ବାତ୍ୟା ଆଶ୍ରୟସ୍ଥଳକୁ ଯାଆନ୍ତୁ।",
                "regional_hindi": f"आपातकालीन अलर्ट: चक्रवात {cyclone_name} के कारण तटीय इलाकों से तुरंत सुरक्षित स्थानों/चक्रवात शेल्टर की ओर प्रस्थान करें।"
            },
            "parametric_insurance": {
                "payout_trigger": "TRIGGERED (PRE-LANDFALL LIQUIDITY)",
                "severity_index": round(min(10.0, (metrics['wind_speed_kmh']/25) + (metrics['surge_height_m']*1.2)), 1),
                "recommended_liquidity_usd": f"${int((metrics['wind_speed_kmh']*15000) + (metrics['surge_height_m']*500000)):,} (Instant Relief Fund)"
            }
        }

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        # If API call fails or google-generativeai isn't configured, fallback gracefully
        res = generate_disaster_advisory(cyclone_name, metrics, api_key=None)
        res["note"] = f"Using simulated AI engine fallback (Error: {str(e)})"
        return res
