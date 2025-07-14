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
from carga_datos import cargar_xlsx


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
        """Test que archivo xlsx completamente vacío lanza error"""
        # Archivo vacío (0 bytes)
        archivo_vacio_xlsx = os.path.join(self.temp_dir, "vacio.xlsx")
        open(archivo_vacio_xlsx, 'w').close()
        
        with pytest.raises(ValueError, match="no es un archivo Excel válido"):
            cargar_xlsx(archivo_vacio_xlsx)

    def test_xlsx_rutas_con_espacios(self):
        """Test: cargar_xlsx debe manejar rutas con espacios al inicio y final"""
        # Agregar espacios a la ruta
        ruta_con_espacios_final = self.xlsx_valido + "  "
        ruta_con_espacios_inicio = "  " + self.xlsx_valido
        ruta_con_espacios_ambos = "  " + self.xlsx_valido + "  "
        
        # Todas estas rutas deberían funcionar igual
        resultado1 = cargar_xlsx(self.xlsx_valido)
        resultado2 = cargar_xlsx(ruta_con_espacios_final)
        resultado3 = cargar_xlsx(ruta_con_espacios_inicio)
        resultado4 = cargar_xlsx(ruta_con_espacios_ambos)
        
        # Verificar que todos los resultados sean iguales
        assert resultado1.equals(resultado2)
        assert resultado1.equals(resultado3)
        assert resultado1.equals(resultado4) 