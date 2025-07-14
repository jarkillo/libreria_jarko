import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os
import sys
import platform
import stat
import unittest.mock as mock

# Agregar el directorio padre al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent.parent))
from carga_datos import cargar_csv, cargar_parquet, cargar_xlsx


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
        
        # Crear archivo Excel renombrado como CSV
        self.archivo_excel = os.path.join(self.temp_dir, "test_excel.csv")
        with open(self.archivo_excel, 'wb') as f:
            # Contenido mínimo de un archivo Excel
            f.write(b'PK\x03\x04\x14\x00\x00\x00\x08\x00')
        
        # Crear archivo con filas inconsistentes más específico
        self.csv_filas_inconsistentes = os.path.join(self.temp_dir, "test_filas_inconsistentes.csv")
        with open(self.csv_filas_inconsistentes, 'w', encoding='utf-8') as f:
            f.write("nombre,edad,ciudad\n")
            f.write("Juan,25\n")  # Falta ciudad
            f.write("Ana,30,Barcelona,España\n")  # Columna extra
        
        # Crear archivo con solo encabezado
        self.csv_solo_encabezado = os.path.join(self.temp_dir, "test_solo_encabezado.csv")
        with open(self.csv_solo_encabezado, 'w', encoding='utf-8') as f:
            f.write("nombre,edad,ciudad\n")
        
        # Crear archivo con caracteres especiales
        self.csv_caracteres_especiales = os.path.join(self.temp_dir, "test_caracteres_especiales.csv")
        with open(self.csv_caracteres_especiales, 'w', encoding='utf-8') as f:
            f.write("nombre,edad,ciudad\n")
            f.write("José,25,\"Madrid, España\"\n")
            f.write("María,30,\"Barcelona; Cataluña\"\n")

        # NUEVOS TESTS ADICIONALES
        
        # CSV con solo una columna pero múltiples separadores
        self.csv_una_columna_separadores = os.path.join(self.temp_dir, "test_una_columna_separadores.csv")
        with open(self.csv_una_columna_separadores, 'w', encoding='utf-8') as f:
            f.write("descripcion\n")
            f.write("Producto A; precio: 100; stock: 50\n")
            f.write("Producto B; precio: 200; stock: 30\n")
        
        # CSV con solo una línea en blanco
        self.csv_linea_blanco = os.path.join(self.temp_dir, "test_linea_blanco.csv")
        with open(self.csv_linea_blanco, 'w', encoding='utf-8') as f:
            f.write(" \n")  # Solo una línea con espacio
        
        # CSV con BOM pero encoding utf-8 (no utf-8-sig)
        self.csv_bom_utf8 = os.path.join(self.temp_dir, "test_bom_utf8.csv")
        with open(self.csv_bom_utf8, 'wb') as f:
            f.write('\ufeff'.encode('utf-8'))  # BOM
            f.write("nombre,edad\nJuan,25\n".encode('utf-8'))
        
        # CSV con columnas duplicadas múltiples
        self.csv_columnas_multi_duplicadas = os.path.join(self.temp_dir, "test_multi_duplicadas.csv")
        with open(self.csv_columnas_multi_duplicadas, 'w', encoding='utf-8') as f:
            f.write("nombre,nombre,nombre,edad\n")
            f.write("Juan,Pedro,Carlos,25\n")

    def teardown_method(self):
        """Limpiar archivos de test después de cada test"""
        import shutil
        shutil.rmtree(self.temp_dir)

    # Tests de casos exitosos
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
        df = cargar_csv(Path(self.csv_valido), sep=";")
        
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
    
    def test_separador_por_defecto(self):
        """Test que el separador por defecto es ','"""
        df = cargar_csv(self.csv_comas)  # No especificar separador
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["nombre", "edad", "ciudad"]

    def test_archivo_con_bom(self):
        """Test archivo con BOM (Byte Order Mark)"""
        df = cargar_csv(self.csv_con_bom)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert list(df.columns) == ["nombre", "edad", "ciudad"]
        assert df.iloc[0]["nombre"] == "Juan"

    def test_columnas_duplicadas(self):
        """Test archivo con columnas duplicadas"""
        df = cargar_csv(self.csv_columnas_duplicadas)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        # pandas debería renombrar las columnas duplicadas
        assert len(df.columns) == 3
        assert "nombre" in df.columns

    def test_una_columna_con_comas_internas(self):
        """Test archivo con una columna que contiene comas internas"""
        df = cargar_csv(self.csv_una_columna_comas)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["descripcion"]
        # Verificar que las comas internas se preservan
        assert "Juan, tiene 25 años" in df.iloc[0]["descripcion"]

    def test_caracteres_especiales(self):
        """Test archivo con caracteres especiales y comillas"""
        df = cargar_csv(self.csv_caracteres_especiales)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert df.iloc[0]["nombre"] == "José"
        assert "Madrid, España" in df.iloc[0]["ciudad"]

    # Tests de errores de archivo
    def test_archivo_no_existe(self):
        """Test error: archivo no existe"""
        with pytest.raises(FileNotFoundError, match="El archivo .* no existe"):
            cargar_csv("archivo_inexistente.csv")

    def test_ruta_es_directorio(self):
        """Test error: la ruta es un directorio, no un archivo"""
        with pytest.raises(ValueError, match="La ruta .* no es un archivo válido"):
            cargar_csv(self.temp_dir)

    def test_archivo_vacio(self):
        """Test error: archivo vacío"""
        with pytest.raises(ValueError, match="El archivo .* está vacío"):
            cargar_csv(self.csv_vacio)

    def test_archivo_solo_encabezado(self):
        """Test error: archivo con solo encabezado"""
        with pytest.raises(ValueError, match="El archivo .* está vacío"):
            cargar_csv(self.csv_solo_encabezado)

    # Tests de errores de validación de tipos
    def test_tipo_ruta_invalido(self):
        """Test error: tipo de ruta inválido"""
        with pytest.raises(TypeError, match="El parámetro 'ruta' debe ser str o Path"):
            cargar_csv(123)  # type: ignore  # Pasar int en lugar de str/Path

    def test_tipo_separador_invalido(self):
        """Test error: tipo de separador inválido"""
        with pytest.raises(TypeError, match="El parámetro 'sep' debe ser str"):
            cargar_csv(self.csv_valido, sep=123)  # type: ignore  # Pasar int en lugar de str

    def test_tipo_encoding_invalido(self):
        """Test error: tipo de encoding inválido"""
        with pytest.raises(TypeError, match="El parámetro 'encoding' debe ser str"):
            cargar_csv(self.csv_valido, encoding=123)  # type: ignore  # Pasar int en lugar de str

    # Tests de errores de encoding
    def test_encoding_incorrecto(self):
        """Test error: encoding incorrecto"""
        with pytest.raises(ValueError, match="No se pudo leer el archivo .* con codificación"):
            cargar_csv(self.csv_latin1, encoding="utf-8")
    
    def test_encoding_inexistente(self):
        """Test error: encoding inexistente debe lanzar LookupError o UnicodeDecodeError"""
        with pytest.raises(ValueError, match="La codificación .* no es válida"):
            cargar_csv(self.csv_comas, encoding="encoding_inexistente")

    # Tests de errores de separador
    def test_separador_incorrecto(self):
        """Test comportamiento con separador incorrecto"""
        # Con separador incorrecto, pandas crea un DataFrame con una sola columna
        df = cargar_csv(self.csv_valido, sep=",")
        # Con separador incorrecto, todo debería quedar en una sola columna
        assert len(df.columns) == 1
    
    def test_separador_incorrecto_punto_coma(self):
        """Test separador incorrecto: usar ; en archivo con ,"""
        df = cargar_csv(self.csv_comas, sep=";")
        # Con separador incorrecto, todo debería quedar en una sola columna
        assert len(df.columns) == 1

    # Tests de archivos mal formados
    def test_archivo_csv_malformado(self):
        """Test comportamiento con archivo CSV malformado (columnas inconsistentes)"""
        # pandas puede manejar archivos con columnas inconsistentes
        # pero genera warnings o errores dependiendo de la configuración
        try:
            df = cargar_csv(self.csv_malformado, sep=";")
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert not df.empty
        except ValueError as e:
            # Si falla, debe ser por parseo
            assert "No se pudo parsear el archivo" in str(e)

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

    def test_filas_inconsistentes(self):
        """Test archivo con filas que tienen diferentes números de columnas"""
        try:
            df = cargar_csv(self.csv_filas_inconsistentes)
            # pandas puede manejar esto rellenando con NaN
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
        except ValueError as e:
            # Si falla, debe ser por parseo
            assert "No se pudo parsear el archivo" in str(e)

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

    # Tests de archivos con formatos incorrectos
    def test_archivo_binario_renombrado(self):
        """Test archivo binario renombrado como CSV"""
        with pytest.raises(ValueError, match="No se pudo leer el archivo .* con codificación"):
            cargar_csv(self.archivo_binario)

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

    def test_archivo_excel_renombrado(self):
        """Test archivo Excel renombrado como CSV"""
        with pytest.raises(ValueError, match="El archivo .* está vacío"):
            cargar_csv(self.archivo_excel)

    # Tests de permisos y memoria
    def test_archivo_sin_permisos(self):
        """Test archivo sin permisos de lectura"""
        # Solo ejecutar en sistemas Unix-like
        if platform.system() == "Windows":
            pytest.skip("Test de permisos no compatible con Windows")
        
        # Crear archivo temporal y quitarle permisos
        archivo_sin_permisos = os.path.join(self.temp_dir, "sin_permisos.csv")
        with open(archivo_sin_permisos, 'w') as f:
            f.write("nombre,edad\nJuan,25\n")
        
        # Quitar permisos de lectura
        try:
            os.chmod(archivo_sin_permisos, 0o000)
            with pytest.raises(ValueError, match="No tienes permisos para leer el archivo"):
                cargar_csv(archivo_sin_permisos)
        finally:
            # Restaurar permisos para limpiar el archivo
            try:
                os.chmod(archivo_sin_permisos, stat.S_IRUSR | stat.S_IWUSR)
            except (OSError, FileNotFoundError):
                pass

    def test_archivo_muy_grande(self):
        """Test archivo muy grande para memoria"""
        # Usar mock para simular MemoryError
        with mock.patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.side_effect = MemoryError("Insufficient memory")
            
            with pytest.raises(ValueError, match="es demasiado grande para cargar en memoria"):
                cargar_csv(self.csv_comas)

    # TESTS ADICIONALES

    def test_csv_una_columna_multiples_separadores(self):
        """Test CSV con una columna que contiene múltiples separadores internos"""
        df = cargar_csv(self.csv_una_columna_separadores)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert len(df.columns) == 1
        assert list(df.columns) == ["descripcion"]
        # Verificar que los separadores internos se preservan
        assert "precio: 100" in df.iloc[0]["descripcion"]
        assert "stock: 50" in df.iloc[0]["descripcion"]

    def test_csv_linea_blanco(self):
        """Test CSV con solo una línea en blanco"""
        with pytest.raises(ValueError, match="El archivo .* está vacío"):
            cargar_csv(self.csv_linea_blanco)

    def test_csv_bom_encoding_utf8(self):
        """Test CSV con BOM pero usando encoding utf-8 (no utf-8-sig)"""
        # Debería manejar el BOM correctamente o lanzar error claro
        try:
            df = cargar_csv(self.csv_bom_utf8)
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1
            # Verificar que el BOM no afecta el primer nombre de columna
            columns = list(df.columns)
            assert any("nombre" in col for col in columns)
        except ValueError as e:
            # Si falla, debe ser por encoding
            assert "encoding" in str(e) or "parsear" in str(e)

    def test_csv_columnas_multiples_duplicadas(self):
        """Test CSV con múltiples columnas duplicadas"""
        df = cargar_csv(self.csv_columnas_multi_duplicadas)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert len(df.columns) == 4
        # pandas debería renombrar las columnas duplicadas
        columns = list(df.columns)
        assert columns.count("nombre") == 1  # Solo una columna debería mantener el nombre original
        assert "edad" in columns

    def test_csv_estructura_final_con_separadores(self):
        """Test para verificar estructura final con múltiples separadores"""
        # Usar archivo con separadores internos pero que debería parsearse correctamente
        df = cargar_csv(self.csv_caracteres_especiales)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert len(df.columns) == 3
        # Verificar que las comas y punto y comas internos se preservan
        assert "Madrid, España" in df.iloc[0]["ciudad"]
        assert "Barcelona; Cataluña" in df.iloc[1]["ciudad"]

    def test_csv_detectar_bom_automaticamente(self):
        """Test para verificar que se detecta BOM automáticamente"""
        # Probar con archivo que tiene BOM usando utf-8-sig
        df = cargar_csv(self.csv_con_bom)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        columns = list(df.columns)
        # Verificar que no hay caracteres extraños del BOM
        assert "nombre" in columns
        assert not any('\ufeff' in col for col in columns)

    def test_csv_advertencia_columnas_duplicadas(self):
        """Test que maneja columnas duplicadas sin lanzar error pero con estructura correcta"""
        df = cargar_csv(self.csv_columnas_duplicadas)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert len(df.columns) == 3
        # pandas maneja las columnas duplicadas automáticamente
        columns = list(df.columns)
        assert len(set(columns)) <= 3  # No más de 3 columnas únicas


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


