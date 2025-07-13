"""
Módulo de carga de datos para la librería Jarko.

Este módulo contiene funciones para cargar datos desde diferentes formatos:
- CSV
- Excel (.xlsx)
- Parquet
"""

from .cargar_csv import cargar_csv
from .cargar_parquet import cargar_parquet
from .cargar_xlsx import cargar_xlsx

__all__ = ["cargar_csv", "cargar_parquet", "cargar_xlsx"] 