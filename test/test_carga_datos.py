import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent.parent))
from carga_datos import cargar_csv


class TestCargarCsv:
    """Tests para la función cargar_csv"""

    def setup_method(self):
        """Configurar archivos de test antes de cada test"""
        # Crear directorio temporal para tests
        self.temp_dir = tempfile.mkdtemp()
        
        # Crear archivo CSV válido con punto y coma
        self.csv_valido = os.path.join(self.temp_dir, "test_valido.csv")
        with open(self.csv_valido, 'w', encoding='utf-8') as f:
            f.write("nombre;edad;ciudad\n")
            f.write("Juan;25;Madrid\n")
            f.write("Ana;30;Barcelona\n")
        
        # Crear archivo CSV con comas
        self.csv_comas = os.path.join(self.temp_dir, "test_comas.csv")
        with open(self.csv_comas, 'w', encoding='utf-8') as f:
            f.write("nombre,edad,ciudad\n")
            f.write("Juan,25,Madrid\n")
            f.write("Ana,30,Barcelona\n")
        
        # Crear archivo CSV vacío
        self.csv_vacio = os.path.join(self.temp_dir, "test_vacio.csv")
        with open(self.csv_vacio, 'w', encoding='utf-8') as f:
            f.write("")
        
        # Crear archivo con encoding latin1
        self.csv_latin1 = os.path.join(self.temp_dir, "test_latin1.csv")
        with open(self.csv_latin1, 'w', encoding='latin1') as f:
            f.write("nombre;edad;ciudad\n")
            f.write("José;25;Córdoba\n")
        
        # Crear archivo con contenido malformado
        self.csv_malformado = os.path.join(self.temp_dir, "test_malformado.csv")
        with open(self.csv_malformado, 'w', encoding='utf-8') as f:
            f.write("nombre;edad;ciudad\n")
            f.write("Juan;25;Madrid;extra_columna\n")
            f.write("Ana;30\n")  # Faltan columnas

    def teardown_method(self):
        """Limpiar archivos de test después de cada test"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_cargar_csv_valido(self):
        """Test caso exitoso: cargar CSV válido con separador por defecto"""
        df = cargar_csv(self.csv_valido)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["nombre", "edad", "ciudad"]
        assert df.iloc[0]["nombre"] == "Juan"
        assert df.iloc[0]["edad"] == 25
        assert df.iloc[1]["nombre"] == "Ana"

    def test_cargar_csv_con_comas(self):
        """Test caso exitoso: cargar CSV con separador de comas"""
        df = cargar_csv(self.csv_comas, sep=",")
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["nombre", "edad", "ciudad"]
        assert df.iloc[0]["nombre"] == "Juan"

    def test_cargar_csv_con_path_object(self):
        """Test caso exitoso: cargar CSV usando Path object"""
        df = cargar_csv(Path(self.csv_valido))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2

    def test_cargar_csv_con_encoding_latin1(self):
        """Test caso exitoso: cargar CSV con encoding latin1"""
        df = cargar_csv(self.csv_latin1, encoding="latin1")
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert df.iloc[0]["nombre"] == "José"

    def test_archivo_no_existe(self):
        """Test error: archivo no existe"""
        with pytest.raises(FileNotFoundError, match="El archivo .* no existe"):
            cargar_csv("archivo_inexistente.csv")

    def test_ruta_es_directorio(self):
        """Test error: la ruta es un directorio, no un archivo"""
        with pytest.raises(ValueError, match="La ruta .* no es un archivo válido"):
            cargar_csv(self.temp_dir)

    def test_tipo_ruta_invalido(self):
        """Test error: tipo de ruta inválido"""
        # Nota: usamos type: ignore para evitar errores de linter intencionalmente
        with pytest.raises(TypeError, match="El parámetro 'ruta' debe ser str o Path"):
            cargar_csv(123)  # type: ignore  # Pasar int en lugar de str/Path

    def test_tipo_separador_invalido(self):
        """Test error: tipo de separador inválido"""
        # Nota: usamos type: ignore para evitar errores de linter intencionalmente
        with pytest.raises(TypeError, match="El parámetro 'sep' debe ser str"):
            cargar_csv(self.csv_valido, sep=123)  # type: ignore  # Pasar int en lugar de str

    def test_tipo_encoding_invalido(self):
        """Test error: tipo de encoding inválido"""
        # Nota: usamos type: ignore para evitar errores de linter intencionalmente
        with pytest.raises(TypeError, match="El parámetro 'encoding' debe ser str"):
            cargar_csv(self.csv_valido, encoding=123)  # type: ignore  # Pasar int en lugar de str

    def test_encoding_incorrecto(self):
        """Test error: encoding incorrecto"""
        with pytest.raises(ValueError, match="No se pudo leer el archivo .* con codificación"):
            cargar_csv(self.csv_latin1, encoding="utf-8")

    def test_archivo_vacio(self):
        """Test error: archivo vacío"""
        with pytest.raises(ValueError, match="El archivo .* está vacío"):
            cargar_csv(self.csv_vacio)

    def test_separador_incorrecto(self):
        """Test error: separador incorrecto causa problemas de parseo"""
        # Este test puede variar dependiendo de cómo pandas maneja el separador incorrecto
        # En algunos casos podría no fallar, sino crear un DataFrame con una sola columna
        df = cargar_csv(self.csv_valido, sep=",")
        # Con separador incorrecto, todo debería quedar en una sola columna
        assert len(df.columns) == 1

    def test_archivo_csv_malformado(self):
        """Test comportamiento con archivo CSV malformado (columnas inconsistentes)"""
        # El archivo malformado contiene:
        # - Cabecera: "nombre;edad;ciudad"
        # - Fila con columna extra: "Juan;25;Madrid;extra_columna"
        # - Fila con columnas faltantes: "Ana;30"
        
        # Pandas puede procesar estos archivos de formas impredecibles:
        # a veces usa la primera columna como índice, a veces lanza errores
        
        try:
            df = cargar_csv(self.csv_malformado)
            
            # Si pandas logra procesar el archivo, verificar que:
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2  # Dos filas de datos
            assert list(df.columns) == ["nombre", "edad", "ciudad"]  # Columnas de la cabecera
            
            # Pandas puede interpretar el archivo de diferentes maneras:
            # 1. Comportamiento normal: nombres en la columna 'nombre'
            # 2. Comportamiento con índice: nombres como índices del DataFrame
            
            # Verificar que al menos el DataFrame no está vacío y tiene la estructura esperada
            assert not df.empty
            assert df.shape == (2, 3)
            
            # Verificar que contiene algunos de los datos esperados
            # (sin importar si están en las columnas correctas debido a la naturaleza malformada)
            datos_esperados = {"Juan", "Ana", "25", "30", "Madrid"}
            datos_encontrados = set()
            
            # Recopilar todos los valores del DataFrame (incluyendo índices)
            for col in df.columns:
                datos_encontrados.update(str(val) for val in df[col].values if pd.notna(val))
            
            # Agregar índices si no son numéricos
            if not df.index.is_numeric():
                datos_encontrados.update(str(idx) for idx in df.index.values)
            
            # Verificar que encontramos al menos algunos datos esperados
            assert len(datos_esperados.intersection(datos_encontrados)) >= 3, \
                f"No se encontraron suficientes datos esperados. Encontrados: {datos_encontrados}"
            
        except ValueError as e:
            # Si nuestra función detecta y lanza ValueError por parseo
            assert "No se pudo parsear el archivo" in str(e)
            
        except Exception as e:
            # Si ocurre otro error inesperado, fallar el test
            pytest.fail(f"Error inesperado al procesar archivo malformado: {e}") 