import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AgroSentinel · Consulta Agrícola",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background-color: #0d1f0f;
    background-image:
        radial-gradient(ellipse at 20% 10%, rgba(52, 111, 47, 0.18) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 90%, rgba(180, 210, 80, 0.08) 0%, transparent 50%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111f10;
    border-right: 1px solid rgba(180, 210, 80, 0.15);
}
section[data-testid="stSidebar"] * {
    color: #c8dfa0 !important;
}

/* Header hero */
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3.2rem;
    line-height: 1.1;
    color: #e8f5c0;
    letter-spacing: -0.5px;
    margin-bottom: 0.2rem;
}
.hero-subtitle {
    font-size: 1rem;
    color: #7aac5a;
    font-weight: 300;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* KPI cards */
.kpi-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(180, 210, 80, 0.2);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: rgba(180, 210, 80, 0.5); }
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: #b4d250;
    line-height: 1;
}
.kpi-label {
    font-size: 0.75rem;
    color: #7aac5a;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.4rem;
}

/* Section divider */
.section-label {
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4a7a3a;
    border-bottom: 1px solid rgba(180,210,80,0.12);
    padding-bottom: 0.5rem;
    margin: 1.5rem 0 1rem;
}

/* Selectbox / inputs */
.stSelectbox label, .stFileUploader label {
    color: #c8dfa0 !important;
    font-size: 0.85rem !important;
}

/* Dataframe */
.stDataFrame {
    border: 1px solid rgba(180, 210, 80, 0.15) !important;
    border-radius: 8px;
    overflow: hidden;
}

/* Alert */
.stAlert {
    background: rgba(180, 210, 80, 0.08) !important;
    border: 1px solid rgba(180, 210, 80, 0.3) !important;
    color: #c8dfa0 !important;
    border-radius: 8px !important;
}

/* Plotly chart backgrounds */
.js-plotly-plot {
    border-radius: 12px;
    overflow: hidden;
}

/* Hide Streamlit branding */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Chart theme ────────────────────────────────────────────────────────────────
CHART_BG     = "rgba(0,0,0,0)"
CHART_PAPER  = "rgba(0,0,0,0)"
GRID_COLOR   = "rgba(180,210,80,0.08)"
FONT_COLOR   = "#c8dfa0"
ACCENT       = "#b4d250"
PALETTE      = ["#b4d250", "#7aac5a", "#4a7a3a", "#2f5426", "#e8f5c0", "#346f2f"]

def apply_chart_theme(fig):
    fig.update_layout(
        paper_bgcolor=CHART_PAPER,
        plot_bgcolor=CHART_BG,
        font_color=FONT_COLOR,
        font_family="DM Sans",
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            bgcolor="rgba(0,0,0,0.3)",
            bordercolor="rgba(180,210,80,0.2)",
            borderwidth=1,
        ),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, showgrid=True, zeroline=False)
    fig.update_yaxes(gridcolor=GRID_COLOR, showgrid=True, zeroline=False)
    return fig

# ─── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    # Normalise column names (strip whitespace)
    df.columns = df.columns.str.strip()
    return df

METRIC_COLS = ['Área sembrada (ha)', 'Área cosechada (ha)', 'Producción (t)']
DETAIL_COLS = ['Año', 'Municipio', 'Cultivo',
               'Área sembrada (ha)', 'Área cosechada (ha)',
               'Producción (t)', 'Rendimiento (t/ha)']

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 1.5rem;'>
        <div style='font-family: DM Serif Display, serif; font-size:1.5rem; color:#e8f5c0;'>🌿 AgroSentinel</div>
        <div style='font-size:0.7rem; color:#4a7a3a; letter-spacing:0.2em; text-transform:uppercase; margin-top:4px;'>
            Desempeño Agrícola · 2019–2024
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">📂 Fuente de datos</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Carga el archivo Excel",
        type=["xlsx"],
        help="Archivo: 20250617_BaseAgricola20192024.xlsx"
    )

    if uploaded_file:
        df_raw = load_data(uploaded_file)

        st.markdown('<div class="section-label">🔍 Filtros</div>', unsafe_allow_html=True)

        departamentos = sorted(df_raw['Departamento'].dropna().unique().tolist())
        depto_sel = st.selectbox("Departamento", departamentos)

        cultivos_disponibles = sorted(
            df_raw[df_raw['Departamento'] == depto_sel]['Cultivo'].dropna().unique().tolist()
        )
        cultivo_sel = st.selectbox("Cultivo", cultivos_disponibles)

        st.markdown('<div class="section-label">📊 Vista</div>', unsafe_allow_html=True)
        mostrar_tabla_detalle = st.checkbox("Mostrar detalle municipal", value=False)

