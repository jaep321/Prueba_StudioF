import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

def generate_dashboard():
    base_path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    csv_path = os.path.join(base_path, "output", "Clientes_Segmentados.csv")
    output_html = os.path.join(base_path, "docs", "index.html")
    
    # Create docs folder if not exists
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    
    print("Cargando datos...")
    if not os.path.exists(csv_path):
        print("Error: No se encontró Clientes_Segmentados.csv")
        return

    df = pd.read_csv(csv_path)

    # --- Generación de Gráficos ---
    
    # 1. Scatter RFM
    df_viz = df[df['Monetary'] < df['Monetary'].quantile(0.999)].copy() # Sin outliers extremos
    fig_scatter = px.scatter(
        df_viz, 
        x="Recency", 
        y="Monetary", 
        color="Cluster",
        hover_data=["FkCliente", "Frequency", "Tipo"],
        title="Mapa de Clientes (Recencia vs Valor)",
        color_continuous_scale="Viridis",
        height=500
    )
    # Exportar a div
    div_scatter = pio.to_html(fig_scatter, full_html=False, include_plotlyjs='cdn')

    # 2. Distribución Clusters
    cluster_counts = df["Cluster"].value_counts().reset_index()
    cluster_counts.columns = ["Cluster", "Cantidad"]
    fig_bar = px.bar(
        cluster_counts, 
        x="Cluster", 
        y="Cantidad", 
        color="Cluster", 
        text="Cantidad",
        title="Conteo de Clientes por Segmento",
        height=400
    )
    div_bar = pio.to_html(fig_bar, full_html=False, include_plotlyjs=False)

    # 3. Canales
    channel_cols = [c for c in df.columns if "Share_Channel_" in c]
    if channel_cols:
        channel_data = df.groupby("Cluster")[channel_cols].mean().reset_index()
        channel_data.columns = [c.replace("Share_Channel_", "") for c in channel_data.columns]
        df_melt = channel_data.melt(id_vars="Cluster", var_name="Canal", value_name="Proporcion")
        
        fig_channels = px.bar(
            df_melt, 
            x="Cluster", 
            y="Proporcion", 
            color="Canal", 
            title="Preferencia de Canal",
            barmode="stack",
            height=400
        )
        div_channels = pio.to_html(fig_channels, full_html=False, include_plotlyjs=False)
    else:
        div_channels = "<p>No hay datos de canales</p>"

    # --- KPIs ---
    total_clientes = len(df)
    avg_monetary = df["Monetary"].mean()
    riesgo = len(df[df["Recency"] > 120])
    pct_riesgo = (riesgo / total_clientes * 100)

    # --- HTML Template ---
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard Studio F</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f8f9fa; }}
            .card {{ margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .kpi-card {{ text-align: center; padding: 20px; background: white; border-radius: 8px; }}
            .kpi-value {{ font-size: 2em; font-weight: bold; color: #2c3e50; }}
            .kpi-label {{ color: #7f8c8d; }}
        </style>
    </head>
    <body>
        <div class="container py-4">
            <h1 class="mb-4 text-center">📊 Tablero de Control - Segmentación de Clientes</h1>
            <p class="text-center text-muted">Generado automáticamente con Python + Plotly</p>
            
            <!-- KPIs -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="kpi-card">
                        <div class="kpi-value">{total_clientes:,}</div>
                        <div class="kpi-label">Clientes Totales</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="kpi-card">
                        <div class="kpi-value">${avg_monetary:,.0f}</div>
                        <div class="kpi-label">Venta Promedio</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="kpi-card">
                        <div class="kpi-value">{riesgo:,}</div>
                        <div class="kpi-label">Clientes enRIESGO (>120 días)</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="kpi-card">
                        <div class="kpi-value">{pct_riesgo:.1f}%</div>
                        <div class="kpi-label">Tasa de Riesgo</div>
                    </div>
                </div>
            </div>

            <!-- Row 1: Scatter -->
            <div class="row">
                <div class="col-12">
                    <div class="card p-3">
                        {div_scatter}
                    </div>
                </div>
            </div>

            <!-- Row 2: Bars -->
            <div class="row">
                <div class="col-md-6">
                    <div class="card p-3">
                        {div_bar}
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card p-3">
                        {div_channels}
                    </div>
                </div>
            </div>
            
            <footer class="text-center mt-4">
                <p>Prueba Técnica - Jorge | Generado el {pd.Timestamp.now().strftime('%Y-%m-%d')}</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Dashboard estático generado en: {output_html}")

if __name__ == "__main__":
    generate_dashboard()
