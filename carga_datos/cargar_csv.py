"""
Módulo para cargar archivos CSV.

Este módulo contiene funciones específicas para la carga de archivos CSV
con manejo robusto de errores y validación de tipos.
"""

import pandas as pd
from pathlib import Path
from typing import Union


def cargar_csv(ruta: Union[str, Path], sep: str = ",", encoding: str = "utf-8") -> pd.DataFrame:
    """
    Carga un archivo CSV y lo devuelve como DataFrame.

    Parámetros:
    ----------
    ruta : Union[str, Path]
        Ruta del archivo CSV que se quiere cargar.
    sep : str, opcional
        Separador del archivo. Por defecto es ','.
    encoding : str, opcional
        Codificación del archivo. Por defecto es 'utf-8'.

    Retorna:
    -------
    pd.DataFrame
        El contenido del CSV como DataFrame.

    Errores:
    -------
    - Lanza FileNotFoundError si el archivo no existe.
    - Lanza ValueError si el encoding no es válido, el CSV no se puede parsear,
      hay problemas de permisos, memoria insuficiente o el archivo está vacío.
    - Lanza TypeError si los parámetros no son del tipo correcto.

    Ejemplos:
    --------
    >>> df = cargar_csv("datos.csv")
    >>> df = cargar_csv("datos.csv", sep=";", encoding="latin1")
    """
    # Validar tipos de entrada
    if not isinstance(ruta, (str, Path)):
        raise TypeError("El parámetro 'ruta' debe ser str o Path")
    
    if not isinstance(sep, str):
        raise TypeError("El parámetro 'sep' debe ser str")
    
    if not isinstance(encoding, str):
        raise TypeError("El parámetro 'encoding' debe ser str")

    # Crear Path object y validar archivo
    ruta_archivo = Path(str(ruta).strip())
    
    if not ruta_archivo.exists():
        raise FileNotFoundError(f"El archivo '{ruta}' no existe.")
    
    if not ruta_archivo.is_file():
        raise ValueError(f"La ruta '{ruta}' no es un archivo válido.")

    try:
        df = pd.read_csv(ruta_archivo, sep=sep, encoding=encoding)
    except pd.errors.EmptyDataError:
        raise ValueError(f"El archivo '{ruta}' está vacío o no contiene datos válidos.")
    except (UnicodeDecodeError, UnicodeError) as e:
        raise ValueError(
            f"Error de codificación al leer el archivo '{ruta}'. "
            f"Intenta con un encoding diferente. "
            f"Error: {str(e)}"
        )
    except LookupError as e:
        # Encoding inexistente
        raise ValueError(
            f"La codificación '{encoding}' no es válida o no está disponible. "
            f"Error: {str(e)}"
        )
    except pd.errors.ParserError as e:
        raise ValueError(
            f"No se pudo parsear el archivo '{ruta}'. "
            f"Revisa el separador ('{sep}') o el contenido del archivo. "
            f"Error: {str(e)}"
        )
    except (PermissionError, OSError, IOError) as e:
        raise ValueError(
            f"No tienes permisos para leer el archivo '{ruta}'. "
            f"Error: {str(e)}"
        )
    except MemoryError as e:
        raise ValueError(
            f"El archivo '{ruta}' es demasiado grande para cargar en memoria. "
            f"Error: {str(e)}"
        )
    except Exception as e:
        # Capturar errores específicos de pandas por nombre de clase
        exception_name = type(e).__name__
        error_msg = str(e).lower()
        
        # Excepciones específicas de pandas
        if exception_name == 'ParserError' or "parse" in error_msg or "separator" in error_msg:
            raise ValueError(
                f"Error al parsear el archivo '{ruta}'. "
                f"Verifica el separador o formato del archivo. "
                f"Error: {str(e)}"
            )
        elif exception_name == 'EmptyDataError' or "empty" in error_msg:
            raise ValueError(
                f"El archivo '{ruta}' está vacío o no contiene datos válidos. "
                f"Error: {str(e)}"
            )
        elif "not found" in error_msg or "does not exist" in error_msg:
            raise FileNotFoundError(f"El archivo '{ruta}' no existe.")
        else:
            # Re-lanzar excepciones no esperadas para no ocultarlas
            raise

    if df.empty:
        raise ValueError(f"El archivo '{ruta}' está vacío o no contiene datos válidos.")

    return df 