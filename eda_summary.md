# Analysis of BD_Clientes.xlsx
- Shape: (10000, 19)
- Columns: FkCliente, Tipo, CodTipoIdentificacion, TipoIdentificacion, CodGenero, Genero, Fecha_Nacimiento, Fecha_Ingreso, CodMarcaFavorita, CodMedioPagoFavorito, MedioPagoFavorito, CodFranquiciaFavorita, FranquiciaFavorita, Fecha_Actualizacion, CodMedioActualizacion, MedioActualizacion, CodEstado, Estado, f200_id_ciiu
- Missing Values:
  - Genero: 3526
  - Fecha_Nacimiento: 4653
  - CodMarcaFavorita: 126
  - CodMedioPagoFavorito: 156
  - MedioPagoFavorito: 156
  - CodFranquiciaFavorita: 6222
  - FranquiciaFavorita: 6222
  - CodEstado: 158
  - Estado: 158
  - f200_id_ciiu: 8782

- Sample Data:
|   FkCliente | Tipo               |   CodTipoIdentificacion | TipoIdentificacion    |   CodGenero | Genero   | Fecha_Nacimiento   | Fecha_Ingreso   |   CodMarcaFavorita |   CodMedioPagoFavorito | MedioPagoFavorito   |   CodFranquiciaFavorita |   FranquiciaFavorita | Fecha_Actualizacion   |   CodMedioActualizacion | MedioActualizacion   |   CodEstado | Estado   |   f200_id_ciiu |
|------------:|:-------------------|------------------------:|:----------------------|------------:|:---------|:-------------------|:----------------|-------------------:|-----------------------:|:--------------------|------------------------:|---------------------:|:----------------------|------------------------:|:---------------------|------------:|:---------|---------------:|
|        4609 | Cliente Compartido |                       1 | Cédula de Ciudadanía  |           3 | F        | 1999-01-03         | 2015-03-04      |                nan |                    nan | nan                 |                     nan |                  nan | 2020-02-11            |                       6 | Interfaz_Ecomm       |         nan | nan      |            nan |
|        5154 | Cliente Compartido |                       1 | Cédula de Ciudadanía  |           3 | F        | 1984-03-12         | 2014-11-26      |                  1 |                     73 | Visa Credito        |                     nan |                  nan | 2020-02-11            |                       6 | Interfaz_Ecomm       |           1 | Activo   |            nan |
|       10178 | Cliente Compartido |                       2 | Cédula de Extranjería |           3 | N        | nan                | 2017-08-16      |                  1 |                     73 | Visa Credito        |                     nan |                  nan | 2023-09-03            |                       6 | Interfaz_Ecomm       |           1 | Activo   |            nan |

- Numerical Stats:
|       |       FkCliente |   CodTipoIdentificacion |    CodGenero |   CodMarcaFavorita |   CodMedioPagoFavorito |   CodFranquiciaFavorita |   CodMedioActualizacion |   CodEstado |   f200_id_ciiu |
|:------|----------------:|------------------------:|-------------:|-------------------:|-----------------------:|------------------------:|------------------------:|------------:|---------------:|
| count | 10000           |            10000        | 10000        |        9874        |              9844      |             3778        |            10000        | 9842        |        1218    |
| mean  |     4.37469e+06 |                1.0466   |     2.956    |           1.71511  |                59.6433 |                5.23107  |                5.9037   |    0.92024  |        5711.09 |
| std   |     2.63117e+06 |                0.396036 |     0.325076 |           0.471792 |                14.0605 |                0.421576 |                0.638018 |    0.270935 |        4905.52 |
| min   |  4609           |                1        |     0        |           1        |                 2      |                5        |                1        |    0        |          10    |
| 25%   |     2.09056e+06 |                1        |     3        |           1        |                48      |                5        |                6        |    1        |          81    |
| 50%   |     3.786e+06   |                1        |     3        |           2        |                58      |                5        |                6        |    1        |        9999    |
| 75%   |     7.4084e+06  |                1        |     3        |           2        |                73      |                5        |                6        |    1        |        9999    |
| max   |     7.82754e+06 |                6        |     3        |           4        |                92      |                6        |                6        |    1        |        9999    |

==============================

