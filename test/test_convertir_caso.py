import pytest
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent.parent))
from normalizacion_texto import convertir_a_minusculas, convertir_a_mayusculas


class TestConvertirAMinusculas:
    """Tests para la función convertir_a_minusculas"""

    def test_convertir_mayusculas_a_minusculas(self):
        """Test básico de conversión de mayúsculas a minúsculas"""
        resultado = convertir_a_minusculas("HOLA MUNDO")
        assert resultado == "hola mundo"

    def test_convertir_texto_mixto(self):
        """Test con texto en caso mixto"""
        resultado = convertir_a_minusculas("HoLa MuNdO")
        assert resultado == "hola mundo"

    def test_convertir_ya_en_minusculas(self):
        """Test con texto ya en minúsculas"""
        resultado = convertir_a_minusculas("hola mundo")
        assert resultado == "hola mundo"

    def test_convertir_con_acentos_mayusculas(self):
        """Test con acentos en mayúsculas"""
        resultado = convertir_a_minusculas("JOSÉ MARÍA")
        assert resultado == "josé maría"

    def test_convertir_con_numeros(self):
        """Test con números (se mantienen igual)"""
        resultado = convertir_a_minusculas("TEXTO123")
        assert resultado == "texto123"

    def test_convertir_con_puntuacion(self):
        """Test con signos de puntuación"""
        resultado = convertir_a_minusculas("¡HOLA! ¿CÓMO ESTÁS?")
        assert resultado == "¡hola! ¿cómo estás?"

    def test_convertir_string_vacio(self):
        """Test con string vacío"""
        resultado = convertir_a_minusculas("")
        assert resultado == ""

    def test_convertir_solo_espacios(self):
        """Test con solo espacios"""
        resultado = convertir_a_minusculas("   ")
        assert resultado == "   "

    def test_convertir_numero_a_minusculas(self):
        """Test convirtiendo número a string y luego a minúsculas"""
        resultado = convertir_a_minusculas(123)
        assert resultado == "123"

    def test_convertir_float_a_minusculas(self):
        """Test convirtiendo float a string"""
        resultado = convertir_a_minusculas(45.67)
        assert resultado == "45.67"

    def test_convertir_boolean_a_minusculas(self):
        """Test convirtiendo boolean a string"""
        resultado = convertir_a_minusculas(True)
        assert resultado == "true"

    def test_convertir_none_input_minusculas(self):
        """Test con input None - debe lanzar TypeError"""
        with pytest.raises(TypeError) as excinfo:
            convertir_a_minusculas(None)
        assert "no puede ser None" in str(excinfo.value)

    def test_convertir_caracteres_no_latinos_minusculas(self):
        """Test con caracteres no latinos"""
        resultado = convertir_a_minusculas("МОСКВА 北京")
        assert resultado == "москва 北京"  # Solo cambian los que tienen minúsculas

    def test_convertir_lista_a_minusculas(self):
        """Test convirtiendo lista a string"""
        resultado = convertir_a_minusculas(["HOLA", "MUNDO"])
        assert "hola" in resultado and "mundo" in resultado


class TestConvertirAMayusculas:
    """Tests para la función convertir_a_mayusculas"""

    def test_convertir_minusculas_a_mayusculas(self):
        """Test básico de conversión de minúsculas a mayúsculas"""
        resultado = convertir_a_mayusculas("hola mundo")
        assert resultado == "HOLA MUNDO"

    def test_convertir_texto_mixto_mayusculas(self):
        """Test con texto en caso mixto"""
        resultado = convertir_a_mayusculas("HoLa MuNdO")
        assert resultado == "HOLA MUNDO"

    def test_convertir_ya_en_mayusculas(self):
        """Test con texto ya en mayúsculas"""
        resultado = convertir_a_mayusculas("HOLA MUNDO")
        assert resultado == "HOLA MUNDO"

    def test_convertir_con_acentos_minusculas(self):
        """Test con acentos en minúsculas"""
        resultado = convertir_a_mayusculas("josé maría")
        assert resultado == "JOSÉ MARÍA"

    def test_convertir_con_numeros_mayusculas(self):
        """Test con números (se mantienen igual)"""
        resultado = convertir_a_mayusculas("texto123")
        assert resultado == "TEXTO123"

    def test_convertir_con_puntuacion_mayusculas(self):
        """Test con signos de puntuación"""
        resultado = convertir_a_mayusculas("¡hola! ¿cómo estás?")
        assert resultado == "¡HOLA! ¿CÓMO ESTÁS?"

    def test_convertir_string_vacio_mayusculas(self):
        """Test con string vacío"""
        resultado = convertir_a_mayusculas("")
        assert resultado == ""

    def test_convertir_solo_espacios_mayusculas(self):
        """Test con solo espacios"""
        resultado = convertir_a_mayusculas("   ")
        assert resultado == "   "

    def test_convertir_numero_a_mayusculas(self):
        """Test convirtiendo número a string"""
        resultado = convertir_a_mayusculas(123)
        assert resultado == "123"

    def test_convertir_float_a_mayusculas(self):
        """Test convirtiendo float a string"""
        resultado = convertir_a_mayusculas(45.67)
        assert resultado == "45.67"

    def test_convertir_boolean_a_mayusculas(self):
        """Test convirtiendo boolean a string"""
        resultado = convertir_a_mayusculas(False)
        assert resultado == "FALSE"

    def test_convertir_none_input_mayusculas(self):
        """Test con input None - debe lanzar TypeError"""
        with pytest.raises(TypeError) as excinfo:
            convertir_a_mayusculas(None)
        assert "no puede ser None" in str(excinfo.value)

    def test_convertir_caracteres_no_latinos_mayusculas(self):
        """Test con caracteres no latinos"""
        resultado = convertir_a_mayusculas("москва 北京")
        assert resultado == "МОСКВА 北京"  # Solo cambian los que tienen mayúsculas

    def test_convertir_lista_a_mayusculas(self):
        """Test convirtiendo lista a string"""
        resultado = convertir_a_mayusculas(["hola", "mundo"])
        assert "HOLA" in resultado and "MUNDO" in resultado

    def test_convertir_caracteres_especiales_mayusculas(self):
        """Test con caracteres especiales que tienen versión mayúscula"""
        resultado = convertir_a_mayusculas("ñáéíóú")
        assert resultado == "ÑÁÉÍÓÚ"

    def test_convertir_simbolos_matematicos(self):
        """Test que símbolos matemáticos se mantienen"""
        resultado = convertir_a_mayusculas("texto + números = resultado")
        assert resultado == "TEXTO + NÚMEROS = RESULTADO"