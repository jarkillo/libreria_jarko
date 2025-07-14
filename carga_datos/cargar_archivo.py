"""
Módulo para cargar archivos con detección automática de formato.

Este módulo contiene la función cargar_archivo() que detecta automáticamente 
el formato del archivo por su extensión y llama a la función correspondiente.
"""

import pandas as pd
from pathlib import Path
from typing import Union

from .cargar_csv import cargar_csv
from .cargar_xlsx import cargar_xlsx
from .cargar_parquet import cargar_parquet
from .utils import procesar_ruta


def cargar_archivo(ruta: Union[str, Path]) -> pd.DataFrame:
    """
    Carga un archivo detectando automáticamente el formato por extensión.
    
    Analiza la extensión del archivo y llama internamente a:
    - cargar_csv() si es .csv
    - cargar_xlsx() si es .xlsx
    - cargar_parquet() si es .parquet
    
    Parámetros:
    ----------
    ruta : Union[str, Path]
        Ruta del archivo que se quiere cargar.
    
    Retorna:
    -------
    pd.DataFrame
        El contenido del archivo como DataFrame.
    
    Formatos soportados:
    -------------------
    - .csv, .CSV (y variaciones de mayúsculas/minúsculas)
    - .xlsx, .XLSX (y variaciones de mayúsculas/minúsculas)
    - .parquet, .PARQUET (y variaciones de mayúsculas/minúsculas)
    
    Formatos NO soportados:
    ----------------------
    - .xls (Excel antiguo)
    - .ods (LibreOffice/OpenOffice)
    - .json, .xml, .tsv, .txt
    - Cualquier otra extensión
    
    Errores:
    -------
    - Lanza FileNotFoundError si el archivo no existe.
    - Lanza ValueError si la extensión no es soportada.
    - Lanza TypeError si el parámetro no es del tipo correcto.
    - Propaga errores de las funciones internas (cargar_csv, cargar_xlsx, cargar_parquet).
    
    Ejemplos:
    --------
    >>> df = cargar_archivo("datos.csv")        # Llama a cargar_csv()
    >>> df = cargar_archivo("datos.xlsx")       # Llama a cargar_xlsx()
    >>> df = cargar_archivo("datos.parquet")    # Llama a cargar_parquet()
    >>> df = cargar_archivo(Path("datos.csv"))  # Funciona con Path objects
    """
    # Validar tipo de entrada
    if not isinstance(ruta, (str, Path)):
        raise TypeError("El parámetro 'ruta' debe ser str o Path")
    
    # Crear Path object
    ruta_archivo = procesar_ruta(ruta)
    
    # Verificar que el archivo existe
    if not ruta_archivo.exists():
        raise FileNotFoundError(f"El archivo '{ruta}' no existe.")
    
    if not ruta_archivo.is_file():
        raise ValueError(f"La ruta '{ruta}' no es un archivo válido.")
    
    # Obtener extensión en minúsculas para comparación case-insensitive
    extension = ruta_archivo.suffix.lower()
    
    # Mapear extensiones a funciones
    if extension == '.csv':
        return cargar_csv(ruta_archivo)
    elif extension == '.xlsx':
        return cargar_xlsx(ruta_archivo)
    elif extension == '.parquet':
        return cargar_parquet(ruta_archivo)
    else:
        # Construir mensaje de error informativo
        formatos_soportados = ['.csv', '.xlsx', '.parquet']
        raise ValueError(
            f"Extensión de archivo no soportada: '{extension}'. "
            f"Formatos soportados: {', '.join(formatos_soportados)}"
        ) 