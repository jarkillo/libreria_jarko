"""
Módulo para cargar archivos Excel (.xlsx).

Este módulo contiene funciones específicas para la carga de archivos Excel
con manejo robusto de errores y validación de tipos.
"""

import pandas as pd
from pathlib import Path
from typing import Union, Optional, Literal


def cargar_xlsx(ruta: Union[str, Path], sheet_name: Union[str, int] = 0, 
                header: Optional[int] = 0, engine: Literal['xlrd', 'openpyxl', 'odf', 'pyxlsb', 'calamine'] = 'openpyxl') -> pd.DataFrame:
    """
    Carga un archivo Excel (.xlsx) y lo devuelve como DataFrame.

    Parámetros:
    ----------
    ruta : Union[str, Path]
        Ruta del archivo Excel que se quiere cargar.
    sheet_name : Union[str, int], opcional
        Nombre o índice de la hoja a cargar. Por defecto es 0 (primera hoja).
    header : Optional[int], opcional
        Número de fila a usar como encabezado. Por defecto es 0 (primera fila).
        Si es None, no usa encabezado.
    engine : str, opcional
        Motor de lectura. Por defecto es 'openpyxl' para archivos .xlsx.

    Retorna:
    -------
    pd.DataFrame
        El contenido del archivo Excel como DataFrame.

    Errores:
    -------
    - Lanza FileNotFoundError si el archivo no existe.
    - Lanza ValueError si el archivo no es un Excel válido, la hoja especificada no existe,
      hay problemas de permisos, memoria insuficiente o el archivo está vacío.
    - Lanza TypeError si los parámetros no son del tipo correcto.

    Ejemplos:
    --------
    >>> df = cargar_xlsx("datos.xlsx")
    >>> df = cargar_xlsx("datos.xlsx", sheet_name="Hoja1")
    >>> df = cargar_xlsx("datos.xlsx", sheet_name=1, header=None)
    """
    # Validar tipos de entrada
    if not isinstance(ruta, (str, Path)):
        raise TypeError("El parámetro 'ruta' debe ser str o Path")
    
    if not isinstance(sheet_name, (str, int)):
        raise TypeError("El parámetro 'sheet_name' debe ser str o int")
    
    if header is not None and not isinstance(header, int):
        raise TypeError("El parámetro 'header' debe ser int o None")
    
    if engine not in ['xlrd', 'openpyxl', 'odf', 'pyxlsb', 'calamine']:
        raise TypeError("El parámetro 'engine' debe ser uno de: 'xlrd', 'openpyxl', 'odf', 'pyxlsb', 'calamine'")

    # Crear Path object y validar archivo
    ruta_archivo = Path(ruta)
    
    if not ruta_archivo.exists():
        raise FileNotFoundError(f"El archivo '{ruta}' no existe.")
    
    if not ruta_archivo.is_file():
        raise ValueError(f"La ruta '{ruta}' no es un archivo válido.")

    try:
        df = pd.read_excel(ruta_archivo, sheet_name=sheet_name, header=header, engine=engine)
    except ImportError as e:
        raise ValueError(
            f"No se pudo importar la librería necesaria para leer archivos Excel. "
            f"Instala 'openpyxl' con: pip install openpyxl. "
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
    except (OSError, IOError) as e:
        raise ValueError(
            f"No tienes permisos para leer el archivo '{ruta}'. "
            f"Error: {str(e)}"
        )
    except (UnicodeDecodeError, UnicodeError) as e:
        raise ValueError(
            f"Error de codificación al leer el archivo '{ruta}'. "
            f"El archivo podría estar corrupto. "
            f"Error: {str(e)}"
        )
    except ValueError as e:
        # Capturar errores específicos de pandas Excel
        error_msg = str(e).lower()
        if "worksheet" in error_msg and ("does not exist" in error_msg or "not found" in error_msg):
            raise ValueError(
                f"La hoja '{sheet_name}' no existe en el archivo '{ruta}'. "
                f"Error: {str(e)}"
            )
        elif "worksheet index" in error_msg and "invalid" in error_msg:
            raise ValueError(
                f"El índice de hoja '{sheet_name}' no existe en el archivo '{ruta}'. "
                f"Error: {str(e)}"
            )
        elif "excel file format cannot be determined" in error_msg:
            raise ValueError(
                f"El archivo '{ruta}' no es un archivo Excel válido. "
                f"Error: {str(e)}"
            )
        elif "unsupported format" in error_msg or "corrupt" in error_msg:
            raise ValueError(
                f"El archivo '{ruta}' está corrupto o tiene un formato no soportado. "
                f"Error: {str(e)}"
            )
        else:
            raise ValueError(
                f"Error al procesar el archivo '{ruta}': {str(e)}"
            )
    except Exception as e:
        # Capturar errores específicos de Excel por nombre de clase
        exception_name = type(e).__name__
        error_msg = str(e).lower()
        
        # Excepciones específicas de Excel/Zip
        if exception_name in ['BadZipFile', 'InvalidFileException'] or "not a zip file" in error_msg or "invalid file" in error_msg:
            raise ValueError(
                f"El archivo '{ruta}' no es un archivo Excel válido. "
                f"Error: {str(e)}"
            )
        elif exception_name == 'XLRDError' or "xlrd" in error_msg:
            raise ValueError(
                f"Error al leer el archivo Excel '{ruta}' con xlrd. "
                f"Error: {str(e)}"
            )
        elif "not supported" in error_msg or "unsupported" in error_msg:
            raise ValueError(
                f"El formato del archivo '{ruta}' no es soportado por el engine '{engine}'. "
                f"Error: {str(e)}"
            )
        elif "sheet" in error_msg and ("not found" in error_msg or "does not exist" in error_msg):
            raise ValueError(
                f"La hoja especificada '{sheet_name}' no existe en el archivo '{ruta}'. "
                f"Error: {str(e)}"
            )
        else:
            # Re-lanzar excepciones no esperadas para no ocultarlas
            raise

    if df.empty:
        raise ValueError(f"El archivo '{ruta}' está vacío o no contiene datos válidos.")

    return df 