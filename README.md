Actividad 0 – Preparación, conexión y reconciliación

Objetivo

Se nos pidió entorno de trabajo en Python para analizar la base de datos Sakila anteriormente migrada de MySQL a SQL Server, centralizar las equivalencias de nombres mediante un diccionario y verificar las cantidades de registros después de la migración.

Tecnologías utilizadas

- Python 3.12
- SQL Server en Docker
- Visual Studio Code
- mssql-python
- python-dotenv
- Pandas y otras bibliotecas incluidas en requirements.txt

Estructura del proyecto

- conexion.py: prueba la conexión a SQL Server.
- esquema.py: contiene el diccionario que relaciona los nombres canónicos de Sakila con los nombres físicos de la base migrada.
- conteo_mysql.py: analiza las inserciones del archivo original sakila-data.sql y genera conteo_origen_mysql.csv.
- reconciliacion.py: consulta los registros de SQL Server, los compara con los recuentos de origen y genera reconciliacion_final.csv.
- validar_esquema.py: comprueba que las columnas registradas en el diccionario existan en SQL Server.
- requirements.txt: dependencias de Python.
- .env: configuración privada de conexión; no debe subirse al repositorio.
- sakila-data.sql y sakila-schema.sql: archivos originales de Sakila utilizados como referencia.

Configuración

Crear un entorno virtual de Python e instalar las dependencias:


python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

Crear un archivo .env con las variables:

env
DB_SERVER=localhost
DB_PORT=1433
DB_NAME=Sakila_Espanol
DB_USER=sa
DB_PASSWORD=TU_CONTRASENA (la contraseña real debe mantenerse fuera del código fuente y de GitHub)

La conexión actual utiliza autenticación de SQL Server con usuario y contraseña. Para un entorno Windows con autenticación integrada, será necesario adaptar el método de conexión.

Ejecución

Los siguientes comandos deben ejecutarse desde la carpeta raíz del proyecto, con SQL Server iniciado y la base de datos configurada en .env.

1. Activar el entorno virtual

En macOS:
source .venv/bin/activate


2. Configurar OpenSSL en macOS**

En el equipo Mac utilizado para el desarrollo, mssql-python requiere indicar la ubicación de las bibliotecas de Python 3.12:

export DYLD_LIBRARY_PATH=/Library/Frameworks/Python.framework/Versions/3.12/lib

Este comando debe ejecutarse cada vez que se abre una terminal nueva, antes de utilizar los scripts que se conectan a SQL Server.

3. Generar el conteo del origen MySQL**

python conteo_mysql.py

Genera el archivo conteo_origen_mysql.csv a partir de sakila-data.sql.

4. Verificar la conexión con SQL Server**

python conexion.py


Resultado esperado:

¡Conexión exitosa! Base de datos: Sakila_Espanol

5. Ejecutar la reconciliación**

python reconciliacion.py


Compara las 16 tablas y genera reconciliacion_final.csv. En la migración utilizada para el desarrollo, todas las diferencias fueron cero.

6. Validar las columnas del diccionario**

python validar_esquema.py

Resultado esperado en la migración utilizada:

Columnas faltantes: 0

**Importante:** los comandos deben ejecutarse en el orden indicado. Si se abre una terminal nueva, hay que activar nuevamente el entorno virtual y configurar OpenSSL en macOS antes de ejecutar los programas que consultan SQL Server.

 Resultados de la reconciliación

Se compararon las cantidades de registros de las 16 tablas de Sakila entre los datos originales de MySQL y la base migrada a SQL Server.

Inicialmente, los recuentos de origen se obtuvieron analizando las instrucciones INSERT del archivo sakila-data.sql, mediante el programa conteo_mysql.py.

Las 15 tablas con inserciones directas en el archivo original presentaron la misma cantidad de registros en SQL Server, con diferencia cero.

 Verificación de la tabla film_text

La tabla film_text presenta una particularidad: el archivo sakila-data.sql no contiene instrucciones INSERT directas para esta tabla.

Esto se debe a que el esquema original de Sakila incluye un trigger denominado ins_film, definido en sakila-schema.sql, que inserta automáticamente un registro en film_text cada vez que se agrega una película a la tabla film.

Inicialmente, a partir de las 1.000 películas y del funcionamiento del trigger, se estableció un recuento esperado de 1.000 registros.

Posteriormente, para comprobar esta cantidad sin depender únicamente de la deducción, se utilizó MySQL Workbench y se ejecutó una consulta directamente sobre una base MySQL con los datos de Sakila cargados:

sql
SELECT COUNT(*) AS cantidad
FROM sakila.film_text;

Resultado obtenido en MySQL: 1.000 registros.