# Analysis of BD_Transaccional.xlsx
- Shape: (65501, 24)
- Columns: FkCliente, FechaCalendario, FkTiempo, FkProducto, FkMarca, FkTipoEstablecimiento, FkCategoria, NumDocumento, Cantidad, VentaSinIVA, CodDepartamento, Departamento, CodCiudad, Ciudad, Zona, NkTienda, Tipo, TipoEstablecimiento, NkFamilia, NkLinea, Familia, Linea, TipoProduccion, DescripcionMarca
- No missing values.

- Sample Data:
|   FkCliente | FechaCalendario   |   FkTiempo |   FkProducto |   FkMarca |   FkTipoEstablecimiento |   FkCategoria | NumDocumento   |   Cantidad |   VentaSinIVA |   CodDepartamento | Departamento    |   CodCiudad | Ciudad   | Zona            |   NkTienda | Tipo   | TipoEstablecimiento   |   NkFamilia |   NkLinea | Familia    | Linea   | TipoProduccion   | DescripcionMarca   |
|------------:|:------------------|-----------:|-------------:|----------:|------------------------:|--------------:|:---------------|-----------:|--------------:|------------------:|:----------------|------------:|:---------|:----------------|-----------:|:-------|:----------------------|------------:|----------:|:-----------|:--------|:-----------------|:-------------------|
|       77574 | 2023-01-01        |   20230101 |      1784635 |         2 |                       2 |           255 | FV2-00081451   |          1 |         79790 |               384 | Valle Del Cauca |        8794 | Tuluá    | Norte Del Valle |        105 | Ela    | Tienda                |       2     |     28    | Inferiores | Jean    | No Producido     | Ela                |
|       77574 | 2023-01-01        |   20230101 |      1786937 |         2 |                       2 |           255 | FV2-00081451   |          1 |         50378 |               384 | Valle Del Cauca |        8794 | Tuluá    | Norte Del Valle |        105 | Ela    | Tienda                |       1     |     11    | Superiores | Blusa   | Producido        | Ela                |
|       77574 | 2023-01-01        |   20230101 |      1800915 |         2 |                       2 |           255 | FV2-00081451   |          1 |         83109 |               384 | Valle Del Cauca |        8794 | Tuluá    | Norte Del Valle |        105 | Ela    | Tienda                |       1     |     11    | Superiores | Blusa   | Producido        | Ela                |

- Numerical Stats:
|       |       FkCliente |        FkTiempo |      FkProducto |     FkMarca |   FkTipoEstablecimiento |   FkCategoria |     Cantidad |       VentaSinIVA |   CodDepartamento |   CodCiudad |   NkTienda |
|:------|----------------:|----------------:|----------------:|------------:|------------------------:|--------------:|-------------:|------------------:|------------------:|------------:|-----------:|
| count | 65501           | 65501           | 65501           | 65501       |            65501        |     65501     | 65501        |   65501           |         65501     |    65501    |  65501     |
| mean  |     3.76764e+06 |     2.02308e+07 |     1.94461e+06 |     1.72283 |                2.07858  |       180.809 |     0.935696 |   90388.1         |           321.444 |     5330.98 |    322.346 |
| std   |     2.439e+06   |   344.557       | 95157           |     1.05844 |                0.269083 |       114.822 |     0.415633 |   77000.5         |           149.251 |     2842.11 |    227.471 |
| min   |  5154           |     2.02301e+07 |     1.08676e+06 |     1       |                2        |         1     |    -3        | -503277           |            57     |     2358    |      1     |
| 25%   |     1.8441e+06  |     2.02305e+07 |     1.88969e+06 |     1       |                2        |         4     |     1        |   50336           |           182     |     2510    |    145     |
| 50%   |     3.27548e+06 |     2.02308e+07 |     1.95435e+06 |     2       |                2        |       255     |     1        |   80622           |           384     |     3504    |    238     |
| 75%   |     6.23362e+06 |     2.02311e+07 |     2.01141e+06 |     2       |                2        |       255     |     1        |  127664           |           459     |     8484    |    542     |
| max   |     7.81129e+06 |     2.02312e+07 |     2.13137e+06 |     8       |                3        |       255     |    28        |       1.48024e+06 |           465     |     8827    |    761     |

==============================
