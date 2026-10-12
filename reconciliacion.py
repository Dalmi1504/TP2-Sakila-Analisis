
import os
import csv
import mssql_python
from dotenv import load_dotenv
from esquema import ESQUEMA, nombre_tabla_sql

# 1. Cargar las variables de conexión
load_dotenv()

servidor = os.getenv("DB_SERVER")
puerto = os.getenv("DB_PORT")
base_datos = os.getenv("DB_NAME")
usuario = os.getenv("DB_USER")
contrasena = os.getenv("DB_PASSWORD")

# 2. Leer los recuentos originales de MySQL
origen_mysql = {}

with open("conteo_origen_mysql.csv", "r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        nombre_tabla = fila["tabla"]

        cantidad = (
            int(fila["filas_origen"])
            if fila["filas_origen"]
            else None
        )

        origen_mysql[nombre_tabla] = cantidad

# 3. Conectarnos a SQL Server
conexion = mssql_python.connect(
    f"SERVER={servidor},{puerto};"
    f"DATABASE={base_datos};"
    f"UID={usuario};"
    f"PWD={contrasena};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

cursor = conexion.cursor()
resultados = []

# 4. Recorrer las 16 tablas y comparar
for nombre_original in ESQUEMA:

    tabla_sql = nombre_tabla_sql(nombre_original)

    # Contar las filas en SQL Server
    cursor.execute(f"SELECT COUNT(*) FROM {tabla_sql}")
    cantidad_sql = cursor.fetchone()[0]

    # Obtener las filas originales de MySQL
    cantidad_mysql = origen_mysql.get(nombre_original)

    # Calcular la diferencia: destino menos origen
    diferencia = (
        cantidad_sql - cantidad_mysql
        if cantidad_mysql is not None
        else None
    )

    resultados.append({
        "tabla": nombre_original,
        "filas_origen": cantidad_mysql,
        "filas_sql_server": cantidad_sql,
        "diferencia": diferencia
    })

# 5. Mostrar la tabla de reconciliación
print("RECONCILIACIÓN MYSQL VS SQL SERVER")
print("-" * 65)
print(f"{'Tabla':<20} {'MySQL':>10} {'SQL Server':>12} {'Diferencia':>12}")
print("-" * 65)

for fila in resultados:
    print(
        f"{fila['tabla']:<20} "
        f"{str(fila['filas_origen']):>10} "
        f"{fila['filas_sql_server']:>12} "
        f"{str(fila['diferencia']):>12}"
    )

print("-" * 65)

# 6. Exportar el resultado final
with open(
    "reconciliacion_final.csv",
    "w",
    newline="",
    encoding="utf-8"
) as archivo:

    escritor = csv.DictWriter(
        archivo,
        fieldnames=[
            "tabla",
            "filas_origen",
            "filas_sql_server",
            "diferencia"
        ]
    )

    escritor.writeheader()
    escritor.writerows(resultados)

# 7. Cerrar la conexión
cursor.close()
conexion.close()

print("Archivo generado: reconciliacion_final.csv")
print("Nota: film_text utiliza un recuento esperado por trigger.")
