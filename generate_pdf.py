# ResiliTrack AI — Pitch Deck PDF Generator
# Full rewrite with strict layout grid applied to all 8 slides.

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# ── Page geometry ──────────────────────────────────────────────────────────────
W, H   = landscape(A4)   # 841.89 x 595.28 pts
LBAR   = 5               # left accent bar width
TBAR   = 6               # top accent bar height
BBAR   = 6               # bottom accent bar height
PAD    = 10              # inner card padding
M      = LBAR + 14       # left margin (after lbar + gap)
MR     = 14              # right margin
MB     = 14              # bottom margin
HPAD   = 66              # header area height (top bar + title + subtitle + gap)

# Derived content region (all slides draw inside this)
CX  = M                  # content left x
CW  = W - M - MR         # content width
CYT = H - HPAD           # content top y   (just below header)
CYB = MB                 # content bottom y
CH  = CYT - CYB          # content height  (~509 pt)

# ── Colours ────────────────────────────────────────────────────────────────────
BG     = HexColor("#0F172A")
CARD   = HexColor("#1E293B")
DCARD  = HexColor("#0D1F2D")
BLUE   = HexColor("#1E88E5")
LBLUE  = HexColor("#38BDF8")
WHITE  = HexColor("#FFFFFF")
LGRAY  = HexColor("#B0BEC5")
RED    = HexColor("#EF4444")
GREEN  = HexColor("#10B981")
ORANGE = HexColor("#F59E0B")

# ── Primitives ─────────────────────────────────────────────────────────────────
def _bg(c):
    c.setFillColor(BG); c.rect(0, 0, W, H, fill=1, stroke=0)

def _tbar(c, col):
    c.setFillColor(col); c.rect(0, H-TBAR, W, TBAR, fill=1, stroke=0)

def _bbar(c, col):
    c.setFillColor(col); c.rect(0, 0, W, BBAR, fill=1, stroke=0)

def _lbar(c, col):
    c.setFillColor(col); c.rect(0, 0, LBAR, H, fill=1, stroke=0)

def _header(c, title, subtitle, tcol, scol=None):
    """Draw standard title + subtitle inside header band."""
    scol = scol or LGRAY
    c.setFillColor(tcol);  c.setFont("Helvetica-Bold", 24)
    c.drawString(CX, H - 36, title)
    c.setFillColor(scol);  c.setFont("Helvetica-Oblique", 11)
    c.drawString(CX, H - 56, subtitle)

def _pgnum(c, n, total=8):
    c.setFillColor(LGRAY); c.setFont("Helvetica", 9)
    c.drawRightString(W - MR, 10, f"{n} / {total}")

def _rect(c, x, y, w, h, fill=CARD, stroke=None, sw=1):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke); c.setLineWidth(sw)
        c.rect(x, y, w, h, fill=1, stroke=1)
    else:
        c.rect(x, y, w, h, fill=1, stroke=0)

def _tline(c, x, y, w, h, col):
    """Coloured top accent line on a card."""
    c.setFillColor(col); c.rect(x, y+h-4, w, 4, fill=1, stroke=0)

def _t(c, text, x, y, size=11, col=WHITE, bold=False, italic=False):
    c.setFillColor(col)
    if bold:   f = "Helvetica-Bold"
    elif italic: f = "Helvetica-Oblique"
    else:      f = "Helvetica"
    c.setFont(f, size); c.drawString(x, y, text)

def _ct(c, text, cx, y, size=11, col=WHITE, bold=False, italic=False):
    c.setFillColor(col)
    f = "Helvetica-Bold" if bold else ("Helvetica-Oblique" if italic else "Helvetica")
    c.setFont(f, size); c.drawCentredString(cx, y, text)

def _wrap(c, text, x, y, max_w, size=10, col=LGRAY, lh=15):
    """Word-wrap text; returns final y after last line."""
    c.setFillColor(col); c.setFont("Helvetica", size)
    words = text.split(); line = ""; cy = y
    for w_ in words:
        test = (line + " " + w_).strip()
        if c.stringWidth(test, "Helvetica", size) <= max_w:
            line = test
        else:
            if line: c.drawString(x, cy, line); cy -= lh
            line = w_
    if line: c.drawString(x, cy, line)
    return cy

def _arrow(c, cx, ytop, ybot, label):
    """Vertical arrow from ytop down to ybot with label below."""
    c.setStrokeColor(LBLUE); c.setLineWidth(1.3)
    c.line(cx, ytop, cx, ybot + 10)
    c.setFillColor(LBLUE); c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(cx, ybot, "v")
    _ct(c, label, cx, ybot - 12, 9, LGRAY, italic=True)

