import streamlit as st
import math

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ThermoScale · Celsius → Kelvin",
    page_icon="🌡️",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Outfit:wght@300;400;600;800&display=swap');

/* ── Root & body ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #05050f !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 80% 60% at 50% 0%, #0d1a3a 0%, #05050f 70%) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
section.main > div { padding-top: 2rem !important; }

/* ── Typography base ── */
* { font-family: 'Outfit', sans-serif; }
h1, h2, h3 { font-family: 'Outfit', sans-serif; }

/* ── Hero label ── */
.hero-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    color: #4b8eff;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
/* ── Main title ── */
.main-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: #e8f0ff;
    line-height: 1.1;
    margin-bottom: 0.15rem;
}
.main-title span { color: #4b8eff; }

/* ── Subtitle ── */
.subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #3d5a99;
    letter-spacing: 0.08em;
    margin-bottom: 2.2rem;
}

/* ── Card container ── */
.card {
    background: linear-gradient(145deg, #0c1528 0%, #080e1f 100%);
    border: 1px solid #1a2d5a;
    border-radius: 20px;
    padding: 2rem 2.2rem 1.8rem;
    box-shadow: 0 0 60px rgba(75, 142, 255, 0.07), 0 20px 40px rgba(0,0,0,0.5);
    margin-bottom: 1.2rem;
}

/* ── Input label override ── */
[data-testid="stNumberInput"] label,
[data-testid="stSlider"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.18em !important;
    color: #3d6ec7 !important;
    text-transform: uppercase !important;
}

/* ── Number input ── */
[data-testid="stNumberInput"] input {
    background: #0a1020 !important;
    border: 1.5px solid #1e3566 !important;
    border-radius: 10px !important;
    color: #c8dcff !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 1.35rem !important;
    text-align: center !important;
    padding: 0.6rem 0.8rem !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #4b8eff !important;
    box-shadow: 0 0 0 3px rgba(75, 142, 255, 0.15) !important;
}

/* ── Slider ── */
[data-testid="stSlider"] .stSlider > div > div > div {
    background: #1a2d5a !important;
}
[data-testid="stSlider"] .stSlider > div > div > div > div {
    background: linear-gradient(90deg, #1a3a8c, #4b8eff) !important;
}

/* ── Result box ── */
.result-box {
    background: linear-gradient(135deg, #071630 0%, #0a1f4a 50%, #071630 100%);
    border: 1px solid #2a4a8a;
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin: 1rem 0;
}
.result-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #4b8eff, transparent);
}
.result-value {
    font-family: 'Space Mono', monospace;
    font-size: 3rem;
    font-weight: 700;
    color: #4b8eff;
    line-height: 1;
    margin-bottom: 0.2rem;
    text-shadow: 0 0 30px rgba(75, 142, 255, 0.4);
}
.result-unit {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    color: #3d6ec7;
    text-transform: uppercase;
}
.result-formula {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: #1e3a6e;
    margin-top: 0.9rem;
    letter-spacing: 0.06em;
}

/* ── Phase badge ── */
.phase-badge {
    display: inline-block;
    padding: 0.28rem 0.9rem;
    border-radius: 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 700;
    margin-top: 0.8rem;
}
.phase-solid   { background: #0d2545; color: #4b8eff; border: 1px solid #1e3d7a; }
.phase-liquid  { background: #0d3040; color: #42c5f5; border: 1px solid #1e5a7a; }
.phase-gas     { background: #3d0d10; color: #ff6b6b; border: 1px solid #7a1e24; }
.phase-plasma  { background: #3d1f00; color: #ffaa33; border: 1px solid #7a4200; }

/* ── Fact row ── */
.fact-row {
    display: flex;
    gap: 0.7rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}
.fact-chip {
    flex: 1;
    min-width: 120px;
    background: #08111f;
    border: 1px solid #111e35;
    border-radius: 10px;
    padding: 0.7rem 0.8rem;
    text-align: center;
}
.fact-chip-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.16em;
    color: #274475;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.fact-chip-value {
    font-family: 'Space Mono', monospace;
    font-size: 0.88rem;
    color: #7aadff;
    font-weight: 700;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid #0f1e38;
    margin: 1.5rem 0;
}

/* ── Footer ── */
.footer {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    color: #1a2d50;
    text-align: center;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
ABSOLUTE_ZERO = -273.15

def celsius_to_kelvin(c: float) -> float:
    return c - ABSOLUTE_ZERO

def get_phase(kelvin: float):
    """Return (label, css_class, emoji) for water's state at this temperature."""
    if kelvin < 273.15:
        return "Hielo · Sólido", "phase-solid", "🧊"
    elif kelvin < 373.15:
        return "Agua · Líquido", "phase-liquid", "💧"
    elif kelvin < 5000:
        return "Vapor · Gas", "phase-gas", "♨️"
    else:
        return "Plasma", "phase-plasma", "⚡"

def celsius_to_fahrenheit(c: float) -> float:
    return c * 9/5 + 32

def celsius_to_rankine(c: float) -> float:
    return (c + 273.15) * 9/5


# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown('<p class="hero-label">· Conversor de Temperatura ·</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Thermo<span>Scale</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Celsius  →  Kelvin  ·  Escala Absoluta</p>', unsafe_allow_html=True)

# ── Input card ──
st.markdown('<div class="card">', unsafe_allow_html=True)

col_in, col_sl = st.columns([1, 2], gap="large")

with col_in:
    celsius = st.number_input(
        "Temperatura (°C)",
        min_value=-273.15,
        max_value=1_000_000.0,
        value=25.0,
        step=0.01,
        format="%.2f",
        help="Mínimo: −273.15 °C (cero absoluto)",
    )

with col_sl:
    celsius_slider = st.slider(
        "Rango rápido",
        min_value=-273.15,
        max_value=500.0,
        value=float(celsius),
        step=0.5,
        label_visibility="visible",
    )
    # Keep slider & input in sync (slider wins if moved)
    if celsius_slider != celsius:
        celsius = celsius_slider

st.markdown('</div>', unsafe_allow_html=True)

# ── Calculation ──
kelvin = celsius_to_kelvin(celsius)
phase_label, phase_class, phase_emoji = get_phase(kelvin)
fahrenheit = celsius_to_fahrenheit(celsius)
rankine = celsius_to_rankine(celsius)

# ── Result card ──
st.markdown(f"""
<div class="result-box">
    <div class="result-value">{kelvin:,.4f}</div>
    <div class="result-unit">Kelvin (K)</div>
    <div class="result-formula">K = °C + 273.15 &nbsp;·&nbsp; {celsius:.2f} + 273.15 = {kelvin:.4f}</div>
    <div><span class="phase-badge {phase_class}">{phase_emoji} {phase_label} (H₂O)</span></div>
</div>
""", unsafe_allow_html=True)

# ── Conversions row ──
st.markdown(f"""
<div class="fact-row">
    <div class="fact-chip">
        <div class="fact-chip-label">Celsius</div>
        <div class="fact-chip-value">{celsius:.2f} °C</div>
    </div>
    <div class="fact-chip">
        <div class="fact-chip-label">Kelvin</div>
        <div class="fact-chip-value">{kelvin:.4f} K</div>
    </div>
    <div class="fact-chip">
        <div class="fact-chip-label">Fahrenheit</div>
        <div class="fact-chip-value">{fahrenheit:.2f} °F</div>
    </div>
    <div class="fact-chip">
        <div class="fact-chip-label">Rankine</div>
        <div class="fact-chip-value">{rankine:.4f} °R</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Reference expander ──
st.markdown('<hr class="divider">', unsafe_allow_html=True)

with st.expander("📐 Referencias de temperatura"):
    refs = {
        "Cero absoluto": -273.15,
        "Nitrógeno líquido": -195.79,
        "Hielo (0 °C)": 0.0,
        "Cuerpo humano": 37.0,
        "Agua hirviendo": 100.0,
        "Superficie del Sol": 5505.0,
    }
    for label, c_val in refs.items():
        k_val = celsius_to_kelvin(c_val)
        st.markdown(
            f"<span style='font-family:Space Mono,monospace;font-size:0.78rem;"
            f"color:#3d6ec7;letter-spacing:0.1em;'>{label}</span>"
            f"<span style='font-family:Space Mono,monospace;font-size:0.78rem;"
            f"color:#7aadff;float:right;'>{c_val} °C → {k_val:.2f} K</span><br>",
            unsafe_allow_html=True,
        )

# ── Footer ──
st.markdown("""
<p class="footer">
  K = °C + 273.15 &nbsp;·&nbsp; Escala Kelvin definida por William Thomson (Lord Kelvin) · 1848
</p>
""", unsafe_allow_html=True)
