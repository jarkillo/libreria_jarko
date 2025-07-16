"""
Módulo para normalización de caracteres especiales.

Este módulo contiene funciones para normalizar caracteres especiales,
símbolos extraños y reemplazarlos por equivalentes ASCII más comunes.
"""

import re
from typing import Any, Dict, Optional
from .utils import validar_entrada_texto, manejar_excepcion_texto


# Diccionario de reemplazos para caracteres especiales comunes
REEMPLAZOS_CARACTERES: Dict[str, str] = {
    # Comillas y apostrofes
    '"': '"',
    '"': '"',
    ''': "'",
    ''': "'",
    '«': '"',
    '»': '"',
    '‚': ',',
    '„': '"',
    
    # Guiones y rayas
    '–': '-',  # en dash
    '—': '-',  # em dash
    '−': '-',  # minus sign
    '‒': '-',  # figure dash
    '―': '-',  # horizontal bar
    
    # Espacios especiales
    ' ': ' ',  # non-breaking space
    '\u200b': '',  # zero-width space
    '\u2009': ' ',  # thin space
    '\u2008': ' ',  # punctuation space
    '\u2007': ' ',  # figure space
    
    # Puntos y símbolos
    '…': '...',  # ellipsis
    '•': '*',   # bullet
    '·': '*',   # middle dot
    '‰': '%',   # per mille
    '™': 'TM',  # trademark
    '®': 'R',   # registered
    '©': 'C',   # copyright
    
    # Símbolos matemáticos básicos
    '×': 'x',   # multiplication
    '÷': '/',   # division
    '±': '+/-', # plus-minus
    
    # Monedas comunes a texto
    '€': 'EUR',
    '£': 'GBP', 
    '¥': 'YEN',
    '¢': 'cent',
}


def normalizar_caracteres(texto: Any, reemplazos_personalizados: Optional[Dict[str, str]] = None) -> str:
    """
    Normaliza caracteres especiales y extraños a equivalentes ASCII.
    
    Reemplaza caracteres especiales comunes (comillas tipográficas, guiones largos,
    espacios especiales, etc.) por sus equivalentes ASCII más simples.
    
    Parámetros:
    ----------
    texto : Any
        El texto a normalizar. Se convertirá a string si no lo es.
    reemplazos_personalizados : Dict[str, str], opcional
        Diccionario adicional de reemplazos personalizados.
        Se aplicarán después de los reemplazos por defecto.
    
    Retorna:
    -------
    str
        El texto con caracteres normalizados.
    
    Errores:
    -------
    - Lanza TypeError si no se puede convertir el input a string o si 
      reemplazos_personalizados no es un diccionario.
    
    Ejemplos:
    --------
    >>> normalizar_caracteres("Texto con "comillas" y –guiones–")
    'Texto con "comillas" y -guiones-'
    >>> normalizar_caracteres("Precio: 25€ • Descuento: 10‰")
    'Precio: 25EUR * Descuento: 10%'
    >>> normalizar_caracteres("3×4÷2±1")
    '3x4/2+/-1'
    """
    # Validar entrada
    texto_validado = validar_entrada_texto(texto, 'normalizar_caracteres')
    
    # Validar reemplazos personalizados
    if reemplazos_personalizados is not None:
        if not isinstance(reemplazos_personalizados, dict):
            raise TypeError("El parámetro 'reemplazos_personalizados' debe ser un diccionario")
    
    try:
        texto_normalizado = texto_validado
        
        # Aplicar reemplazos por defecto
        for caracter_original, caracter_reemplazo in REEMPLAZOS_CARACTERES.items():
            texto_normalizado = texto_normalizado.replace(caracter_original, caracter_reemplazo)
        
        # Aplicar reemplazos personalizados si se proporcionan
        if reemplazos_personalizados:
            for caracter_original, caracter_reemplazo in reemplazos_personalizados.items():
                texto_normalizado = texto_normalizado.replace(caracter_original, caracter_reemplazo)
        
        # Limpiar caracteres de control que puedan haber quedado
        # Mantener solo caracteres imprimibles y espacios básicos
        texto_normalizado = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', texto_normalizado)
        
        return texto_normalizado
        
    except Exception as e:
        manejar_excepcion_texto(e, 'normalizar_caracteres', texto_validado) 