# Librería Jarko - Funciones Utilitarias

[![Tests](https://github.com/jarkillo/libreria_jarko/actions/workflows/python-tests.yml/badge.svg)](https://github.com/USUARIO/libreria_jarko/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/USUARIO/libreria_jarko/branch/main/graph/badge.svg)](https://codecov.io/gh/jarkillo/libreria_jarko)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Esta librería contiene funciones utilitarias para facilitar tareas comunes de procesamiento de datos.

## Funciones Disponibles

### `cargar_csv`

**Descripción**: Carga un archivo CSV y lo devuelve como DataFrame de pandas con validaciones robustas.

**Firma**: 
```python
def cargar_csv(ruta: Union[str, Path], sep: str = ";", encoding: str = "utf-8") -> pd.DataFrame
```

**Parámetros**:
- `ruta`: Ruta del archivo CSV (str o Path)
- `sep`: Separador del archivo (por defecto ";")
- `encoding`: Codificación del archivo (por defecto "utf-8")

**Retorna**: DataFrame de pandas con el contenido del CSV

**Errores**:
- `FileNotFoundError`: Si el archivo no existe
- `ValueError`: Si hay problemas de encoding, parseo o archivo vacío
- `TypeError`: Si los parámetros no son del tipo correcto

**Ejemplo de uso**:
```python
# Importar desde el paquete (recomendado)
import libreria_jarko as lj
df = lj.cargar_csv("datos.csv")

# O importar directamente la función
from libreria_jarko import cargar_csv
df = cargar_csv("datos.csv")

# También funciona importar desde el módulo específico
from carga_datos import cargar_csv
df = cargar_csv("datos.csv")

# Ejemplos de uso con diferentes parámetros
df = cargar_csv("datos.csv", sep=",")          # Separador personalizado
df = cargar_csv("datos.csv", encoding="latin1") # Encoding específico
```

## Instalación

Para usar esta librería necesitas:
```bash
pip install pandas
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
