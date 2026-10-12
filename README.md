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
