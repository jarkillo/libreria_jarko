"""
Librería Jarko - Funciones Utilitarias

Esta librería contiene funciones utilitarias para facilitar tareas comunes 
de procesamiento de datos y normalización de texto.
"""

# Importar funciones de carga de datos
from .carga_datos import cargar_csv, cargar_parquet, cargar_xlsx, cargar_archivo

# Importar funciones de normalización de texto
from .normalizacion_texto import (
    quitar_acentos,
    convertir_a_minusculas,
    convertir_a_mayusculas,
    limpiar_espacios,
    normalizar_caracteres,
    normalizar_texto
)

__version__ = "0.2.0"
__author__ = "Jarko"

# Exportar funciones principales
__all__ = [
    # Funciones de carga de datos
    "cargar_csv",
    "cargar_parquet",
    "cargar_xlsx",
    "cargar_archivo",
    # Funciones de normalización de texto
    "quitar_acentos",
    "convertir_a_minusculas",
    "convertir_a_mayusculas",
    "limpiar_espacios",
    "normalizar_caracteres",
    "normalizar_texto"
]