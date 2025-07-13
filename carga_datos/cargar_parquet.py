"""
Módulo para cargar archivos Parquet.

Este módulo contiene funciones específicas para la carga de archivos Parquet
con manejo robusto de errores y validación de tipos.
"""

import pandas as pd
from pathlib import Path
from typing import Union, Optional, List


def cargar_parquet(ruta: Union[str, Path], columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Carga un archivo Parquet y lo devuelve como DataFrame.

    Parámetros:
    ----------
    ruta : Union[str, Path]
        Ruta del archivo Parquet que se quiere cargar.
    columns : Optional[List[str]], opcional
        Lista de nombres de columnas específicas a cargar. Si es None, carga todas las columnas.

    Retorna:
    -------
    pd.DataFrame
        El contenido del archivo Parquet como DataFrame.

    Errores:
    -------
    - Lanza FileNotFoundError si el archivo no existe.
    - Lanza ValueError si el archivo no es un Parquet válido, las columnas especificadas no existen,
      hay problemas de permisos, memoria insuficiente o el archivo está vacío.
    - Lanza TypeError si los parámetros no son del tipo correcto.

    Ejemplos:
    --------
    >>> df = cargar_parquet("datos.parquet")
    >>> df = cargar_parquet("datos.parquet", columns=["nombre", "edad"])
    """
    # Validar tipos de entrada
    if not isinstance(ruta, (str, Path)):
        raise TypeError("El parámetro 'ruta' debe ser str o Path")
    
    if columns is not None and not isinstance(columns, list):
        raise TypeError("El parámetro 'columns' debe ser lista o None")
    
    if columns is not None and not all(isinstance(col, str) for col in columns):
        raise TypeError("Todos los elementos de 'columns' deben ser strings")

    # Crear Path object y validar archivo
    ruta_archivo = Path(ruta)
    
    if not ruta_archivo.exists():
        raise FileNotFoundError(f"El archivo '{ruta}' no existe.")
    
    if not ruta_archivo.is_file():
        raise ValueError(f"La ruta '{ruta}' no es un archivo válido.")

    try:
        df = pd.read_parquet(ruta_archivo, columns=columns)
    except ImportError as e:
        raise ValueError(
            f"No se pudo importar la librería necesaria para leer archivos Parquet. "
            f"Instala 'pyarrow' con: pip install pyarrow. "
            f"Error: {str(e)}"
        )
    except MemoryError as e:
        raise ValueError(
            f"El archivo '{ruta}' es demasiado grande para cargar en memoria. "
            f"Error: {str(e)}"
        )
    except PermissionError as e:
        raise ValueError(
            f"No tienes permisos para leer el archivo '{ruta}'. "
            f"Error: {str(e)}"
        )
    except Exception as e:
        # Capturar errores específicos de pyarrow por nombre de clase
        exception_name = type(e).__name__
        error_msg = str(e).lower()
        
        if exception_name == 'ArrowInvalid':
            if "no match for fieldref" in error_msg or "columna_inexistente" in error_msg:
                raise ValueError(
                    f"Una o más columnas especificadas no existen en el archivo '{ruta}'. "
                    f"Columnas solicitadas: {columns}. "
                    f"Error: {str(e)}"
                )
            else:
                raise ValueError(
                    f"El archivo '{ruta}' no es un archivo Parquet válido. "
                    f"Error: {str(e)}"
                )
        elif "not a parquet file" in error_msg or "invalid parquet file" in error_msg or "magic bytes not found" in error_msg:
            raise ValueError(
                f"El archivo '{ruta}' no es un archivo Parquet válido. "
                f"Error: {str(e)}"
            )
        elif exception_name == 'ArrowIOError' or "no match for fieldref" in error_msg or ("column" in error_msg and "does not exist" in error_msg):
            raise ValueError(
                f"Una o más columnas especificadas no existen en el archivo '{ruta}'. "
                f"Columnas solicitadas: {columns}. "
                f"Error: {str(e)}"
            )
        elif exception_name in ['OSError', 'IOError'] or "permission" in error_msg or "denied" in error_msg:
            raise ValueError(
                f"No tienes permisos para leer el archivo '{ruta}'. "
                f"Error: {str(e)}"
            )
        elif "file size is 0 bytes" in error_msg or "empty" in error_msg:
            raise ValueError(
                f"El archivo '{ruta}' está vacío o no contiene datos válidos. "
                f"Error: {str(e)}"
            )
        else:
            raise ValueError(
                f"Error inesperado al cargar el archivo '{ruta}': {str(e)}"
            )

    if df.empty:
        raise ValueError(f"El archivo '{ruta}' está vacío o no contiene datos válidos.")

    return df 