# ─── Main content ───────────────────────────────────────────────────────────────
if not uploaded_file:
    # Landing / empty state
    st.markdown("""
    <div style='text-align:center; padding: 5rem 2rem;'>
        <div class='hero-title'>Consulta de<br>Desempeño Agrícola</div>
        <div class='hero-subtitle'>Colombia · 2019 – 2024</div>
        <p style='color:#4a7a3a; max-width:480px; margin:0 auto; font-size:0.95rem; line-height:1.7;'>
            Carga el archivo Excel en el panel izquierdo para explorar área sembrada, 
            área cosechada, producción y rendimiento por departamento y cultivo.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Filter data ────────────────────────────────────────────────────────────────
df_filtrado = df_raw[
    (df_raw['Departamento'].str.contains(depto_sel, case=False, na=False)) &
    (df_raw['Cultivo'].str.contains(cultivo_sel, case=False, na=False))
].copy()

# Coerce metrics to numeric
for col in METRIC_COLS:
    if col in df_filtrado.columns:
        df_filtrado[col] = pd.to_numeric(df_filtrado[col], errors='coerce')

if 'Rendimiento (t/ha)' in df_filtrado.columns:
    df_filtrado['Rendimiento (t/ha)'] = pd.to_numeric(df_filtrado['Rendimiento (t/ha)'], errors='coerce')

# ─── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='padding: 1.5rem 0 0.5rem;'>
    <div class='hero-subtitle'>Resultados · {depto_sel}</div>
    <div class='hero-title'>{cultivo_sel}</div>
</div>
""", unsafe_allow_html=True)

if df_filtrado.empty:
    st.warning("No se encontraron registros para la combinación seleccionada.")
    st.stop()

# ─── KPI Cards ──────────────────────────────────────────────────────────────────
total_sembrada   = df_filtrado['Área sembrada (ha)'].sum()   if 'Área sembrada (ha)'   in df_filtrado.columns else 0
total_cosechada  = df_filtrado['Área cosechada (ha)'].sum()  if 'Área cosechada (ha)'  in df_filtrado.columns else 0
total_produccion = df_filtrado['Producción (t)'].sum()       if 'Producción (t)'       in df_filtrado.columns else 0
rendimiento_prom = df_filtrado['Rendimiento (t/ha)'].mean()  if 'Rendimiento (t/ha)'  in df_filtrado.columns else None
registros        = len(df_filtrado)

