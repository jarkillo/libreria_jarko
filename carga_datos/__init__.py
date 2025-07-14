"""
Módulo de carga de datos para la librería Jarko.

Este módulo contiene funciones para cargar datos desde diferentes formatos:
- CSV
- Excel (.xlsx)
- Parquet
- Detección automática de formato
"""

from .cargar_csv import cargar_csv
from .cargar_parquet import cargar_parquet
from .cargar_xlsx import cargar_xlsx
from .cargar_archivo import cargar_archivo

__all__ = ["cargar_csv", "cargar_parquet", "cargar_xlsx", "cargar_archivo"] 