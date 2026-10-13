Actividad 2  Diagnóstico de calidad de datos

Seminario de Actualización – TP2 

Variante 5 Rendimiento comercial por tienda y por empleado 

Base de datos: Sakila_Espanol (SQL Server)

1. Dimensiones y estructura del conjunto.

Se analizaron 16.044 registros y 6 columnas provenientes de la tabla 'pago', relacionados con la tabla 'empleado' para identificar la tienda que procesó cada operación.
Las columnas analizadas fueron 'pago_id', 'cliente_id', 'empleado_id', 'tienda_id', 'monto' y 'fecha_pago'.

2. Tipos de datos.

Los identificadores se encuentran representados como números enteros ('int64'), los montos como números decimales ('float64') y las fechas como 'datetime64[us]'.
Los tipos son adecuados para las operaciones de agrupación, cálculo y análisis previstas. No se requieren conversiones adicionales.

3. Valores faltantes.

Se verificaron los valores nulos de las seis columnas mediante pandas.
Resultado: 0 valores faltantes (0 %) en todas las columnas.
Decisión: conservar los registros originales, sin imputaciones.

4. Registros duplicados.

Se utilizó 'pago_id' como identificador único de cada operación.
Resultado: 0 pagos duplicados (0 %).
Decisión: no eliminar registros, ya que no se identificaron duplicaciones según la clave de negocio.

5. Rangos válidos y valores atípicos.

Los montos observados varían entre $0 y $11,99, con un promedio aproximado de $4,20.
Se aplicó el método del rango intercuartílico (IQR):
Primer cuartil (Q1): $2,99.
Tercer cuartil (Q3): $4,99.
IQR: $2,00.
Límite inferior: -$0,01.
Límite superior: $7,99.
Se identificaron 857 pagos atípicos (5,34 %), todos superiores al límite calculado.
Para distinguir anomalías de valores legítimos, se analizó la frecuencia de los importes atípicos. De los 857 pagos, 855 presentan montos terminados en ,99 ($8,99, $9,99, $10,99 y $11,99), siguiendo un patrón compatible con los precios habituales. Esto sugiere que podrían corresponder a operaciones comerciales reales, aunque superen el límite estadístico.
Los dos importes restantes ($8,97 y $9,98) aparecen una sola vez cada uno. Por su baja frecuencia y diferencia respecto del patrón predominante, requieren una revisión particular para determinar si corresponden a operaciones legítimas o errores de carga.

Se realizó una validación adicional de los 857 pagos atípicos mediante su relación con la tabla de alquileres. Se comprobó que todos tienen un alquiler asociado y que el cliente registrado en cada pago coincide con el del alquiler correspondiente. No se encontraron pagos atípicos sin alquiler ni inconsistencias entre clientes.
Esta verificación aporta evidencia de integridad referencial y respalda la posibilidad de que se trate de operaciones legítimas. Sin embargo, no permite confirmar por sí sola que los importes cobrados sean correctos, por lo que sería necesario contrastarlos con las tarifas correspondientes.

Decisión de transformación: conservar los 857 pagos atípicos sin modificar sus importes, ya que no se detectaron inconsistencias en sus relaciones y eliminarlos podría distorsionar los ingresos totales y el ticket promedio. Cualquier corrección futura deberá estar respaldada por un error comprobado.

6. Categorías y relaciones del negocio.

Se analizaron las relaciones entre pagos, empleados y tiendas.
Los controles específicos de la variante 5 arrojaron los siguientes resultados:
- Pagos sin empleado válido: 0.
- Empleados sin operaciones registradas: 0.
- Clientes con pagos procesados en ambas tiendas: 599.

El último resultado describe una característica de las operaciones registradas, no necesariamente una inconsistencia. No permite afirmar que los clientes hayan visitado físicamente ambas sucursales.

Decisión:conservar las relaciones existentes, diferenciando la tienda que procesa el pago de la tienda de origen del cliente.

7. Cardinalidad y reglas de negocio.

El conjunto contiene operaciones asociadas a 2 empleados y 2 tiendas. Los identificadores de clientes observados abarcan del 1 al 599.

Se verificaron dos reglas de negocio:
- Pagos con monto negativo: 0 incumplimientos.
- Pagos con fecha posterior al momento del análisis: 0 incumplimientos.
No se detectaron registros que requieran correcciones por estas condiciones.
Además, se contrastaron de forma independiente los controles de pagos negativos y pagos sin empleado válido mediante T-SQL y pandas. Ambos métodos coincidieron, con 0 casos en cada control.

8. Cobertura temporal.

Los pagos registrados abarcan desde el 24 de mayo de 2005 hasta el 14 de febrero de 2006.
La columna 'fecha_pago' contiene fechas válidas para su procesamiento y no presenta valores nulos. No se detectaron fechas futuras respecto del momento del análisis.
Decisión: conservar las fechas originales. El período histórico deberá indicarse al interpretar los resultados comerciales.


Conclusión general.

El conjunto analizado presenta buena integridad en los controles ejecutados: no se detectaron valores faltantes, identificadores duplicados, pagos sin empleado válido, empleados sin operaciones, montos negativos ni fechas futuras.
El principal hallazgo estadístico corresponde a los 857 pagos atípicos, cuya validez comercial no puede determinarse únicamente mediante el IQR.
Se recomienda conservar los datos originales y profundizar la revisión de esos importes antes de efectuar transformaciones correctivas. De esta manera se preserva la trazabilidad y se evita alterar injustificadamente las métricas de rendimiento comercial.