class TestCargarXlsx:
    """Tests para la función cargar_xlsx"""

    def setup_method(self):
        """Configurar archivos de test antes de cada test"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Crear archivo Excel válido para tests exitosos
        self.xlsx_valido = os.path.join(self.temp_dir, "test_valido.xlsx")
        # Crear un DataFrame de ejemplo y guardarlo como Excel
        df_ejemplo = pd.DataFrame({
            'nombre': ['Juan', 'Ana', 'Carlos'],
            'edad': [25, 30, 35],
            'ciudad': ['Madrid', 'Barcelona', 'Valencia'],
            'activo': [True, False, True]
        })
        try:
            df_ejemplo.to_excel(self.xlsx_valido, sheet_name='Datos', index=False)
            self.xlsx_existe = True
        except ImportError:
            self.xlsx_existe = False
        
        # Crear archivo Excel con múltiples hojas
        self.xlsx_multiple_hojas = os.path.join(self.temp_dir, "test_multiple_hojas.xlsx")
        if self.xlsx_existe:
            try:
                with pd.ExcelWriter(self.xlsx_multiple_hojas) as writer:
                    df_ejemplo.to_excel(writer, sheet_name='Hoja1', index=False)
                    df_ejemplo.to_excel(writer, sheet_name='Hoja2', index=False)
                    # Hoja con datos diferentes
                    df_ventas = pd.DataFrame({
                        'producto': ['A', 'B', 'C'],
                        'precio': [100, 200, 300]
                    })
                    df_ventas.to_excel(writer, sheet_name='Ventas', index=False)
            except Exception:
                self.xlsx_existe = False
        
        # Crear archivo Excel con header=None
        self.xlsx_sin_header = os.path.join(self.temp_dir, "test_sin_header.xlsx")
        if self.xlsx_existe:
            try:
                df_sin_header = pd.DataFrame([
                    ['Juan', 25, 'Madrid'],
                    ['Ana', 30, 'Barcelona'],
                    ['Carlos', 35, 'Valencia']
                ])
                df_sin_header.to_excel(self.xlsx_sin_header, header=False, index=False)
            except Exception:
                pass
        
        # Crear archivo Excel con celdas vacías y combinadas (simulado)
        self.xlsx_celdas_especiales = os.path.join(self.temp_dir, "test_celdas_especiales.xlsx")
        if self.xlsx_existe:
            try:
                df_especial = pd.DataFrame({
                    'nombre': ['Juan', None, 'Carlos'],
                    'edad': [25, 30, None],
                    'observaciones': ['Activo', '', 'Inactivo']
                })
                df_especial.to_excel(self.xlsx_celdas_especiales, index=False)
            except Exception:
                pass

    def teardown_method(self):
        """Limpiar archivos de test después de cada test"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_archivo_xlsx_no_existe(self):
        """Test error: archivo xlsx no existe"""
        with pytest.raises(FileNotFoundError, match="El archivo .* no existe"):
            cargar_xlsx("archivo_inexistente.xlsx")

    def test_tipo_ruta_xlsx_invalido(self):
        """Test error: tipo de ruta inválido para xlsx"""
        with pytest.raises(TypeError, match="El parámetro 'ruta' debe ser str o Path"):
            cargar_xlsx(123)  # type: ignore

    def test_tipo_sheet_name_invalido(self):
        """Test error: tipo de sheet_name inválido"""
        ruta_xlsx = os.path.join(self.temp_dir, "test.xlsx")
        with open(ruta_xlsx, 'w') as f:
            f.write("fake xlsx")
        
        with pytest.raises(TypeError, match="El parámetro 'sheet_name' debe ser str o int"):
            cargar_xlsx(ruta_xlsx, sheet_name=12.5)  # type: ignore

    def test_tipo_header_invalido(self):
        """Test error: tipo de header inválido"""
        ruta_xlsx = os.path.join(self.temp_dir, "test.xlsx")
        with open(ruta_xlsx, 'w') as f:
            f.write("fake xlsx")
        
        with pytest.raises(TypeError, match="El parámetro 'header' debe ser int o None"):
            cargar_xlsx(ruta_xlsx, header="invalid")  # type: ignore

    def test_engine_invalido(self):
        """Test error: engine inválido"""
        ruta_xlsx = os.path.join(self.temp_dir, "test.xlsx")
        with open(ruta_xlsx, 'w') as f:
            f.write("fake xlsx")
        
        with pytest.raises(TypeError, match="El parámetro 'engine' debe ser uno de"):
            cargar_xlsx(ruta_xlsx, engine="invalid_engine")  # type: ignore

    def test_archivo_no_es_xlsx(self):
        """Test error: archivo no es xlsx válido"""
        archivo_falso = os.path.join(self.temp_dir, "fake.xlsx")
        with open(archivo_falso, 'w') as f:
            f.write("esto no es xlsx")
        
        with pytest.raises(ValueError, match="no es un archivo Excel válido"):
            cargar_xlsx(archivo_falso)

    # TESTS ADICIONALES

    @pytest.mark.skipif(not hasattr(pd, 'read_excel'), reason="pandas no tiene soporte para Excel")
    def test_xlsx_bien_formado_por_indice(self):
        """Test cargar Excel bien formado por índice de hoja"""
        if not self.xlsx_existe:
            pytest.skip("openpyxl no disponible")
        
        df = cargar_xlsx(self.xlsx_valido, sheet_name=0)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert len(df.columns) == 4
        expected_columns = ['nombre', 'edad', 'ciudad', 'activo']
        assert all(col in df.columns for col in expected_columns)
        assert df.iloc[0]['nombre'] == 'Juan'

    @pytest.mark.skipif(not hasattr(pd, 'read_excel'), reason="pandas no tiene soporte para Excel")
    def test_xlsx_bien_formado_por_nombre(self):
        """Test cargar Excel bien formado por nombre de hoja"""
        if not self.xlsx_existe:
            pytest.skip("openpyxl no disponible")
        
        df = cargar_xlsx(self.xlsx_multiple_hojas, sheet_name='Ventas')
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert len(df.columns) == 2
        assert list(df.columns) == ['producto', 'precio']
        assert df.iloc[0]['producto'] == 'A'
        assert df.iloc[0]['precio'] == 100

    def test_xlsx_hoja_inexistente_por_nombre(self):
        """Test error: hoja inexistente por nombre"""
        if not self.xlsx_existe:
            pytest.skip("openpyxl no disponible")
        
        with pytest.raises(ValueError, match="La hoja .* no existe"):
            cargar_xlsx(self.xlsx_multiple_hojas, sheet_name='HojaInexistente')

    def test_xlsx_hoja_inexistente_por_indice(self):
        """Test error: hoja inexistente por índice"""
        if not self.xlsx_existe:
            pytest.skip("openpyxl no disponible")
        
        with pytest.raises(ValueError, match="El índice de hoja .* no existe"):
            cargar_xlsx(self.xlsx_valido, sheet_name=5)

    def test_xlsx_sin_permisos(self):
        """Test error: archivo Excel sin permisos"""
        if not self.xlsx_existe:
            pytest.skip("openpyxl no disponible")
        
        if platform.system() == "Windows":
            pytest.skip("Permisos en Windows se manejan diferente")
        
        # Quitar permisos de lectura
        os.chmod(self.xlsx_valido, 0o000)
        
        try:
            with pytest.raises(ValueError, match="No tienes permisos para leer el archivo"):
                cargar_xlsx(self.xlsx_valido)
        finally:
            # Restaurar permisos para cleanup
            os.chmod(self.xlsx_valido, 0o644)

    def test_xlsx_formato_corrupto(self):
        """Test error: archivo con formato corrupto"""
        archivo_corrupto = os.path.join(self.temp_dir, "corrupto.xlsx")
        with open(archivo_corrupto, 'wb') as f:
            f.write(b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x00\x00\x00\x00")  # Zip corrupto
        
        with pytest.raises(ValueError, match="no es un archivo Excel válido"):
            cargar_xlsx(archivo_corrupto)

    @pytest.mark.skipif(not hasattr(pd, 'read_excel'), reason="pandas no tiene soporte para Excel")
    def test_xlsx_header_none(self):
        """Test cargar Excel con header=None"""
        if not self.xlsx_existe:
            pytest.skip("openpyxl no disponible")
        
        df = cargar_xlsx(self.xlsx_sin_header, header=None)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        # Las columnas deberían ser numéricas (0, 1, 2, etc.)
        assert all(isinstance(col, int) for col in df.columns)
        assert df.iloc[0, 0] == 'Juan'  # Primera fila, primera columna

    @pytest.mark.skipif(not hasattr(pd, 'read_excel'), reason="pandas no tiene soporte para Excel")
    def test_xlsx_celdas_vacias(self):
        """Test archivo con celdas vacías y valores NaN"""
        if not self.xlsx_existe:
            pytest.skip("openpyxl no disponible")
        
        df = cargar_xlsx(self.xlsx_celdas_especiales)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        # Verificar que maneja valores NaN correctamente
        assert pd.isna(df.iloc[1, 0])  # Segunda fila, primera columna (nombre)
        assert pd.isna(df.iloc[2, 1])  # Tercera fila, segunda columna (edad)

    def test_xlsx_csv_renombrado(self):
        """Test error: archivo CSV renombrado como Excel"""
        csv_falso = os.path.join(self.temp_dir, "falso.xlsx")
        with open(csv_falso, 'w', encoding='utf-8') as f:
            f.write("nombre,edad,ciudad\n")
            f.write("Juan,25,Madrid\n")
        
        with pytest.raises(ValueError, match="no es un archivo Excel válido"):
            cargar_xlsx(csv_falso)

    def test_xlsx_ruta_es_directorio(self):
        """Test error: la ruta es un directorio, no un archivo"""
        with pytest.raises(ValueError, match="La ruta .* no es un archivo válido"):
            cargar_xlsx(self.temp_dir)

    def test_xlsx_archivo_grande_memoria(self):
        """Test archivo Excel muy grande para memoria"""
        if not self.xlsx_existe:
            pytest.skip("openpyxl no disponible")
        
        # Usar mock para simular MemoryError
        with mock.patch('pandas.read_excel') as mock_read_excel:
            mock_read_excel.side_effect = MemoryError("Insufficient memory")
            
            with pytest.raises(ValueError, match="es demasiado grande para cargar en memoria"):
                cargar_xlsx(self.xlsx_valido)

    @pytest.mark.skipif(not hasattr(pd, 'read_excel'), reason="pandas no tiene soporte para Excel")
    def test_xlsx_con_path_object(self):
        """Test cargar Excel usando Path object"""
        if not self.xlsx_existe:
            pytest.skip("openpyxl no disponible")
        
        df = cargar_xlsx(Path(self.xlsx_valido))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3

    @pytest.mark.skipif(not hasattr(pd, 'read_excel'), reason="pandas no tiene soporte para Excel")
    def test_xlsx_engine_especifico(self):
        """Test cargar Excel con engine específico"""
        if not self.xlsx_existe:
            pytest.skip("openpyxl no disponible")
        
        df = cargar_xlsx(self.xlsx_valido, engine='openpyxl')
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3

    def test_xlsx_vacio(self):
        """Test error: archivo Excel vacío"""
        xlsx_vacio = os.path.join(self.temp_dir, "vacio.xlsx")
        with open(xlsx_vacio, 'w') as f:
            f.write("")
        
        with pytest.raises(ValueError, match="no es un archivo Excel válido"):
            cargar_xlsx(xlsx_vacio) 

class TestCargarArchivo:
    """
    Tests para la función cargar_archivo() que debe ser implementada.
    
    Esta función debe analizar la extensión del archivo y llamar internamente a:
    - cargar_csv() si es .csv
    - cargar_xlsx() si es .xlsx  
    - cargar_parquet() si es .parquet
    
    FORMATOS SOPORTADOS:
    ✅ .csv, .CSV (y variaciones de mayúsculas/minúsculas)
    ✅ .xlsx, .XLSX (y variaciones de mayúsculas/minúsculas)
    ✅ .parquet, .PARQUET (y variaciones de mayúsculas/minúsculas)
    
    FORMATOS NO SOPORTADOS:
    ❌ .xls (Excel antiguo)
    ❌ .ods (LibreOffice/OpenOffice)
    ❌ .json, .xml, .tsv, .txt
    ❌ Cualquier otra extensión no listada como soportada
    
    NOTA: Estos tests están listos para ser ejecutados una vez que la función cargar_archivo
    sea implementada en el módulo carga_datos.
    """

    def setup_method(self):
        """Configurar archivos de test antes de cada test"""
        # Crear directorio temporal para tests
        self.temp_dir = tempfile.mkdtemp()
        
        # Crear archivos de prueba con diferentes extensiones
        self.archivo_csv = os.path.join(self.temp_dir, "datos.csv")
        self.archivo_xlsx = os.path.join(self.temp_dir, "datos.xlsx")
        self.archivo_parquet = os.path.join(self.temp_dir, "datos.parquet")
        self.archivo_csv_mayusculas = os.path.join(self.temp_dir, "datos.CSV")
        self.archivo_xlsx_nombre_extraño = os.path.join(self.temp_dir, "datos.tabla.excel.xlsx")
        self.archivo_extension_desconocida = os.path.join(self.temp_dir, "datos.txt")
        self.archivo_sin_extension = os.path.join(self.temp_dir, "datos")
        self.archivo_doble_extension = os.path.join(self.temp_dir, "archivo.csv.exe")
        
        # Crear los archivos (contenido mínimo)
        with open(self.archivo_csv, 'w', encoding='utf-8') as f:
            f.write("nombre,edad\nJuan,25\n")
        
        with open(self.archivo_xlsx, 'w', encoding='utf-8') as f:
            f.write("dummy excel content")
        
        with open(self.archivo_parquet, 'w', encoding='utf-8') as f:
            f.write("dummy parquet content")
        
        with open(self.archivo_csv_mayusculas, 'w', encoding='utf-8') as f:
            f.write("nombre,edad\nAna,30\n")
        
        with open(self.archivo_xlsx_nombre_extraño, 'w', encoding='utf-8') as f:
            f.write("dummy excel content")
        
        with open(self.archivo_extension_desconocida, 'w', encoding='utf-8') as f:
            f.write("contenido texto")
        
        with open(self.archivo_sin_extension, 'w', encoding='utf-8') as f:
            f.write("contenido sin extension")
        
        with open(self.archivo_doble_extension, 'w', encoding='utf-8') as f:
            f.write("contenido con doble extension")

    def teardown_method(self):
        """Limpiar archivos de test después de cada test"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_cargar_archivo_csv_bien_formado(self):
        """Test: archivo .csv bien formado debe llamar a cargar_csv"""
        with mock.patch('carga_datos.cargar_archivo.cargar_csv') as mock_cargar_csv:
            mock_df = pd.DataFrame({"nombre": ["Juan"], "edad": [25]})
            mock_cargar_csv.return_value = mock_df
            
            from carga_datos import cargar_archivo
            resultado = cargar_archivo(self.archivo_csv)
            
            mock_cargar_csv.assert_called_once_with(self.archivo_csv)
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_xlsx_bien_formado(self):
        """Test: archivo .xlsx bien formado debe llamar a cargar_xlsx"""
        with mock.patch('carga_datos.cargar_archivo.cargar_xlsx') as mock_cargar_xlsx:
            mock_df = pd.DataFrame({"nombre": ["Ana"], "edad": [30]})
            mock_cargar_xlsx.return_value = mock_df
            
            from carga_datos import cargar_archivo
            resultado = cargar_archivo(self.archivo_xlsx)
            
            mock_cargar_xlsx.assert_called_once_with(self.archivo_xlsx)
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_parquet_bien_formado(self):
        """Test: archivo .parquet bien formado debe llamar a cargar_parquet"""
        with mock.patch('carga_datos.cargar_archivo.cargar_parquet') as mock_cargar_parquet:
            mock_df = pd.DataFrame({"nombre": ["Carlos"], "edad": [35]})
            mock_cargar_parquet.return_value = mock_df
            
            from carga_datos import cargar_archivo
            resultado = cargar_archivo(self.archivo_parquet)
            
            mock_cargar_parquet.assert_called_once_with(self.archivo_parquet)
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_extension_desconocida(self):
        """Test: archivo con extensión desconocida debe lanzar ValueError"""
        from carga_datos import cargar_archivo
        
        with pytest.raises(ValueError, match="Extensión de archivo no soportada"):
            cargar_archivo(self.archivo_extension_desconocida)

    def test_cargar_archivo_sin_extension(self):
        """Test: archivo sin extensión debe lanzar ValueError"""
        from carga_datos import cargar_archivo
        
        with pytest.raises(ValueError, match="Extensión de archivo no soportada"):
            cargar_archivo(self.archivo_sin_extension)

    def test_cargar_archivo_csv_mayusculas(self):
        """Test: archivo .CSV (mayúsculas) debe tratarse como .csv"""
        with mock.patch('carga_datos.cargar_archivo.cargar_csv') as mock_cargar_csv:
            mock_df = pd.DataFrame({"nombre": ["Maria"], "edad": [28]})
            mock_cargar_csv.return_value = mock_df
            
            from carga_datos import cargar_archivo
            resultado = cargar_archivo(self.archivo_csv_mayusculas)
            
            mock_cargar_csv.assert_called_once_with(self.archivo_csv_mayusculas)
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_xlsx_nombre_extraño(self):
        """Test: archivo .xlsx con nombre extraño debe funcionar igual"""
        with mock.patch('carga_datos.cargar_archivo.cargar_xlsx') as mock_cargar_xlsx:
            mock_df = pd.DataFrame({"columna": ["valor"]})
            mock_cargar_xlsx.return_value = mock_df
            
            from carga_datos import cargar_archivo
            resultado = cargar_archivo(self.archivo_xlsx_nombre_extraño)
            
            mock_cargar_xlsx.assert_called_once_with(self.archivo_xlsx_nombre_extraño)
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_doble_extension_falsa(self):
        """Test: archivo con doble extensión falsa debe lanzar ValueError"""
        from carga_datos import cargar_archivo
        
        with pytest.raises(ValueError, match="Extensión de archivo no soportada"):
            cargar_archivo(self.archivo_doble_extension)

    def test_cargar_archivo_path_object(self):
        """Test: cargar_archivo debe funcionar con Path object"""
        with mock.patch('carga_datos.cargar_archivo.cargar_csv') as mock_cargar_csv:
            mock_df = pd.DataFrame({"test": ["data"]})
            mock_cargar_csv.return_value = mock_df
            
            from carga_datos import cargar_archivo
            resultado = cargar_archivo(Path(self.archivo_csv))
            
            mock_cargar_csv.assert_called_once_with(Path(self.archivo_csv))
            assert isinstance(resultado, pd.DataFrame)

    def test_cargar_archivo_tipos_invalidos(self):
        """Test: cargar_archivo debe validar tipos de entrada"""
        from carga_datos import cargar_archivo
        
        with pytest.raises(TypeError, match="El parámetro 'ruta' debe ser str o Path"):
            cargar_archivo(123)  # type: ignore
        
        with pytest.raises(TypeError, match="El parámetro 'ruta' debe ser str o Path"):
            cargar_archivo(None)  # type: ignore
        
        with pytest.raises(TypeError, match="El parámetro 'ruta' debe ser str o Path"):
            cargar_archivo(["ruta", "lista"])  # type: ignore

    def test_cargar_archivo_no_existe(self):
        """Test: cargar_archivo debe manejar archivo inexistente"""
        from carga_datos import cargar_archivo
        
        with pytest.raises(FileNotFoundError, match="El archivo .* no existe"):
            cargar_archivo("archivo_inexistente.csv")

    @mock.patch('carga_datos.cargar_csv')
    def test_cargar_archivo_propaga_errores_funciones_internas(self, mock_cargar_csv):
        """Test: cargar_archivo debe propagar errores de las funciones internas"""
        with mock.patch('carga_datos.cargar_archivo.cargar_csv') as mock_cargar_csv:
            mock_cargar_csv.side_effect = ValueError("Error específico de cargar_csv")
            
            from carga_datos import cargar_archivo
            
            with pytest.raises(ValueError, match="Error específico de cargar_csv"):
                cargar_archivo(self.archivo_csv)
            
            mock_cargar_csv.assert_called_once_with(self.archivo_csv)

    def test_cargar_archivo_ruta_como_string(self):
        """Test: cargar_archivo debe funcionar con ruta como string (no Path)"""
        with mock.patch('carga_datos.cargar_archivo.cargar_csv') as mock_cargar_csv:
            mock_df = pd.DataFrame({"nombre": ["Test"], "edad": [25]})
            mock_cargar_csv.return_value = mock_df
            
            from carga_datos import cargar_archivo
            resultado = cargar_archivo(self.archivo_csv)  # Pasando como string
            
            mock_cargar_csv.assert_called_once_with(self.archivo_csv)
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_nombre_con_espacios_al_final(self):
        """Test: cargar_archivo debe manejar archivos con espacios al final del nombre"""
        # Crear archivo con espacios al final
        archivo_espacios = os.path.join(self.temp_dir, "archivo.csv ")
        with open(archivo_espacios, 'w', encoding='utf-8') as f:
            f.write("nombre,edad\nJuan,25\n")
        
        with mock.patch('carga_datos.cargar_archivo.cargar_csv') as mock_cargar_csv:
            mock_df = pd.DataFrame({"nombre": ["Juan"], "edad": [25]})
            mock_cargar_csv.return_value = mock_df
            
            from carga_datos import cargar_archivo
            resultado = cargar_archivo(archivo_espacios)
            
            mock_cargar_csv.assert_called_once_with(archivo_espacios)
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_formatos_no_soportados(self):
        """Test: cargar_archivo debe rechazar formatos no implementados (.xls, .ods, etc.)
        
        IMPORTANTE: Solo se soportan .csv, .xlsx, .parquet
        No se aceptan: .xls, .ods, .json, .xml, .tsv, etc.
        """
        # Crear archivos con formatos no soportados
        archivo_xls = os.path.join(self.temp_dir, "datos.xls")
        archivo_ods = os.path.join(self.temp_dir, "datos.ods")
        archivo_json = os.path.join(self.temp_dir, "datos.json")
        archivo_xml = os.path.join(self.temp_dir, "datos.xml")
        archivo_tsv = os.path.join(self.temp_dir, "datos.tsv")
        
        with open(archivo_xls, 'w', encoding='utf-8') as f:
            f.write("contenido xls")
        with open(archivo_ods, 'w', encoding='utf-8') as f:
            f.write("contenido ods")
        with open(archivo_json, 'w', encoding='utf-8') as f:
            f.write('{"nombre": "Juan"}')
        with open(archivo_xml, 'w', encoding='utf-8') as f:
            f.write('<root><nombre>Juan</nombre></root>')
        with open(archivo_tsv, 'w', encoding='utf-8') as f:
            f.write("nombre\tedad\nJuan\t25")
        
        from carga_datos import cargar_archivo
        
        # Todos estos formatos deben lanzar ValueError
        with pytest.raises(ValueError, match="Extensión de archivo no soportada"):
            cargar_archivo(archivo_xls)
        
        with pytest.raises(ValueError, match="Extensión de archivo no soportada"):
            cargar_archivo(archivo_ods)
        
        with pytest.raises(ValueError, match="Extensión de archivo no soportada"):
            cargar_archivo(archivo_json)
        
        with pytest.raises(ValueError, match="Extensión de archivo no soportada"):
            cargar_archivo(archivo_xml)
        
        with pytest.raises(ValueError, match="Extensión de archivo no soportada"):
            cargar_archivo(archivo_tsv)

    def test_cargar_archivo_extensiones_mixtas_case_insensitive(self):
        """Test: cargar_archivo debe manejar extensiones con mayúsculas y minúsculas mezcladas"""
        # Crear archivos con extensiones mixtas
        archivo_Csv = os.path.join(self.temp_dir, "datos.Csv")
        archivo_XlsX = os.path.join(self.temp_dir, "datos.XlsX")
        archivo_PARQUET = os.path.join(self.temp_dir, "datos.PARQUET")
        
        with open(archivo_Csv, 'w', encoding='utf-8') as f:
            f.write("nombre,edad\nLuis,40\n")
        with open(archivo_XlsX, 'w', encoding='utf-8') as f:
            f.write("dummy excel content")
        with open(archivo_PARQUET, 'w', encoding='utf-8') as f:
            f.write("dummy parquet content")
        
        from carga_datos import cargar_archivo
        
        with mock.patch('carga_datos.cargar_archivo.cargar_csv') as mock_csv:
            mock_csv.return_value = pd.DataFrame({"test": ["data"]})
            cargar_archivo(archivo_Csv)
            mock_csv.assert_called_once()
        
        with mock.patch('carga_datos.cargar_archivo.cargar_xlsx') as mock_xlsx:
            mock_xlsx.return_value = pd.DataFrame({"test": ["data"]})
            cargar_archivo(archivo_XlsX)
            mock_xlsx.assert_called_once()
        
        with mock.patch('carga_datos.cargar_archivo.cargar_parquet') as mock_parquet:
            mock_parquet.return_value = pd.DataFrame({"test": ["data"]})
            cargar_archivo(archivo_PARQUET)
            mock_parquet.assert_called_once() 