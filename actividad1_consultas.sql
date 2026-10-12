-- CONSULTA 1: RELACIÓN ENTRE PAGOS, EMPLEADOS Y TIENDAS
-- Pregunta:
-- ¿Podemos identificar qué empleado procesó cada pago
-- y a qué tienda pertenece ese empleado?
-- Objetivo:
-- Comprobar que las tablas pago y empleado se relacionan
-- correctamente y visualizar los primeros 10 registros.
-- ============================================================

USE Sakila_Espanol;

SELECT TOP (10)
    p.pago_id,
    p.monto,
    p.fecha_pago,
    p.empleado_id,
    e.nombre AS empleado_nombre,
    e.apellido AS empleado_apellido,
    e.tienda_id
FROM pago AS p
LEFT JOIN empleado AS e
    ON p.empleado_id = e.empleado_id
ORDER BY p.pago_id;

-- CONSULTA 2: CONTROL DE PAGOS SIN EMPLEADO
-- Preguntas:
-- ¿Cuántos pagos existen en total?
-- ¿Hay pagos que no tienen un empleado válido asociado?
-- Objetivo:
-- Detectar pagos que no puedan relacionarse con un empleado.
-- Esto permite controlar la calidad de los datos antes
-- de calcular los ingresos por empleado.

USE Sakila_Espanol;

SELECT
    COUNT(*) AS total_pagos,
    SUM(
        CASE
            WHEN e.empleado_id IS NULL THEN 1
            ELSE 0
        END
    ) AS pagos_sin_empleado
FROM pago AS p
LEFT JOIN empleado AS e
    ON p.empleado_id = e.empleado_id;

-- CONSULTA 3: CONTROL DE EMPLEADOS SIN OPERACIONES
-- Preguntas:
-- ¿Cuántas operaciones registró cada empleado?
-- ¿Existe algún empleado que no haya procesado ningún pago?
-- Objetivo:
-- Contar las operaciones de cada empleado e identificar
-- aquellos que no registraron pagos.
-- Se utiliza LEFT JOIN para incluir también a los empleados
-- que no tienen operaciones.

USE Sakila_Espanol;

SELECT
    e.empleado_id,
    e.nombre,
    e.apellido,
    e.tienda_id,
    COUNT(p.pago_id) AS cantidad_operaciones
FROM empleado AS e
LEFT JOIN pago AS p
    ON e.empleado_id = p.empleado_id
GROUP BY
    e.empleado_id,
    e.nombre,
    e.apellido,
    e.tienda_id
ORDER BY e.empleado_id;

-- CONSULTA 4: CLIENTES CON PAGOS EN AMBAS TIENDAS
-- Preguntas:
-- ¿Existen clientes cuyos pagos fueron procesados
-- por empleados de las dos tiendas?
-- ¿En cuántas tiendas distintas registró pagos cada cliente?
-- Objetivo:
-- Identificar clientes cuyos pagos fueron atendidos por
-- empleados pertenecientes a más de una tienda.
-- Aclaración:
-- Se considera la tienda del empleado que procesó el pago,
-- no necesariamente la tienda física donde estuvo el cliente.

USE Sakila_Espanol;

SELECT
    p.cliente_id,
    COUNT(DISTINCT e.tienda_id) AS tiendas_distintas
FROM pago AS p
INNER JOIN empleado AS e
    ON p.empleado_id = e.empleado_id
GROUP BY p.cliente_id
HAVING COUNT(DISTINCT e.tienda_id) > 1
ORDER BY p.cliente_id;

-- CONSULTA 5: DISTRIBUCIÓN DE CLIENTES POR TIENDA
-- Preguntas:
-- ¿Cuántos clientes están registrados en cada tienda?
-- ¿Cómo se distribuyen los clientes entre las sucursales?
-- Objetivo:
-- Conocer la cantidad de clientes asignados a cada tienda
-- y diferenciar la tienda registrada del cliente de la
-- tienda del empleado que procesa sus pagos.

USE Sakila_Espanol;

SELECT
    c.tienda_id AS tienda_asignada,
    COUNT(*) AS cantidad_clientes
FROM cliente AS c
GROUP BY c.tienda_id
ORDER BY c.tienda_id;

-- CONSULTA 6: MÉTRICAS COMERCIALES POR EMPLEADO
-- Preguntas:
-- ¿Cuántas operaciones procesó cada empleado?
-- ¿Cuánto dinero representan esas operaciones?
-- ¿Cuál es el importe promedio de cada pago?
-- ¿Qué diferencias comerciales existen entre los empleados?
--
-- Objetivo:
-- Calcular las tres métricas principales:
-- 1. Cantidad de operaciones: COUNT()
-- 2. Ingreso total: SUM()
-- 3. Ticket promedio: AVG()
-- Estas métricas permiten comparar el volumen de operaciones
-- con los ingresos y el importe promedio de los pagos.

USE Sakila_Espanol;

SELECT
    e.empleado_id,
    e.nombre,
    e.apellido,
    e.tienda_id,
    COUNT(p.pago_id) AS cantidad_operaciones,
    COALESCE(SUM(p.monto), 0) AS ingreso_total,
    AVG(p.monto) AS ticket_promedio
FROM empleado AS e
LEFT JOIN pago AS p
    ON e.empleado_id = p.empleado_id
GROUP BY
    e.empleado_id,
    e.nombre,
    e.apellido,
    e.tienda_id
ORDER BY e.tienda_id;



-- CONSULTA 7: PARTICIPACIÓN DE EMPLEADOS Y TIENDAS
-- Preguntas:
-- ¿Qué porcentaje de los ingresos de su tienda representa
-- cada empleado?
-- ¿Qué porcentaje del ingreso total del negocio representa
-- cada tienda?
-- Objetivo:
-- Calcular las métricas comerciales y sus participaciones
-- utilizando funciones de ventana.

-- SUM() OVER (PARTITION BY tienda_id):
-- Calcula el ingreso total de cada tienda.

-- SUM() OVER ():
-- Calcula el ingreso total de todo el negocio.
--
-- NULLIF():
-- Evita errores de división por cero.

USE Sakila_Espanol;

WITH rendimiento AS (
    SELECT
        e.empleado_id,
        e.nombre,
        e.apellido,
        e.tienda_id,
        COUNT(p.pago_id) AS cantidad_operaciones,
        COALESCE(SUM(p.monto), 0) AS ingreso_total,
        AVG(p.monto) AS ticket_promedio
    FROM empleado AS e
    LEFT JOIN pago AS p
        ON e.empleado_id = p.empleado_id
    GROUP BY
        e.empleado_id,
        e.nombre,
        e.apellido,
        e.tienda_id
),
participaciones AS (
    SELECT
        *,
        SUM(ingreso_total) OVER (
            PARTITION BY tienda_id
        ) AS ingreso_tienda,
        SUM(ingreso_total) OVER () AS ingreso_negocio
    FROM rendimiento
)
SELECT
    empleado_id,
    nombre,
    apellido,
    tienda_id,
    cantidad_operaciones,
    ingreso_total,
    ticket_promedio,
    100.0 * ingreso_total
        / NULLIF(ingreso_tienda, 0)
        AS porcentaje_empleado_tienda,
    100.0 * ingreso_tienda
        / NULLIF(ingreso_negocio, 0)
        AS porcentaje_tienda_negocio
FROM participaciones
ORDER BY tienda_id, empleado_id;