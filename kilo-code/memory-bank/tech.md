# Tecnologías y Configuración Técnica: SAC Automation

## Tecnologías Principales

### Lenguaje y Framework
- **Python**: 3.8+ (versión actual 3.12)
- **Selenium WebDriver**: 4.35.0 - Automatización web
- **OpenPyXL**: 3.1.5 - Manipulación de archivos Excel
- **WebDriver Manager**: 4.0.2 - Gestión automática de drivers

### Infraestructura
- **Sistema Operativo**: Windows 10/11 (principal), compatible con Linux/macOS
- **Navegador**: Google Chrome (con ChromeDriver automático)
- **Entorno Virtual**: venv (estándar de Python)

## Configuración de Desarrollo

### Dependencias Críticas
```
selenium==4.35.0
openpyxl==3.1.5
webdriver-manager==4.0.2
cryptography==44.0.2
pyinstaller==6.18.0
pillow==11.0.0
```

### Configuración de WebDriver
- Modo incógnito activado
- Deshabilitación de web security para entornos corporativos
- Ignorar errores de certificado SSL
- Ventana maximizada por defecto

### Gestión de Configuración
- Archivo `config.ini`: Rutas de archivos fuente y destino
- Excel maestro: `PARAMETROS_LOCALES` para configuración específica
- Variables de entorno opcionales para proxy corporativo

## Arquitectura Técnica

### Patrón de Diseño
- **Separación de Responsabilidades**: Módulos especializados (data_handler, web_automator, config_loader)
- **Page Object Model (POM)**: Planificado para futuras implementaciones
- **Inyección de Dependencias**: Coordinación a través de main.py

### Seguridad Implementada
- **Sanitización de Logs**: Función `_sanitize_log_message()` con hashing de rutas
- **Validación de Inputs**: Prevención de directory traversal
- **Manejo Seguro de Credenciales**: Almacenamiento en Excel con sanitización de logs
- **Auditorías de Dependencias**: pip-audit integrado

### Manejo de Excepciones
- **Reintentos Automáticos**: Para operaciones web inestables
- **Backoff Exponencial**: En timeouts y elementos no encontrados
- **Logging Robusto**: Captura de errores sin detener ejecución completa
- **Recuperación de Estado**: Continuación del procesamiento ante fallos individuales

## Herramientas de Desarrollo

### Calidad y Testing
- **pip-audit**: Escaneo continuo de vulnerabilidades en dependencias
- **bandit**: Análisis estático de seguridad (opcional)
- **Logging Detallado**: Múltiples niveles con configuración segura

### Ejecución y Distribución
- **Script Batch**: `run_sac_automation.bat` para ejecución simplificada en entorno de desarrollo.
- **Ejecutable Standalone**: `dist/SAC_Automation.exe` generado con PyInstaller.
  - Comando: `pyinstaller --noconsole --onefile --icon=app_icon.ico --name="SAC_Automation" main.py`
- **Modo Verbose**: Opción `--verbose` para debugging detallado.
- **Entorno Virtual**: Activación automática en script de inicio y usado para el build del executable.

## Restricciones Técnicas

### Dependencias Externas
- **Sistema SAC**: Interfaz web sujeta a cambios sin previo aviso
- **Red Corporativa**: Requisitos de conectividad específicos de EPM
- **Versiones de Chrome**: Compatibilidad con ChromeDriver específico

### Limitaciones
- **Interfaz Web**: Dependencia de selectores XPath (frágiles a cambios UI)
- **Archivos Excel**: Estructura fija requerida para funcionamiento
- **Credenciales**: Almacenamiento en texto plano según política actual

## Optimizaciones Implementadas

### Rendimiento
- **Procesamiento por Lotes**: Manejo eficiente de múltiples tareas
- **Espera Inteligente**: WebDriverWait con timeouts optimizados
- **Copia Segura**: Timestamp en archivos Excel para evitar conflictos

### Mantenibilidad
- **Código Modular**: Separación clara de responsabilidades
- **Documentación Completa**: Docstrings y comentarios detallados
- **Configuración Centralizada**: Fácil modificación de parámetros

## Monitoreo y Observabilidad

### Logging
- **Archivo Principal**: `sac_automation.log` con rotación automática
- **Niveles Múltiples**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Sanitización**: Prevención de exposición de datos sensibles

### Métricas
- **Contadores de Procesamiento**: Tareas completadas vs fallidas
- **Tiempos de Ejecución**: Marca de tiempo en cada operación
- **Estados en Excel**: Actualización automática del progreso