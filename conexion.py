
import os
import mssql_python
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Datos de conexión
servidor = os.getenv("DB_SERVER")
puerto = os.getenv("DB_PORT")
base_datos = os.getenv("DB_NAME")
usuario = os.getenv("DB_USER")
contrasena = os.getenv("DB_PASSWORD")

# Conectarnos a SQL Server
try:
    
    conexion = mssql_python.connect(
    f"SERVER={servidor},{puerto};"
    f"DATABASE={base_datos};"
    f"UID={usuario};"
    f"PWD={contrasena};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    )


    cursor = conexion.cursor()
    cursor.execute("SELECT DB_NAME()")
    resultado = cursor.fetchone()

    print("¡Conexión exitosa!")
    print("Base de datos:", resultado[0])

    cursor.close()
    conexion.close()

except Exception as error:
    print("Error al conectar:", error)
