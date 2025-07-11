import pandas as pd
from pathlib import Path
from typing import Union

def cargar_csv(ruta: Union[str, Path], sep: str = ";", encoding: str = "utf-8") -> pd.DataFrame:
    """
    Carga un archivo CSV y lo devuelve como DataFrame.

    Parámetros:
    ----------
    ruta : Union[str, Path]
        Ruta del archivo CSV que se quiere cargar.
    sep : str, opcional
        Separador del archivo. Por defecto es ';'.
    encoding : str, opcional
        Codificación del archivo. Por defecto es 'utf-8'.

    Retorna:
    -------
    pd.DataFrame
        El contenido del CSV como DataFrame.

    Errores:
    -------
    - Lanza FileNotFoundError si el archivo no existe.
    - Lanza ValueError si el encoding no es válido o el CSV no se puede parsear.
    - Lanza TypeError si los parámetros no son del tipo correcto.

    Ejemplos:
    --------
    >>> df = cargar_csv("datos.csv")
    >>> df = cargar_csv("datos.csv", sep=",", encoding="latin1")
    """
    # Validar tipos de entrada
    if not isinstance(ruta, (str, Path)):
        raise TypeError("El parámetro 'ruta' debe ser str o Path")
    
    if not isinstance(sep, str):
        raise TypeError("El parámetro 'sep' debe ser str")
    
    if not isinstance(encoding, str):
        raise TypeError("El parámetro 'encoding' debe ser str")

    # Crear Path object y validar archivo
    ruta_archivo = Path(ruta)
    
    if not ruta_archivo.exists():
        raise FileNotFoundError(f"El archivo '{ruta}' no existe.")
    
    if not ruta_archivo.is_file():
        raise ValueError(f"La ruta '{ruta}' no es un archivo válido.")

    try:
        df = pd.read_csv(ruta_archivo, sep=sep, encoding=encoding)
    except pd.errors.EmptyDataError:
        raise ValueError(f"El archivo '{ruta}' está vacío o no contiene datos válidos.")
    except UnicodeDecodeError as e:
        raise ValueError(
            f"No se pudo leer el archivo '{ruta}' con codificación '{encoding}'. "
            f"Error: {str(e)}"
        )
    except pd.errors.ParserError as e:
        raise ValueError(
            f"No se pudo parsear el archivo '{ruta}'. "
            f"Revisa el separador ('{sep}') o el contenido del archivo. "
            f"Error: {str(e)}"
        )
    except Exception as e:
        raise ValueError(
            f"Error inesperado al cargar el archivo '{ruta}': {str(e)}"
        )

    if df.empty:
        raise ValueError(f"El archivo '{ruta}' está vacío o no contiene datos válidos.")

    return df
