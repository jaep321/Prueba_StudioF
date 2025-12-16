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

    # --- KPIs GLOBALES ---
    total_clientes = len(df)
    avg_monetary = df["Monetary"].mean()
    riesgo = len(df[df["Recency"] > 120])
    pct_riesgo = (riesgo / total_clientes * 100)

    # --- Generación de Gráficos (HTML Divs) ---
    
    # TAB 1: OVERVIEW (Trend + Map)
    if not df_trend.empty:
        fig_trend = px.line(df_trend, x='Mes', y='Ventas', title="Evolución Mensual 2023", markers=True)
        div_trend = pio.to_html(fig_trend, full_html=False, include_plotlyjs='cdn')
    else: div_trend = "No data"
    
    if not df_zone.empty:
        top_cities = df_zone.sort_values('VentaSinIVA', ascending=False).head(10)
        fig_map = px.bar(top_cities, x='VentaSinIVA', y='Ciudad', orientation='h', title="Top 10 Ciudades (Ventas)")
        div_map = pio.to_html(fig_map, full_html=False, include_plotlyjs=False)
    else: div_map = "No data"

    # TAB 2: SEGMENTATION (Scatter + Donut + Table)
    df_viz = df[df['Monetary'] < df['Monetary'].quantile(0.999)].copy()
    fig_scatter = px.scatter(df_viz, x="Recency", y="Monetary", color="Cluster", hover_data=["FkCliente"], title="Gráfico de Dispersión (Recencia vs Monto)", height=500)
    div_scatter = pio.to_html(fig_scatter, full_html=False, include_plotlyjs=False)
    
    cnt = df["Cluster"].value_counts().reset_index()
    cnt.columns = ["Cluster", "Cnt"]
    fig_donut = px.pie(cnt, names="Cluster", values="Cnt", hole=0.4, title="Distribución por Cluster")
    fig_donut.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    div_donut = pio.to_html(fig_donut, full_html=False, include_plotlyjs=False)
    
    # Table (General)
    # Fix: Ensure columns are clean
    table_head = df.head(50)[['FkCliente', 'Cluster', 'Recency', 'Monetary']].to_html(classes="table table-sm table-striped table-hover", index=False)
    
    # TAB 3: ALERTS (Risk Tables)
    # Semáforo Fuga (>90 days)
    risk_df = df[df['Recency'] > 90].sort_values('Recency', ascending=False).head(20)
    risk_html = risk_df[['FkCliente', 'Recency', 'Monetary', 'Cluster']].to_html(classes="table table-danger table-striped", index=False)
    
    # Alerta Lavado (>50M)
    vip_df = df[df['Monetary'] > 50000000].head(20)
    vip_html = vip_df[['FkCliente', 'Monetary', 'Frequency', 'Cluster']].to_html(classes="table table-warning table-hover", index=False) if not vip_df.empty else "<p>Sin alertas de lavado</p>"

    # --- HTML Template ---
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
            .kpi-card {{ text-align: center; padding: 15px; background: white; border-radius: 8px; border-left: 5px solid #3498db; }}
            .kpi-value {{ font-size: 1.8em; font-weight: bold; color: #2c3e50; }}
            .kpi-label {{ color: #7f8c8d; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="mb-4 text-center">📊 Tablero de Control - Studio F</h1>
            
            <!-- KPIs GLOBALES -->
            <div class="row mb-4">
                <div class="col-md-3"><div class="kpi-card"><div class="kpi-value">{total_clientes:,}</div><div class="kpi-label">Clientes Totales</div></div></div>
                <div class="col-md-3"><div class="kpi-card"><div class="kpi-value">${avg_monetary:,.0f}</div><div class="kpi-label">Venta Promedio</div></div></div>
                <div class="col-md-3"><div class="kpi-card" style="border-color: #e74c3c"><div class="kpi-value">{riesgo:,}</div><div class="kpi-label">Clientes en Riesgo (>120d)</div></div></div>
                <div class="col-md-3"><div class="kpi-card" style="border-color: #e74c3c"><div class="kpi-value">{pct_riesgo:.1f}%</div><div class="kpi-label">Tasa de Fuga</div></div></div>
            </div>
            
            <!-- TABS -->
            <ul class="nav nav-tabs" id="myTab" role="tablist">
                <li class="nav-item"><button class="nav-link active" id="tab1-tab" data-bs-toggle="tab" data-bs-target="#tab1" type="button">1. Visión General</button></li>
                <li class="nav-item"><button class="nav-link" id="tab2-tab" data-bs-toggle="tab" data-bs-target="#tab2" type="button">2. Segmentación</button></li>
                <li class="nav-item"><button class="nav-link" id="tab3-tab" data-bs-toggle="tab" data-bs-target="#tab3" type="button">3. Alertas y Riesgo</button></li>
            </ul>
            
            <div class="tab-content border border-top-0 p-3 bg-white" id="myTabContent">
                
                <!-- TAB 1: OVERVIEW -->
                <div class="tab-pane fade show active" id="tab1">
                    <div class="row">
                        <div class="col-md-6"><div class="card p-2">{div_trend}</div></div>
                        <div class="col-md-6"><div class="card p-2">{div_map}</div></div>
                    </div>
                </div>
                
                <!-- TAB 2: SEGMENTATION -->
                <div class="tab-pane fade" id="tab2">
                    <div class="row">
                        <!-- Scatter más ancho -->
                        <div class="col-lg-8">
                            <div class="card p-2">
                                <h5 class="card-title text-center">Mapa de Clientes (Recencia vs Valor)</h5>
                                {div_scatter}
                            </div>
                        </div>
                        <!-- Donut más compacto -->
                        <div class="col-lg-4">
                            <div class="card p-2">
                                <h5 class="card-title text-center">Distribución</h5>
                                {div_donut}
                            </div>
                        </div>
                    </div>
                    
                    <!-- Separate Row for Table -->
                    <div class="row mt-4">
                        <div class="col-12">
                            <div class="card p-3">
                                <h5 class="card-title">Muestra de Clientes por Cluster</h5>
                                <div class="table-responsive">
                                    {table_head}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- TAB 3: ALERTS -->
                <div class="tab-pane fade" id="tab3">
                    <div class="row">
                        <div class="col-md-6">
                            <h5 class="text-danger">🚨 Semáforo de Fuga (Top 20 > 90 días)</h5>
                            {risk_html}
                        </div>
                        <div class="col-md-6">
                            <h5 class="text-warning">💰 Alerta Lavado / VIP (Top > $50M)</h5>
                            {vip_html}
                        </div>
                    </div>
                </div>
            </div>
            
            <footer class="text-center mt-4 text-muted">Generado con Python</footer>
        </div>
    </body>
    </html>
    """
    
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Dashboard generado en: {output_html}")

if __name__ == "__main__":
    generate_dashboard()
