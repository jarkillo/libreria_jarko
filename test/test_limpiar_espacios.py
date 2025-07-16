import pytest
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent.parent))
from normalizacion_texto import limpiar_espacios


class TestLimpiarEspacios:
    """Tests para la función limpiar_espacios"""

    def test_limpiar_espacios_inicio_fin(self):
        """Test básico eliminando espacios al inicio y final"""
        resultado = limpiar_espacios("  hola mundo  ")
        assert resultado == "hola mundo"

    def test_limpiar_espacios_multiples_medio(self):
        """Test eliminando múltiples espacios en el medio"""
        resultado = limpiar_espacios("hola    mundo")
        assert resultado == "hola mundo"

    def test_limpiar_espacios_mixtos(self):
        """Test con espacios al inicio, final y múltiples en medio"""
        resultado = limpiar_espacios("  hola   mundo   ")
        assert resultado == "hola mundo"

    def test_limpiar_tabulaciones(self):
        """Test convirtiendo tabulaciones a espacios"""
        resultado = limpiar_espacios("hola\tmundo\ttexto")
        assert resultado == "hola mundo texto"

    def test_limpiar_saltos_linea(self):
        """Test convirtiendo saltos de línea a espacios"""
        resultado = limpiar_espacios("hola\nmundo\ntexto")
        assert resultado == "hola mundo texto"

    def test_limpiar_espacios_mixed_whitespace(self):
        """Test con mix de espacios, tabs y saltos de línea"""
        resultado = limpiar_espacios("  hola\t\nmundo  \n\ttexto  ")
        assert resultado == "hola mundo texto"

    def test_limpiar_espacios_puntuacion_comas(self):
        """Test limpiando espacios alrededor de comas"""
        resultado = limpiar_espacios("hola , mundo , texto")
        assert resultado == "hola, mundo, texto"

    def test_limpiar_espacios_puntuacion_punto_coma(self):
        """Test limpiando espacios alrededor de punto y coma"""
        resultado = limpiar_espacios("hola ; mundo ; texto")
        assert resultado == "hola; mundo; texto"

    def test_limpiar_espacios_puntuacion_dos_puntos(self):
        """Test limpiando espacios alrededor de dos puntos"""
        resultado = limpiar_espacios("titulo : contenido")
        assert resultado == "titulo: contenido"

    def test_limpiar_espacios_puntuacion_punto(self):
        """Test limpiando espacios antes de puntos"""
        resultado = limpiar_espacios("Hola mundo .")
        assert resultado == "Hola mundo."

    def test_limpiar_espacios_signos_exclamacion(self):
        """Test limpiando espacios antes de signos de exclamación"""
        resultado = limpiar_espacios("¡Hola mundo !")
        assert resultado == "¡Hola mundo!"

    def test_limpiar_espacios_signos_interrogacion(self):
        """Test limpiando espacios antes de signos de interrogación"""
        resultado = limpiar_espacios("¿Cómo estás ?")
        assert resultado == "¿Cómo estás?"

    def test_limpiar_espacios_parentesis(self):
        """Test limpiando espacios alrededor de paréntesis"""
        resultado = limpiar_espacios("texto ( contenido ) final")
        assert resultado == "texto (contenido) final"

    def test_limpiar_espacios_corchetes(self):
        """Test limpiando espacios alrededor de corchetes"""
        resultado = limpiar_espacios("texto [ contenido ] final")
        assert resultado == "texto [contenido] final"

    def test_limpiar_espacios_llaves(self):
        """Test limpiando espacios alrededor de llaves"""
        resultado = limpiar_espacios("texto { contenido } final")
        assert resultado == "texto {contenido} final"

    def test_limpiar_espacios_puntuacion_multiple(self):
        """Test con múltiples tipos de puntuación"""
        resultado = limpiar_espacios("hola , mundo ; texto : final .")
        assert resultado == "hola, mundo; texto: final."

    def test_limpiar_string_vacio(self):
        """Test con string vacío"""
        resultado = limpiar_espacios("")
        assert resultado == ""

    def test_limpiar_solo_espacios(self):
        """Test con solo espacios"""
        resultado = limpiar_espacios("     ")
        assert resultado == ""

    def test_limpiar_solo_tabs_y_saltos(self):
        """Test con solo tabulaciones y saltos de línea"""
        resultado = limpiar_espacios("\t\n\t\n")
        assert resultado == ""

    def test_limpiar_texto_sin_espacios_extra(self):
        """Test con texto que ya está bien formateado"""
        resultado = limpiar_espacios("texto bien formateado")
        assert resultado == "texto bien formateado"

    def test_limpiar_numero_como_input(self):
        """Test convirtiendo número a string"""
        resultado = limpiar_espacios(123)
        assert resultado == "123"

    def test_limpiar_float_como_input(self):
        """Test convirtiendo float a string"""
        resultado = limpiar_espacios(45.67)
        assert resultado == "45.67"

    def test_limpiar_boolean_como_input(self):
        """Test convirtiendo boolean a string"""
        resultado = limpiar_espacios(True)
        assert resultado == "True"

    def test_limpiar_none_input(self):
        """Test con input None - debe lanzar TypeError"""
        with pytest.raises(TypeError) as excinfo:
            limpiar_espacios(None)
        assert "no puede ser None" in str(excinfo.value)

    def test_limpiar_lista_como_input(self):
        """Test convirtiendo lista a string y limpiando"""
        resultado = limpiar_espacios(["hola", "mundo"])
        # Resultado depende de la representación string de la lista
        assert "hola" in resultado and "mundo" in resultado

    def test_limpiar_espacios_extremo(self):
        """Test con caso extremo de muchos espacios consecutivos"""
        resultado = limpiar_espacios("   hola          mundo     ")
        assert resultado == "hola mundo"

    def test_limpiar_texto_con_acentos_y_espacios(self):
        """Test que la función preserva acentos mientras limpia espacios"""
        resultado = limpiar_espacios("  José   María  ")
        assert resultado == "José María"

    def test_limpiar_espacios_unicode_especiales(self):
        """Test con diferentes tipos de espacios Unicode"""
        # Non-breaking space y otros espacios especiales
        texto = "hola\u00A0mundo\u2009texto"  # Non-breaking space + thin space
        resultado = limpiar_espacios(texto)
        assert resultado == "hola mundo texto"

    def test_limpiar_puntuacion_compleja(self):
        """Test con puntuación compleja y espacios"""
        resultado = limpiar_espacios("Hola , mundo ; ¿cómo estás ? ¡Bien !")
        assert resultado == "Hola, mundo; ¿cómo estás? ¡Bien!"

    def test_limpiar_conservar_espacios_necesarios(self):
        """Test que conserva espacios necesarios entre palabras"""
        resultado = limpiar_espacios("una dos tres cuatro")
        assert resultado == "una dos tres cuatro"

    def test_limpiar_texto_con_numeros_y_espacios(self):
        """Test con números y espacios mixtos"""
        resultado = limpiar_espacios("  123   +   456   =   579  ")
        assert resultado == "123 + 456 = 579"