# ── SLIDE 1 — TITLE ───────────────────────────────────────────────────────────
def s1(c):
    _bg(c); _tbar(c, BLUE); _bbar(c, LBLUE); _lbar(c, BLUE)
    # Corner circles (decorative, stay inside corners)
    c.setFillColor(HexColor("#1A3356")); c.circle(W-60, H-60, 90, fill=1, stroke=0)
    c.setFillColor(HexColor("#0E243C")); c.circle(60,    60,   70, fill=1, stroke=0)

    _ct(c, "ResiliTrack AI",  W/2, H*0.60, 52, WHITE, bold=True)
    _ct(c, "Anticipatory Disaster Intelligence Platform", W/2, H*0.45, 19, LBLUE)
    _ct(c, "Track 5: Cyclone Impact & Infrastructure Vulnerability Forecaster",
        W/2, H*0.34, 13, LGRAY)

    c.setStrokeColor(LBLUE); c.setLineWidth(1.2)
    c.line(W*0.28, H*0.27, W*0.72, H*0.27)

    _ct(c, "Google Earth Engine  |  Gemini 1.5 Flash  |  OpenStreetMap  |  Streamlit Cloud",
        W/2, H*0.20, 10, LGRAY)
    _ct(c, "Build with AI: Code for Communities  -  2nd Edition",
        W/2, H*0.11, 11, ORANGE, bold=True)
    _pgnum(c, 1); c.showPage()

# ── SLIDE 2 — THE PROBLEM ─────────────────────────────────────────────────────
def s2(c):
    _bg(c); _tbar(c, RED); _lbar(c, RED)
    _header(c, "THE PROBLEM",
            "Why generic cyclone warnings fail coastal communities", RED)

    problems = [
        ("01  Blind Spot in Last-Mile Intelligence",
         "Weather cones cover hundreds of sq km but cannot tell if a specific hospital feeder "
         "road will be under 1.5 m of water at 3 AM — the critical hour before landfall."),
        ("02  Cascading Infrastructure Failure",
         "Disaster commanders cannot identify which emergency shelters will be cut off before "
         "flooding occurs, making it impossible to pre-position life-saving resources."),
        ("03  Communication Bottleneck",
         "Emergency officers receive raw satellite imagery without AI synthesis into immediate, "
         "localized, multi-lingual tactical actions for frontline workers and citizens."),
    ]

    n   = len(problems)
    gap = 10
    bh  = (CH - gap*(n-1)) / n   # each card fills equal share of content height
    bw  = CW

    for i, (title, body) in enumerate(problems):
        by = CYT - (i+1)*bh - i*gap
        _rect(c, CX, by, bw, bh, fill=CARD, stroke=RED, sw=1.2)
        _tline(c, CX, by, bw, bh, RED)
        _t(c, title, CX+12, by+bh-24, 13, RED, bold=True)
        _wrap(c, body, CX+12, by+bh-44, bw-24, 11, WHITE, 16)

    _pgnum(c, 2); c.showPage()

# ── SLIDE 3 — THE SOLUTION ────────────────────────────────────────────────────
def s3(c):
    _bg(c); _tbar(c, BLUE); _lbar(c, BLUE)
    _header(c, "THE SOLUTION  -  ResiliTrack AI",
            "Shifting from reactive recovery to anticipatory pre-landfall action", BLUE)

    pillars = [
        ("SIMULATE",  ["Storm Surge &", "Hydro-Elevation", "Mapping"],
         "GEE NASADEM/SRTM elevation matrices combined with wind speed & 24h "
         "rainfall accumulation to generate hyper-local flood depth overlays.", BLUE),
        ("ANALYZE",   ["Infrastructure", "Exposure Graph"],
         "Extracts hospitals, power grids, bridges from OpenStreetMap. Calculates "
         "accessibility decay and flags isolated trauma centers.", LBLUE),
        ("DECIDE",    ["Gemini AI", "Operations Intel"],
         "Synthesizes satellite maps + telemetry into executive reports, priority "
         "evacuation zones, and multi-lingual citizen alerts.", GREEN),
        ("FUND",      ["Parametric", "Insurance Score"],
         "Pre-landfall severity index triggers instant emergency liquidity "
         "payouts BEFORE the storm makes landfall.", ORANGE),
    ]

    n   = len(pillars)
    gap = 8
    pw  = (CW - gap*(n-1)) / n
    ph  = CH

    for i, (label, title_lines, body, col) in enumerate(pillars):
        px = CX + i*(pw+gap)
        py = CYB
        cx = px + pw/2

        _rect(c, px, py, pw, ph, fill=CARD)
        _tline(c, px, py, pw, ph, col)

        # Label
        _ct(c, label, cx, py+ph-22, 10, col, bold=True)

        # Title lines
        ty = py + ph - 42
        for line in title_lines:
            _ct(c, line, cx, ty, 13, WHITE, bold=True); ty -= 17

        # Body
        _wrap(c, body, px+8, ty-8, pw-16, 9, LGRAY, 14)

    _pgnum(c, 3); c.showPage()

