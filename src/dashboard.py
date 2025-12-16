import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración de la página
st.set_page_config(
    page_title="Tablero de Control - Studio F",
    page_icon="📊",
    layout="wide"
)

# --- Cargar Datos ---
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Segmentados (Principal)
    path_seg = os.path.join(base_path, "output", "Clientes_Segmentados.csv")
    if not os.path.exists(path_seg): path_seg = os.path.join(base_path, "Clientes_Segmentados.csv")
    
    # 2. Ventas Mensuales (Tendencia)
    path_trend = os.path.join(base_path, "output", "Ventas_Mensuales.csv")
    if not os.path.exists(path_trend): path_trend = os.path.join(base_path, "Ventas_Mensuales.csv")

    # 3. Ventas Zona (Mapa)
    path_zone = os.path.join(base_path, "output", "Ventas_Zona.csv")
    if not os.path.exists(path_zone): path_zone = os.path.join(base_path, "Ventas_Zona.csv")
    
    df_seg = pd.read_csv(path_seg) if os.path.exists(path_seg) else None
    df_trend = pd.read_csv(path_trend) if os.path.exists(path_trend) else None
    df_zone = pd.read_csv(path_zone) if os.path.exists(path_zone) else None
    
    return df_seg, df_trend, df_zone

df, df_trend, df_zone = load_data()

st.title("📊 Tablero de Control - Studio F")

if df is not None:
    # Sidebar Global
    st.sidebar.header("Filtros Globales")
    cluster_filter = st.sidebar.multiselect(
        "Filtrar por Cluster:",
        options=sorted(df["Cluster"].unique()),
        default=sorted(df["Cluster"].unique())
    )
    
    # Filtrar DF principal
    df_filtered = df[df["Cluster"].isin(cluster_filter)]
    
    # KPIs Globales
    c1, c2, c3, c4 = st.columns(4)
    total_ventas = df_filtered["Monetary"].sum()
    ticket_prom = df_filtered["Monetary"].mean()
    activos = len(df_filtered[df_filtered["Recency"] < 120])
    tasa_fuga = (len(df_filtered[df_filtered["Recency"] >= 120]) / len(df_filtered) * 100)
    
    c1.metric("Ventas Totales (Base)", f"${total_ventas:,.0f}")
    c2.metric("Ticket Promedio", f"${ticket_prom:,.0f}")
    c3.metric("Clientes Activos (<120d)", f"{activos:,}")
    c4.metric("Tasa de Fuga", f"{tasa_fuga:.1f}%")
    
    st.markdown("---")

    # --- TABS (Páginas) ---
    tab1, tab2, tab3 = st.tabs(["1. Visión General", "2. Segmentación", "3. Alertas y Riesgo"])
    
    # --- TAB 1: VISION GENERAL ---
    with tab1:
        st.header("Visión General del Negocio")
        
        # Graficos Tendencia y Mapa
        col_trend, col_map = st.columns(2)
        
        with col_trend:
            st.subheader("Tendencia de Ventas (2023)")
            if df_trend is not None:
                fig_trend = px.line(df_trend, x='Mes', y='Ventas', markers=True, title="Evolución Mensual")
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.info("No hay datos de tendencia mensual disponibles.")
                
        with col_map:
            st.subheader("Ventas por Ciudad")
            if df_zone is not None:
                # Top 10 ciudades
                top_cities = df_zone.sort_values('VentaSinIVA', ascending=False).head(10)
                fig_map = px.bar(top_cities, x='VentaSinIVA', y='Ciudad', orientation='h', title="Top 10 Ciudades")
                st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.info("No hay datos geográficos disponibles.")

    # --- TAB 2: SEGMENTACION ---
    with tab2:
        st.header("Análisis de Segmentación de Clientes")
        
        c1, c2 = st.columns((2, 1))
        
        with c1:
            st.subheader("Mapa de Calor (Recencia vs Valor)")
            # Outlier filter visual
            df_viz = df_filtered[df_filtered["Monetary"] < 20000000] 
            fig_scatter = px.scatter(
                df_viz, x="Recency", y="Monetary", color="Cluster",
                hover_data=["FkCliente", "Tipo"], color_continuous_scale="Viridis",
                title="Distribución de Clientes"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with c2:
            st.subheader("Distribución")
            cluster_counts = df_filtered["Cluster"].value_counts().reset_index()
            cluster_counts.columns = ["Cluster", "Cantidad"]
            fig_donut = px.pie(cluster_counts, names="Cluster", values="Cantidad", hole=0.4)
            st.plotly_chart(fig_donut, use_container_width=True)
            
        st.subheader("Detalle de Clientes")
        st.dataframe(df_filtered[["FkCliente", "Cluster", "Recency", "Frequency", "Monetary", "Tipo"]].head(100))

    # --- TAB 3: ALERTAS ---
    with tab3:
        st.header("Alertas y Gestión de Riesgo")
        
        col_risk, col_high = st.columns(2)
        
        with col_risk:
            st.subheader("🚨 Semáforo de Fuga (Inactivos > 90 días)")
            riesgo_df = df_filtered[df_filtered["Recency"] > 90].sort_values("Recency", ascending=False)
            st.warning(f"{len(riesgo_df)} Clientes en zona de peligro.")
            st.dataframe(riesgo_df[["FkCliente", "Recency", "Monetary", "Cluster"]])
            
        with col_high:
            st.subheader("💰 Alerta VIP / Lavado (> $50M)")
            vip_risk = df_filtered[df_filtered["Monetary"] > 50000000]
            if not vip_risk.empty:
                st.error(f"¡ATENCIÓN! {len(vip_risk)} Clientes con montos atípicos detectados.")
                st.dataframe(vip_risk)
            else:
                st.success("No se detectaron transacciones atípicas mayores a $50M en este filtro.")

else:
    st.error("No se encontraron los archivos de datos. Ejecute primero el script de segmentación.")
