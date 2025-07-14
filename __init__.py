"""
Librería Jarko - Funciones Utilitarias

Esta librería contiene funciones utilitarias para facilitar tareas comunes 
de procesamiento de datos.
"""

from .carga_datos import cargar_csv, cargar_parquet, cargar_xlsx, cargar_archivo

__version__ = "0.1.0"
__author__ = "Jarko"

# Exportar funciones principales
__all__ = [
    "cargar_csv",
    "cargar_parquet",
    "cargar_xlsx",
    "cargar_archivo",
] 