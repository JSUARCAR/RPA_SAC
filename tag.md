# Ficha Técnica (TAG): SAC Automation

## 1. Tecnologías Principales

- **Lenguaje de Programación:** Python 3.8+
- **Framework de Automatización Web:** Selenium 4
- **Manipulación de Archivos Excel:** OpenPyXL
- **Encriptación (potencial):** Cryptography

## 2. Gestión de Dependencias y Entorno

- **Gestor de Entorno Virtual:** `venv` (módulo estándar de Python)
- **Gestor de Paquetes:** `pip`
- **Archivo de Dependencias:** `requirements.txt` (con versiones fijadas y hashes de seguridad)
- **Gestor de WebDriver:** `webdriver-manager` (para la descarga automática de ChromeDriver)

## 3. Sistema Operativo y Ejecución

- **Plataforma Principal:** Windows 10/11
- **Script de Ejecución:** Batch Script (`.bat`) para una ejecución simplificada en Windows.
- **Shell Requerido:** `cmd.exe` o `PowerShell` para la ejecución del `.bat`.

## 4. Herramientas de Calidad y Seguridad

- **Auditoría de Dependencias:** `pip-audit` (integrado en el script de inicio)
- **Análisis Estático de Código (potencial):** `bandit` (mencionado en la documentación)

## 5. Configuración del Proyecto

- **Archivo de Control Principal:** `Control_PQR_JSUARCAR_EMTELCO - AUTOMATIZADA - JSUARCAR.xlsx` (ubicado en una ruta de red)
- **Archivo de Log:** `sac_automation.log` (generado en el directorio raíz del proyecto)
- **Configuración de Credenciales y Rutas:** Almacenadas directamente en la hoja `PARAMETROS_LOCALES` del archivo Excel.