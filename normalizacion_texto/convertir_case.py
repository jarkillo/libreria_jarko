"""
Módulo para conversión de mayúsculas y minúsculas.

Este módulo contiene funciones para convertir texto entre mayúsculas 
y minúsculas de forma robusta.
"""

from typing import Any
from .utils import validar_entrada_texto, manejar_excepcion_texto


def convertir_a_minusculas(texto: Any) -> str:
    """
    Convierte todo el texto a minúsculas.
    
    Parámetros:
    ----------
    texto : Any
        El texto a convertir. Se convertirá a string si no lo es.
    
    Retorna:
    -------
    str
        El texto en minúsculas.
    
    Errores:
    -------
    - Lanza TypeError si no se puede convertir el input a string.
    
    Ejemplos:
    --------
    >>> convertir_a_minusculas("HOLA MUNDO")
    'hola mundo'
    >>> convertir_a_minusculas("José MARÍA")
    'josé maría'
    >>> convertir_a_minusculas(123)
    '123'
    """
    # Validar entrada
    texto_validado = validar_entrada_texto(texto, 'convertir_a_minusculas')
    
    try:
        return texto_validado.lower()
    except Exception as e:
        manejar_excepcion_texto(e, 'convertir_a_minusculas', texto_validado)


def convertir_a_mayusculas(texto: Any) -> str:
    """
    Convierte todo el texto a mayúsculas.
    
    Parámetros:
    ----------
    texto : Any
        El texto a convertir. Se convertirá a string si no lo es.
    
    Retorna:
    -------
    str
        El texto en mayúsculas.
    
    Errores:
    -------
    - Lanza TypeError si no se puede convertir el input a string.
    
    Ejemplos:
    --------
    >>> convertir_a_mayusculas("hola mundo")
    'HOLA MUNDO'
    >>> convertir_a_mayusculas("josé maría")
    'JOSÉ MARÍA'
    >>> convertir_a_mayusculas(123)
    '123'
    """
    # Validar entrada
    texto_validado = validar_entrada_texto(texto, 'convertir_a_mayusculas')
    
    try:
        return texto_validado.upper()
    except Exception as e:
        manejar_excepcion_texto(e, 'convertir_a_mayusculas', texto_validado) 