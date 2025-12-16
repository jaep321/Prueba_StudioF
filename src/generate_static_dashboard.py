import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

def generate_dashboard():
    base_path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    
    # Paths
    csv_seg = os.path.join(base_path, "output", "Clientes_Segmentados.csv")
    csv_trend = os.path.join(base_path, "output", "Ventas_Mensuales.csv")
    csv_zone = os.path.join(base_path, "output", "Ventas_Zona.csv")
    output_html = os.path.join(base_path, "docs", "index.html")
    
    print("Cargando datos...")
    if not os.path.exists(csv_seg): return
    
    df = pd.read_csv(csv_seg)
    df_trend = pd.read_csv(csv_trend) if os.path.exists(csv_trend) else pd.DataFrame()
    df_zone = pd.read_csv(csv_zone) if os.path.exists(csv_zone) else pd.DataFrame()

    # --- Generación de Gráficos (HTML Divs) ---
    
    # PAGE 1: OVERVIEW
    # Trend
    if not df_trend.empty:
        fig_trend = px.line(df_trend, x='Mes', y='Ventas', title="Evolución Mensual 2023", markers=True)
        div_trend = pio.to_html(fig_trend, full_html=False, include_plotlyjs='cdn')
    else: div_trend = "No data"
    
    # Map (Bar City)
    if not df_zone.empty:
        top_cities = df_zone.sort_values('VentaSinIVA', ascending=False).head(10)
        fig_map = px.bar(top_cities, x='VentaSinIVA', y='Ciudad', orientation='h', title="Top 10 Ciudades")
        div_map = pio.to_html(fig_map, full_html=False, include_plotlyjs=False)
    else: div_map = "No data"

    # PAGE 2: SEGMENTATION
    # Sccatter
    df_viz = df[df['Monetary'] < df['Monetary'].quantile(0.999)].copy()
    fig_scatter = px.scatter(df_viz, x="Recency", y="Monetary", color="Cluster", hover_data=["FkCliente"], title="Mapa RFM", height=500)
    div_scatter = pio.to_html(fig_scatter, full_html=False, include_plotlyjs=False)
    
    # Donut
    cnt = df["Cluster"].value_counts().reset_index()
    cnt.columns = ["Cluster", "Cnt"]
    fig_donut = px.pie(cnt, names="Cluster", values="Cnt", hole=0.4, title="Distribución")
    div_donut = pio.to_html(fig_donut, full_html=False, include_plotlyjs=False)
    
    # PAGE 3: ALERTS
    # Risk Table (Simulated with HTML)
    risk_df = df[df['Recency'] > 90].sort_values('Monetary', ascending=False).head(10)
    risk_html = risk_df[['FkCliente', 'Recency', 'Monetary', 'Cluster']].to_html(classes="table table-striped", index=False)

    # --- HTML Template with Bootstrap Tabs ---
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard Studio F</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <style>
            body {{ background-color: #f8f9fa; padding-top: 20px; }}
            .card {{ margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .nav-tabs .nav-link.active {{ background-color: #e9ecef; font-weight: bold; }}
            .tab-content {{ padding: 20px; background: white; border: 1px solid #dee2e6; border-top: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="mb-4 text-center">📊 Tablero de Control - Studio F</h1>
            
            <ul class="nav nav-tabs" id="myTab" role="tablist">
                <li class="nav-item"><button class="nav-link active" id="overview-tab" data-bs-toggle="tab" data-bs-target="#overview" type="button">1. Visión General</button></li>
                <li class="nav-item"><button class="nav-link" id="seg-tab" data-bs-toggle="tab" data-bs-target="#seg" type="button">2. Segmentación</button></li>
                <li class="nav-item"><button class="nav-link" id="risk-tab" data-bs-toggle="tab" data-bs-target="#risk" type="button">3. Alertas y Riesgo</button></li>
            </ul>
            
            <div class="tab-content" id="myTabContent">
                <!-- TAB 1 -->
                <div class="tab-pane fade show active" id="overview">
                    <div class="row">
                        <div class="col-md-6"><div class="card p-2">{div_trend}</div></div>
                        <div class="col-md-6"><div class="card p-2">{div_map}</div></div>
                    </div>
                </div>
                
                <!-- TAB 2 -->
                <div class="tab-pane fade" id="seg">
                    <div class="row">
                        <div class="col-md-8"><div class="card p-2">{div_scatter}</div></div>
                        <div class="col-md-4"><div class="card p-2">{div_donut}</div></div>
                    </div>
                </div>
                
                <!-- TAB 3 -->
                <div class="tab-pane fade" id="risk">
                    <h3 class="text-danger">Top 10 Clientes en Riesgo (>90 días)</h3>
                    {risk_html}
                </div>
            </div>
            
            <footer class="text-center mt-4 text-muted">Generado con Python</footer>
        </div>
    </body>
    </html>
    """
    
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Update: Dashboard generated at {output_html}")

if __name__ == "__main__":
    generate_dashboard()
