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

# Función para cargar datos
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_csv = os.path.join(base_path, "output", "Clientes_Segmentados.csv")
    
    if not os.path.exists(ruta_csv):
        ruta_csv = os.path.join(base_path, "Clientes_Segmentados.csv")
        
    if not os.path.exists(ruta_csv):
        return None
        
    df = pd.read_csv(ruta_csv)
    return df

df = load_data()

st.title("📊 Tablero de Control - Studio F")

if df is not None:
    # Sidebar
    st.sidebar.header("Filtros")
    cluster_filter = st.sidebar.multiselect(
        "Seleccionar Cluster:",
        options=sorted(df["Cluster"].unique()),
        default=sorted(df["Cluster"].unique())
    )
    
    df_filtered = df[df["Cluster"].isin(cluster_filter)]
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    total_clientes = len(df_filtered)
    avg_monetary = df_filtered["Monetary"].mean()
    riesgo_fuga = len(df_filtered[df_filtered["Recency"] > 120])
    pct_riesgo = (riesgo_fuga / total_clientes * 100) if total_clientes > 0 else 0
    
    col1.metric("Clientes Totales", f"{total_clientes:,}")
    col2.metric("Venta Promedio", f"${avg_monetary:,.0f}")
    col3.metric("Clientes en Riesgo (>120d)", f"{riesgo_fuga:,}")
    col4.metric("Tasa de Riesgo", f"{pct_riesgo:.1f}%")
    
    st.markdown("---")
    
    # Gráficos Row 1
    c1, c2 = st.columns((2, 1))
    
    with c1:
        st.subheader("Mapa RFM (Recencia vs Valor)")
        df_viz = df_filtered[df_filtered["Monetary"] < df_filtered["Monetary"].quantile(0.999)]
        fig_scatter = px.scatter(
            df_viz, x="Recency", y="Monetary", color="Cluster",
            hover_data=["FkCliente", "Frequency", "Tipo"],
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with c2:
        st.subheader("Distribución")
        cluster_counts = df_filtered["Cluster"].value_counts().reset_index()
        cluster_counts.columns = ["Cluster", "Cantidad"]
        fig_bar = px.bar(cluster_counts, x="Cluster", y="Cantidad", color="Cluster", text="Cantidad")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    # Gráficos Row 2 - Canales
    st.subheader("Preferencia de Canal")
    channel_cols = [c for c in df.columns if "Share_Channel_" in c]
    if channel_cols:
        channel_data = df_filtered.groupby("Cluster")[channel_cols].mean().reset_index()
        channel_data.columns = [c.replace("Share_Channel_", "") for c in channel_data.columns]
        df_melt = channel_data.melt(id_vars="Cluster", var_name="Canal", value_name="Proporcion")
        
        fig_channels = px.bar(
            df_melt, x="Cluster", y="Proporcion", color="Canal", 
            barmode="stack"
        )
        st.plotly_chart(fig_channels, use_container_width=True)

    # Tabla
    st.markdown("---")
    st.subheader("Detalle de Clientes")
    st.dataframe(df_filtered)
    
else:
    st.error("No se encontraron datos.")
