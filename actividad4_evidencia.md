# Actividad 4 — Evidencia de ejecución e idempotencia del ETL

## 1. Objetivo

Demostrar que el pipeline ETL de la variante 5, *Rendimiento comercial por tienda y por empleado*, puede ejecutarse repetidamente sin acumular registros duplicados en la tabla destino `dbo.TP2_RendimientoComercial`, dentro de la base de datos `Sakila_Espanol`.

## 2. Ejecución del pipeline

El proceso se ejecutó desde la terminal de VS Code mediante el comando:

```bash
python actividad4_etl.py
```

El pipeline realiza las siguientes operaciones:

- Extrae pagos y datos de empleados desde SQL Server.
- Lee el archivo complementario `metas_comerciales.csv`.
- Ejecuta controles de calidad.
- Limpia, agrupa y combina los datos mediante pandas.
- Calcula las métricas comerciales.
- Carga los resultados en `dbo.TP2_RendimientoComercial`.

## 3. Resultados de las ejecuciones

| Indicador | Primera ejecución | Segunda ejecución |
|---|---:|---:|
| Pagos extraídos | 16.044 | 16.044 |
| Registros del CSV | 2 | 2 |
| Pagos sin empleado o tienda válida | 0 | 0 |
| Empleados sin operaciones | 0 | 0 |
| Clientes con operaciones en ambas tiendas | 599 | 599 |
| Filas generadas | 2 | 2 |
| Filas insertadas | 2 | 2 |
| Estado | Exitosa | Exitosa |

Ambas ejecuciones finalizaron correctamente, según los mensajes registrados por `logging`.

## 4. Verificación de la tabla destino

Se ejecutó la siguiente consulta en SQL Server:

```sql
SELECT COUNT(*) AS cantidad_registros
FROM dbo.TP2_RendimientoComercial;
```

Resultado obtenido después de las ejecuciones:

| cantidad_registros |
|---:|
| 2 |

El conteo confirma que no se acumularon registros adicionales después de ejecutar nuevamente el pipeline.

## 5. Estrategia de idempotencia

Se implementó una estrategia de **carga completa por reemplazo**, mediante `DELETE + INSERT` dentro de una transacción.

La función `cargar_datos()` elimina los resultados anteriores de la tabla destino y carga nuevamente el conjunto completo de métricas calculadas.

Si ocurre un error durante la carga, se ejecuta `rollback()` para revertir los cambios pendientes.

Esta estrategia se eligió porque la tabla contiene un conjunto pequeño de resultados agregados que pueden reconstruirse a partir de los datos originales.

No se utiliza una carga incremental porque no es necesario conservar un historial de versiones ni procesar únicamente registros nuevos.

## 6. Conclusión

El pipeline ETL se ejecutó correctamente en dos ocasiones consecutivas y la tabla destino mantuvo una cantidad de 2 registros.

La estrategia de reemplazo completo permite evitar la acumulación de duplicados y obtener resultados reproducibles mientras los datos de origen permanezcan sin cambios.

La verificación de conteo demuestra la estabilidad de la cantidad de filas. La igualdad completa del contenido requeriría comparar también las métricas almacenadas.