En la base migrada a SQL Server se verificó la cantidad de registros de la tabla equivalente, pelicula_texto, mediante la consulta:

sql
SELECT COUNT(*) AS cantidad
FROM pelicula_texto;

Resultado obtenido en SQL Server: 1.000 registros.

Por lo tanto, se confirmó mediante consultas a las bases de datos que ambas tablas contienen 1.000 registros, con una diferencia de cero.

Esta comprobación complementa el análisis realizado sobre los archivos originales y permite validar directamente el recuento de film_text en MySQL.

 Archivo de reconciliación

Los resultados se guardan en reconciliacion_final.csv, generado mediante reconciliacion.py, con las siguientes columnas:

- Tabla: nombre canónico de la tabla original de Sakila.
- Filas de origen: cantidad obtenida a partir de los datos originales de MySQL.
- Filas de SQL Server: cantidad consultada directamente en la base migrada.
- Diferencia: resta entre las cantidades de SQL Server y del origen.

Las 16 tablas presentan una diferencia de cero registros.

Los recuentos de origen de las 15 tablas con inserciones directas provienen del análisis del archivo SQL original. Para film_text, además del recuento esperado por el trigger, se realizó una verificación directa en MySQL Workbench.

 Diccionario de esquema y portabilidad

El archivo esquema.py centraliza las equivalencias entre los nombres canónicos de las tablas y columnas de Sakila y los nombres físicos utilizados en la migración a SQL Server.

Por ejemplo:

| Nombre original de Sakila | Nombre en SQL Server |
| payment | pago |

El diccionario permite que los programas trabajen con los nombres originales de Sakila y obtengan los nombres físicos correspondientes mediante las funciones definidas en esquema.py.

Las consultas desarrolladas deben utilizar estas funciones para resolver los nombres físicos de las tablas y columnas, evitando escribirlos directamente en otros archivos.

Esto tiene como objetivo facilitar la adaptación del proyecto a otras migraciones de Sakila que utilicen nombres diferentes.
Por ejemplo, si otro equipo conserva la tabla payment con su nombre original en lugar de utilizar pago, se modifica la equivalencia correspondiente en esquema.py, sin necesidad de cambiar la lógica de las consultas.

 Validación del esquema

Se desarrolló y ejecutó el programa validar_esquema.py, que verifica la correspondencia entre los nombres físicos de columnas registrados en esquema.py y las columnas existentes en SQL Server.

Para realizar esta comprobación, el programa consulta la vista INFORMATION_SCHEMA.COLUMNS de SQL Server.

Posteriormente, compara los nombres obtenidos con las columnas definidas en el diccionario.
Esta comprobación permite verificar que los nombres físicos de columnas definidos en esquema.py existen en la base migrada. Sin embargo, no garantiza por sí sola que todas las equivalencias sean semánticamente correctas.

 Conclusión

Durante la Actividad 0 se preparó el entorno de trabajo en Python, se configuró la conexión con SQL Server y se implementó un diccionario de equivalencias entre los nombres originales de Sakila y los nombres físicos de la base migrada.
Se desarrollaron programas para obtener los recuentos del origen MySQL, consultar las cantidades de registros en SQL Server, generar un archivo CSV de reconciliación y validar los nombres de las columnas.
La reconciliación realizada sobre las 16 tablas presentó una diferencia de cero registros.
En particular, se investigó el funcionamiento de la tabla film_text y su trigger ins_film. Posteriormente, se comprobó directamente mediante MySQL Workbench que la tabla contenía 1.000 registros en una base MySQL con datos de Sakila, coincidiendo con los 1.000 registros encontrados en SQL Server.
La coincidencia de cantidades permite verificar la consistencia de los recuentos, aunque no garantiza por sí sola que todos los valores de los registros migrados sean idénticos.
Finalmente, la validación del esquema confirmó que las columnas físicas registradas en el diccionario existen en SQL Server, sin detectar columnas faltantes.


 Actividad 1 – Extracción y análisis del rendimiento comercial

 Objetivo

Analizar el rendimiento comercial por tienda y por empleado utilizando la base de datos Sakila migrada a SQL Server, correspondiente a la variante 5 del trabajo práctico.

El objetivo es obtener las métricas necesarias mediante consultas T-SQL, trasladar los resultados a pandas y comparar los cálculos realizados en ambas herramientas.

 Tecnologías utilizadas

- SQL Server
- Python 3.12
- pandas
- Jupyter Notebook
- Visual Studio Code
- mssql-python

 Archivos desarrollados

- actividad1_consultas.sql: contiene las consultas T-SQL comentadas.
- actividad1_analisis.ipynb: notebook con la extracción de datos, validaciones, comparación de resultados, medición de tiempos y visualizaciones.

 Desarrollo

 1. Extracción optimizada de datos