# ── SLIDE 4 — GEMINI ADVANTAGE ───────────────────────────────────────────────
def s4(c):
    _bg(c); _tbar(c, GREEN); _lbar(c, GREEN)
    _header(c, "THE GEMINI AI ADVANTAGE",
            "Gemini 1.5 Flash - context-aware, proportional, multi-lingual Virtual Disaster Commander",
            GREEN)

    hw = (CW - 12) / 2   # half width
    lx = CX; rx = CX + hw + 12
    cy = CYB; ch = CH

    # Left card
    _rect(c, lx, cy, hw, ch, fill=CARD)
    _tline(c, lx, cy, hw, ch, GREEN)
    _t(c, "What Gemini Produces:", lx+10, cy+ch-22, 13, GREEN, bold=True)
    items = [
        "->  Structured executive risk reports",
        "->  Priority evacuation zone commands",
        "->  Infrastructure isolation assessments",
        "->  Multi-lingual citizen SMS dispatches",
        "      Bengali  /  Odia  /  Hindi  /  English",
        "->  Parametric insurance severity index",
    ]
    iy = cy + ch - 46
    for item in items:
        _t(c, item, lx+12, iy, 11, WHITE); iy -= 24

    # Right card
    _rect(c, rx, cy, hw, ch, fill=CARD)
    _tline(c, rx, cy, hw, ch, ORANGE)
    _t(c, "Edge-Case Handling (Refined Prompts):", rx+10, cy+ch-22, 13, ORANGE, bold=True)

    cases = [
        ("Minor Storm  (<119 km/h)",
         "Scales to MODERATE or LOW. Focuses on preparedness, avoids panic."),
        ("Zero Infrastructure Risk",
         "Confirms critical infrastructure is secure and fully operational."),
        ("Below Catastrophe Threshold",
         "Sets payout to NOT MET with $0 — no false triggers, ever."),
        ("API Key Absent",
         "Gracefully falls back to pre-built realistic simulation engine."),
    ]
    eh = (CH - 32 - 10*3) / 4
    ey = cy + ch - 44

    for (et, eb) in cases:
        _rect(c, rx+8, ey-eh, hw-16, eh, fill=DCARD)
        _t(c, et, rx+16, ey-12, 11, ORANGE, bold=True)
        _wrap(c, eb, rx+16, ey-28, hw-32, 10, LGRAY, 14)
        ey -= eh + 10

    _pgnum(c, 4); c.showPage()

# ── SLIDE 5 — COMMUNITY IMPACT ────────────────────────────────────────────────
def s5(c):
    _bg(c); _tbar(c, ORANGE); _lbar(c, ORANGE)
    _header(c, "COMMUNITY IMPACT",
            "Real-world value for millions of vulnerable coastal residents across South & Southeast Asia",
            ORANGE)

    impacts = [
        ("Saves Lives",
         "Hyper-localized evacuation orders — not generic warnings. Residents in low-lying fishing "
         "hamlets and riverine delta islands get specific, actionable guidance hours before landfall.", GREEN),
        ("Protects Critical Infrastructure",
         "Pre-landfall alerts ensure backup generators are deployed and amphibious transport is "
         "pre-positioned for isolated trauma centers and hospitals before flooding occurs.", BLUE),
        ("Inclusive Communication",
         "Auto-generates native-language alerts in Bengali, Odia, Hindi, and English — reaching "
         "the most vulnerable communities who may not understand broadcast warnings.", LBLUE),
        ("Financial Resilience",
         "Parametric insurance scores trigger immediate liquidity payouts BEFORE the storm hits — "
         "communities buy supplies instead of waiting weeks for post-disaster aid approval.", ORANGE),
    ]

    gap = 10
    cw  = (CW - gap) / 2
    ch  = (CH - gap) / 2

    for i, (title, body, col) in enumerate(impacts):
        col_i = i % 2; row_i = i // 2
        ix = CX + col_i*(cw+gap)
        iy = CYB + (1-row_i)*(ch+gap)

        _rect(c, ix, iy, cw, ch, fill=CARD)
        _tline(c, ix, iy, cw, ch, col)
        _t(c, title, ix+10, iy+ch-24, 14, col, bold=True)
        _wrap(c, body, ix+10, iy+ch-46, cw-20, 11, WHITE, 16)

    _pgnum(c, 5); c.showPage()

