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
        with pytest.raises(ValueError, match="Error de codificación al leer el archivo"):
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
        with pytest.raises(ValueError, match="Error de codificación al leer el archivo"):
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
        """Test que cuando hay columnas duplicadas en CSV, se pueda cargar sin errores"""
        # Crear archivo con columnas duplicadas
        archivo_duplicado = os.path.join(self.temp_dir, "test_duplicado.csv")
        with open(archivo_duplicado, 'w', encoding='utf-8') as f:
            f.write("nombre,edad,nombre\nJuan,25,Juan2\n")
        
        # Debería cargar sin errores, pandas maneja las columnas duplicadas
        resultado = cargar_csv(archivo_duplicado)
        
        # Verificar que se cargó correctamente
        assert isinstance(resultado, pd.DataFrame)
        assert not resultado.empty
        assert len(resultado) == 1
        # pandas agrega sufijos automáticamente para columnas duplicadas
        assert 'nombre' in resultado.columns

    def test_csv_rutas_con_espacios(self):
        """Test: cargar_csv debe manejar rutas con espacios al inicio y final"""
        # Crear archivo CSV normal
        archivo_normal = os.path.join(self.temp_dir, "normal.csv")
        with open(archivo_normal, 'w', encoding='utf-8') as f:
            f.write("nombre,edad\nJuan,25\n")
        
        # Agregar espacios a la ruta
        ruta_con_espacios_final = archivo_normal + "  "
        ruta_con_espacios_inicio = "  " + archivo_normal
        ruta_con_espacios_ambos = "  " + archivo_normal + "  "
        
        # Todas estas rutas deberían funcionar igual
        resultado1 = cargar_csv(archivo_normal)
        resultado2 = cargar_csv(ruta_con_espacios_final)
        resultado3 = cargar_csv(ruta_con_espacios_inicio)
        resultado4 = cargar_csv(ruta_con_espacios_ambos)
        
        # Verificar que todos los resultados sean iguales
        assert resultado1.equals(resultado2)
        assert resultado1.equals(resultado3)
        assert resultado1.equals(resultado4)

    def test_logging_excepcion_inesperada(self):
        """Test: verificar que se registran excepciones inesperadas en logs"""
        import logging
        from unittest.mock import patch
        
        # Crear mock del logger para capturar logs
        with patch('carga_datos.cargar_csv.logging.warning') as mock_warning:
            # Simular una excepción inesperada usando un mock que falle
            with patch('pandas.read_csv') as mock_read_csv:
                # Crear una excepción no manejada específicamente
                mock_read_csv.side_effect = RuntimeError("Error inesperado simulado")
                
                # Verificar que la excepción se re-lanza
                with pytest.raises(RuntimeError, match="Error inesperado simulado"):
                    cargar_csv(self.csv_valido)
                
                # Verificar que se registró en el log
                mock_warning.assert_called_once()
                llamada_args = mock_warning.call_args[0][0]
                assert "Excepción inesperada en cargar_csv" in llamada_args
                assert "RuntimeError" in llamada_args
                assert "Error inesperado simulado" in llamada_args 