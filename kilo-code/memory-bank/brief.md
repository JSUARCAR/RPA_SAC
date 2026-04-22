# Resumen Conciso del Proyecto SAC Automation

## Propósito
Automatización de carga masiva de anexos en el sistema SAC (Sistema de Administración de Contratos) de EPM, utilizando Selenium para interacción web y Excel como fuente de datos.

## Arquitectura Modular
- **main.py**: Orquestador principal que coordina el flujo de ejecución.
- **core/data_handler.py**: Manejo de datos desde Excel, incluyendo lectura de tareas y actualización de estados.
- **core/web_automator.py**: Automatización web con Selenium para login, búsqueda de procesos y carga de anexos.
- **core/config_loader.py**: Gestión centralizada de configuración desde múltiples fuentes.
- **core/logger_setup.py**: Configuración segura de logging con sanitización de datos sensibles.

## Tecnologías
- **Python 3.12**: Lenguaje principal.
- **Selenium WebDriver**: Automatización de navegador Chrome.
- **OpenPyXL**: Manipulación de archivos Excel.
- **WebDriver Manager**: Gestión automática de drivers de navegador.

## Flujo Principal
1. Carga configuración desde config.ini y Excel.
2. Lee tareas pendientes filtradas por fecha, medio y estado.
3. Para cada tarea: login en SAC, búsqueda de proceso, carga de anexo.
4. Actualiza estado en Excel y libera recursos.

## Características Clave
- Manejo robusto de excepciones con reintentos.
- Logging seguro sin exposición de credenciales.
- Copia segura de archivos Excel con timestamp.
- Búsqueda automática de archivos anexo por radicado o proceso SAC.

## Entrega y Ejecución
- **Script Batch**: Para desarrollo y pruebas rápidas.
- **Ejecutable Windows (.exe)**: Versión profesional autocontenida para usuarios finales (analistas), con ícono personalizado y sin consola.