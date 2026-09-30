from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

# Color palette
DARK_BG = RGBColor(0x0F, 0x17, 0x2A)
BLUE_ACCENT = RGBColor(0x1E, 0x88, 0xE5)
LIGHT_BLUE = RGBColor(0x38, 0xBD, 0xF8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xB0, 0xBE, 0xC5)
RED_ACCENT = RGBColor(0xEF, 0x44, 0x44)
GREEN_ACCENT = RGBColor(0x10, 0xB9, 0x81)
ORANGE_ACCENT = RGBColor(0xF5, 0x9E, 0x0B)

def set_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_text_box(slide, text, left, top, width, height, font_size=16,
                 bold=False, color=WHITE, align=PP_ALIGN.LEFT, italic=False):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.italic = italic
    return txBox

def add_rect(slide, left, top, width, height, fill_color, line_color=None):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
    else:
        shape.line.fill.background()
    return shape

# ─── SLIDE 1: Title ───────────────────────────────────────────────────────────
slide1 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide1, DARK_BG)
add_rect(slide1, 0, 0, 13.33, 0.08, BLUE_ACCENT)
add_rect(slide1, 0, 7.42, 13.33, 0.08, LIGHT_BLUE)
add_text_box(slide1, "🌀", 5.9, 1.0, 2, 1.2, font_size=52, align=PP_ALIGN.CENTER)
add_text_box(slide1, "ResiliTrack AI", 1, 2.2, 11.33, 1.2,
             font_size=52, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text_box(slide1, "Anticipatory Disaster Intelligence Platform", 1, 3.3, 11.33, 0.6,
             font_size=22, bold=False, color=LIGHT_BLUE, align=PP_ALIGN.CENTER)
add_text_box(slide1, "Track 5: Cyclone Impact & Infrastructure Vulnerability Forecaster", 1, 4.0, 11.33, 0.6,
             font_size=16, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
add_rect(slide1, 3.5, 4.8, 6.33, 0.04, LIGHT_BLUE)
add_text_box(slide1, "Powered by Google Earth Engine  •  Gemini 1.5 Flash  •  OpenStreetMap", 1, 5.0, 11.33, 0.5,
             font_size=13, color=LIGHT_GRAY, align=PP_ALIGN.CENTER, italic=True)
add_text_box(slide1, "Build with AI: Code for Communities — 2nd Edition", 1, 6.6, 11.33, 0.5,
             font_size=12, color=ORANGE_ACCENT, align=PP_ALIGN.CENTER)

# ─── SLIDE 2: Problem ─────────────────────────────────────────────────────────
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide2, DARK_BG)
add_rect(slide2, 0, 0, 13.33, 0.08, RED_ACCENT)
add_rect(slide2, 0, 1.0, 0.06, 6.5, RED_ACCENT)
add_text_box(slide2, "⚠  The Problem", 0.3, 0.2, 10, 0.7,
             font_size=30, bold=True, color=RED_ACCENT)
add_text_box(slide2, "Why generic cyclone warnings fail coastal communities", 0.3, 0.85, 10, 0.4,
             font_size=14, color=LIGHT_GRAY, italic=True)

problems = [
    ("🎯 Blind Spot in Last-Mile Intelligence",
     "Weather cones cover hundreds of km² but can't tell if a specific hospital feeder road or power sub-station will be under 1.5m of water at 3 AM."),
    ("🔁 Cascading Infrastructure Failure",
     "Disaster commanders struggle to identify which emergency shelters will be cut off before flooding occurs — making pre-positioned resources impossible."),
    ("📡 Communication Bottleneck",
     "Emergency officers receive raw satellite imagery without AI synthesis into immediate, localized, multi-lingual tactical actions."),
]

for i, (title, body) in enumerate(problems):
    y = 1.4 + i * 1.8
    add_rect(slide2, 0.3, y, 12.5, 1.55, RGBColor(0x1E, 0x29, 0x3B), RED_ACCENT)
    add_text_box(slide2, title, 0.5, y + 0.12, 12.0, 0.45, font_size=15, bold=True, color=RED_ACCENT)
    add_text_box(slide2, body, 0.5, y + 0.55, 12.0, 0.9, font_size=13, color=LIGHT_GRAY)

# ─── SLIDE 3: Solution ────────────────────────────────────────────────────────
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide3, DARK_BG)
add_rect(slide3, 0, 0, 13.33, 0.08, BLUE_ACCENT)
add_rect(slide3, 0, 1.0, 0.06, 6.5, BLUE_ACCENT)
add_text_box(slide3, "💡 The Solution — ResiliTrack AI", 0.3, 0.15, 11, 0.7,
             font_size=30, bold=True, color=BLUE_ACCENT)
add_text_box(slide3, "Shifting disaster response from reactive recovery to anticipatory pre-landfall action", 0.3, 0.8, 12, 0.4,
             font_size=14, color=LIGHT_GRAY, italic=True)

