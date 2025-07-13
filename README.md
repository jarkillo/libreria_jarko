# Librería Jarko - Funciones Utilitarias

[![Tests](https://github.com/jarkillo/libreria_jarko/actions/workflows/python-tests.yml/badge.svg)](https://github.com/USUARIO/libreria_jarko/actions/workflows/python-tests.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Esta librería contiene funciones utilitarias para facilitar tareas comunes de procesamiento de datos, organizadas en módulos especializados.

## Funciones Disponibles

### Módulo `carga_datos`

#### `cargar_csv`

**Descripción**: Carga un archivo CSV y lo devuelve como DataFrame de pandas con validaciones robustas.

**Firma**: 
```python
def cargar_csv(ruta: Union[str, Path], sep: str = ",", encoding: str = "utf-8") -> pd.DataFrame
```

**Parámetros**:
- `ruta`: Ruta del archivo CSV (str o Path)
- `sep`: Separador del archivo (por defecto ",")
- `encoding`: Codificación del archivo (por defecto "utf-8")

**Retorna**: DataFrame de pandas con el contenido del CSV

**Errores**:
- `FileNotFoundError`: Si el archivo no existe
- `ValueError`: Si hay problemas de encoding, parseo, archivo vacío, permisos o memoria insuficiente
- `TypeError`: Si los parámetros no son del tipo correcto

**Ejemplo de uso**:
```python
# Importar desde el paquete principal (recomendado)
from libreria_jarko import cargar_csv
df = cargar_csv("datos.csv")

# O importar desde el módulo específico
from libreria_jarko.carga_datos import cargar_csv
df = cargar_csv("datos.csv")

# Ejemplos de uso con diferentes parámetros
df = cargar_csv("datos.csv", sep=";")          # Separador personalizado
df = cargar_csv("datos.csv", encoding="latin1") # Encoding específico
```

#### `cargar_parquet`

**Descripción**: Carga un archivo Parquet y lo devuelve como DataFrame de pandas con validaciones robustas.

**Firma**: 
```python
def cargar_parquet(ruta: Union[str, Path], columns: Optional[List[str]] = None) -> pd.DataFrame
```

**Parámetros**:
- `ruta`: Ruta del archivo Parquet (str o Path)
- `columns`: Lista de columnas específicas a cargar (opcional)

**Retorna**: DataFrame de pandas con el contenido del archivo Parquet

**Errores**:
- `FileNotFoundError`: Si el archivo no existe
- `ValueError`: Si hay problemas con el archivo, columnas inexistentes, permisos o memoria insuficiente
- `TypeError`: Si los parámetros no son del tipo correcto

**Ejemplo de uso**:
```python
# Importar desde el paquete principal (recomendado)
from libreria_jarko import cargar_parquet
df = cargar_parquet("datos.parquet")

# Cargar solo columnas específicas
df = cargar_parquet("datos.parquet", columns=["nombre", "edad"])

# O importar desde el módulo específico
from libreria_jarko.carga_datos import cargar_parquet
df = cargar_parquet("datos.parquet")
```

#### `cargar_xlsx`

**Descripción**: Carga un archivo Excel (.xlsx) y lo devuelve como DataFrame de pandas con validaciones robustas.

**Firma**: 
```python
def cargar_xlsx(ruta: Union[str, Path], sheet_name: Union[str, int] = 0, 
                header: Optional[int] = 0, engine: Literal['xlrd', 'openpyxl', 'odf', 'pyxlsb', 'calamine'] = 'openpyxl') -> pd.DataFrame
```

**Parámetros**:
- `ruta`: Ruta del archivo Excel (str o Path)
- `sheet_name`: Nombre o índice de la hoja (por defecto 0)
- `header`: Número de fila para encabezado (por defecto 0, None para sin encabezado)
- `engine`: Motor de lectura (por defecto 'openpyxl')

**Retorna**: DataFrame de pandas con el contenido del archivo Excel

**Errores**:
- `FileNotFoundError`: Si el archivo no existe
- `ValueError`: Si hay problemas con el archivo, hoja inexistente, permisos o memoria insuficiente
- `TypeError`: Si los parámetros no son del tipo correcto

**Ejemplo de uso**:
```python
# Importar desde el paquete principal (recomendado)
from libreria_jarko import cargar_xlsx
df = cargar_xlsx("datos.xlsx")

# Cargar hoja específica
df = cargar_xlsx("datos.xlsx", sheet_name="Hoja1")
df = cargar_xlsx("datos.xlsx", sheet_name=1)

# Sin encabezado
df = cargar_xlsx("datos.xlsx", header=None)

# O importar desde el módulo específico
from libreria_jarko.carga_datos import cargar_xlsx
df = cargar_xlsx("datos.xlsx")
```

**Casos especiales que maneja**:
- ✅ Archivos CSV correctamente formateados
- ✅ Archivos con BOM (Byte Order Mark) 
- ✅ Archivos con columnas duplicadas (pandas las renombra automáticamente)
- ✅ Separadores incorrectos (detecta y maneja apropiadamente)
- ✅ Archivos con comas internas en los valores
- ✅ Archivos con caracteres especiales y acentos
- ✅ Archivos con filas inconsistentes (columnas faltantes o extras)
- ✅ Archivos con encabezados malformados
- ✅ Archivos con separadores mixtos por línea
- ✅ Archivos binarios renombrados como CSV (detecta y lanza error)
- ✅ Archivos JSON/Excel renombrados como CSV (detecta y lanza error)
- ✅ Archivos con problemas de permisos
- ✅ Archivos demasiado grandes para memoria
- ✅ Archivos con encoding inexistente o inválido
- ✅ Archivos vacíos o con solo encabezado
- ✅ Validación de tipos de parámetros

**Tests comprehensivos**: Las funciones cuentan con tests que cubren todos los casos de uso y errores posibles, garantizando robustez y confiabilidad.

## Instalación

Para usar esta librería necesitas:
```bash
pip install pandas pyarrow openpyxl
```

Para ejecutar los tests:
```bash
pip install pytest
python -m pytest test/ -v
```

## CI/CD y Calidad del Código

Este proyecto utiliza GitHub Actions para:

- **Tests automatizados**: Ejecuta pytest en Python 3.9-3.12
- **Compatibilidad multiplataforma**: Tests en Ubuntu, Windows y macOS
- **Linting**: Verificación de estilo con flake8
- **Cobertura de código**: Reportes con coverage y Codecov
- **Integración continua**: Tests en cada push y pull request

### Comandos para desarrollo

```bash
# Ejecutar todos los tests
python -m pytest test/ -v

# Ejecutar tests con cobertura
coverage run -m pytest test/
coverage report -m

# Ejecutar linter
flake8 . --max-line-length=127

# Instalar en modo desarrollo
pip install -e .
```

## Convenciones

- Funciones y variables en `snake_case`
- Clases en `PascalCase`
- Constantes en `MAYUSCULAS_CON_GUIONES`
- Tipado explícito en todas las funciones
- Documentación en español con ejemplos ejecutables
- Tests obligatorios para cada función
- Cobertura de código > 90%
- Código compatible con Python 3.9+ 
