"""
Utilidades compartidas para el manejo de archivos.

Este módulo contiene funciones auxiliares que son utilizadas
por múltiples módulos de carga de datos.
"""

from pathlib import Path
from typing import Union
import logging


def procesar_ruta(ruta: Union[str, Path]) -> Path:
    """
    Procesa una ruta eliminando espacios en blanco y convirtiéndola a Path.
    
    Esta función maneja defensivamente rutas que pueden tener espacios
    accidentales al inicio o final, convirtiéndolas en Path objects limpios.
    
    Parámetros:
    ----------
    ruta : Union[str, Path]
        Ruta del archivo que se quiere procesar.
    
    Retorna:
    -------
    Path
        Path object con espacios eliminados.
    
    Errores:
    -------
    - Lanza TypeError si el parámetro no es str o Path.
    
    Ejemplos:
    --------
    >>> procesar_ruta("archivo.csv")
    PosixPath('archivo.csv')
    >>> procesar_ruta("  archivo.csv  ")
    PosixPath('archivo.csv')
    >>> procesar_ruta(Path("archivo.csv "))
    PosixPath('archivo.csv')
    """
    # Validar tipos de entrada
    if not isinstance(ruta, (str, Path)):
        raise TypeError("El parámetro 'ruta' debe ser str o Path")
    
    return Path(str(ruta).strip()) 


def manejar_excepcion_inesperada(excepcion: Exception, nombre_funcion: str) -> None:
    """
    Maneja excepciones inesperadas de forma consistente.
    
    Esta función registra la excepción en el log y la re-lanza para
    mantener el comportamiento original, pero de forma centralizada.
    
    Parámetros:
    ----------
    excepcion : Exception
        La excepción que se produjo.
    nombre_funcion : str
        Nombre de la función donde ocurrió la excepción (ej: 'cargar_csv').
    
    Errores:
    -------
    - Re-lanza la excepción original después del logging.
    
    Ejemplos:
    --------
    >>> try:
    ...     # algún código que puede fallar
    ...     pass
    ... except Exception as e:
    ...     manejar_excepcion_inesperada(e, 'cargar_csv')
    """
    exception_name = type(excepcion).__name__
    logging.warning(f"Excepción inesperada en {nombre_funcion}: {exception_name}: {str(excepcion)}")
    raise excepcion