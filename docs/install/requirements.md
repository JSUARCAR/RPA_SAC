# Requisitos de Instalación

## Dependencias del Sistema

### Python
- **Versión mínima**: Python 3.10
- **Versión recomendada**: Python 3.12

### Navegador
- **Chrome**: Versión 130+ (para compatibilidad con ChromeDriver 130+)
- **Chromium**: Alternativa compatible

### ChromeDriver
- Gestionado automáticamente por `webdriver-manager`
- No requiere instalación manual

## Dependencias Python

Ver archivo `requirements.txt`:

```
openpyxl>=3.1.0
selenium>=4.15.0
webdriver-manager>=4.0.0
configparser>=5.3.0
```

## Dependencias de Documentación (Opcional)

Ver archivo `requirements_docs.txt`:

```
pydocstyle>=6.3.0
interrogate>=1.5.0
docstring-parser>=0.15
mypy>=1.8.0
mkdocs>=1.5.0
mkdocstrings[python]>=0.24.0
pre-commit>=3.6.0
```

## Permisos Requeridos

- Lectura/escritura en directorio de trabajo
- Acceso a Internet (para ChromeDriver)
- Acceso al portal SAC (credenciales válidas)
