# ==============================================================================
# Script: debug_login.py
# Propósito: Diagnóstico del flujo de login - Ingeniería inversa
# Uso: python debug_login.py
# ==============================================================================

import sys
import os
import logging
import configparser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.data_handler import DataHandler
from core.logger_setup import setup_logging


def diagnose_credentials():
    """
    Diagnostica el flujo completo de lectura de credenciales.
    """
    print("=" * 70)
    print("DIAGNÓSTICO DE LOGIN - SAC AUTOMATION RPA")
    print("=" * 70)

    setup_logging(verbose=True)
    logging.info("Iniciando diagnóstico de login...")

    try:
        config = configparser.ConfigParser()
        config.read("config.ini")

        if "Paths" not in config:
            print("[ERROR] Sección 'Paths' no encontrada en config.ini")
            return False

        print(f"\n[1] Config.ini Paths:")
        print(f"    - source_excel_path: {config['Paths'].get('source_excel_path')}")
        print(f"    - dest_dir: {config['Paths'].get('dest_dir')}")

        print("\n[2] Inicializando DataHandler...")
        data_handler = DataHandler(config["Paths"])

        print("\n[3] Configuración cargada desde Excel:")
        cfg = data_handler.config
        print(f"    - sac_url: {cfg.get('sac_url')}")
        print(f"    - sac_admin_url: {cfg.get('sac_admin_url')}")
        print(f"    - user (M2): '{cfg.get('user')}'")
        print(
            f"    - password (N2): {'*** LONGITUD: ' + str(len(cfg.get('password', ''))) if cfg.get('password') else 'NONE/EMPTY'}"
        )
        print(f"    - anexos_mercurio_path (K3): {cfg.get('anexos_mercurio_path')}")
        print(f"    - anexos_correo_path (K2): {cfg.get('anexos_correo_path')}")

        user = cfg.get("user")
        password = cfg.get("password")

        print("\n[4] Validación de credenciales:")

        validation_passed = True

        if not user:
            print("    [FAIL] Usuario está vacío o None")
            validation_passed = False
        elif str(user).strip() == "":
            print("    [FAIL] Usuario está en blanco")
            validation_passed = False
        else:
            print(f"    [PASS] Usuario: '{user}'")

        if not password:
            print("    [FAIL] Contraseña está vacía o None")
            validation_passed = False
        elif str(password).strip() == "":
            print("    [FAIL] Contraseña está en blanco")
            validation_passed = False
        else:
            print(f"    [PASS] Contraseña (longitud: {len(str(password))})")
            if len(str(password)) < 4:
                print("    [WARN] Contraseña sospechosamente corta")

        print("\n[5] Validación de rutas de anexos:")
        if not cfg.get("anexos_mercurio_path"):
            print("    [WARN] anexos_mercurio_path está vacío")
        else:
            print(f"    [INFO] anexos_mercurio_path: {cfg.get('anexos_mercurio_path')}")

        if not cfg.get("anexos_correo_path"):
            print("    [WARN] anexos_correo_path está vacío")
        else:
            print(f"    [INFO] anexos_correo_path: {cfg.get('anexos_correo_path')}")

        print("\n[6] Tareas pendientes encontradas:")
        tasks = data_handler.get_pending_tasks()
        print(f"    Total: {len(tasks)} tareas")

        if tasks:
            print("\n    Primeras 3 tareas:")
            for i, task in enumerate(tasks[:3]):
                print(
                    f"    [{i + 1}] Fila {task['row_index']}: Proceso {task['proceso_sac']}"
                )

        print("\n" + "=" * 70)
        if validation_passed:
            print("RESULTADO: Diagnóstico COMPLETADO - Credenciales VÁLIDAS")
            print("El bot debería poder iniciar sesión. Si falla, revisar:")
            print("  1. Contraseña expirada en el sistema SAC")
            print("  2. Cuenta bloqueada en EPM")
            print("  3. Cambios en la página web del SAC")
        else:
            print("RESULTADO: Diagnóstico FALLIDO - Revisar credenciales en Excel")
        print("=" * 70)

        return validation_passed

    except FileNotFoundError as e:
        print(f"\n[ERROR] Archivo no encontrado: {e}")
        print("    Verificar que el archivo Excel exista en la ruta de config.ini")
        return False
    except ValueError as e:
        print(f"\n[ERROR] Error de validación: {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR CRÍTICO] {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = diagnose_credentials()
    sys.exit(0 if success else 1)
