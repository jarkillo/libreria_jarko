"""
Tests para funciones utilitarias del módulo carga_datos.

Este módulo contiene tests para las funciones de utilidad como procesar_ruta.
"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

# Agregar el directorio parent para poder importar
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from carga_datos.utils import procesar_ruta


class TestProcesarRuta:
    """Test de la función procesar_ruta"""

    def setup_method(self):
        """Configurar archivos temporales para tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.archivo_test = os.path.join(self.temp_dir, "test.txt")
        
        # Crear archivo de prueba
        with open(self.archivo_test, 'w') as f:
            f.write("test content")
    
    def teardown_method(self):
        """Limpiar archivos temporales"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_procesar_ruta_string_sin_espacios(self):
        """Test: procesar_ruta con string sin espacios"""
        ruta_sin_espacios = self.archivo_test
        resultado = procesar_ruta(ruta_sin_espacios)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == self.archivo_test

    def test_procesar_ruta_string_con_espacios_final(self):
        """Test: procesar_ruta debe remover espacios al final"""
        ruta_con_espacios = self.archivo_test + "   "
        resultado = procesar_ruta(ruta_con_espacios)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == self.archivo_test

    def test_procesar_ruta_string_con_espacios_inicio(self):
        """Test: procesar_ruta debe remover espacios al inicio"""
        ruta_con_espacios = "   " + self.archivo_test
        resultado = procesar_ruta(ruta_con_espacios)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == self.archivo_test

    def test_procesar_ruta_string_con_espacios_ambos_lados(self):
        """Test: procesar_ruta debe remover espacios en ambos lados"""
        ruta_con_espacios = "   " + self.archivo_test + "   "
        resultado = procesar_ruta(ruta_con_espacios)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == self.archivo_test

    def test_procesar_ruta_path_object_sin_espacios(self):
        """Test: procesar_ruta con objeto Path sin espacios"""
        ruta_path = Path(self.archivo_test)
        resultado = procesar_ruta(ruta_path)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == self.archivo_test

    def test_procesar_ruta_path_object_con_espacios_final(self):
        """Test: procesar_ruta con objeto Path con espacios al final"""
        ruta_con_espacios = Path(self.archivo_test + "   ")
        resultado = procesar_ruta(ruta_con_espacios)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == self.archivo_test

    def test_procesar_ruta_path_object_con_espacios_inicio(self):
        """Test: procesar_ruta con objeto Path con espacios al inicio"""
        ruta_con_espacios = Path("   " + self.archivo_test)
        resultado = procesar_ruta(ruta_con_espacios)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == self.archivo_test

    def test_procesar_ruta_path_object_con_espacios_ambos_lados(self):
        """Test: procesar_ruta con objeto Path con espacios en ambos lados"""
        ruta_con_espacios = Path("   " + self.archivo_test + "   ")
        resultado = procesar_ruta(ruta_con_espacios)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == self.archivo_test

    def test_procesar_ruta_mantiene_ruta_relativa(self):
        """Test: procesar_ruta debe mantener rutas relativas"""
        ruta_relativa = "carpeta/archivo.txt"
        resultado = procesar_ruta(ruta_relativa)
        
        assert isinstance(resultado, Path)
        # Normalizar ambas rutas para comparación multiplataforma
        assert os.path.normpath(str(resultado)) == os.path.normpath(ruta_relativa)

    def test_procesar_ruta_mantiene_ruta_absoluta(self):
        """Test: procesar_ruta debe mantener rutas absolutas"""
        ruta_absoluta = self.archivo_test
        resultado = procesar_ruta(ruta_absoluta)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == ruta_absoluta
        assert resultado.is_absolute()

    def test_procesar_ruta_espacios_solo_espacios(self):
        """Test: procesar_ruta con solo espacios debe retornar Path vacío o punto"""
        ruta_solo_espacios = "    "
        resultado = procesar_ruta(ruta_solo_espacios)
        
        assert isinstance(resultado, Path)
        # En Windows, Path("") se convierte a ".", que es comportamiento esperado
        assert str(resultado) in ["", "."]

    def test_procesar_ruta_string_vacio(self):
        """Test: procesar_ruta con string vacío debe retornar Path vacío o punto"""
        ruta_vacia = ""
        resultado = procesar_ruta(ruta_vacia)
        
        assert isinstance(resultado, Path)
        # En Windows, Path("") se convierte a ".", que es comportamiento esperado
        assert str(resultado) in ["", "."]

    def test_procesar_ruta_espacios_internos_preservados(self):
        """Test: procesar_ruta debe preservar espacios internos en nombres de archivo"""
        # Crear archivo con espacios en el nombre
        archivo_con_espacios = os.path.join(self.temp_dir, "archivo con espacios.txt")
        with open(archivo_con_espacios, 'w') as f:
            f.write("contenido")
        
        ruta_con_espacios_internos = "   " + archivo_con_espacios + "   "
        resultado = procesar_ruta(ruta_con_espacios_internos)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == archivo_con_espacios

    def test_procesar_ruta_tipos_entrada_correctos(self):
        """Test: procesar_ruta debe aceptar solo str o Path"""
        # Tipo correcto str
        resultado_str = procesar_ruta(self.archivo_test)
        assert isinstance(resultado_str, Path)
        
        # Tipo correcto Path
        resultado_path = procesar_ruta(Path(self.archivo_test))
        assert isinstance(resultado_path, Path)
        
        # Tipo incorrecto
        with pytest.raises(TypeError, match="debe ser str o Path"):
            procesar_ruta(123)  # type: ignore
        
        with pytest.raises(TypeError, match="debe ser str o Path"):
            procesar_ruta(["lista"])  # type: ignore

    def test_procesar_ruta_caracteres_especiales(self):
        """Test: procesar_ruta debe manejar caracteres especiales"""
        # Crear archivo con caracteres especiales
        archivo_especial = os.path.join(self.temp_dir, "archivo_especial!@#.txt")
        with open(archivo_especial, 'w') as f:
            f.write("contenido")
        
        ruta_especial = "   " + archivo_especial + "   "
        resultado = procesar_ruta(ruta_especial)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == archivo_especial

    def test_procesar_ruta_rutas_con_puntos(self):
        """Test: procesar_ruta debe manejar rutas con puntos (relativas)"""
        ruta_con_puntos = "./carpeta/../archivo.txt"
        resultado = procesar_ruta(ruta_con_puntos)
        
        assert isinstance(resultado, Path)
        # Normalizar ambas rutas para comparación multiplataforma
        # En Windows, Path normaliza automáticamente las rutas
        resultado_normalizado = os.path.normpath(str(resultado))
        esperado_normalizado = os.path.normpath(ruta_con_puntos)
        assert resultado_normalizado == esperado_normalizado

    def test_procesar_ruta_multiples_espacios_consecutivos(self):
        """Test: procesar_ruta debe eliminar múltiples espacios consecutivos"""
        ruta_multiples_espacios = "     " + self.archivo_test + "     "
        resultado = procesar_ruta(ruta_multiples_espacios)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == self.archivo_test

    def test_procesar_ruta_tabs_y_espacios(self):
        """Test: procesar_ruta debe eliminar tabs y espacios"""
        ruta_tabs_espacios = "\t\t   " + self.archivo_test + "   \t\t"
        resultado = procesar_ruta(ruta_tabs_espacios)
        
        assert isinstance(resultado, Path)
        assert str(resultado) == self.archivo_test 


class TestManejarExcepcionInesperada:
    """Tests para la función manejar_excepcion_inesperada"""

    def test_manejar_excepcion_inesperada_re_lanza(self):
        """Test: verificar que manejar_excepcion_inesperada re-lanza la excepción original"""
        from carga_datos.utils import manejar_excepcion_inesperada
        from unittest.mock import patch
        
        excepcion_original = ValueError("Error de prueba")
        
        with patch('logging.warning') as mock_warning:
            with pytest.raises(ValueError, match="Error de prueba"):
                manejar_excepcion_inesperada(excepcion_original, 'test_funcion')
            
            # Verificar que se registró en el log
            mock_warning.assert_called_once()
            llamada_args = mock_warning.call_args[0][0]
            assert "Excepción inesperada en test_funcion" in llamada_args
            assert "ValueError" in llamada_args
            assert "Error de prueba" in llamada_args

    def test_manejar_excepcion_inesperada_formato_log(self):
        """Test: verificar el formato correcto del mensaje de log"""
        from carga_datos.utils import manejar_excepcion_inesperada
        from unittest.mock import patch
        
        excepcion_test = RuntimeError("Excepción de ejemplo")
        
        with patch('logging.warning') as mock_warning:
            with pytest.raises(RuntimeError):
                manejar_excepcion_inesperada(excepcion_test, 'cargar_ejemplo')
            
            # Verificar formato específico del log
            mock_warning.assert_called_once_with(
                "Excepción inesperada en cargar_ejemplo: RuntimeError: Excepción de ejemplo"
            )