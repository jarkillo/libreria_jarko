import pytest
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent.parent))
from normalizacion_texto import normalizar_caracteres


class TestNormalizarCaracteres:
    """Tests para la función normalizar_caracteres"""

    def test_normalizar_comillas_tipograficas(self):
        """Test básico normalizando comillas tipográficas"""
        resultado = normalizar_caracteres("Texto con \"comillas\" tipográficas")
        assert resultado == 'Texto con "comillas" tipográficas'

    def test_normalizar_apostrofes_tipograficos(self):
        """Test normalizando apostrofes tipográficos"""
        resultado = normalizar_caracteres("It's can't won't")
        assert resultado == "It's can't won't"

    def test_normalizar_guiones_largos(self):
        """Test normalizando guiones largos (em dash, en dash)"""
        resultado = normalizar_caracteres("Texto —con guiones– largos")
        assert resultado == "Texto -con guiones- largos"

    def test_normalizar_comillas_francesas(self):
        """Test normalizando comillas francesas"""
        resultado = normalizar_caracteres("«Texto» con comillas francesas")
        assert resultado == '"Texto" con comillas francesas'

    def test_normalizar_puntos_suspensivos(self):
        """Test normalizando puntos suspensivos (ellipsis)"""
        resultado = normalizar_caracteres("Texto… con puntos suspensivos")
        assert resultado == "Texto... con puntos suspensivos"

    def test_normalizar_bullets(self):
        """Test normalizando bullets y puntos medios"""
        resultado = normalizar_caracteres("Lista • item · otro")
        assert resultado == "Lista * item * otro"

    def test_normalizar_simbolos_matematicos(self):
        """Test normalizando símbolos matemáticos básicos"""
        resultado = normalizar_caracteres("3×4÷2±1")
        assert resultado == "3x4/2+/-1"

    def test_normalizar_monedas(self):
        """Test normalizando símbolos de monedas"""
        resultado = normalizar_caracteres("Precio: 25€, 10£, 100¥")
        assert resultado == "Precio: 25EUR, 10GBP, 100YEN"

    def test_normalizar_simbolos_comerciales(self):
        """Test normalizando símbolos comerciales"""
        resultado = normalizar_caracteres("Producto™ registrado® copyright©")
        assert resultado == "ProductoTM registradoR copyrightC"

    def test_normalizar_por_mille(self):
        """Test normalizando símbolo por mille"""
        resultado = normalizar_caracteres("Concentración: 5‰")
        assert resultado == "Concentración: 5%"

    def test_normalizar_espacios_especiales(self):
        """Test normalizando espacios especiales Unicode"""
        # Non-breaking space, thin space, etc.
        texto = "texto\u00A0con\u2009espacios\u2008especiales"
        resultado = normalizar_caracteres(texto)
        assert resultado == "texto con espacios especiales"

    def test_normalizar_espacios_zero_width(self):
        """Test eliminando espacios de ancho cero"""
        texto = "texto\u200bcon\u200bespacios\u200binvisibles"
        resultado = normalizar_caracteres(texto)
        assert resultado == "textoconespaciosinvisibles"

    def test_normalizar_texto_sin_caracteres_especiales(self):
        """Test con texto que no tiene caracteres especiales"""
        texto = "texto normal sin caracteres especiales"
        resultado = normalizar_caracteres(texto)
        assert resultado == texto

    def test_normalizar_string_vacio(self):
        """Test con string vacío"""
        resultado = normalizar_caracteres("")
        assert resultado == ""

    def test_normalizar_solo_espacios_normales(self):
        """Test con solo espacios normales"""
        resultado = normalizar_caracteres("   ")
        assert resultado == "   "

    def test_normalizar_numero_como_input(self):
        """Test convirtiendo número a string"""
        resultado = normalizar_caracteres(123)
        assert resultado == "123"

    def test_normalizar_float_como_input(self):
        """Test convirtiendo float a string"""
        resultado = normalizar_caracteres(45.67)
        assert resultado == "45.67"

    def test_normalizar_boolean_como_input(self):
        """Test convirtiendo boolean a string"""
        resultado = normalizar_caracteres(True)
        assert resultado == "True"

    def test_normalizar_none_input(self):
        """Test con input None - debe lanzar TypeError"""
        with pytest.raises(TypeError) as excinfo:
            normalizar_caracteres(None)
        assert "no puede ser None" in str(excinfo.value)

    def test_normalizar_con_reemplazos_personalizados(self):
        """Test con reemplazos personalizados"""
        reemplazos = {"José": "Jose", "María": "Maria"}
        resultado = normalizar_caracteres("José y María", reemplazos)
        assert resultado == "Jose y Maria"

    def test_normalizar_reemplazos_personalizados_sobrescriben(self):
        """Test que reemplazos personalizados sobrescriben los por defecto"""
        reemplazos = {"€": "EUROS"}
        resultado = normalizar_caracteres("Precio: 25€", reemplazos)
        assert resultado == "Precio: 25EUROS"

    def test_normalizar_reemplazos_personalizados_invalidos(self):
        """Test con reemplazos personalizados no válidos"""
        with pytest.raises(TypeError) as excinfo:
            normalizar_caracteres("texto", "no es diccionario")  # type: ignore
        assert "debe ser un diccionario" in str(excinfo.value)

    def test_normalizar_reemplazos_personalizados_none(self):
        """Test con reemplazos personalizados None (valor válido)"""
        resultado = normalizar_caracteres("Texto con €", None)
        assert resultado == "Texto con EUR"

    def test_normalizar_caracteres_control(self):
        """Test eliminando caracteres de control"""
        # Incluir algunos caracteres de control ASCII
        texto = "texto\x00con\x1Fcaracteres\x7Fcontrol"
        resultado = normalizar_caracteres(texto)
        assert resultado == "textoconcaracterescontrol"

    def test_normalizar_mix_completo(self):
        """Test con mix completo de caracteres especiales"""
        texto = "Texto \"especial\" con —guiones— y • bullets, 25€ ©2024"
        resultado = normalizar_caracteres(texto)
        assert resultado == 'Texto "especial" con -guiones- y * bullets, 25EUR C2024'

    def test_normalizar_lista_como_input(self):
        """Test convirtiendo lista a string"""
        resultado = normalizar_caracteres(["texto", "con", "€"])
        assert "EUR" in resultado

    def test_normalizar_caracteres_unicode_complejos(self):
        """Test con caracteres Unicode complejos"""
        texto = "Texto con \u2026 y \u2013 y \u201C comillas \u201D"
        resultado = normalizar_caracteres(texto)
        assert resultado == 'Texto con ... y - y " comillas "'

    def test_normalizar_preservar_acentos(self):
        """Test que la normalización preserva acentos (no los elimina)"""
        texto = "José María con € y —guiones—"
        resultado = normalizar_caracteres(texto)
        assert resultado == "José María con EUR y -guiones-"

    def test_normalizar_texto_largo(self):
        """Test con texto largo para verificar performance"""
        texto = "Texto" + "€" * 100 + "con" + "—" * 100 + "caracteres"
        resultado = normalizar_caracteres(texto)
        assert "EUR" * 100 in resultado
        assert "-" * 100 in resultado

    def test_normalizar_centavos(self):
        """Test normalizando símbolo de centavos"""
        resultado = normalizar_caracteres("Precio: 50¢")
        assert resultado == "Precio: 50cent"

    def test_normalizar_comas_especiales(self):
        """Test normalizando comas especiales tipográficas"""
        resultado = normalizar_caracteres("Texto‚ con comas„ especiales")
        assert resultado == 'Texto, con comas" especiales'