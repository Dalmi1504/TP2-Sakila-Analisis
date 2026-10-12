
from pathlib import Path
import re
import csv
from esquema import ESQUEMA

# 1. Leer el archivo original de MySQL
texto = Path("sakila-data.sql").read_text(encoding="utf-8")

# 2. Crear una lista para guardar los resultados
resultados = []

print("RECUENTO ORIGINAL DE MYSQL")
print("-" * 55)

# 3. Recorrer las 16 tablas del diccionario
for nombre_tabla in ESQUEMA:

    # Buscar las instrucciones INSERT de cada tabla
    patron = rf"INSERT INTO `?{nombre_tabla}`? VALUES\s*(.*?);"
    bloques = re.findall(patron, texto, re.S)

    # Contar los registros encontrados
    cantidad = 0

    for bloque in bloques:
        registros = re.findall(r"(?m)^\s*\(\d+,", bloque)
        cantidad += len(registros)

    # 4. Caso especial: film_text
    if nombre_tabla == "film_text" and not bloques:

        # film_text se completa mediante el trigger ins_film.
        # Usamos la cantidad de film como valor esperado.
        cantidad = next(
            (
                fila["filas_origen"]
                for fila in resultados
                if fila["tabla"] == "film"
            ),
            None
        )

        metodo = "Estimado por trigger ins_film"

    elif bloques:
        metodo = "INSERT del archivo original"

    else:
        cantidad = None
        metodo = "Sin datos verificables"

    # 5. Guardar el resultado en la lista
    resultados.append({
        "tabla": nombre_tabla,
        "filas_origen": cantidad,
        "metodo": metodo
    })

    # Mostrar el resultado
    if cantidad is not None:
        print(f"{nombre_tabla}: {cantidad} registros ({metodo})")
    else:
        print(f"{nombre_tabla}: sin recuento disponible")

# 6. Crear el archivo CSV
with open(
    "conteo_origen_mysql.csv",
    "w",
    newline="",
    encoding="utf-8"
) as archivo:

    escritor = csv.DictWriter(
        archivo,
        fieldnames=["tabla", "filas_origen", "metodo"]
    )

    escritor.writeheader()
    escritor.writerows(resultados)

# 7. Mostrar el resultado final
print("-" * 55)
print(f"Total de tablas revisadas: {len(ESQUEMA)}")
print("Archivo generado: conteo_origen_mysql.csv")
