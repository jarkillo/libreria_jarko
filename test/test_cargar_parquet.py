import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os
import sys
import platform
import unittest.mock as mock

# Agregar el directorio padre al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent.parent))
from carga_datos import cargar_parquet


class TestCargarParquet:
    """Tests para la función cargar_parquet"""

    def setup_method(self):
        """Configurar archivos de test antes de cada test"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Crear archivo Parquet válido para tests exitosos
        self.parquet_valido = os.path.join(self.temp_dir, "test_valido.parquet")
        # Crear un DataFrame de ejemplo y guardarlo como Parquet
        df_ejemplo = pd.DataFrame({
            'nombre': ['Juan', 'Ana', 'Carlos'],
            'edad': [25, 30, 35],
            'ciudad': ['Madrid', 'Barcelona', 'Valencia'],
            'activo': [True, False, True]
        })
        try:
            df_ejemplo.to_parquet(self.parquet_valido)
            self.parquet_existe = True
        except ImportError:
            self.parquet_existe = False
        
        # Crear archivo Parquet vacío (simulado)
        self.parquet_vacio = os.path.join(self.temp_dir, "test_vacio.parquet")
        if self.parquet_existe:
            df_vacio = pd.DataFrame()
            try:
                df_vacio.to_parquet(self.parquet_vacio)
            except Exception:
                # Si no se puede crear Parquet vacío, crear archivo texto
                with open(self.parquet_vacio, 'w') as f:
                    f.write("")

    def teardown_method(self):
        """Limpiar archivos de test después de cada test"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_archivo_parquet_no_existe(self):
        """Test error: archivo parquet no existe"""
        with pytest.raises(FileNotFoundError, match="El archivo .* no existe"):
            cargar_parquet("archivo_inexistente.parquet")

    def test_tipo_ruta_parquet_invalido(self):
        """Test error: tipo de ruta inválido para parquet"""
        with pytest.raises(TypeError, match="El parámetro 'ruta' debe ser str o Path"):
            cargar_parquet(123)  # type: ignore

    def test_tipo_columns_invalido(self):
        """Test error: tipo de columns inválido"""
        ruta_parquet = os.path.join(self.temp_dir, "test.parquet")
        with open(ruta_parquet, 'w') as f:
            f.write("fake parquet")
        
        with pytest.raises(TypeError, match="El parámetro 'columns' debe ser lista o None"):
            cargar_parquet(ruta_parquet, columns="invalid")  # type: ignore

    def test_columns_elementos_no_string(self):
        """Test error: elementos de columns no son strings"""
        ruta_parquet = os.path.join(self.temp_dir, "test.parquet")
        with open(ruta_parquet, 'w') as f:
            f.write("fake parquet")
        
        with pytest.raises(TypeError, match="Todos los elementos de 'columns' deben ser strings"):
            cargar_parquet(ruta_parquet, columns=[123, "nombre"])  # type: ignore

    def test_archivo_no_es_parquet(self):
        """Test error: archivo no es parquet válido"""
        archivo_falso = os.path.join(self.temp_dir, "fake.parquet")
        with open(archivo_falso, 'w') as f:
            f.write("esto no es parquet")
        
        with pytest.raises(ValueError, match="no es un archivo Parquet válido"):
            cargar_parquet(archivo_falso)

    # TESTS ADICIONALES

    @pytest.mark.skipif(not hasattr(pd, 'read_parquet'), reason="pandas no tiene soporte para Parquet")
    def test_parquet_bien_formado_completo(self):
        """Test cargar Parquet bien formado completo"""
        if not self.parquet_existe:
            pytest.skip("PyArrow no disponible")
        
        df = cargar_parquet(self.parquet_valido)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert len(df.columns) == 4
        expected_columns = ['nombre', 'edad', 'ciudad', 'activo']
        assert all(col in df.columns for col in expected_columns)
        assert df.iloc[0]['nombre'] == 'Juan'
        assert df.iloc[1]['edad'] == 30

    @pytest.mark.skipif(not hasattr(pd, 'read_parquet'), reason="pandas no tiene soporte para Parquet")
    def test_parquet_bien_formado_columnas_especificas(self):
        """Test cargar Parquet con columnas específicas"""
        if not self.parquet_existe:
            pytest.skip("PyArrow no disponible")
        
        df = cargar_parquet(self.parquet_valido, columns=['nombre', 'edad'])
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert len(df.columns) == 2
        assert list(df.columns) == ['nombre', 'edad']
        assert df.iloc[0]['nombre'] == 'Juan'
        assert df.iloc[1]['edad'] == 30

    def test_parquet_columnas_inexistentes(self):
        """Test error: columnas inexistentes en parámetro columns"""
        if not self.parquet_existe:
            pytest.skip("PyArrow no disponible")
        
        with pytest.raises(ValueError, match="no existen en el archivo"):
            cargar_parquet(self.parquet_valido, columns=['nombre', 'columna_inexistente'])

    def test_parquet_sin_permisos(self):
        """Test error: archivo Parquet sin permisos"""
        if not self.parquet_existe:
            pytest.skip("PyArrow no disponible")
        
        if platform.system() == "Windows":
            pytest.skip("Permisos en Windows se manejan diferente")
        
        # Quitar permisos de lectura
        os.chmod(self.parquet_valido, 0o000)
        
        try:
            with pytest.raises(ValueError, match="No tienes permisos para leer el archivo"):
                cargar_parquet(self.parquet_valido)
        finally:
            # Restaurar permisos para cleanup
            os.chmod(self.parquet_valido, 0o644)

    def test_parquet_ruta_es_directorio(self):
        """Test error: la ruta es un directorio, no un archivo"""
        with pytest.raises(ValueError, match="La ruta .* no es un archivo válido"):
            cargar_parquet(self.temp_dir)

    def test_parquet_archivo_grande_memoria(self):
        """Test archivo Parquet muy grande para memoria"""
        if not self.parquet_existe:
            pytest.skip("PyArrow no disponible")
        
        # Usar mock para simular MemoryError
        with mock.patch('pandas.read_parquet') as mock_read_parquet:
            mock_read_parquet.side_effect = MemoryError("Insufficient memory")
            
            with pytest.raises(ValueError, match="es demasiado grande para cargar en memoria"):
                cargar_parquet(self.parquet_valido)

    def test_parquet_vacio(self):
        """Test error: archivo Parquet vacío"""
        # Crear archivo vacío
        parquet_vacio = os.path.join(self.temp_dir, "vacio.parquet")
        with open(parquet_vacio, 'w') as f:
            f.write("")
        
        with pytest.raises(ValueError, match="no es un archivo Parquet válido"):
            cargar_parquet(parquet_vacio)

    def test_parquet_esquema_inconsistente(self):
        """Test Parquet con esquema inconsistente"""
        # Crear archivo con formato incorrecto
        parquet_malo = os.path.join(self.temp_dir, "malo.parquet")
        with open(parquet_malo, 'wb') as f:
            f.write(b"PAR1\x00\x00\x00\x00")  # Header incorrecto
        
        with pytest.raises(ValueError, match="no es un archivo Parquet válido"):
            cargar_parquet(parquet_malo)

    def test_parquet_con_path_object(self):
        """Test cargar Parquet usando Path object"""
        if not self.parquet_existe:
            pytest.skip("PyArrow no disponible")
        
        df = cargar_parquet(Path(self.parquet_valido))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3

    def test_parquet_rutas_con_espacios(self):
        """Test: cargar_parquet debe manejar rutas con espacios al inicio y final"""
        # Agregar espacios a la ruta
        ruta_con_espacios_final = self.parquet_valido + "  "
        ruta_con_espacios_inicio = "  " + self.parquet_valido
        ruta_con_espacios_ambos = "  " + self.parquet_valido + "  "
        
        # Todas estas rutas deberían funcionar igual
        resultado1 = cargar_parquet(self.parquet_valido)
        resultado2 = cargar_parquet(ruta_con_espacios_final)
        resultado3 = cargar_parquet(ruta_con_espacios_inicio)
        resultado4 = cargar_parquet(ruta_con_espacios_ambos)
        
        # Verificar que todos los resultados sean iguales
        assert resultado1.equals(resultado2)
        assert resultado1.equals(resultado3)
        assert resultado1.equals(resultado4) 