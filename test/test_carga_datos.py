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
        
        # Crear archivo con encabezado mal formado
        self.csv_encabezado_malo = os.path.join(self.temp_dir, "test_encabezado_malo.csv")
        with open(self.csv_encabezado_malo, 'w', encoding='utf-8') as f:
            f.write(";;;\n")
            f.write("Juan;25;Madrid\n")
        
        # Crear archivo con columnas duplicadas
        self.csv_columnas_duplicadas = os.path.join(self.temp_dir, "test_duplicadas.csv")
        with open(self.csv_columnas_duplicadas, 'w', encoding='utf-8') as f:
            f.write("nombre,nombre,edad\n")
            f.write("Juan,Pedro,25\n")
        
        # Crear archivo con BOM
        self.csv_con_bom = os.path.join(self.temp_dir, "test_bom.csv")
        with open(self.csv_con_bom, 'w', encoding='utf-8-sig') as f:
            f.write("nombre,edad,ciudad\n")
            f.write("Juan,25,Madrid\n")
        
        # Crear archivo binario renombrado como CSV
        self.archivo_binario = os.path.join(self.temp_dir, "test_binario.csv")
        with open(self.archivo_binario, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01')
        
        # Crear archivo con separadores mixtos
        self.csv_separadores_mixtos = os.path.join(self.temp_dir, "test_separadores_mixtos.csv")
        with open(self.csv_separadores_mixtos, 'w', encoding='utf-8') as f:
            f.write("nombre,edad,ciudad\n")
            f.write("Juan;25;Madrid\n")  # Mezcla , y ;
            f.write("Ana,30,Barcelona\n")
        
        # Crear archivo con una columna y muchas comas (usar separador diferente)
        self.csv_una_columna_comas = os.path.join(self.temp_dir, "test_una_columna_comas.csv")
        with open(self.csv_una_columna_comas, 'w', encoding='utf-8') as f:
            f.write("descripcion\n")
            f.write("\"Juan, tiene 25 años, vive en Madrid, España\"\n")
            f.write("\"Ana, 30 años, Barcelona, Cataluña\"\n")
        
        # Crear archivo JSON renombrado como CSV
        self.archivo_json = os.path.join(self.temp_dir, "test_json.csv")
        with open(self.archivo_json, 'w', encoding='utf-8') as f:
            f.write('{"nombre": "Juan", "edad": 25, "ciudad": "Madrid"}\n')
            f.write('{"nombre": "Ana", "edad": 30, "ciudad": "Barcelona"}\n')

    def teardown_method(self):
        """Limpiar archivos de test después de cada test"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_cargar_csv_valido(self):
        """Test caso exitoso: cargar CSV válido con separador punto y coma"""
        df = cargar_csv(self.csv_valido, sep=";")
        
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
        df = cargar_csv(self.csv_latin1, sep=";", encoding="latin1")
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert df.iloc[0]["nombre"] == "José"
    
    def test_encoding_por_defecto(self):
        """Test que el encoding por defecto es 'utf-8'"""
        df = cargar_csv(self.csv_comas)  # No especificar encoding
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert df.iloc[0]["nombre"] == "Juan"

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
    
    def test_separador_incorrecto_punto_coma(self):
        """Test separador incorrecto: usar ; en archivo con ,"""
        df = cargar_csv(self.csv_comas, sep=";")
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
            df = cargar_csv(self.csv_malformado, sep=";")
            
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
    
    def test_encoding_inexistente(self):
        """Test error: encoding inexistente debe lanzar LookupError o UnicodeDecodeError"""
        with pytest.raises((LookupError, UnicodeDecodeError, ValueError)):
            cargar_csv(self.csv_comas, encoding="encoding_inexistente")
    
    def test_encabezado_mal_formado(self):
        """Test archivo con encabezado mal formado (solo separadores)"""
        # Puede fallar o crear DataFrame con columnas vacías
        try:
            df = cargar_csv(self.csv_encabezado_malo, sep=";")
            # Si no falla, verificar que maneja las columnas vacías
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1  # Una fila de datos
        except ValueError as e:
            # Si falla, debe ser por parseo
            assert "parsear" in str(e) or "vacío" in str(e)
    
    def test_columnas_duplicadas(self):
        """Test archivo con columnas duplicadas"""
        df = cargar_csv(self.csv_columnas_duplicadas)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        # pandas debería renombrar las columnas duplicadas
        assert len(df.columns) == 3
        assert "nombre" in df.columns
    
    def test_archivo_con_bom(self):
        """Test archivo con BOM (Byte Order Mark)"""
        df = cargar_csv(self.csv_con_bom)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert list(df.columns) == ["nombre", "edad", "ciudad"]
        assert df.iloc[0]["nombre"] == "Juan"
    
    def test_archivo_binario_renombrado(self):
        """Test archivo binario renombrado como CSV"""
        with pytest.raises((UnicodeDecodeError, ValueError)):
            cargar_csv(self.archivo_binario)
    
    def test_separadores_mixtos(self):
        """Test archivo con separadores mixtos por línea"""
        # Esto debería causar problemas de parseo
        try:
            df = cargar_csv(self.csv_separadores_mixtos)
            # Si no falla, verificar estructura anómala
            assert isinstance(df, pd.DataFrame)
            # Probablemente tenga columnas con valores raros
        except ValueError as e:
            # Si falla, debe ser por parseo inconsistente
            assert "parsear" in str(e)
    
    def test_una_columna_con_comas_internas(self):
        """Test archivo con una columna que contiene comas internas"""
        df = cargar_csv(self.csv_una_columna_comas)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["descripcion"]
        # Verificar que las comas internas se preservan
        assert "Juan, tiene 25 años" in df.iloc[0]["descripcion"]
    
    def test_archivo_json_renombrado(self):
        """Test archivo JSON renombrado como CSV"""
        # JSON podría procesarse como CSV mal formado o lanzar error
        try:
            df = cargar_csv(self.archivo_json)
            # Si no falla, debería ser un DataFrame mal formado
            assert isinstance(df, pd.DataFrame)
            # Probablemente con estructura extraña
        except ValueError as e:
            # Si falla, debe ser por parseo
            assert "parsear" in str(e) or "vacío" in str(e)
    
    def test_archivo_sin_permisos(self):
        """Test archivo sin permisos de lectura"""
        import platform
        
        # Solo ejecutar en sistemas Unix-like
        if platform.system() == "Windows":
            pytest.skip("Test de permisos no compatible con Windows")
        
        import stat
        
        # Crear archivo temporal y quitarle permisos
        archivo_sin_permisos = os.path.join(self.temp_dir, "sin_permisos.csv")
        with open(archivo_sin_permisos, 'w') as f:
            f.write("nombre,edad\nJuan,25\n")
        
        # Quitar permisos de lectura
        try:
            os.chmod(archivo_sin_permisos, 0o000)
            with pytest.raises((PermissionError, ValueError)):
                cargar_csv(archivo_sin_permisos)
        finally:
            # Restaurar permisos para limpiar el archivo
            try:
                os.chmod(archivo_sin_permisos, stat.S_IRUSR | stat.S_IWUSR)
            except (OSError, FileNotFoundError):
                pass
    
    def test_archivo_muy_grande(self):
        """Test archivo muy grande usando mock"""
        import unittest.mock as mock
        
        # Simular MemoryError al leer archivo grande
        with mock.patch('pandas.read_csv', side_effect=MemoryError("Archivo demasiado grande")):
            with pytest.raises(ValueError, match="es demasiado grande para cargar en memoria"):
                cargar_csv(self.csv_comas) 