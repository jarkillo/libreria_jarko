"""
Módulo para limpieza y normalización de espacios.

Este módulo contiene funciones para limpiar espacios en blanco extra,
tabulaciones, saltos de línea y otros caracteres de espaciado.
"""

import re
from typing import Any
from .utils import validar_entrada_texto, manejar_excepcion_texto


def limpiar_espacios(texto: Any) -> str:
    """
    Limpia espacios en blanco extra del texto.
    
    Realiza las siguientes operaciones:
    - Elimina espacios al inicio y final (strip)
    - Convierte múltiples espacios consecutivos en uno solo
    - Convierte tabulaciones y saltos de línea en espacios simples
    - Elimina espacios antes y después de signos de puntuación comunes
    
    Parámetros:
    ----------
    texto : Any
        El texto a limpiar. Se convertirá a string si no lo es.
    
    Retorna:
    -------
    str
        El texto con espacios normalizados.
    
    Errores:
    -------
    - Lanza TypeError si no se puede convertir el input a string.
    
    Ejemplos:
    --------
    >>> limpiar_espacios("  hola   mundo  ")
    'hola mundo'
    >>> limpiar_espacios("texto\\t\\ncon\\tespacios")
    'texto con espacios'
    >>> limpiar_espacios("hola ,  mundo  ;  bien")
    'hola, mundo; bien'
    """
    # Validar entrada
    texto_validado = validar_entrada_texto(texto, 'limpiar_espacios')
    
    try:
        # 1. Eliminar espacios al inicio y final
        texto_limpio = texto_validado.strip()
        
        # 2. Convertir tabulaciones, saltos de línea y otros espacios en blanco a espacios simples
        texto_limpio = re.sub(r'\s+', ' ', texto_limpio)
        
        # 3. Limpiar espacios alrededor de signos de puntuación comunes
        # Espacios antes de: , ; : . ! ? ) ] }
        texto_limpio = re.sub(r'\s+([,.;:!?)\]}])', r'\1', texto_limpio)
        
        # Espacios después de: ( [ {
        texto_limpio = re.sub(r'([(\[{])\s+', r'\1', texto_limpio)
        
        # Múltiples espacios consecutivos a uno solo (por si quedaron)
        texto_limpio = re.sub(r' {2,}', ' ', texto_limpio)
        
        return texto_limpio
        
    except Exception as e:
        manejar_excepcion_texto(e, 'limpiar_espacios', texto_validado) 