# ── SLIDE 6 — SYSTEM ARCHITECTURE ────────────────────────────────────────────
def s6(c):
    _bg(c); _tbar(c, LBLUE); _lbar(c, LBLUE)
    _header(c, "SYSTEM ARCHITECTURE",
            "End-to-end data flow: Satellite + Telemetry  ->  Gemini AI  ->  Operational Outputs",
            LBLUE)

    # ── Fixed heights for each zone ───────────────────────────────────────────
    src_h   = 68    # source box height
    arr_h   = 44    # arrow zone height (line + label)
    gem_h   = 60    # Gemini box height
    out_h   = 52    # output box height
    bot_label = 18  # footer label height

    # Total = src_h + arr_h + gem_h + arr_h + out_h + bot_label
    total = src_h + arr_h + gem_h + arr_h + out_h + bot_label
    # Verify it fits:  total < CH  (509 pt) — yes, ~306 pt — centre vertically
    vpad = (CH - total) / 2   # vertical padding top & bottom

    # Start drawing from the top of content region
    y = CYT - vpad   # top of source boxes

    # Row 1: Source boxes
    src_gap = 10
    sw = (CW - src_gap*2) / 3
    sy = y - src_h

    for i, (t, b) in enumerate([
        ("Google Earth Engine",   "Sentinel-1 SAR / Sentinel-2 / NASADEM DEM"),
        ("Meteorological Data",   "NOAA / IMD / Open-Meteo / Cyclone Tracks"),
        ("OpenStreetMap Assets",  "Hospitals / Roads & Bridges / Power Grids"),
    ]):
        sx = CX + i*(sw+src_gap); cx = sx + sw/2
        _rect(c, sx, sy, sw, src_h, fill=CARD, stroke=LBLUE, sw=1.2)
        _tline(c, sx, sy, sw, src_h, LBLUE)
        _ct(c, t, cx, sy+src_h-22, 12, LBLUE, bold=True)
        _ct(c, b, cx, sy+src_h-44,  9, LGRAY)

    # Arrow 1
    a1t = sy                        # top of arrow = bottom of source boxes
    a1b = a1t - arr_h
    _arrow(c, W/2, a1t, a1b + 14, "feeds into")

    # Gemini box
    gw = CW * 0.64
    gx = CX + (CW - gw) / 2
    gy = a1b - gem_h

    _rect(c, gx, gy, gw, gem_h, fill=CARD, stroke=BLUE, sw=2)
    _tline(c, gx, gy, gw, gem_h, BLUE)
    _ct(c, "Gemini 1.5 Flash  -  Multimodal Decision Engine",
        gx+gw/2, gy+gem_h-24, 14, BLUE, bold=True)
    _ct(c, "Synthesizes elevation matrices + live telemetry + infrastructure exposure graphs",
        gx+gw/2, gy+14, 10, LGRAY)

    # Arrow 2
    a2t = gy
    a2b = a2t - arr_h
    _arrow(c, W/2, a2t, a2b + 14, "outputs")

    # Output boxes
    out_gap = 10
    ow = (CW - out_gap*2) / 3
    oy = a2b - out_h

    for i, (label, col) in enumerate([
        ("Inundation Map",       BLUE),
        ("Multi-Lingual Alerts", GREEN),
        ("Insurance Score",      ORANGE),
    ]):
        ox = CX + i*(ow+out_gap); ocx = ox + ow/2
        _rect(c, ox, oy, ow, out_h, fill=CARD, stroke=col, sw=1.5)
        _ct(c, label, ocx, oy + out_h/2 - 6, 13, col, bold=True)

    _ct(c, "Deployed on Streamlit Cloud  |  Containerized via Docker",
        W/2, CYB + 2, 9, LGRAY, italic=True)
    _pgnum(c, 6); c.showPage()

