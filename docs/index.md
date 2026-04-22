# SAC Automation RPA

Sistema de automatización robótica de procesos (RPA) para la carga masiva de anexos en el Sistema de Administración de Contratos (SAC) de EPM.

## Descripción

Este proyecto automatiza el proceso de carga de anexos (documentos PDF, correos .msg) al sistema SAC, reduciendo significativamente el tiempo operativo y minimizando errores humanos.

## Características

- **Automatización de Login**: Navegación automática al portal SAC con credenciales desde Excel
- **Búsqueda Inteligente**: Localización de procesos por número SAC
- **Carga de Anexos**: Upload automático de archivos con metadatos
- **Recuperación de Sesión**: Auto-reconexión ante expiración de sesión
- **Manejo de Errores**: Reintentos automáticos y logging detallado
- **Trazabilidad**: Actualización automática del Excel de control

## Requisitos

- Python 3.10+
- Chrome/Chromium
- ChromeDriver (gestionado automáticamente)
- Microsoft Excel

## Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/anexos-sac-rpa.git
cd anexos-sac-rpa

# Crear entorno virtual
python -m venv sac_env
sac_env\Scripts\activate  # Windows
# source sac_env/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Instalar herramientas de documentación (opcional)
pip install -r requirements_docs.txt
```

## Uso Básico

```bash
# Ejecución normal
python main.py

# Con modo debug
python main.py --verbose

# Solo diagnóstico de login
python debug_login.py
```

## Estructura del Proyecto

```
├── core/                   # Módulos core del proyecto
│   ├── web_automator.py   # Automatización Selenium
│   ├── data_handler.py     # Manejo de Excel
│   ├── config_loader.py    # Carga de configuración
│   └── logger_setup.py     # Configuración de logging
├── src/                    # Implementación alternativa
├── docs/                    # Documentación
├── scripts/                 # Scripts de utilidad
├── main.py                 # Punto de entrada
└── config.ini              # Configuración general
```

## Métricas de Calidad

| Métrica | Estado |
|---------|--------|
| Docstring Coverage | 86.2% |
| Target | 90% |
| Estilo Docstrings | NumPy Convention |

## Documentación

- [API Reference](api/)
- [Installation Guide](install/requirements.md)
- [Configuration Guide](install/configuration.md)
- [Troubleshooting](troubleshooting.md)

## Licencia

Propiedad de EPM - Uso interno