pillars = [
    ("🌊", "SIMULATE", "Hydro-Elevation Mapping", "GEE NASADEM/SRTM elevation matrices combined\nwith wind speed & 24h rainfall accumulation.", BLUE_ACCENT),
    ("🏥", "ANALYZE", "Infrastructure Exposure Graph", "Extracts hospitals, power grids, bridges from\nOpenStreetMap — calculates accessibility decay.", LIGHT_BLUE),
    ("🧠", "DECIDE", "Gemini AI Operations Intel", "Synthesizes satellite maps + telemetry into\nexecutive reports & multi-lingual alerts.", GREEN_ACCENT),
    ("💳", "FUND", "Parametric Insurance Score", "Pre-landfall severity index triggers instant\nliquidity payouts before the storm hits.", ORANGE_ACCENT),
]

for i, (icon, label, title, body, color) in enumerate(pillars):
    x = 0.3 + i * 3.22
    add_rect(slide3, x, 1.4, 3.0, 5.8, RGBColor(0x1E, 0x29, 0x3B))
    add_rect(slide3, x, 1.4, 3.0, 0.06, color)
    add_text_box(slide3, icon, x, 1.55, 3.0, 0.7, font_size=28, align=PP_ALIGN.CENTER)
    add_text_box(slide3, label, x, 2.3, 3.0, 0.4, font_size=10, bold=True, color=color, align=PP_ALIGN.CENTER)
    add_text_box(slide3, title, x, 2.7, 3.0, 0.5, font_size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text_box(slide3, body, x + 0.1, 3.25, 2.8, 1.5, font_size=11, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# ─── SLIDE 4: Gemini AI Advantage ─────────────────────────────────────────────
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide4, DARK_BG)
add_rect(slide4, 0, 0, 13.33, 0.08, GREEN_ACCENT)
add_rect(slide4, 0, 1.0, 0.06, 6.5, GREEN_ACCENT)
add_text_box(slide4, "🧠 The Gemini AI Advantage", 0.3, 0.15, 11, 0.7,
             font_size=30, bold=True, color=GREEN_ACCENT)
add_text_box(slide4, "Gemini 1.5 Flash acts as a Virtual Disaster Commander", 0.3, 0.8, 12, 0.4,
             font_size=14, color=LIGHT_GRAY, italic=True)

add_rect(slide4, 0.3, 1.3, 6.0, 5.9, RGBColor(0x1E, 0x29, 0x3B))
add_text_box(slide4, "What Gemini Produces:", 0.5, 1.4, 5.6, 0.45, font_size=15, bold=True, color=GREEN_ACCENT)
gemini_outputs = [
    "🎯  Structured executive risk reports",
    "🚨  Priority evacuation zone commands",
    "⚡  Infrastructure isolation assessments",
    "📱  Multi-lingual citizen SMS dispatches\n      (Bengali · Odia · Hindi · English)",
    "💳  Parametric insurance severity index",
]
for j, item in enumerate(gemini_outputs):
    add_text_box(slide4, item, 0.5, 1.95 + j * 0.9, 5.6, 0.8, font_size=12, color=WHITE)

add_rect(slide4, 6.6, 1.3, 6.4, 5.9, RGBColor(0x1E, 0x29, 0x3B))
add_text_box(slide4, "Edge-Case Handling (Refined Prompts):", 6.8, 1.4, 6.0, 0.45, font_size=15, bold=True, color=ORANGE_ACCENT)
edge_cases = [
    ("Minor Storm (<119 km/h)", "Downgrades to MODERATE/LOW threat. Focuses on preparedness, not panic."),
    ("Zero Infrastructure Risk", "Explicitly confirms critical infrastructure is secure and operational."),
    ("Below Catastrophe Threshold", "Sets parametric payout to NOT MET with $0, no false triggers."),
    ("API Key Absent", "Gracefully falls back to a pre-built realistic simulation engine."),
]
for j, (ec_title, ec_body) in enumerate(edge_cases):
    y = 2.0 + j * 1.2
    add_rect(slide4, 6.8, y, 5.9, 1.0, RGBColor(0x0F, 0x2A, 0x1F))
    add_text_box(slide4, "⚡ " + ec_title, 7.0, y + 0.05, 5.5, 0.35, font_size=12, bold=True, color=GREEN_ACCENT)
    add_text_box(slide4, ec_body, 7.0, y + 0.4, 5.5, 0.5, font_size=11, color=LIGHT_GRAY)

# ─── SLIDE 5: Community Impact ────────────────────────────────────────────────
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide5, DARK_BG)
add_rect(slide5, 0, 0, 13.33, 0.08, ORANGE_ACCENT)
add_rect(slide5, 0, 1.0, 0.06, 6.5, ORANGE_ACCENT)
add_text_box(slide5, "🌍 Community Impact", 0.3, 0.15, 11, 0.7,
             font_size=30, bold=True, color=ORANGE_ACCENT)
