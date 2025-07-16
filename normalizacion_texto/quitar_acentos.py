"""
Módulo para quitar acentos y caracteres diacríticos.

Este módulo contiene funciones para eliminar acentos, tildes y otros
caracteres diacríticos del texto, convirtiéndolos a su equivalente ASCII.
"""

import unicodedata
from typing import Any, Dict
from .utils import validar_entrada_texto, manejar_excepcion_texto


# Diccionario de caracteres especiales que no se descomponen con NFD
CARACTERES_ESPECIALES: Dict[str, str] = {
    'Å': 'A', 'å': 'a',
    'Æ': 'AE', 'æ': 'ae', 
    'Ø': 'O', 'ø': 'o',
    'Þ': 'Th', 'þ': 'th',
    'Ð': 'D', 'ð': 'd',
    'Œ': 'OE', 'œ': 'oe',
    'ß': 'ss',
    'Đ': 'D', 'đ': 'd',
    'Ħ': 'H', 'ħ': 'h',
    'Ł': 'L', 'ł': 'l',
    'Ŋ': 'N', 'ŋ': 'n',
    'Ŧ': 'T', 'ŧ': 't',
}


def quitar_acentos(texto: Any) -> str:
    """
    Quita acentos y caracteres diacríticos del texto.
    
    Convierte caracteres como á, é, í, ó, ú, ñ, ç a sus equivalentes
    sin acentos: a, e, i, o, u, n, c. También maneja caracteres especiales
    como Ø, Æ, ß que no se descomponen automáticamente.
    
    Parámetros:
    ----------
    texto : Any
        El texto del cual quitar los acentos. Se convertirá a string si no lo es.
    
    Retorna:
    -------
    str
        El texto sin acentos ni caracteres diacríticos.
    
    Errores:
    -------
    - Lanza TypeError si no se puede convertir el input a string.
    
    Ejemplos:
    --------
    >>> quitar_acentos("José María")
    'Jose Maria'
    >>> quitar_acentos("niño español")
    'nino espanol'
    >>> quitar_acentos("São Paulo, Çà et là")
    'Sao Paulo, Ca et la'
    >>> quitar_acentos("Åbo Øresund Zürich")
    'Abo Oresund Zurich'
    >>> quitar_acentos("Москва")  # Mantiene caracteres no latinos
    'Москва'
    """
    # Validar entrada
    texto_validado = validar_entrada_texto(texto, 'quitar_acentos')
    
    try:
        # Primero aplicar reemplazos para caracteres especiales
        texto_procesado = texto_validado
        for caracter_especial, reemplazo in CARACTERES_ESPECIALES.items():
            texto_procesado = texto_procesado.replace(caracter_especial, reemplazo)
        
        # Normalizar a NFD (Normalization Form Decomposed)
        # Esto separa los caracteres base de sus diacríticos
        texto_normalizado = unicodedata.normalize('NFD', texto_procesado)
        
        # Filtrar solo caracteres que NO sean marcas diacríticas
        # 'Mn' = Nonspacing_Mark (acentos, tildes, etc.)
        texto_sin_acentos = ''.join(
            caracter for caracter in texto_normalizado
            if unicodedata.category(caracter) != 'Mn'
        )
        
        return texto_sin_acentos
        
    except Exception as e:
        manejar_excepcion_texto(e, 'quitar_acentos', texto_validado) 