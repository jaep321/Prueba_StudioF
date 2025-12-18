# Prueba T?cnica - Analista de Datos BI

Este repositorio contiene la **Soluci?n Completa** a la prueba t?cnica para el cargo de Analista de Datos BI.
A continuaci?n se presenta la respuesta detallada a cada uno de los puntos solicitados en el documento `Prueba_tecnica_clientes.docx`.

## Tablero HTML (opcional)

[![Tablero HTML](images/Tablero_control.png)](https://jaep321.github.io/Prueba_StudioF/)

## ?? Estructura de la Soluci?n

1.  [Entendimiento de la Informaci?n](#1-entendimiento-de-la-informaci?n)
2.  [Identificaci?n de Variables](#2-identificaci?n-de-variables-para-el-modelo-de-segmentaci?n)
3.  [Segmentaci?n de Clientes (K-Means)](#3-segmentaci?n-con-metodolog?a-estad?stica)
4.  [Se?ales de Fuga](#4-generaci?n-de-se?ales-de-fuga-de-clientes)
5.  [Tablero de Control](#5-tablero-de-control-html--power-bi)

---

## 1. Entendimiento de la Informaci?n

**Objetivo:** Descripci?n detallada de las variables insumo (`BD_Clientes` y `BD_Transaccional`).

### BD_Clientes (Maestra de Clientes)

| Variable | Tipo de Dato | Descripci?n | Transformaci?n Sugerida |
|----------|--------------|-------------|-------------------------|
| `FkCliente` | Num?rico (Entero) | Identificador ?nico del cliente. | Ninguna (Llave primaria). |
| `Tipo` | Texto | Tipo de cliente (ej. Cliente Compartido). | Estandarizaci?n si hay variantes. |
| `CodTipoIdentificacion` | Num?rico | C?digo del tipo de documento. | - |
| `TipoIdentificacion` | Texto | Descripci?n del tipo de documento (CC, CE). | - |
| `CodGenero` | Num?rico | C?digo del g?nero. | - |
| `Genero` | Texto | G?nero del cliente (F, M, N). | Normalizaci?n: CodGenero 0 corresponde a vac?os. Clasificar como 'No Informado'. |
| `Fecha_Nacimiento` | Fecha | Fecha de nacimiento. | C?lculo de `Edad`. Validar fechas futuras o nulas. |
| `Fecha_Ingreso` | Fecha | Fecha de registro del cliente. | C?lculo de `Antig?edad`. |
| `CodMarcaFavorita` | Num?rico | C?digo de la marca favorita. | - |
| `CodMedioPagoFavorito` | Num?rico | C?digo medio de pago favorito. | Medio de pago favorito con el que pago el cliente. |
| `MedioPagoFavorito` | Texto | Descripci?n medio pago favorito. | Medio de pago favorito con el que pago el cliente. |
| `CodFranquiciaFavorita` | Num?rico | C?digo franquicia favorita. | Franquicia de la tarjeta debito/cr?dito. |
| `FranquiciaFavorita` | Texto | Descripci?n franquicia favorita. | Franquicia de la tarjeta debito/cr?dito. |
| `Fecha_Actualizacion` | Fecha | ?ltima actualizaci?n de datos. | Recencia de contacto. |
| `CodMedioActualizacion` | Num?rico | C?digo del medio de actualizaci?n. | - |
| `MedioActualizacion` | Texto | Descripci?n del medio de actualizaci?n. | - |
| `CodEstado` | Num?rico | C?digo del estado. | - |
| `Estado` | Texto | Estado del cliente (Activo/Inactivo). | Filtro para campa?as (Solo Activos). |
| `CIIU_Actividad_economica` | Num?rico | Actividad econ?mica (f200_id_ciiu). | Clasificaci?n sectorial. |

**Campos esperados seg?n el documento (validar existencia en la base):**

| Variable | Tipo de Dato | Descripci?n | Transformaci?n Sugerida |
|----------|--------------|-------------|-------------------------|
| `CodDepartamento` | Num?rico | C?digo del departamento del cliente. | Cruce geogr?fico. |
| `Departamento` | Texto | Nombre del departamento. | Limpieza de nombres. |
| `CodCiudad` | Num?rico | C?digo de la ciudad del cliente. | Cruce geogr?fico. |
| `Ciudad` | Texto | Nombre de la ciudad. | Limpieza de nombres. |
| `Zona` | Texto | Zona geogr?fica comercial. | An?lisis de cobertura. |
| `NkTienda` | Num?rico | Tienda preferida/frecuente. | Identificaci?n de tienda ancla. |

### BD_Transaccional (Hist?rico Transaccional)

| Variable | Tipo de Dato | Descripci?n | Transformaci?n Sugerida |
|----------|--------------|-------------|-------------------------|
| `FkCliente` | Num?rico | Llave for?nea del cliente. | Cruce con BD_Clientes. |
| `FechaCalendario` | Fecha | Fecha de la transacci?n. | Extracci?n de A?o, Mes, D?aSemana. C?lculo de `Recencia`. |
| `FkTiempo` | Num?rico | Llave de tiempo (YYYYMMDD). | Redundante con FechaCalendario. |
| `FkProducto` | Num?rico | Identificador del producto. | - |
| `FkMarca` | Num?rico | Identificador de la marca. | - |
| `FkTipoEstablecimiento` | Num?rico | Identificador del tipo de establecimiento. | - |
| `FkCategoria` | Num?rico | Identificador de la categor?a. | - |
| `NumDocumento` | Texto | Identificador de la factura/ticket. | Conteo para `Frecuencia`. |
| `Cantidad` | Num?rico | Unidades compradas. | Suma total de items. |
| `VentaSinIVA` | Num?rico | Monto de la venta (sin impuesto). | Suma para `Monto`. Manejo de devoluciones. |
| `CodDepartamento` | Num?rico | C?digo del departamento. | - |
| `Departamento` | Texto | Nombre del departamento geogr?fico. | An?lisis geogr?fico. |
| `CodCiudad` | Num?rico | C?digo de la ciudad. | - |
| `Ciudad` | Texto | Nombre de la ciudad. | - |
| `Zona` | Texto | Zona geogr?fica comercial. | - |
| `NkTienda` | Num?rico | Identificador de la tienda. | - |
| `Tipo` | Texto | Tipo de tienda/marca (ej. Ela). | - |
| `FechaAperturaTienda` | Fecha | Fecha de apertura de la tienda. | (Variable listada en requerimientos pero no hallada en dataset). |
| `TipoEstablecimiento` | Texto | Canal de venta (Tienda, Ecomm, Bodega). | Preferencia de Canal. |
| `NkFamilia` | Num?rico | Identificador de familia de producto. | - |
| `NkLinea` | Num?rico | Identificador de l?nea de producto. | - |
| `Familia` | Texto | Familia de producto (ej. Superiores). | - |
| `Linea` | Texto | L?nea de producto (ej. Blusa, Jean). | C?lculo de Preferencias (% de gasto por l?nea). |
| `TipoProduccion` | Texto | Origen (Producido/No Producido). | - |
| `DescripcionMarca` | Texto | Descripci?n de la marca. | Preferencia de Marca. |

---

## 2. Identificaci?n de Variables para el Modelo de Segmentaci?n

Para el modelo de segmentaci?n y riesgo (fuga), se construyeron las siguientes variables clave:

1.  **Recencia (Recency):** D?as desde la ?ltima compra. (Clave para Fuga).
2.  **Frecuencia (Frequency):** N?mero de facturas ?nicas.
3.  **Monto (Monetary):** Total vendido sin IVA.
4.  **Preferencia de Canal:** % de compras en Tienda vs Bodega vs Virtual.
5.  **Preferencia de L?nea (Top 10 + Otras):** % de gasto por l?neas con mayor venta.
6.  **Preferencia de Familia:** % de gasto por familia (Superiores, Inferiores, Monopieza, etc.).
7.  **Preferencia de Marca:** % de gasto por `DescripcionMarca`.

**Factores expl?citos solicitados (productos y canales):**
*   **Producto/Servicio:** participaci?n del gasto por `Familia`, `Linea` (Top 10 + Otras) y `DescripcionMarca`.
*   **Canal de distribuci?n:** `TipoEstablecimiento` y `Tipo`.

**Variables adicionales de enriquecimiento (si existen en la fuente):**
*   **Geograf?a:** `Ciudad`, `Departamento`, `Zona`.
*   **Tienda ancla:** `NkTienda`.

**Nota sobre Lavado de Activos:**
Se incluyen variables de *Monto Total* y *Frecuencia* excesiva. Se detect? un cliente con monto an?malo (?$445 Millones) que se marca como alerta prioritaria.

---

## 3. Segmentaci?n con Metodolog?a Estad?stica

### Justificaci?n Metodol?gica
Para este an?lisis se seleccion? el **Aprendizaje No Supervisado (Clustering)**, espec?ficamente el algoritmo **K-Means**, basado en el modelo **RFM (Recencia, Frecuencia, Valor Monetario)**.

**?Por qu? se escogi? este m?todo?**

1.  **Naturaleza de los Datos (Sin Etiquetas):** Los datos proporcionados son puramente transaccionales y **no cuentan con una etiqueta previa** (ej. "Cliente VIP", "Cliente Riesgoso"). Por lo tanto, los modelos predictivos supervisados (como ?rboles de decisi?n o regresi?n log?stica) no son aplicables en esta fase inicial, ya que requieren un hist?rico clasificado para entrenar.
2.  **Modelo RFM:** Es el est?ndar de la industria en retail para evaluar el valor del cliente. Permite agrupar objetivamente a los usuarios bas?ndose en hechos (lo que hicieron) en lugar de suposiciones demogr?ficas.
3.  **Objetividad del Algoritmo:** K-Means permite descubrir patrones ocultos y agrupar clientes por similitud matem?tica en su comportamiento de compra, eliminando el sesgo humano en la clasificaci?n.

### Resultados del Modelo
Se utiliz? **K-Means Clustering** sobre las variables normalizadas (**RFM + producto + canal**). Se hallaron **4 segmentos** con los siguientes perfiles:

*   **Cluster 1: Compradores Base (57.5% de la poblaci?n)**
    *   **Caracter?sticas:** Recencia promedio 64 d?as. Frecuencia 3.34. Gasto promedio $616k.
    *   **Canal:** Tienda f?sica ~97%, virtual ~3%.
    *   **Preferencia:** L?neas Blusa (34%) y Jean (24%). Familias Superiores (51%) e Inferiores (37%).
    *   **Acci?n:** Programa de fidelizaci?n est?ndar y combos Blusa + Jean.

*   **Cluster 0: Complementos/Calzado/Tercera Pieza (34.8% de la poblaci?n)**
    *   **Caracter?sticas:** Recencia 69 d?as. Frecuencia 3.18. Gasto promedio $558k.
    *   **Canal:** Tienda f?sica ~95%, virtual ~5%.
    *   **Preferencia:** L?nea Otras (68%), Tenis (7%), Chaqueta (7%). Familias Tercera Pieza (23%), Calzado (19%), Complementos (18%).
    *   **Acci?n:** Campa?as de complementos y calzado con bundles.

*   **Cluster 3: Monopieza/Vestidos (7.6% de la poblaci?n)**
    *   **Caracter?sticas:** Recencia 69 d?as. Frecuencia 2.11. Gasto promedio $372k.
    *   **Canal:** Tienda f?sica ~96%, virtual ~4%.
    *   **Preferencia:** L?nea Vestido (51%) y Enterizo (21%). Familia Monopieza (75%).
    *   **Acci?n:** Promociones de temporada (vestidos/enterizos) y cross-selling de accesorios.

*   **Cluster 2: Outlier / VIP / Alerta (1 Cliente)**
    *   **Caracter?sticas:** Gasto ?$445 Millones. 2149 transacciones en un a?o. Recencia 0.
    *   **Acci?n:** **AUDITOR?A INMEDIATA**. Puede ser cliente corporativo, error de sistema o caso potencial de lavado de activos por volumen inusual.

### Resultados Visuales
![Scatter Plot](images/scatter_rfm.png)
*Gr?fico: Recencia vs Valor Monetario. Se observa la dispersi?n de los segmentos.*

![Distribuci?n](images/cluster_distribution.png)
*Gr?fico: Distribuci?n de clientes por cluster.*

---

## 4. Generaci?n de Se?ales de Fuga de Clientes

Basado en el an?lisis de Recencia del Cluster principal:
*   Promedio de inactividad: 66 d?as.
*   Desviaci?n est?ndar: 60 d?as.

**Regla de Alerta de Fuga:**
Se define un cliente en riesgo de fuga si su inactividad supera los **120 d?as** (aprox. 4 meses, o Promedio + 1 Desviaci?n Est?ndar).

**Estrategia:**
1.  **Se?al Amarilla (60-90 d?as):** Email de "Te extra?amos" con novedades.
2.  **Se?al Roja (>90-120 d?as):** Oferta agresiva de reactivaci?n (Descuento temporal).
3.  **Fuga Confirmada (>180 d?as):** Pasar a base de recuperaci?n (Win-back).

**Alineaci?n con el tablero:** el KPI de riesgo usa el umbral **>120 d?as** y el sem?foro lista alertas tempranas **>90 d?as**.

---

## 5. Tablero de Control HTML + Power BI

Se gener? un **prototipo HTML** en Python (Plotly) y se dejaron los datasets listos para construir el tablero en Power BI.

**Funcionalidades:**
*   Filtros din?micos por Cluster.
*   C?lculo de KPIs en tiempo real (Ventas, Riesgo).
*   Gr?ficos interactivos (Zoom, Hover) con Plotly.

### P?ginas sugeridas (Power BI)
*   **P?gina 1:** KPIs + tendencia mensual + mapa de ventas por ciudad.
*   **P?gina 2:** Dispersi?n Recencia vs Monto + distribuci?n por cluster + tabla detalle.
*   **P?gina 3:** Sem?foro de fuga + alerta VIP/lavado.

### ??? Generar y abrir el tablero
```bash
python src/generate_static_dashboard.py
```
Luego abrir `docs/index.html`.

**Datasets para tablero:**
*   `output/Clientes_Segmentados.csv`: base consolidada con RFM y cluster.
*   `output/Ventas_Mensuales.csv`: tendencia mensual.
*   `output/Ventas_Zona.csv`: ventas por ciudad/zona.
*   `output/Ventas_Linea.csv`: ventas por linea (Top 10).
*   `docs/index.html`: prototipo HTML.

---

## ?? Ejecuci?n del C?digo

El an?lisis fue realizado en Python. Para replicar:

1.  Instalar dependencias: `pip install -r requirements.txt`
2.  Ejecutar segmentaci?n: `python src/03_segmentation.py`
3.  Generar tablero HTML: `python src/generate_static_dashboard.py`

**Archivos Generados:**
- `output/Clientes_Segmentados.csv`: Base final con la columna `Cluster` asignada.
- `output/Ventas_Mensuales.csv`: Ventas por mes.
- `output/Ventas_Zona.csv`: Ventas por ciudad.
- `output/Ventas_Linea.csv`: Ventas por linea (Top 10).
- `docs/index.html`: Tablero HTML.