add_text_box(slide5, "Real-world value for millions of vulnerable coastal residents", 0.3, 0.8, 12, 0.4,
             font_size=14, color=LIGHT_GRAY, italic=True)

impacts = [
    ("🏃 Saves Lives", "Hyper-localized evacuation orders — not generic warnings. Residents in low-lying fishing hamlets and riverine delta islands get specific, actionable guidance.", GREEN_ACCENT),
    ("🏥 Protects Critical Infrastructure", "Hospitals are never caught off-guard. Pre-landfall alerts ensure backup generators are deployed and amphibious transport is pre-positioned for isolated trauma centers.", BLUE_ACCENT),
    ("🗣️ Inclusive Communication", "Overcomes the language barrier by auto-generating native-language alerts in Bengali, Odia, Hindi, and English — reaching the most vulnerable who may not speak English.", LIGHT_BLUE),
    ("💰 Financial Resilience", "Parametric insurance scores trigger immediate liquidity payouts BEFORE the storm hits — allowing communities to buy supplies and fuel relief operations instead of waiting for post-disaster aid.", ORANGE_ACCENT),
]

for i, (title, body, color) in enumerate(impacts):
    row = i // 2
    col = i % 2
    x = 0.3 + col * 6.5
    y = 1.4 + row * 2.9
    add_rect(slide5, x, y, 6.2, 2.6, RGBColor(0x1E, 0x29, 0x3B))
    add_rect(slide5, x, y, 6.2, 0.06, color)
    add_text_box(slide5, title, x + 0.15, y + 0.12, 5.9, 0.45, font_size=15, bold=True, color=color)
    add_text_box(slide5, body, x + 0.15, y + 0.6, 5.9, 1.8, font_size=11, color=LIGHT_GRAY)

# ─── SLIDE 6: Architecture ────────────────────────────────────────────────────
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide6, DARK_BG)
add_rect(slide6, 0, 0, 13.33, 0.08, LIGHT_BLUE)
add_rect(slide6, 0, 1.0, 0.06, 6.5, LIGHT_BLUE)
add_text_box(slide6, "⚙️ System Architecture", 0.3, 0.15, 11, 0.7,
             font_size=30, bold=True, color=LIGHT_BLUE)

