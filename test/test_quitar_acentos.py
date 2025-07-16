import pytest
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent.parent))
from normalizacion_texto import quitar_acentos


class TestQuitarAcentos:
    """Tests para la función quitar_acentos"""

    def test_quitar_acentos_texto_basico(self):
        """Test básico de eliminación de acentos"""
        resultado = quitar_acentos("José María")
        assert resultado == "Jose Maria"

    def test_quitar_acentos_espanol(self):
        """Test con texto en español con múltiples acentos"""
        texto = "niño español con corazón"
        resultado = quitar_acentos(texto)
        assert resultado == "nino espanol con corazon"

    def test_quitar_acentos_vocales_acentuadas(self):
        """Test con todas las vocales acentuadas"""
        texto = "áéíóú ÁÉÍÓÚ"
        resultado = quitar_acentos(texto)
        assert resultado == "aeiou AEIOU"

    def test_quitar_acentos_caracteres_especiales(self):
        """Test con caracteres especiales como ñ, ç"""
        texto = "niño São Paulo Françoise"
        resultado = quitar_acentos(texto)
        assert resultado == "nino Sao Paulo Francoise"

    def test_quitar_acentos_otros_idiomas(self):
        """Test con caracteres de otros idiomas latinos"""
        texto = "Çà et là, naïve café résumé"
        resultado = quitar_acentos(texto)
        assert resultado == "Ca et la, naive cafe resume"

    def test_quitar_acentos_texto_sin_acentos(self):
        """Test con texto que no tiene acentos"""
        texto = "hello world 123"
        resultado = quitar_acentos(texto)
        assert resultado == "hello world 123"

    def test_quitar_acentos_string_vacio(self):
        """Test con string vacío"""
        resultado = quitar_acentos("")
        assert resultado == ""

    def test_quitar_acentos_solo_espacios(self):
        """Test con solo espacios"""
        resultado = quitar_acentos("   ")
        assert resultado == "   "

    def test_quitar_acentos_numeros(self):
        """Test convirtiendo números a string"""
        resultado = quitar_acentos(123)
        assert resultado == "123"

    def test_quitar_acentos_float(self):
        """Test convirtiendo float a string"""
        resultado = quitar_acentos(45.67)
        assert resultado == "45.67"

    def test_quitar_acentos_boolean(self):
        """Test convirtiendo boolean a string"""
        resultado = quitar_acentos(True)
        assert resultado == "True"

    def test_quitar_acentos_caracteres_no_latinos(self):
        """Test con caracteres no latinos (se mantienen)"""
        texto = "Москва 北京 العربية"
        resultado = quitar_acentos(texto)
        # Los caracteres no latinos se mantienen sin cambios
        assert resultado == "Москва 北京 العربية"

    def test_quitar_acentos_mixed_content(self):
        """Test con contenido mixto: latinos, no latinos, acentos, números"""
        texto = "José 123 Москва niña café 北京"
        resultado = quitar_acentos(texto)
        assert resultado == "Jose 123 Москва nina cafe 北京"

    def test_quitar_acentos_puntuacion_con_acentos(self):
        """Test con puntuación y acentos"""
        texto = "¿Cómo está usted? ¡Está fantástico!"
        resultado = quitar_acentos(texto)
        assert resultado == "¿Como esta usted? ¡Esta fantastico!"

    def test_quitar_acentos_none_input(self):
        """Test con input None - debe lanzar TypeError"""
        with pytest.raises(TypeError) as excinfo:
            quitar_acentos(None)
        assert "no puede ser None" in str(excinfo.value)

    def test_quitar_acentos_lista_como_input(self):
        """Test convirtiendo lista a string"""
        resultado = quitar_acentos(["José", "María"])
        assert "Jose" in resultado and "Maria" in resultado

    def test_quitar_acentos_diccionario_como_input(self):
        """Test convirtiendo diccionario a string"""
        resultado = quitar_acentos({"nombre": "José"})
        assert "Jose" in resultado

    def test_quitar_acentos_caracteres_especiales_unicode(self):
        """Test con caracteres unicode especiales con diacríticos"""
        texto = "Åbo Øresund Zürich"
        resultado = quitar_acentos(texto)
        assert resultado == "Abo Oresund Zurich"

    def test_quitar_acentos_texto_largo(self):
        """Test con texto largo para verificar performance"""
        texto = "á" * 1000 + "ñ" * 1000 + "ü" * 1000
        resultado = quitar_acentos(texto)
        assert resultado == "a" * 1000 + "n" * 1000 + "u" * 1000

    def test_quitar_acentos_caracteres_combinados(self):
        """Test con caracteres que combinan múltiples diacríticos"""
        # Algunos caracteres especiales que combinan múltiples marcas
        texto = "e\u0301\u0302"  # e con acento agudo y circunflejo
        resultado = quitar_acentos(texto)
        assert resultado == "e" 