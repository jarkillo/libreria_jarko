"""
Utilidades compartidas para el módulo de normalización de texto.

Este módulo contiene funciones auxiliares que son utilizadas
por múltiples funciones de normalización.
"""

import logging
from typing import Any, NoReturn


def validar_entrada_texto(texto: Any, nombre_funcion: str) -> str:
    """
    Valida que la entrada sea un string y la convierte si es necesario.
    
    Parámetros:
    ----------
    texto : Any
        El texto a validar (se intentará convertir a str si no lo es).
    nombre_funcion : str
        Nombre de la función que llama (para mensajes de error).
    
    Retorna:
    -------
    str
        El texto validado como string.
    
    Errores:
    -------
    - Lanza TypeError si no se puede convertir a string.
    
    Ejemplos:
    --------
    >>> validar_entrada_texto("hola", "test")
    'hola'
    >>> validar_entrada_texto(123, "test")
    '123'
    """
    if texto is None:
        raise TypeError(f"El parámetro 'texto' en {nombre_funcion} no puede ser None")
    
    # Intentar convertir a string si no lo es
    try:
        return str(texto)
    except Exception as e:
        raise TypeError(
            f"El parámetro 'texto' en {nombre_funcion} no se puede convertir a string. "
            f"Error: {str(e)}"
        )


def manejar_excepcion_texto(excepcion: Exception, nombre_funcion: str, texto_original: str) -> NoReturn:
    """
    Maneja excepciones inesperadas en funciones de texto de forma consistente.
    
    Parámetros:
    ----------
    excepcion : Exception
        La excepción que se produjo.
    nombre_funcion : str
        Nombre de la función donde ocurrió la excepción.
    texto_original : str
        El texto original que se estaba procesando.
    
    Errores:
    -------
    - Re-lanza la excepción original después del logging.
    """
    exception_name = type(excepcion).__name__
    texto_muestra = texto_original[:50] + "..." if len(texto_original) > 50 else texto_original
    logging.warning(
        f"Excepción inesperada en {nombre_funcion} procesando '{texto_muestra}': "
        f"{exception_name}: {str(excepcion)}"
    )
    raise excepcion