sources = [("☁️ GEE Feeds", "Sentinel-1 SAR\nSentinel-2\nNASADEM DEM"), ("🌦️ Meteorological", "NOAA / IMD\nOpen-Meteo\nCyclone Tracks"), ("🗺️ OpenStreetMap", "Hospitals\nRoads & Bridges\nPower Sub-stations")]
for i, (t, b) in enumerate(sources):
    x = 0.3 + i * 2.5
    add_rect(slide6, x, 1.1, 2.2, 1.8, RGBColor(0x1E, 0x29, 0x3B), LIGHT_BLUE)
    add_text_box(slide6, t, x, 1.15, 2.2, 0.45, font_size=13, bold=True, color=LIGHT_BLUE, align=PP_ALIGN.CENTER)
    add_text_box(slide6, b, x, 1.6, 2.2, 1.2, font_size=10, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

add_text_box(slide6, "▼ feeds into", 0.3, 3.0, 13.0, 0.4, font_size=11, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

add_rect(slide6, 3.5, 3.5, 6.3, 1.3, RGBColor(0x1E, 0x29, 0x3B), BLUE_ACCENT)
add_text_box(slide6, "🧠 Gemini 1.5 Flash — Multimodal Decision Engine", 3.5, 3.55, 6.3, 0.5, font_size=14, bold=True, color=BLUE_ACCENT, align=PP_ALIGN.CENTER)
add_text_box(slide6, "Synthesizes elevation + telemetry + infrastructure graphs", 3.5, 4.05, 6.3, 0.55, font_size=11, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

add_text_box(slide6, "▼ outputs", 0.3, 4.85, 13.0, 0.4, font_size=11, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

outputs = [("🗺️ Inundation Map", BLUE_ACCENT), ("📱 Multi-Lingual Alerts", GREEN_ACCENT), ("💳 Insurance Score", ORANGE_ACCENT)]
for i, (t, c) in enumerate(outputs):
    x = 1.5 + i * 3.8
    add_rect(slide6, x, 5.3, 3.3, 0.9, RGBColor(0x1E, 0x29, 0x3B), c)
    add_text_box(slide6, t, x, 5.38, 3.3, 0.7, font_size=12, bold=True, color=c, align=PP_ALIGN.CENTER)

add_text_box(slide6, "Deployed on Streamlit Cloud  •  Containerized via Docker", 0.3, 6.5, 13.0, 0.5, font_size=11, color=LIGHT_GRAY, align=PP_ALIGN.CENTER, italic=True)

# ─── SLIDE 7: Live Demo ───────────────────────────────────────────────────────
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide7, DARK_BG)
add_rect(slide7, 0, 0, 13.33, 0.08, GREEN_ACCENT)
add_rect(slide7, 0, 1.0, 0.06, 6.5, GREEN_ACCENT)
add_text_box(slide7, "🚀 Live Demo Walkthrough", 0.3, 0.15, 11, 0.7,
             font_size=30, bold=True, color=GREEN_ACCENT)
add_text_box(slide7, "Prototype: https://efomw9k5jde5gwkxe3ybuj.streamlit.app/", 0.3, 0.8, 12, 0.4,
             font_size=13, color=LIGHT_BLUE, italic=True)

steps = [
    ("Step 1", "Select a target coastal sector (e.g., Bay of Bengal — Odisha / West Bengal)", "Use the sidebar dropdown to choose the region and observe the GIS map center change in real-time."),
    ("Step 2", "Adjust cyclone severity parameters", "Move the sliders: Max Wind Speed, Storm Surge Height, 24h Rainfall. Watch the inundation zone polygon intensity and infrastructure markers update."),
    ("Step 3", "Run Gemini Multimodal Risk Synthesis", "Click the '🚀 Run Gemini Multimodal Risk Synthesis' button. Gemini generates a full executive report, evacuation zones, tactical commands, and 4 language dispatches."),
    ("Step 4", "Explore the analytics & submission tab", "Review Asset Inundation Depth charts, the Detailed Infrastructure Exposure Table, and the built-in submission description template."),
]

for i, (step, title, body) in enumerate(steps):
    y = 1.4 + i * 1.45
    add_rect(slide7, 0.3, y, 1.1, 1.2, BLUE_ACCENT)
    add_text_box(slide7, step, 0.3, y + 0.3, 1.1, 0.5, font_size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_rect(slide7, 1.55, y, 11.5, 1.2, RGBColor(0x1E, 0x29, 0x3B))
    add_text_box(slide7, title, 1.7, y + 0.05, 11.1, 0.4, font_size=13, bold=True, color=WHITE)
    add_text_box(slide7, body, 1.7, y + 0.5, 11.1, 0.6, font_size=11, color=LIGHT_GRAY)

# ─── SLIDE 8: Close / Roadmap ─────────────────────────────────────────────────
slide8 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide8, DARK_BG)
add_rect(slide8, 0, 0, 13.33, 0.08, LIGHT_BLUE)
add_rect(slide8, 0, 7.42, 13.33, 0.08, BLUE_ACCENT)
add_text_box(slide8, "🔭 Roadmap & Closing", 0.3, 0.15, 11, 0.7,
             font_size=30, bold=True, color=LIGHT_BLUE)

roadmap = [
    ("Near-Term", "Integrate live IoT river gauge sensors for real-time ground truth validation of flood depth predictions."),
    ("Mid-Term", "Build automated WhatsApp/Telegram bot for direct citizen dispatch, integrating with national alert systems."),
    ("Long-Term", "Expand coverage to full APAC coastline: Philippines, Vietnam, Bangladesh, Myanmar."),
]
for i, (phase, body) in enumerate(roadmap):
    x = 0.3 + i * 4.3
    add_rect(slide8, x, 1.1, 4.1, 3.5, RGBColor(0x1E, 0x29, 0x3B), LIGHT_BLUE)
    add_text_box(slide8, phase, x, 1.15, 4.1, 0.4, font_size=14, bold=True, color=LIGHT_BLUE, align=PP_ALIGN.CENTER)
    add_text_box(slide8, body, x + 0.15, 1.7, 3.8, 2.5, font_size=12, color=LIGHT_GRAY)

add_rect(slide8, 0.3, 4.9, 12.73, 1.8, RGBColor(0x1E, 0x29, 0x3B), ORANGE_ACCENT)
add_text_box(slide8, '"With ResiliTrack AI, we aren\'t just weathering the storm — we are outsmarting it."', 0.5, 5.0, 12.3, 0.8, font_size=16, bold=True, color=ORANGE_ACCENT, align=PP_ALIGN.CENTER, italic=True)

add_text_box(slide8, "GitHub: github.com/swatiicfai/ResiliTrack-AI-CycloneShield-", 0.3, 6.7, 8, 0.5, font_size=12, color=LIGHT_GRAY)
add_text_box(slide8, "Live App: efomw9k5jde5gwkxe3ybuj.streamlit.app", 0.3, 7.1, 8, 0.4, font_size=12, color=LIGHT_BLUE)

# Save
out_path = "ResiliTrack_AI_Pitch_Deck.pptx"
prs.save(out_path)
print(f"Saved: {out_path}")
