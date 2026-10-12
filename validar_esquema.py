
import os
import mssql_python
from dotenv import load_dotenv
from esquema import ESQUEMA

# 1. Cargar los datos de conexión
load_dotenv()

servidor = os.getenv("DB_SERVER")
puerto = os.getenv("DB_PORT")
base_datos = os.getenv("DB_NAME")
usuario = os.getenv("DB_USER")
contrasena = os.getenv("DB_PASSWORD")

# 2. Conectarnos a SQL Server
conexion = mssql_python.connect(
    f"SERVER={servidor},{puerto};"
    f"DATABASE={base_datos};"
    f"UID={usuario};"
    f"PWD={contrasena};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

cursor = conexion.cursor()

print("VALIDACIÓN DE COLUMNAS")
print("-" * 50)

errores = 0

# 3. Recorrer las tablas del diccionario
for nombre_original, datos in ESQUEMA.items():

    nombre_fisico = datos["tabla"]

    # Obtener las columnas reales de SQL Server
    cursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'dbo'
          AND TABLE_NAME = ?
    """, (nombre_fisico,))

    columnas_reales = {
        fila[0] for fila in cursor.fetchall()
    }

    # Comparar con las columnas del diccionario
    columnas_esperadas = set(datos["columnas"].values())

    faltantes = columnas_esperadas - columnas_reales

    if faltantes:
        errores += len(faltantes)
        print(f"{nombre_original}: ERROR")
        print(f"  Columnas faltantes: {faltantes}")
    else:
        print(f"{nombre_original}: OK")

# 4. Mostrar resultado final
print("-" * 50)
print(f"Columnas faltantes: {errores}")

cursor.close()
conexion.close()

