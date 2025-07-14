import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os
import sys
import unittest.mock as mock

# Agregar el directorio padre al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent.parent))
from carga_datos import cargar_archivo


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
        import importlib
        cargar_archivo_mod = importlib.import_module('carga_datos.cargar_archivo')
        
        with mock.patch.object(cargar_archivo_mod, 'cargar_csv') as mock_cargar_csv:
            mock_df = pd.DataFrame({"nombre": ["Juan"], "edad": [25]})
            mock_cargar_csv.return_value = mock_df
            
            resultado = cargar_archivo(self.archivo_csv)
            
            mock_cargar_csv.assert_called_once_with(Path(self.archivo_csv))
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_xlsx_bien_formado(self):
        """Test: archivo .xlsx bien formado debe llamar a cargar_xlsx"""
        import importlib
        cargar_archivo_mod = importlib.import_module('carga_datos.cargar_archivo')
        
        with mock.patch.object(cargar_archivo_mod, 'cargar_xlsx') as mock_cargar_xlsx:
            mock_df = pd.DataFrame({"nombre": ["Ana"], "edad": [30]})
            mock_cargar_xlsx.return_value = mock_df
            
            resultado = cargar_archivo(self.archivo_xlsx)

            mock_cargar_xlsx.assert_called_once_with(Path(self.archivo_xlsx))
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_parquet_bien_formado(self):
        """Test: archivo .parquet bien formado debe llamar a cargar_parquet"""
        import importlib
        cargar_archivo_mod = importlib.import_module('carga_datos.cargar_archivo')
        
        with mock.patch.object(cargar_archivo_mod, 'cargar_parquet') as mock_cargar_parquet:
            mock_df = pd.DataFrame({"nombre": ["Carlos"], "edad": [35]})
            mock_cargar_parquet.return_value = mock_df
            
            resultado = cargar_archivo(self.archivo_parquet)
            
            mock_cargar_parquet.assert_called_once_with(Path(self.archivo_parquet))
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_extension_desconocida(self):
        """Test: archivo con extensión desconocida debe lanzar ValueError"""
        with pytest.raises(ValueError, match="Extensión de archivo no soportada"):
            cargar_archivo(self.archivo_extension_desconocida)

    def test_cargar_archivo_sin_extension(self):
        """Test: archivo sin extensión debe lanzar ValueError"""
        with pytest.raises(ValueError, match="Extensión de archivo no soportada"):
            cargar_archivo(self.archivo_sin_extension)

    def test_cargar_archivo_csv_mayusculas(self):
        """Test: archivo .CSV (mayúsculas) debe tratarse como .csv"""
        import importlib
        cargar_archivo_mod = importlib.import_module('carga_datos.cargar_archivo')
        
        with mock.patch.object(cargar_archivo_mod, 'cargar_csv') as mock_cargar_csv:
            mock_df = pd.DataFrame({"nombre": ["Maria"], "edad": [28]})
            mock_cargar_csv.return_value = mock_df
            
            resultado = cargar_archivo(self.archivo_csv_mayusculas)
            
            mock_cargar_csv.assert_called_once_with(Path(self.archivo_csv_mayusculas))
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_xlsx_nombre_extraño(self):
        """Test: archivo .xlsx con nombre extraño debe funcionar igual"""
        import importlib
        cargar_archivo_mod = importlib.import_module('carga_datos.cargar_archivo')
        
        with mock.patch.object(cargar_archivo_mod, 'cargar_xlsx') as mock_cargar_xlsx:
            mock_df = pd.DataFrame({"columna": ["valor"]})
            mock_cargar_xlsx.return_value = mock_df
            
            resultado = cargar_archivo(self.archivo_xlsx_nombre_extraño)
            
            mock_cargar_xlsx.assert_called_once_with(Path(self.archivo_xlsx_nombre_extraño))
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_doble_extension_falsa(self):
        """Test: archivo con doble extensión falsa debe lanzar ValueError"""
        with pytest.raises(ValueError, match="Extensión de archivo no soportada"):
            cargar_archivo(self.archivo_doble_extension)

    def test_cargar_archivo_path_object(self):
        """Test: cargar_archivo debe funcionar con Path object"""
        import importlib
        cargar_archivo_mod = importlib.import_module('carga_datos.cargar_archivo')
        
        with mock.patch.object(cargar_archivo_mod, 'cargar_csv') as mock_cargar_csv:
            mock_df = pd.DataFrame({"test": ["data"]})
            mock_cargar_csv.return_value = mock_df
            
            resultado = cargar_archivo(Path(self.archivo_csv))
            
            mock_cargar_csv.assert_called_once_with(Path(self.archivo_csv))
            assert isinstance(resultado, pd.DataFrame)

    def test_cargar_archivo_tipos_invalidos(self):
        """Test: cargar_archivo debe validar tipos de entrada"""
        with pytest.raises(TypeError, match="El parámetro 'ruta' debe ser str o Path"):
            cargar_archivo(123)  # type: ignore
        
        with pytest.raises(TypeError, match="El parámetro 'ruta' debe ser str o Path"):
            cargar_archivo(None)  # type: ignore
        
        with pytest.raises(TypeError, match="El parámetro 'ruta' debe ser str o Path"):
            cargar_archivo(["ruta", "lista"])  # type: ignore

    def test_cargar_archivo_no_existe(self):
        """Test: cargar_archivo debe manejar archivo inexistente"""
        with pytest.raises(FileNotFoundError, match="El archivo .* no existe"):
            cargar_archivo("archivo_inexistente.csv")

    def test_cargar_archivo_propaga_errores_funciones_internas(self):
        """Test: cargar_archivo debe propagar errores de las funciones internas"""
        import importlib
        cargar_archivo_mod = importlib.import_module('carga_datos.cargar_archivo')
        
        with mock.patch.object(cargar_archivo_mod, 'cargar_csv') as mock_cargar_csv:
            mock_cargar_csv.side_effect = ValueError("Error específico de cargar_csv")
            
            with pytest.raises(ValueError, match="Error específico de cargar_csv"):
                cargar_archivo(self.archivo_csv)
                
            mock_cargar_csv.assert_called_once_with(Path(self.archivo_csv))

    def test_cargar_archivo_ruta_como_string(self):
        """Test: cargar_archivo debe funcionar con ruta como string (no Path)"""
        import importlib
        cargar_archivo_mod = importlib.import_module('carga_datos.cargar_archivo')
        
        with mock.patch.object(cargar_archivo_mod, 'cargar_csv') as mock_cargar_csv:
            mock_df = pd.DataFrame({"nombre": ["Test"], "edad": [25]})
            mock_cargar_csv.return_value = mock_df
            
            resultado = cargar_archivo(self.archivo_csv)  # Pasando como string
            
            mock_cargar_csv.assert_called_once_with(Path(self.archivo_csv))
            assert isinstance(resultado, pd.DataFrame)
            assert resultado.equals(mock_df)

    def test_cargar_archivo_nombre_con_espacios_al_final(self):
        """Test: cargar_archivo debe manejar rutas con espacios eliminándolos internamente"""
        # Crear archivo normal sin espacios en el nombre
        archivo_sin_espacios = os.path.join(self.temp_dir, "archivo_test.csv")
        with open(archivo_sin_espacios, 'w', encoding='utf-8') as f:
            f.write("nombre,edad\nJuan,25\n")
        
        # Crear rutas con espacios al final, inicio y ambos lados
        ruta_con_espacios_final = archivo_sin_espacios + "   "
        ruta_con_espacios_inicio = "   " + archivo_sin_espacios
        ruta_con_espacios_ambos = "   " + archivo_sin_espacios + "   "
        
        # Todas estas rutas deberían funcionar porque strip() elimina los espacios
        resultado_normal = cargar_archivo(archivo_sin_espacios)
        resultado_final = cargar_archivo(ruta_con_espacios_final)
        resultado_inicio = cargar_archivo(ruta_con_espacios_inicio)
        resultado_ambos = cargar_archivo(ruta_con_espacios_ambos)
        
        # Verificar que todos los resultados sean iguales
        assert resultado_normal.equals(resultado_final)
        assert resultado_normal.equals(resultado_inicio)
        assert resultado_normal.equals(resultado_ambos)
        
        # Verificar que todos son DataFrames válidos
        assert isinstance(resultado_normal, pd.DataFrame)
        assert isinstance(resultado_final, pd.DataFrame)
        assert isinstance(resultado_inicio, pd.DataFrame)
        assert isinstance(resultado_ambos, pd.DataFrame)
            
    def test_cargar_archivo_rutas_con_espacios_completo(self):
        """Test: cargar_archivo debe manejar rutas con espacios en diferentes posiciones"""
        # Crear archivo CSV normal
        archivo_normal = os.path.join(self.temp_dir, "espacios_test.csv")
        with open(archivo_normal, 'w', encoding='utf-8') as f:
            f.write("nombre,edad\nJuan,25\n")
        
        # Agregar espacios a la ruta
        ruta_con_espacios_final = archivo_normal + "  "
        ruta_con_espacios_inicio = "  " + archivo_normal
        ruta_con_espacios_ambos = "  " + archivo_normal + "  "
        
        # Todas estas rutas deberían funcionar igual
        resultado1 = cargar_archivo(archivo_normal)
        resultado2 = cargar_archivo(ruta_con_espacios_final)
        resultado3 = cargar_archivo(ruta_con_espacios_inicio)
        resultado4 = cargar_archivo(ruta_con_espacios_ambos)
        
        # Verificar que todos los resultados sean iguales
        assert resultado1.equals(resultado2)
        assert resultado1.equals(resultado3)
        assert resultado1.equals(resultado4)

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
        
        import importlib
        cargar_archivo_mod = importlib.import_module('carga_datos.cargar_archivo')
        
        with mock.patch.object(cargar_archivo_mod, 'cargar_csv') as mock_csv:
            mock_csv.return_value = pd.DataFrame({"test": ["data"]})
            cargar_archivo(archivo_Csv)
            mock_csv.assert_called_once()
        
        with mock.patch.object(cargar_archivo_mod, 'cargar_xlsx') as mock_xlsx:
            mock_xlsx.return_value = pd.DataFrame({"test": ["data"]})
            cargar_archivo(archivo_XlsX)
            mock_xlsx.assert_called_once()
        
        with mock.patch.object(cargar_archivo_mod, 'cargar_parquet') as mock_parquet:
            mock_parquet.return_value = pd.DataFrame({"test": ["data"]})
            cargar_archivo(archivo_PARQUET)
            mock_parquet.assert_called_once() 