# ── SLIDE 7 — DEMO WALKTHROUGH ────────────────────────────────────────────────
def s7(c):
    _bg(c); _tbar(c, GREEN); _lbar(c, GREEN)
    _header(c, "LIVE DEMO WALKTHROUGH",
            "Live app: https://efomw9k5jde5gwkxe3ybuj.streamlit.app/",
            GREEN, LBLUE)

    steps = [
        ("01", "Select Target Coastal Sector",
         "Use the sidebar dropdown to pick a region (e.g. Bay of Bengal - Odisha/West Bengal). "
         "The interactive GIS map re-centres instantly."),
        ("02", "Adjust Cyclone Severity Parameters",
         "Move sliders: Max Wind Speed, Storm Surge Height, 24h Rainfall. "
         "Watch the flood polygon intensity and infrastructure markers update dynamically."),
        ("03", "Run Gemini Multimodal Risk Synthesis",
         "Click 'Run Gemini Risk Synthesis'. Gemini generates a full executive report, evacuation "
         "zones, tactical commands, and dispatches in 4 languages - Bengali, Odia, Hindi, English."),
        ("04", "Explore Analytics & Submission Tab",
         "Review Asset Inundation Depth charts, the Detailed Infrastructure Exposure Table, "
         "and the built-in hackathon submission description ready to copy-paste."),
    ]

    n      = len(steps)
    gap    = 8
    num_w  = 54
    step_h = (CH - gap*(n-1)) / n

    for i, (num, title, body) in enumerate(steps):
        sy = CYT - (i+1)*step_h - i*gap
        # Badge
        _rect(c, CX, sy, num_w, step_h, fill=BLUE)
        _ct(c, num, CX + num_w/2, sy + step_h/2 - 7, 16, WHITE, bold=True)
        # Card
        tx = CX + num_w + 6
        tw = CW - num_w - 6
        _rect(c, tx, sy, tw, step_h, fill=CARD)
        _t(c, title, tx+10, sy+step_h-22, 13, WHITE, bold=True)
        _wrap(c, body, tx+10, sy+step_h-40, tw-20, 10, LGRAY, 14)

    _pgnum(c, 7); c.showPage()

# ── SLIDE 8 — ROADMAP & CLOSING ──────────────────────────────────────────────
def s8(c):
    _bg(c); _tbar(c, LBLUE); _bbar(c, BLUE); _lbar(c, LBLUE)
    _header(c, "ROADMAP & CLOSING", "", LBLUE)

    rw  = (CW - 20) / 3
    rh  = CH * 0.52
    ry  = CYT - rh

    roadmap = [
        ("Near-Term",
         "Integrate live IoT river gauge sensors for real-time ground truth validation "
         "of flood depth predictions alongside GEE satellite feeds.", BLUE),
        ("Mid-Term",
         "Build automated WhatsApp / Telegram bot for direct citizen dispatch, integrating "
         "with national emergency alert systems (IMD, NDMA).", GREEN),
        ("Long-Term",
         "Expand full APAC coverage: Philippines, Vietnam, Bangladesh, Myanmar — "
         "becoming the region's go-to anticipatory disaster intelligence layer.", ORANGE),
    ]
    for i, (phase, body, col) in enumerate(roadmap):
        rx_ = CX + i*(rw+10); cx = rx_ + rw/2
        _rect(c, rx_, ry, rw, rh, fill=CARD, stroke=col, sw=1.2)
        _tline(c, rx_, ry, rw, rh, col)
        _ct(c, phase, cx, ry+rh-24, 13, col, bold=True)
        _wrap(c, body, rx_+10, ry+rh-46, rw-20, 10, WHITE, 15)

    # Quote box
    qh = 52
    qy = ry - 14 - qh
    _rect(c, CX, qy, CW, qh, fill=CARD, stroke=ORANGE, sw=1.5)
    _ct(c,
        '"With ResiliTrack AI, we aren\'t just weathering the storm - we are outsmarting it."',
        W/2, qy + qh/2 - 6, 13, ORANGE, bold=True, italic=True)

    # Links
    _t(c, "GitHub:   github.com/swatiicfai/ResiliTrack-AI-CycloneShield-",
       CX, qy - 22, 10, LGRAY)
    _t(c, "Live App: https://efomw9k5jde5gwkxe3ybuj.streamlit.app/",
       CX, qy - 38, 10, LBLUE)

    _pgnum(c, 8); c.showPage()

# ── RENDER ─────────────────────────────────────────────────────────────────────
out = "ResiliTrack_AI_Pitch_Deck.pdf"
cv = canvas.Canvas(out, pagesize=landscape(A4))
cv.setTitle("ResiliTrack AI - Cyclone & Infrastructure Risk Forecaster")
cv.setAuthor("ResiliTrack AI Team")
cv.setSubject("Build with AI: Code for Communities - Track 5")

s1(cv); s2(cv); s3(cv); s4(cv); s5(cv); s6(cv); s7(cv); s8(cv)
cv.save()
print("PDF saved: " + out)
