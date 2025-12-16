import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------------
# Configuración de la página
# -------------------------
st.set_page_config(
    page_title="Tablero de Control - Studio F",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# CSS: evita desbordes y mejora tablas/plotly en tabs
# -------------------------
st.markdown(
    """
    <style>
      /* Evita que elementos dentro de tabs/columns se salgan */
      .block-container { padding-top: 1.2rem; }
      div[data-testid="stHorizontalBlock"] { overflow: hidden; }
      div[data-testid="stVerticalBlock"] { overflow: hidden; }

      /* Asegura que Plotly use el ancho disponible */
      .js-plotly-plot, .plot-container { width: 100% !important; }

      /* Dataframe: reduce problemas visuales de encabezados */
      div[data-testid="stDataFrame"] { width: 100% !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Cargar Datos ---
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    path_seg = os.path.join(base_path, "output", "Clientes_Segmentados.csv")
    if not os.path.exists(path_seg):
        path_seg = os.path.join(base_path, "Clientes_Segmentados.csv")

    path_trend = os.path.join(base_path, "output", "Ventas_Mensuales.csv")
    if not os.path.exists(path_trend):
        path_trend = os.path.join(base_path, "Ventas_Mensuales.csv")

    path_zone = os.path.join(base_path, "output", "Ventas_Zona.csv")
    if not os.path.exists(path_zone):
        path_zone = os.path.join(base_path, "Ventas_Zona.csv")

    path_linea = os.path.join(base_path, "output", "Ventas_Linea.csv")
    if not os.path.exists(path_linea):
        path_linea = os.path.join(base_path, "Ventas_Linea.csv")

    df_seg = pd.read_csv(path_seg) if os.path.exists(path_seg) else None
    df_trend = pd.read_csv(path_trend) if os.path.exists(path_trend) else None
    df_zone = pd.read_csv(path_zone) if os.path.exists(path_zone) else None
    df_linea = pd.read_csv(path_linea) if os.path.exists(path_linea) else None

    return df_seg, df_trend, df_zone, df_linea

df, df_trend, df_zone, df_linea = load_data()

st.title("📊 Tablero de Control - Studio F")

if df is None:
    st.error("No se encontraron los archivos de datos. Ejecute primero el script de segmentación.")
    st.stop()

# -------------------------
# Sidebar Global
# -------------------------
st.sidebar.header("Filtros Globales")

# Asegura tipos consistentes
df["Cluster"] = df["Cluster"].astype(str)  # MUY importante para colores discretos
# Si tienes NaN, límpialos
df = df.dropna(subset=["Cluster", "Recency", "Monetary"], how="any")

cluster_filter = st.sidebar.multiselect(
    "Filtrar por Cluster:",
    options=sorted(df["Cluster"].unique()),
    default=sorted(df["Cluster"].unique())
)

df_filtered = df[df["Cluster"].isin(cluster_filter)].copy()

# -------------------------
# KPIs
# -------------------------
c1, c2, c3, c4 = st.columns(4)

total_ventas = float(df_filtered["Monetary"].sum()) if len(df_filtered) else 0.0
ticket_prom = float(df_filtered["Monetary"].mean()) if len(df_filtered) else 0.0
activos = int((df_filtered["Recency"] < 120).sum()) if len(df_filtered) else 0
tasa_fuga = float((df_filtered["Recency"] >= 120).mean() * 100) if len(df_filtered) else 0.0

c1.metric("Ventas Totales (Base)", f"${total_ventas:,.0f}")
c2.metric("Ticket Promedio", f"${ticket_prom:,.0f}")
c3.metric("Clientes Activos (<120d)", f"{activos:,}")
c4.metric("Tasa de Fuga", f"{tasa_fuga:.1f}%")

st.markdown("---")

# -------------------------
# Tabs
# -------------------------
tab1, tab2, tab3 = st.tabs(["1. Visión General", "2. Segmentación de Clientes", "3. Alertas y Riesgo"])

# --- TAB 1 ---
with tab1:
    st.header("Visión General")

    st.subheader("Tendencia de Ventas (2023)")
    if df_trend is not None:
        fig_trend = px.line(df_trend, x="Mes", y="Ventas", markers=True, title="Evolución Mensual")
        fig_trend.update_layout(autosize=True, height=420, margin=dict(l=10, r=10, t=60, b=10))
        st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    c_map, c_cat = st.columns(2, gap="large")

    with c_map:
        st.subheader("Top Ciudades")
        if df_zone is not None:
            top_cities = df_zone.sort_values("VentaSinIVA", ascending=False).head(10)
            fig_map = px.bar(top_cities, x="VentaSinIVA", y="Ciudad", orientation="h", title="Top 10 Ciudades")
            fig_map.update_layout(autosize=True, height=420, margin=dict(l=10, r=10, t=60, b=10))
            st.plotly_chart(fig_map, use_container_width=True)

    with c_cat:
        st.subheader("Ventas por Línea")
        if df_linea is not None:
            top_linea = df_linea.head(10)
            fig_linea = px.bar(top_linea, x="Linea", y="VentaSinIVA", title="Top Categorías")
            fig_linea.update_layout(autosize=True, height=420, margin=dict(l=10, r=10, t=60, b=10))
            st.plotly_chart(fig_linea, use_container_width=True)
        else:
            st.info("No hay datos de Línea disponibles.")

# --- TAB 2 (ARREGLADO) ---
with tab2:
    st.header("Segmentación de Clientes")

    # Contenedor para fijar el ancho y evitar “saltos” dentro del tab
    with st.container():
        left, right = st.columns([2, 1], gap="large")

        with left:
            st.subheader("Gráfico de Dispersión (Recencia vs Monto)")

            # Filtra outliers para visualizar mejor
            df_viz = df_filtered[df_filtered["Monetary"] < 20_000_000].copy()

            fig_scatter = px.scatter(
                df_viz,
                x="Recency",
                y="Monetary",
                color="Cluster",            # DISCRETO (ya es string)
                hover_data=["FkCliente", "Tipo", "Frequency"],
                title="Recencia vs Monto (derecha = más riesgo)"
            )
            fig_scatter.update_layout(
                autosize=True,
                height=480,
                margin=dict(l=10, r=10, t=60, b=10),
                legend_title_text="Cluster"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        with right:
            st.subheader("Distribución por Cluster")

            cluster_counts = (
                df_filtered["Cluster"].value_counts()
                .rename_axis("Cluster")
                .reset_index(name="Cantidad")
            )

            fig_donut = px.pie(
                cluster_counts,
                names="Cluster",
                values="Cantidad",
                hole=0.45
            )
            fig_donut.update_layout(
                autosize=True,
                height=480,
                margin=dict(l=10, r=10, t=30, b=10),
                showlegend=True
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")

    st.subheader("Tabla Detalle de Clientes")
    st.caption("Filtre en el panel lateral para ver un cluster específico.")

    table_cols = ["FkCliente", "Cluster", "Recency", "Frequency", "Monetary", "Tipo"]
    df_table = df_filtered[table_cols].copy().head(200)

    # Tip: redondea Monetary para que no “reviente” el ancho
    df_table["Monetary"] = pd.to_numeric(df_table["Monetary"], errors="coerce").round(0)

    st.dataframe(
        df_table,
        use_container_width=True,
        hide_index=True,
        height=420,
        column_config={
            "FkCliente": st.column_config.NumberColumn("ID Cliente", width="small"),
            "Cluster": st.column_config.TextColumn("Cluster", width="small"),
            "Recency": st.column_config.NumberColumn("Días Ult. Compra", width="small"),
            "Frequency": st.column_config.NumberColumn("Frecuencia", width="small"),
            "Monetary": st.column_config.NumberColumn("Monto Total", format="$ %d"),
            "Tipo": st.column_config.TextColumn("Tipo", width="small"),
        },
    )

# --- TAB 3 ---
with tab3:
    st.header("Alertas y Gestión de Riesgo")

    col_risk, col_high = st.columns(2, gap="large")

    with col_risk:
        st.subheader("🚨 Semáforo de Fuga (Inactivos > 90 días)")
        riesgo_df = df_filtered[df_filtered["Recency"] > 90].sort_values("Recency", ascending=False)
        st.warning(f"{len(riesgo_df)} clientes en zona de peligro (Semáforo Rojo).")
        st.dataframe(
            riesgo_df[["FkCliente", "Recency", "Monetary", "Cluster"]],
            use_container_width=True,
            hide_index=True,
            height=380
        )

    with col_high:
        st.subheader("💰 Alerta VIP / Anomalía (> $50M)")
        vip_risk = df_filtered[df_filtered["Monetary"] > 50_000_000]
        if not vip_risk.empty:
            st.error(f"¡ATENCIÓN! {len(vip_risk)} clientes con montos atípicos (Posible Lavado/VIP).")
            st.dataframe(
                vip_risk[["FkCliente", "Monetary", "Frequency", "Cluster"]],
                use_container_width=True,
                hide_index=True,
                height=380
            )
        else:
            st.success("No se detectaron transacciones atípicas mayores a $50M con este filtro.")
