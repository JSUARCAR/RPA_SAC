@echo off
REM ==============================================================================
REM SAC Automation Launcher - Windows Batch Script
REM Versión: 1.0.0
REM Fecha: 2025-10-24
REM Descripción: Script launcher para automatización SAC con entorno virtual
REM ==============================================================================

echo ==============================================================================
echo SAC Automation - Carga Masiva de Anexos
echo Version 1.0.0 - Windows Launcher
echo ==============================================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH
    echo Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

REM Verificar si el directorio del script existe
if not exist "%~dp0main.py" (
    echo ERROR: No se encuentra main.py en el directorio actual
    echo Directorio actual: %~dp0
    pause
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist "sac_env" (
    echo Creando entorno virtual...
    python -m venv sac_env
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo Entorno virtual creado
) else (
    echo Entorno virtual encontrado
)

REM Activar entorno virtual
echo Activando entorno virtual...
call sac_env\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

REM Verificar si las dependencias están instaladas
echo Verificando dependencias...
python -c "import selenium, openpyxl, cryptography" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    echo Intentando instalación con verificación de hashes...
    pip install -r requirements.txt --require-hashes --quiet
    if errorlevel 1 (
        echo Falló verificación de hashes, intentando instalación sin hashes...
        pip install selenium==4.35.0 openpyxl==3.1.5 cryptography==44.0.2 webdriver-manager==4.0.2 pip-audit==2.9.0 --quiet
        if errorlevel 1 (
            echo ERROR: No se pudieron instalar las dependencias
            echo Verifica tu conexión a internet
            echo Posibles soluciones:
            echo 1. Verifica tu conexión a internet
            echo 2. Actualiza pip: python -m pip install --upgrade pip
            echo 3. Instala manualmente: pip install selenium openpyxl cryptography
            pause
            exit /b 1
        )
        echo Dependencias instaladas (sin verificación de hashes)
    ) else (
        echo Dependencias instaladas con verificación de hashes
    )
) else (
    echo Dependencias verificadas
)

REM Ejecutar escaneo de seguridad (opcional)
echo Ejecutando escaneo de seguridad...
python -m pip_audit --quiet >nul 2>&1
if errorlevel 1 (
    echo ADVERTENCIA: Se encontraron vulnerabilidades en dependencias
    echo Para más detalles ejecuta: python -m pip_audit
    echo.
) else (
    echo Escaneo de seguridad completado
)

REM Ejecutar el script principal
echo.
echo Iniciando SAC Automation...
echo ==============================================================================
python main.py %*

REM Capturar código de salida
set EXITCODE=%errorlevel%

echo.
echo ==============================================================================
if %EXITCODE% equ 0 (
    echo SAC Automation completado exitosamente
) else (
    echo SAC Automation terminó con errores (código: %EXITCODE%)
)

REM Desactivar entorno virtual
call deactivate

echo.
echo Presiona cualquier tecla para Finalizar...
pause >nul

exit /b %EXITCODE%