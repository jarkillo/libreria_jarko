# Librería Jarko - Funciones Utilitarias

[![Tests](https://github.com/jarkillo/libreria_jarko/actions/workflows/python-tests.yml/badge.svg)](https://github.com/USUARIO/libreria_jarko/actions/workflows/python-tests.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Esta librería contiene funciones utilitarias para facilitar tareas comunes de procesamiento de datos y normalización de texto, organizadas en módulos especializados.

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
from libreria_jarko.carga_datos.cargar_csv import cargar_csv
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
from libreria_jarko.carga_datos.cargar_parquet import cargar_parquet
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
from libreria_jarko.carga_datos.cargar_xlsx import cargar_xlsx
df = cargar_xlsx("datos.xlsx")
```

#### `cargar_archivo`

**Descripción**: Carga un archivo detectando automáticamente el formato por extensión y llamando a la función correspondiente.

**Firma**: 
```python
def cargar_archivo(ruta: Union[str, Path]) -> pd.DataFrame
```

**Parámetros**:
- `ruta`: Ruta del archivo a cargar (str o Path)

**Retorna**: DataFrame de pandas con el contenido del archivo

**Formatos soportados**:
- ✅ `.csv`, `.CSV` → llama a `cargar_csv()`
- ✅ `.xlsx`, `.XLSX` → llama a `cargar_xlsx()`
- ✅ `.parquet`, `.PARQUET` → llama a `cargar_parquet()`

**Formatos NO soportados**:
- ❌ `.xls` (Excel antiguo)
- ❌ `.ods` (LibreOffice/OpenOffice)
- ❌ `.json`, `.xml`, `.tsv`, `.txt`
- ❌ Cualquier otra extensión

**Errores**:
- `FileNotFoundError`: Si el archivo no existe
- `ValueError`: Si la extensión no es soportada o hay problemas en la función específica
- `TypeError`: Si el parámetro no es del tipo correcto

**Ejemplo de uso**:
```python
# Importar desde el paquete principal (recomendado)
from libreria_jarko import cargar_archivo

# Detección automática por extensión
df = cargar_archivo("datos.csv")        # Llama a cargar_csv()
df = cargar_archivo("datos.xlsx")       # Llama a cargar_xlsx()
df = cargar_archivo("datos.parquet")    # Llama a cargar_parquet()

# Funciona con Path objects
from pathlib import Path
df = cargar_archivo(Path("datos.csv"))

# O importar desde el módulo específico
from libreria_jarko.carga_datos.cargar_archivo import cargar_archivo
df = cargar_archivo("datos.csv")
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

### Módulo `normalizacion_texto`

#### `quitar_acentos`

**Descripción**: Elimina acentos y caracteres diacríticos del texto, convirtiéndolos a su equivalente ASCII.

**Firma**: 
```python
def quitar_acentos(texto: Any) -> str
```

**Parámetros**:
- `texto`: El texto del cual quitar los acentos (Any - se convertirá a string si no lo es)

**Retorna**: String sin acentos ni caracteres diacríticos

**Errores**:
- `TypeError`: Si no se puede convertir el input a string

**Ejemplo de uso**:
```python
# Importar desde el paquete principal (recomendado)
from libreria_jarko import quitar_acentos
resultado = quitar_acentos("José María")  # "Jose Maria"

# Funciona con diferentes tipos de entrada
resultado = quitar_acentos("niño español")  # "nino espanol"
resultado = quitar_acentos(123)  # "123"

# O importar desde el módulo específico
from libreria_jarko.normalizacion_texto.quitar_acentos import quitar_acentos
```

#### `convertir_a_minusculas`

**Descripción**: Convierte todo el texto a minúsculas de forma robusta.

**Firma**: 
```python
def convertir_a_minusculas(texto: Any) -> str
```

**Parámetros**:
- `texto`: El texto a convertir (Any - se convertirá a string si no lo es)

**Retorna**: String en minúsculas

**Errores**:
- `TypeError`: Si no se puede convertir el input a string

**Ejemplo de uso**:
```python
from libreria_jarko import convertir_a_minusculas
resultado = convertir_a_minusculas("HOLA MUNDO")  # "hola mundo"
resultado = convertir_a_minusculas("José MARÍA")  # "josé maría"
```

#### `convertir_a_mayusculas`

**Descripción**: Convierte todo el texto a mayúsculas de forma robusta.

**Firma**: 
```python
def convertir_a_mayusculas(texto: Any) -> str
```

**Parámetros**:
- `texto`: El texto a convertir (Any - se convertirá a string si no lo es)

**Retorna**: String en mayúsculas

**Errores**:
- `TypeError`: Si no se puede convertir el input a string

**Ejemplo de uso**:
```python
from libreria_jarko import convertir_a_mayusculas
resultado = convertir_a_mayusculas("hola mundo")  # "HOLA MUNDO"
resultado = convertir_a_mayusculas("josé maría")  # "JOSÉ MARÍA"
```

#### `limpiar_espacios`

**Descripción**: Limpia y normaliza espacios en blanco del texto.

**Firma**: 
```python
def limpiar_espacios(texto: Any) -> str
```

**Parámetros**:
- `texto`: El texto a limpiar (Any - se convertirá a string si no lo es)

**Retorna**: String con espacios normalizados

**Operaciones que realiza**:
- Elimina espacios al inicio y final (strip)
- Convierte múltiples espacios consecutivos en uno solo
- Convierte tabulaciones y saltos de línea en espacios simples
- Elimina espacios antes y después de signos de puntuación comunes

**Errores**:
- `TypeError`: Si no se puede convertir el input a string

**Ejemplo de uso**:
```python
from libreria_jarko import limpiar_espacios
resultado = limpiar_espacios("  hola   mundo  ")  # "hola mundo"
resultado = limpiar_espacios("texto\t\ncon\tespacios")  # "texto con espacios"
resultado = limpiar_espacios("hola , mundo ; bien")  # "hola, mundo; bien"
```

#### `normalizar_caracteres`

**Descripción**: Normaliza caracteres especiales y extraños a equivalentes ASCII más comunes.

**Firma**: 
```python
def normalizar_caracteres(texto: Any, reemplazos_personalizados: Optional[Dict[str, str]] = None) -> str
```

**Parámetros**:
- `texto`: El texto a normalizar (Any - se convertirá a string si no lo es)
- `reemplazos_personalizados`: Diccionario adicional de reemplazos personalizados (opcional)

**Retorna**: String con caracteres normalizados

**Caracteres que normaliza**:
- Comillas tipográficas: " " → " "
- Guiones largos: — – → -
- Puntos suspensivos: … → ...
- Símbolos matemáticos: × ÷ ± → x / +/-
- Monedas: € £ ¥ → EUR GBP YEN
- Espacios especiales Unicode → espacios normales

**Errores**:
- `TypeError`: Si no se puede convertir el input a string o si reemplazos_personalizados no es un diccionario

**Ejemplo de uso**:
```python
from libreria_jarko import normalizar_caracteres
resultado = normalizar_caracteres("Texto con "comillas" y —guiones—")  
# 'Texto con "comillas" y -guiones-'

# Con reemplazos personalizados
reemplazos = {"€": "EUROS"}
resultado = normalizar_caracteres("Precio: 25€", reemplazos)  # "Precio: 25EUROS"
```

#### `normalizar_texto`

**Descripción**: Función principal que combina todas las normalizaciones de forma configurable.

**Firma**: 
```python
def normalizar_texto(
    texto: Any,
    quitar_acentos_flag: bool = True,
    convertir_caso: Optional[Literal['minusculas', 'mayusculas']] = 'minusculas',
    limpiar_espacios_flag: bool = True,
    normalizar_caracteres_flag: bool = True,
    reemplazos_personalizados: Optional[Dict[str, str]] = None
) -> str
```

**Parámetros**:
- `texto`: El texto a normalizar (Any - se convertirá a string si no lo es)
- `quitar_acentos_flag`: Si aplicar eliminación de acentos (por defecto True)
- `convertir_caso`: Conversión de caso ('minusculas', 'mayusculas' o None, por defecto 'minusculas')
- `limpiar_espacios_flag`: Si aplicar limpieza de espacios (por defecto True)
- `normalizar_caracteres_flag`: Si aplicar normalización de caracteres especiales (por defecto True)
- `reemplazos_personalizados`: Reemplazos adicionales para normalizar_caracteres (opcional)

**Retorna**: String completamente normalizado según las opciones especificadas

**Orden de operaciones**:
1. Normalizar caracteres especiales
2. Quitar acentos
3. Convertir caso
4. Limpiar espacios

**Errores**:
- `TypeError`: Si los parámetros no son del tipo correcto
- `ValueError`: Si convertir_caso tiene un valor inválido
- Propaga errores de las funciones individuales

**Ejemplo de uso**:
```python
from libreria_jarko import normalizar_texto

# Normalización completa (por defecto)
resultado = normalizar_texto("  José María —texto con "comillas"  ")
# 'jose maria -texto con "comillas"'

# Solo conversión a mayúsculas
resultado = normalizar_texto("texto", convertir_caso='mayusculas')  # 'TEXTO'

# Sin conversión de caso
resultado = normalizar_texto("Texto", convertir_caso=None)  # 'texto'

# Con reemplazos personalizados
reemplazos = {"María": "Maria"}
resultado = normalizar_texto("José María", reemplazos_personalizados=reemplazos)
# 'jose maria'

# Configuración personalizada
resultado = normalizar_texto(
    "  JOSÉ™ MARÍA€  ",
    quitar_acentos_flag=True,
    convertir_caso='minusculas',
    limpiar_espacios_flag=True,
    normalizar_caracteres_flag=True
)
# 'josetm mariateur'
```

### Módulo `utils`

#### `procesar_ruta`

**Descripción**: Procesa una ruta eliminando espacios en blanco y convirtiéndola a Path object.

**Firma**: 
```python
def procesar_ruta(ruta: Union[str, Path]) -> Path
```

**Parámetros**:
- `ruta`: Ruta del archivo que se quiere procesar (str o Path)

**Retorna**: Path object con espacios eliminados

**Errores**:
- `TypeError`: Si el parámetro no es str o Path

**Ejemplo de uso**:
```python
from libreria_jarko.carga_datos.utils import procesar_ruta

# Limpia espacios al inicio y final
ruta_limpia = procesar_ruta("  archivo.csv  ")  # PosixPath('archivo.csv')

# Funciona con Path objects
from pathlib import Path
ruta_limpia = procesar_ruta(Path("archivo.csv "))  # PosixPath('archivo.csv')
```

#### `manejar_excepcion_inesperada`

**Descripción**: Maneja excepciones inesperadas de forma consistente, registrando en el log y re-lanzando la excepción.

**Firma**: 
```python
def manejar_excepcion_inesperada(excepcion: Exception, nombre_funcion: str) -> None
```

**Parámetros**:
- `excepcion`: La excepción que se produjo
- `nombre_funcion`: Nombre de la función donde ocurrió la excepción

**Retorna**: None (re-lanza la excepción original)

**Errores**:
- Re-lanza la excepción original después del logging

**Ejemplo de uso**:
```python
from libreria_jarko.carga_datos.utils import manejar_excepcion_inesperada

try:
    # algún código que puede fallar
    resultado = operacion_riesgosa()
except Exception as e:
    # Registra la excepción y la re-lanza
    manejar_excepcion_inesperada(e, 'mi_funcion')
```

## Instalación

Para usar esta librería necesitas:
```bash
pip install pandas pyarrow openpyxl
```

**Nota**: El módulo de normalización de texto solo requiere librerías estándar de Python (unicodedata, re), por lo que no necesita dependencias adicionales.

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
