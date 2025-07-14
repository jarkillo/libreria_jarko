"""
Tests principales para la librería carga_datos.

Este archivo actúa como punto de entrada para todos los tests modulares.
Los tests específicos están organizados en archivos separados por funcionalidad:

- test_cargar_csv.py: Tests para cargar_csv()
- test_cargar_parquet.py: Tests para cargar_parquet()
- test_cargar_xlsx.py: Tests para cargar_xlsx()
- test_cargar_archivo.py: Tests para cargar_archivo()
- test_utils.py: Tests para funciones utilitarias

Para ejecutar todos los tests:
    python -m pytest test/

Para ejecutar tests específicos:
    python -m pytest test/test_cargar_csv.py
    python -m pytest test/test_cargar_parquet.py
    python -m pytest test/test_cargar_xlsx.py
    python -m pytest test/test_cargar_archivo.py
    python -m pytest test/test_utils.py
"""

# Importar todos los tests para mantener compatibilidad
from .test_cargar_csv import TestCargarCsv
from .test_cargar_parquet import TestCargarParquet
from .test_cargar_xlsx import TestCargarXlsx
from .test_cargar_archivo import TestCargarArchivo
from .test_utils import TestProcesarRuta

# Hacer que las clases de test estén disponibles para pytest
__all__ = [
    'TestCargarCsv',
    'TestCargarParquet', 
    'TestCargarXlsx',
    'TestCargarArchivo',
    'TestProcesarRuta'
] 