"""
Módulo de carga de datos para la librería Jarko.

Este módulo contiene funciones para cargar datos desde diferentes formatos:
- CSV
- Excel (futuro)
- Parquet (futuro)
"""

from .cargar_csv import cargar_csv

__all__ = ["cargar_csv"] 