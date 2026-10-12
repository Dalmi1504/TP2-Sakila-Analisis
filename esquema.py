"""Diccionario de nombres canónicos Sakila -> SQL Server migrado.

Único lugar del proyecto donde se definen los nombres físicos.
"""

ESQUEMA = {
    "actor": {
        "tabla": "actor",
        "columnas": {
            "actor_id": "actor_id",
            "first_name": "nombre",
            "last_name": "apellido",
            "last_update": "ultima_actualizacion",
        },
    },
    "address": {
        "tabla": "direccion",
        "columnas": {
            "address_id": "direccion_id",
            "address": "direccion",
            "address2": "direccion2",
            "district": "distrito",
            "city_id": "ciudad_id",
            "postal_code": "codigo_postal",
            "phone": "telefono",
            "last_update": "ultima_actualizacion",
        },
    },
    "category": {
        "tabla": "categoria",
        "columnas": {
            "category_id": "categoria_id",
            "name": "nombre",
            "last_update": "ultima_actualizacion",
        },
    },
    "city": {
        "tabla": "ciudad",
        "columnas": {
            "city_id": "ciudad_id",
            "city": "ciudad",
            "country_id": "pais_id",
            "last_update": "ultima_actualizacion",
        },
    },
    "country": {
        "tabla": "pais",
        "columnas": {
            "country_id": "pais_id",
            "country": "pais",
            "last_update": "ultima_actualizacion",
        },
    },
    "customer": {
        "tabla": "cliente",
        "columnas": {
            "customer_id": "cliente_id",
            "store_id": "tienda_id",
            "first_name": "nombre",
            "last_name": "apellido",
            "email": "email",
            "address_id": "direccion_id",
            "active": "activo",
            "create_date": "fecha_creacion",
            "last_update": "ultima_actualizacion",
        },
    },
    "film": {
        "tabla": "pelicula",
        "columnas": {
            "film_id": "pelicula_id",
            "title": "titulo",
            "description": "descripcion",
            "release_year": "anio_estreno",
            "language_id": "idioma_id",
            "original_language_id": "idioma_original_id",
            "rental_duration": "duracion_alquiler",
            "rental_rate": "precio_alquiler",
            "length": "duracion",
            "replacement_cost": "costo_reemplazo",
            "rating": "clasificacion",
            "special_features": "caracteristicas_especiales",
            "last_update": "ultima_actualizacion",
        },
    },
    "film_actor": {
        "tabla": "pelicula_actor",
        "columnas": {
            "actor_id": "actor_id",
            "film_id": "pelicula_id",
            "last_update": "ultima_actualizacion",
        },
    },
    "film_category": {
        "tabla": "pelicula_categoria",
        "columnas": {
            "film_id": "pelicula_id",
            "category_id": "categoria_id",
            "last_update": "ultima_actualizacion",
        },
    },
    "film_text": {
        "tabla": "pelicula_texto",
        "columnas": {
            "film_id": "pelicula_id",
            "title": "titulo",
            "description": "descripcion",
        },
    },
    "inventory": {
        "tabla": "inventario",
        "columnas": {
            "inventory_id": "inventario_id",
            "film_id": "pelicula_id",
            "store_id": "tienda_id",
            "last_update": "ultima_actualizacion",
        },
    },
    "language": {
        "tabla": "idioma",
        "columnas": {
            "language_id": "idioma_id",
            "name": "nombre",
            "last_update": "ultima_actualizacion",
        },
    },
    "payment": {
        "tabla": "pago",
        "columnas": {
            "payment_id": "pago_id",
            "customer_id": "cliente_id",
            "staff_id": "empleado_id",
            "rental_id": "alquiler_id",
            "amount": "monto",
            "payment_date": "fecha_pago",
            "last_update": "ultima_actualizacion",
        },
    },
    "rental": {
        "tabla": "alquiler",
        "columnas": {
            "rental_id": "alquiler_id",
            "rental_date": "fecha_alquiler",
            "inventory_id": "inventario_id",
            "customer_id": "cliente_id",
            "return_date": "fecha_devolucion",
            "staff_id": "empleado_id",
            "last_update": "ultima_actualizacion",
        },
    },
    "staff": {
        "tabla": "empleado",
        "columnas": {
            "staff_id": "empleado_id",
            "first_name": "nombre",
            "last_name": "apellido",
            "address_id": "direccion_id",
            "picture": "foto",
            "email": "email",
            "store_id": "tienda_id",
            "active": "activo",
            "username": "usuario",
            "password": "contrasena",
            "last_update": "ultima_actualizacion",
        },
    },
    "store": {
        "tabla": "tienda",
        "columnas": {
            "store_id": "tienda_id",
            "manager_staff_id": "gerente_empleado_id",
            "address_id": "direccion_id",
            "last_update": "ultima_actualizacion",
        },
    },
}

def tabla(nombre_canonico):
    """Devuelve el nombre físico de una tabla canónica."""
    return ESQUEMA[nombre_canonico]["tabla"]

def columna(tabla_canonica, columna_canonica):
    """Devuelve el nombre físico de una columna canónica."""
    return ESQUEMA[tabla_canonica]["columnas"][columna_canonica]

def nombre_tabla_sql(nombre_canonico):
    """Identificador de tabla escapado para SQL Server."""
    return "[" + tabla(nombre_canonico).replace("]", "]]" ) + "]"

def nombre_columna_sql(tabla_canonica, columna_canonica):
    """Identificador de columna escapado para SQL Server."""
    return "[" + columna(tabla_canonica, columna_canonica).replace("]", "]]" ) + "]"
