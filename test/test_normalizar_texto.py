import pytest
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent.parent))
from normalizacion_texto import normalizar_texto


class TestNormalizarTexto:
    """Tests para la función principal normalizar_texto"""

    def test_normalizar_texto_completo_defecto(self):
        """Test básico con todas las normalizaciones por defecto"""
        texto = "  José María —texto con \"comillas\" y ñ  "
        resultado = normalizar_texto(texto)
        assert resultado == 'jose maria -texto con "comillas" y n'

    def test_normalizar_texto_solo_quitar_acentos(self):
        """Test activando solo la eliminación de acentos"""
        texto = "José María"
        resultado = normalizar_texto(
            texto,
            quitar_acentos_flag=True,
            convertir_minusculas=False,
            limpiar_espacios_flag=False,
            normalizar_caracteres_flag=False
        )
        assert resultado == "Jose Maria"

    def test_normalizar_texto_solo_minusculas(self):
        """Test activando solo conversión a minúsculas"""
        texto = "JOSÉ MARÍA"
        resultado = normalizar_texto(
            texto,
            quitar_acentos_flag=False,
            convertir_minusculas=True,
            limpiar_espacios_flag=False,
            normalizar_caracteres_flag=False
        )
        assert resultado == "josé maría"

    def test_normalizar_texto_preservar_mayusculas(self):
        """Test preservando mayúsculas"""
        texto = "José MARÍA"
        resultado = normalizar_texto(
            texto,
            quitar_acentos_flag=True,
            preservar_mayusculas=True,
            limpiar_espacios_flag=False,
            normalizar_caracteres_flag=False
        )
        assert resultado == "Jose MARIA"

    def test_normalizar_texto_solo_espacios(self):
        """Test activando solo limpieza de espacios"""
        texto = "  josé   maría  "
        resultado = normalizar_texto(
            texto,
            quitar_acentos_flag=False,
            convertir_minusculas=False,
            limpiar_espacios_flag=True,
            normalizar_caracteres_flag=False
        )
        assert resultado == "josé maría"

    def test_normalizar_texto_solo_caracteres(self):
        """Test activando solo normalización de caracteres"""
        texto = "José María —con \"comillas\""
        resultado = normalizar_texto(
            texto,
            quitar_acentos_flag=False,
            convertir_minusculas=False,
            limpiar_espacios_flag=False,
            normalizar_caracteres_flag=True
        )
        assert resultado == 'José María -con "comillas"'

    def test_normalizar_texto_reemplazos_personalizados(self):
        """Test con reemplazos personalizados"""
        texto = "José María ©2024"
        reemplazos = {"©": "(c)"}
        resultado = normalizar_texto(
            texto,
            reemplazos_personalizados=reemplazos
        )
        assert resultado == "jose maria (c)2024"

    def test_normalizar_string_vacio(self):
        """Test con string vacío"""
        resultado = normalizar_texto("")
        assert resultado == ""

    def test_normalizar_solo_espacios(self):
        """Test con solo espacios"""
        resultado = normalizar_texto("   ")
        assert resultado == ""

    def test_normalizar_numero_como_input(self):
        """Test convirtiendo número a string"""
        resultado = normalizar_texto(123)
        assert resultado == "123"

    def test_normalizar_none_input(self):
        """Test con input None - debe lanzar TypeError"""
        with pytest.raises(TypeError) as excinfo:
            normalizar_texto(None)
        assert "no puede ser None" in str(excinfo.value)

    def test_normalizar_parametros_incorrectos_booleanos(self):
        """Test con parámetros booleanos incorrectos"""
        with pytest.raises(TypeError) as excinfo:
            normalizar_texto("texto", quitar_acentos_flag="si")  # type: ignore
        assert "debe ser bool" in str(excinfo.value)

    def test_normalizar_reemplazos_personalizados_invalidos(self):
        """Test con reemplazos personalizados inválidos"""
        with pytest.raises(TypeError) as excinfo:
            normalizar_texto("texto", reemplazos_personalizados="invalido")  # type: ignore
        assert "debe ser un diccionario" in str(excinfo.value) 