Se desarrolló una consulta T-SQL que relaciona las tablas "empleado" y "pago" para calcular la cantidad de pagos, los ingresos totales y el ticket promedio por empleado y tienda.

También se utilizaron funciones de ventana para calcular la participación de cada empleado dentro de su tienda y la participación de cada tienda sobre los ingresos totales del negocio.

Las uniones y agregaciones principales se realizaron en SQL Server para evitar trasladar innecesariamente todos los pagos al DataFrame principal.

2. Carga de datos con pandas

Se utilizó pandas.read_sql() para ejecutar la consulta y cargar los resultados agrupados en un DataFrame.

En nuestra consulta principal no utilizamos params porque analizamos todas las tiendas y todos los empleados, sin filtros variables. Si necesitáramos filtrar por tienda o fecha, utilizaríamos consultas parametrizadas para evitar concatenaciones y prevenir inyecciones SQL.

3. Comparación entre SQL Server y pandas

Se calculó una misma métrica de ingresos por tienda y empleado mediante dos enfoques:

- Agregación directamente en SQL Server.
- Agrupación con pandas a partir de los pagos individuales.

Se compararon los resultados para verificar su coincidencia y se midieron los tiempos de ejecución utilizando perf_counter().

Los valores obtenidos coincidieron, sin diferencias en los ingresos calculados.

La comparación de tiempos debe interpretarse considerando que la medición de SQL Server incluye la consulta y transferencia de resultados, mientras que pandas trabaja con datos previamente cargados en memoria.

 4. Controles de calidad

Se verificó la integridad de las relaciones entre pagos y empleados, y se identificaron posibles empleados sin operaciones.

También se realizaron consultas complementarias para analizar la distribución de clientes y la relación de los pagos con ambas tiendas.

 5. Visualizaciones

Se generaron gráficos para representar la participación de los empleados en los ingresos de cada tienda y comparar la recaudación total entre tiendas.

Dado que la base contiene un empleado por tienda, cada empleado representa el 100 % de los ingresos de su tienda en el gráfico de participación interna.

 Resultados obtenidos

| Indicador | Tienda 1 | Tienda 2 |
|---|---:|---:|
| Empleado | Mike Hillyer | Jon Stephens |
| Cantidad de pagos | 8.054 | 7.990 |
| Ingresos totales | $33.482,50 | $33.924,06 |
| Ticket promedio aproximado | $4,16 | $4,25 |
| Participación en el negocio | 49,67 % | 50,33 % |

Ingresos totales del negocio: $67.406,56.

Se analizaron 16.044 pagos. No se encontraron pagos asociados a empleados inexistentes y las métricas de ingresos calculadas en SQL Server y pandas coincidieron.

 Conclusión

La Actividad 1 permitió comprobar que SQL Server y pandas pueden utilizarse de manera complementaria para analizar información comercial.

SQL Server resultó adecuado para resolver las uniones, agregaciones y cálculos principales, mientras que pandas permitió validar los resultados y desarrollar visualizaciones.

La comparación confirmó la consistencia de los ingresos calculados mediante ambos enfoques y permitió identificar una diferencia pequeña en la recaudación de las tiendas, favorable a la tienda 2.

Estado: Actividad 1 finalizada.
 6. Reaparición de dificultades de conexión con SQL Server

**Dificultad:** Durante la Actividad 0 habíamos tenido inconvenientes para conectar Python con SQL Server, ejecutado en Docker. Estos problemas se resolvieron mediante la configuración del controlador `mssql-python`, las variables del archivo `.env` y las bibliotecas necesarias en macOS.

Sin embargo, al comenzar la Actividad 1, volvimos a encontrar dificultades relacionadas con la conexión al trabajar desde un notebook de Jupyter en Visual Studio Code.

**Causa identificada:** Aunque la conexión ya funcionaba desde los scripts de la Actividad 0, el notebook utiliza su propio kernel de Python. Por eso fue necesario comprobar que estuviera utilizando el entorno virtual correcto y que las configuraciones requeridas para acceder a SQL Server estuvieran disponibles en ese proceso.

**Solución:** Revisamos el entorno de ejecución del notebook, seleccionamos el intérprete de Python correspondiente al proyecto y verificamos nuevamente la conexión con la base de datos `Sakila_Espanol`.

Una vez restablecida la comunicación, pudimos ejecutar las consultas T-SQL desde pandas y continuar con el análisis de datos.

**Aprendizaje:** Comprobamos que una conexión exitosa desde un script de Python no garantiza automáticamente que funcione desde Jupyter. Es importante verificar el entorno virtual, el kernel y las variables de configuración cada vez que se utiliza una herramienta o un proceso de ejecución diferente.