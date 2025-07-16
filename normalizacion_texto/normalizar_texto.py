"""
Módulo principal de normalización integral de texto.

Este módulo contiene la función principal normalizar_texto() que combina
todas las funciones de normalización en una sola operación configurable.
"""

from typing import Any, Dict, Optional
from .quitar_acentos import quitar_acentos
from .convertir_case import convertir_a_minusculas, convertir_a_mayusculas
from .limpiar_espacios import limpiar_espacios
from .normalizar_caracteres import normalizar_caracteres
from .utils import validar_entrada_texto, manejar_excepcion_texto


def normalizar_texto(
    texto: Any,
    quitar_acentos_flag: bool = True,
    convertir_minusculas: bool = True,
    limpiar_espacios_flag: bool = True,
    normalizar_caracteres_flag: bool = True,
    reemplazos_personalizados: Optional[Dict[str, str]] = None,
    preservar_mayusculas: bool = False
) -> str:
    """
    Normaliza texto aplicando múltiples transformaciones de forma configurable.

    Esta función principal combina todas las funciones de normalización disponibles,
    permitiendo activar/desactivar cada transformación según las necesidades.

    Parámetros:
    ----------
    texto : Any
        El texto a normalizar. Se convertirá a string si no lo es.
    quitar_acentos_flag : bool, opcional
        Si aplicar eliminación de acentos (por defecto True).
    convertir_minusculas : bool, opcional
        Si convertir a minúsculas (por defecto True).
    limpiar_espacios_flag : bool, opcional
        Si aplicar limpieza de espacios (por defecto True).
    normalizar_caracteres_flag : bool, opcional
        Si aplicar normalización de caracteres especiales (por defecto True).
    reemplazos_personalizados : Dict[str, str], opcional
        Reemplazos adicionales a aplicar en normalizar_caracteres.
    preservar_mayusculas : bool, opcional
        Si preservar mayúsculas (anula convertir_minusculas) (por defecto False).

    Retorna:
    -------
    str
        El texto completamente normalizado según las opciones especificadas.

    Errores:
    -------
    TypeError
        Si los parámetros no son del tipo correcto.
    ValueError
        Si el texto está vacío o es solo espacios.

    Ejemplos:
    --------
    >>> normalizar_texto("  José María —texto con \"comillas\"  ")
    'jose maria -texto con "comillas"'

    >>> normalizar_texto("TEXTO", convertir_minusculas=False)
    'TEXTO'

    >>> normalizar_texto("José MARÍA", preservar_mayusculas=True)
    'Jose MARIA'
    """
    # Validar entrada principal
    texto_validado = validar_entrada_texto(texto, 'normalizar_texto')

    # Validar parámetros booleanos
    if not isinstance(quitar_acentos_flag, bool):
        raise TypeError("El parámetro 'quitar_acentos_flag' debe ser bool")

    if not isinstance(convertir_minusculas, bool):
        raise TypeError("El parámetro 'convertir_minusculas' debe ser bool")

    if not isinstance(limpiar_espacios_flag, bool):
        raise TypeError("El parámetro 'limpiar_espacios_flag' debe ser bool")

    if not isinstance(normalizar_caracteres_flag, bool):
        raise TypeError("El parámetro 'normalizar_caracteres_flag' debe ser bool")

    if not isinstance(preservar_mayusculas, bool):
        raise TypeError("El parámetro 'preservar_mayusculas' debe ser bool")

    # Validar reemplazos personalizados
    if reemplazos_personalizados is not None:
        if not isinstance(reemplazos_personalizados, dict):
            raise TypeError("El parámetro 'reemplazos_personalizados' debe ser un diccionario")

    try:
        texto_resultado = texto_validado

        # 1. Normalizar caracteres especiales (antes que quitar acentos)
        if normalizar_caracteres_flag:
            texto_resultado = normalizar_caracteres(texto_resultado, reemplazos_personalizados)

        # 2. Quitar acentos
        if quitar_acentos_flag:
            texto_resultado = quitar_acentos(texto_resultado)

        # 3. Convertir caso (si no se preservan mayúsculas)
        if not preservar_mayusculas and convertir_minusculas:
            texto_resultado = convertir_a_minusculas(texto_resultado)

        # 4. Limpiar espacios (al final para limpiar cualquier espacio extra)
        if limpiar_espacios_flag:
            texto_resultado = limpiar_espacios(texto_resultado)

        return texto_resultado

    except Exception as e:
        manejar_excepcion_texto(e, 'normalizar_texto', texto_validado)