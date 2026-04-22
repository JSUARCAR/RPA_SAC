# SAC Automation - Carga Masiva de Anexos

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Security Scan](https://img.shields.io/badge/security-pip--audit-green.svg)](https://pypi.org/project/pip-audit/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/JSUARCAR/RPA_SAC/releases)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/JSUARCAR/RPA_SAC/actions)

Automatización segura y eficiente para la carga masiva de anexos en el sistema SAC (Sistema de Administración de Contratos) de EPM. Utiliza Selenium WebDriver con medidas avanzadas de seguridad como encriptación de credenciales, sanitización de logs y validación de inputs.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Screenshots](#-screenshots)
- [Arquitectura de Seguridad](#-arquitectura-de-seguridad)
- [Roadmap](#-roadmap)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## 🚀 Características

- ✅ **Automatización Web Segura**: Selenium con configuración hardened
- 🔐 **Encriptación de Credenciales**: Fernet encryption para datos sensibles
- 📊 **Procesamiento Masivo**: Carga automática desde Excel
- 🛡️ **Sanitización de Logs**: Prevención de exposición de información sensible
- 🔍 **Validación de Inputs**: Directory traversal protection
- 📈 **Métricas de Rendimiento**: Logging detallado y estadísticas
- 🐳 **Contenedorización**: Soporte para Docker (planeado)

## 💻 Requisitos del Sistema

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows 10/11, Linux, macOS
- **Memoria RAM**: Mínimo 4GB
- **Espacio en Disco**: 500MB libres
- **Conexión a Internet**: Para descarga automática de ChromeDriver

## 📦 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/JSUARCAR/RPA_SAC.git
cd RPA_SAC
```

### 2. Configurar Entorno Virtual

```bash
# Crear entorno virtual
python -m venv sac_env

# Activar entorno virtual
# Windows:
sac_env\Scripts\activate
# Linux/macOS:
source sac_env/bin/activate

# Verificar activación (debe mostrar la ruta del entorno virtual)
which python  # o where python en Windows
```

### 3. Instalar Dependencias

```bash
# Actualizar pip en el entorno virtual
python -m pip install --upgrade pip

# Instalación segura con verificación de hashes
pip install -r requirements.txt --require-hashes
```

### 4. Verificar Instalación

```bash
# Ejecutar escaneo de seguridad
python -m pip_audit

# Verificar sintaxis y dependencias
python -c "import selenium, openpyxl, cryptography; print('✅ Instalación exitosa')"
```

### 4. Configuración Inicial

```bash
# Configurar variable de entorno para encriptación
export SAC_ENCRYPTION_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
```

## ⚙️ Configuración

### Archivo Excel de Control

El script requiere un archivo Excel con la siguiente estructura:

1. **Hoja CONTROL_DIARIO_PQR**: Datos de procesos a procesar
2. **Hoja PARAMETROS_LOCALES**: Configuración del sistema
3. **Hoja LOG**: Registro de operaciones

### Credenciales

Las credenciales se almacenan en `PARAMETROS_LOCALES`:
- Celda M2: Usuario
- Celda N2: Contraseña

**Nota de Seguridad**: Las credenciales se mantienen en texto plano en el Excel según configuración operativa actual. El script incluye funciones de sanitización de logs para prevenir exposición accidental de credenciales en archivos de log.

### Variables de Entorno

```bash
# Opcional: Configuración de proxy para entornos corporativos
export HTTP_PROXY="http://proxy.company.com:8080"
export HTTPS_PROXY="http://proxy.company.com:8080"
```

## 🎯 Uso

### Ejecución Básica

#### Opción 1: Ejecutable Windows (.bat)
```batch
# Doble clic en run_sac_automation.bat
# O ejecutar desde PowerShell:
.\run_sac_automation.bat
```

#### Opción 2: Ejecución Manual
```bash
# Activar entorno virtual
source sac_env/bin/activate  # Linux/macOS
# o
sac_env\Scripts\activate     # Windows

# Ejecutar script
python sac_automation.py

# Desactivar entorno
deactivate
```

#### Opción 3: Archivo Excel Específico
```bash
# Con archivo personalizado
python sac_automation.py --excel /path/to/your/file.xlsx
```

### Modo Verbose

```bash
# Con logging detallado
python sac_automation.py --verbose
```

### Procesamiento por Lotes

El script procesa automáticamente todos los registros que cumplan los criterios:
- Fecha del día actual
- Medio: "Escrito" o "M - E-Mail"
- Número de proceso válido
- Estado de anexo pendiente

### Salida del Script

```bash
# Activar entorno virtual antes de ejecutar
source sac_env/bin/activate  # Linux/macOS
# o
sac_env\Scripts\activate     # Windows

# Ejecutar script
python sac_automation.py
```

**Salida esperada:**
```
=== INICIANDO AUTOMATIZACIÓN SAC ===
Archivo Excel: Control_PQR_JSUARCAR_EMTELCO.xlsx
Paso 1: Cargando archivo Excel...
Paso 2: Inicializando navegador...
Paso 3: Realizando login...
Paso 4: Procesando filas del Excel...
Procesando proceso: SAC-2025-001 (fila 10)
✅ ÉXITO: Anexo cargado para radicado 'PQR-001'
=== AUTOMATIZACIÓN COMPLETADA EXITOSAMENTE ===
```

### Desactivar Entorno Virtual

```bash
# Después de usar el script
deactivate
```

## 📸 Screenshots

### Interfaz de Login SAC
![Login Interface](https://via.placeholder.com/800x600/4CAF50/FFFFFF?text=SAC+Login+Interface)

### Dashboard de Procesos
![Process Dashboard](https://via.placeholder.com/800x600/2196F3/FFFFFF?text=SAC+Process+Dashboard)

### Modal de Carga de Anexos
![Upload Modal](https://via.placeholder.com/800x600/FF9800/FFFFFF?text=Anexo+Upload+Modal)

### Reporte de Procesamiento
![Processing Report](https://via.placeholder.com/800x600/9C27B0/FFFFFF?text=Processing+Report)

## 🔒 Arquitectura de Seguridad

### Medidas Implementadas

1. **Sanitización de Logs (CWE-532)**
   - Función `_sanitize_log_message()` reemplaza rutas absolutas con hashes anónimos
   - Función `secure_log()` oculta credenciales y datos sensibles automáticamente
   - Prevención de exposición de información sensible en archivos de log

2. **Validación de Inputs y Directory Traversal (CWE-22)**
   - Método `_sanitize_path()` previene ataques de directory traversal
   - Validación de nombres de archivo con regex seguro
   - Verificación de que rutas estén dentro de directorios permitidos

3. **Configuración Hardened de WebDriver**
   - Modo incógnito para aislamiento de sesiones
   - Deshabilitación de web security (solo desarrollo local)
   - Ignorar errores de certificado SSL para entornos corporativos

4. **Gestión Segura de Dependencias**
   - Versiones pinned con hashes SHA256 en `requirements.txt`
   - Escaneos regulares de vulnerabilidades con `pip-audit`
   - Separación de dependencias críticas vs opcionales
   - Instalación en entornos virtuales aislados

### Auditorías de Seguridad

```bash
# Escaneo continuo de vulnerabilidades
pip-audit --format json | jq '.vulnerabilities[] | select(.severity == "HIGH")'

# Análisis estático de código
bandit -r . --format json
```

## 🗺️ Roadmap

### Versión 1.1.0 (Q1 2025)
- [ ] Soporte para Docker containers
- [ ] API REST para integración con otros sistemas
- [ ] Dashboard web para monitoreo en tiempo real

### Versión 1.2.0 (Q2 2025)
- [ ] Autenticación multifactor (MFA)
- [ ] Paralelización de procesos
- [ ] Integración con sistemas de logging centralizados

### Versión 2.0.0 (Q3 2025)
- [ ] Interfaz gráfica de usuario (GUI)
- [ ] Soporte para múltiples navegadores
- [ ] Machine learning para detección de anomalías

### Mejoras Continuas
- [ ] Mejora de performance
- [ ] Cobertura de tests al 90%
- [ ] Documentación técnica completa

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

### 1. Preparar el Entorno

```bash
# Verificar Python
python --version

# Instalar Git si no está disponible
# Windows: Descargar de https://git-scm.com
# Linux: sudo apt install git
```

### 2. Clonar el Proyecto

```bash
git clone https://github.com/JSUARCAR/RPA_SAC.git
cd RPA_SAC

# ⚠️ IMPORTANTE: Nunca commiteas archivos sensibles
# Verifica .gitignore antes de hacer commits
cat .gitignore
```

### 2. Crear Rama de Feature

```bash
git checkout -b feature/AmazingFeature
```

### 3. Commit tus Cambios

```bash
git commit -m 'Add some AmazingFeature'
```

### 4. Push a la Rama

```bash
git push origin feature/AmazingFeature
```

### 5. Abrir Pull Request

Ve a GitHub y crea un Pull Request desde tu rama.

### Guías de Contribución

- **Código**: Sigue PEP 8 y usa type hints
- **Tests**: Añade tests unitarios para nuevas funcionalidades
- **Documentación**: Actualiza README y docstrings
- **Seguridad**: Ejecuta `pip-audit` antes de commits

### Configuración de Desarrollo

```bash
# Crear y activar entorno virtual de desarrollo
python -m venv dev_env
source dev_env/bin/activate  # Linux/macOS
# o
dev_env\Scripts\activate     # Windows

# Instalar dependencias de desarrollo
pip install -r requirements.txt --require-hashes

# Instalar herramientas adicionales de desarrollo
pip install pytest coverage bandit

# Ejecutar tests
pytest

# Verificar cobertura
coverage run -m pytest
coverage report

# Análisis de seguridad estático
bandit -r .
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto

**Equipo de Desarrollo SAC Automation**
- **Email**: sac-automation@epm.com.co
- **Proyecto**: [GitHub Repository](https://github.com/JSUARCAR/RPA_SAC)
- **Documentación**: [Wiki](https://github.com/JSUARCAR/RPA_SAC/wiki)

---

⭐ **Si este proyecto te ayuda, ¡dale una estrella en GitHub!**

*Desarrollado con ❤️ por el equipo de Automatización EPM*