def fmt(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return f"{n:,.0f}"

cols = st.columns(4)
kpis = [
    (fmt(total_sembrada),    "ha Sembradas"),
    (fmt(total_cosechada),   "ha Cosechadas"),
    (fmt(total_produccion),  "Toneladas Prod."),
    (f"{rendimiento_prom:.1f} t/ha" if rendimiento_prom else "—", "Rendimiento Prom."),
]
for col, (val, label) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{val}</div>
            <div class='kpi-label'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ─── Annual summary ─────────────────────────────────────────────────────────────
if 'Año' in df_filtrado.columns:
    resumen_anual = df_filtrado.groupby('Año')[
        [c for c in METRIC_COLS if c in df_filtrado.columns]
    ].sum().reset_index()

    # ── Charts row ──────────────────────────────────────────────────────────────
    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.markdown('<div class="section-label">📈 Producción por año</div>', unsafe_allow_html=True)
        if 'Producción (t)' in resumen_anual.columns:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=resumen_anual['Año'],
                y=resumen_anual['Producción (t)'],
                marker_color=ACCENT,
                marker_line_width=0,
                name="Producción (t)",
                hovertemplate="<b>%{x}</b><br>%{y:,.0f} t<extra></extra>",
            ))
            if 'Rendimiento (t/ha)' in df_filtrado.columns:
                rend_anual = df_filtrado.groupby('Año')['Rendimiento (t/ha)'].mean().reset_index()
                fig.add_trace(go.Scatter(
                    x=rend_anual['Año'],
                    y=rend_anual['Rendimiento (t/ha)'],
                    mode='lines+markers',
                    name='Rendimiento (t/ha)',
                    yaxis='y2',
                    line=dict(color='#e8f5c0', width=2),
                    marker=dict(size=6),
                    hovertemplate="<b>%{x}</b><br>%{y:.2f} t/ha<extra></extra>",
                ))
                fig.update_layout(
                    yaxis2=dict(
                        overlaying='y', side='right',
                        showgrid=False,
                        title='Rendimiento (t/ha)',
                        title_font_color=FONT_COLOR,
                    )
                )
            fig.update_layout(
                xaxis_title="Año",
                yaxis_title="Producción (t)",
                barmode='group',
                showlegend=True,
            )
            apply_chart_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-label">🌾 Área: Sembrada vs Cosechada</div>', unsafe_allow_html=True)
        area_cols = [c for c in ['Área sembrada (ha)', 'Área cosechada (ha)'] if c in resumen_anual.columns]
        if area_cols:
            fig2 = go.Figure()
            colors_area = [ACCENT, "#4a7a3a"]
            for i, col_name in enumerate(area_cols):
                fig2.add_trace(go.Scatter(
                    x=resumen_anual['Año'],
                    y=resumen_anual[col_name],
                    mode='lines+markers',
                    name=col_name,
                    line=dict(color=colors_area[i], width=2.5),
                    marker=dict(size=7),
                    fill='tozeroy' if i == 0 else 'tonexty',
                    fillcolor=f"rgba(180,210,80,{0.15 - i*0.07})",
                    hovertemplate=f"<b>%{{x}}</b><br>%{{y:,.0f}} ha<extra>{col_name}</extra>",
                ))
            fig2.update_layout(xaxis_title="Año", yaxis_title="Área (ha)", showlegend=True)
            apply_chart_theme(fig2)
            st.plotly_chart(fig2, use_container_width=True)

    # ── Annual summary table ─────────────────────────────────────────────────────
    st.markdown('<div class="section-label">📋 Resumen departamental por año</div>', unsafe_allow_html=True)
    st.dataframe(
        resumen_anual.style.format({c: "{:,.0f}" for c in resumen_anual.columns if c != 'Año'}),
        use_container_width=True,
        hide_index=True,
    )

# ─── Municipal detail ────────────────────────────────────────────────────────────
if mostrar_tabla_detalle:
    st.markdown('<div class="section-label">🏘 Detalle a nivel municipal</div>', unsafe_allow_html=True)
    cols_presentes = [c for c in DETAIL_COLS if c in df_filtrado.columns]
    fmt_dict = {c: "{:,.0f}" for c in cols_presentes if c not in ['Año', 'Municipio', 'Cultivo', 'Rendimiento (t/ha)']}
    if 'Rendimiento (t/ha)' in cols_presentes:
        fmt_dict['Rendimiento (t/ha)'] = "{:.2f}"
    st.dataframe(
        df_filtrado[cols_presentes].sort_values(['Año', 'Municipio']).style.format(fmt_dict),
        use_container_width=True,
        hide_index=True,
        height=400,
    )

    # Download button
    csv = df_filtrado[cols_presentes].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇ Descargar datos filtrados (.csv)",
        data=csv,
        file_name=f"agrosentinel_{depto_sel}_{cultivo_sel}.csv",
        mime="text/csv",
    )

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:3rem 0 1rem; color:#2f5426; font-size:0.75rem; letter-spacing:0.1em;'>
    AGROSENTINEL · DESEMPEÑO AGRÍCOLA COLOMBIA 2019–2024
</div>
""", unsafe_allow_html=True)
