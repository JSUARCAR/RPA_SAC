# ==============================================================================
# Proyecto: Automatización SAC - Carga Masiva de Anexos
# Módulo: main.py (Orquestador Principal)
# Versión: 2.0.0
# Autor:   Equipo de Desarrollo Senior
# Descripción:
#   Punto de entrada de la aplicación. Orchestra el flujo de automatización
#   invocando los módulos de datos, web y configuración.
# ==============================================================================

import logging
import argparse
import configparser
import os
import sys
import time
from datetime import datetime
from core.logger_setup import setup_logging, get_audit_logger, get_metricas
from core.data_handler import DataHandler
from core.web_automator import WebAutomator


def main():
    """
    Función principal que orchestra el proceso de automatización.

    Flujo de ejecución:
    1. Configuración inicial de logging y parsing de argumentos
    2. Carga de configuración desde config.ini
    3. Inicialización del manejador de datos
    4. Obtención de tareas pendientes del Excel de control
    5. Inicialización del automatizador web y autenticación
    6. Procesamiento de cada tarea pendiente
    7. Liberación de recursos y guardado de cambios
    """
    inicio_total = time.time()
    metricas = get_metricas()
    audit = get_audit_logger()

    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    log_file_path = os.path.join(base_path, "sac_automation.log")

    parser = argparse.ArgumentParser(
        description="SAC Automation | Carga Masiva de Anexos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main.py                    Ejecución normal
  python main.py --verbose          Modo debug detallado
        """,
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Activa logging DEBUG en consola"
    )
    args = parser.parse_args()

    setup_logging(log_file=log_file_path, verbose=args.verbose)
    logger = logging.getLogger()

    logger.info("=" * 70)
    logger.info("INICIANDO AUTOMATIZACIÓN SAC v2.0")
    logger.info(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Directorio de trabajo: {base_path}")
    logger.info("=" * 70)

    audit.registrar("SESION", "Inicio de automatización", "INICIADO")

    data_handler = None
    automator = None

    try:
        config_path = os.path.join(base_path, "config.ini")
        logger.debug(f"Cargando configuración desde: {config_path}")

        config = configparser.ConfigParser()
        config.read(config_path)

        if not config.has_section("Paths"):
            raise KeyError(f"Sección [Paths] no encontrada en {config_path}")

        logger.info("Configuración cargada correctamente")

        logger.info("Inicializando manejador de datos...")
        data_handler = DataHandler(config["Paths"])

        logger.info("Consultando tareas pendientes en Excel de control...")
        tasks = data_handler.get_pending_tasks()

        if not tasks:
            logger.warning(
                " cola de trabajo vacía. No se encontraron tareas pendientes que cumplan los criterios de filtrado"
            )
            logger.info("=" * 70)
            logger.info("AUTOMATIZACIÓN FINALIZADA - SIN TRABAJO PENDIENTE")
            logger.info("=" * 70)
            audit.registrar("SESION", "Sin tareas pendientes", "OK")
            return

        logger.info(f" cola de trabajo cargada: {len(tasks)} tarea(s) pendiente(s)")

        metricas.iniciar_tiempo("autenticacion")
        logger.info("Inicializando automatizador web...")
        automator = WebAutomator(data_handler.config)

        logger.info("Estableciendo conexión con portal SAC...")
        automator.login()

        duracion_auth = metricas.finalizar_tiempo("autenticacion") or 0.0
        logger.info(f"Autenticación exitosa. Duración: {duracion_auth:.2f}s")
        audit.registrar(
            "AUTH", "Login en SAC", "OK", {"duracion_s": round(duracion_auth, 2)}
        )

        metricas.iniciar_tiempo("procesamiento_total")
        exitosas = 0
        fallidas = 0

        logger.info("=" * 70)
        logger.info(f"INICIANDO PROCESAMIENTO DE {len(tasks)} TAREA(S)")
        logger.info("=" * 70)

        for idx, task in enumerate(tasks, 1):
            proceso = task["proceso_sac"]
            metricas.iniciar_tiempo(f"tarea_{idx}")

            logger.info(f"[{idx}/{len(tasks)}] Procesando proceso SAC: {proceso}")

            try:
                automator.process_task(task)
                data_handler.update_task_status(task["row_index"], "ANEXO RPA")

                duracion_tarea = metricas.finalizar_tiempo(f"tarea_{idx}") or 0.0
                metricas.registrar_exito()
                exitosas += 1

                logger.info(
                    f"[{idx}/{len(tasks)}] ✓ Proceso {proceso} completado. Duración: {duracion_tarea:.2f}s"
                )
                audit.registrar(
                    "CARGA",
                    f"Anexo cargado - Proceso {proceso}",
                    "OK",
                    {"fila": task["row_index"], "duracion_s": round(duracion_tarea, 2)},
                )
                audit.registrar(
                    "CARGA",
                    f"Anexo cargado - Proceso {proceso}",
                    "OK",
                    {"fila": task["row_index"], "duracion_s": round(duracion_tarea, 2)},
                )

            except Exception as e:
                duracion_tarea = metricas.finalizar_tiempo(f"tarea_{idx}")
                metricas.registrar_error()
                fallidas += 1

                logger.error(f"[{idx}/{len(tasks)}] ✗ Fallo en proceso {proceso}: {e}")
                data_handler.update_task_status(
                    task["row_index"], "ERROR", message=str(e)
                )
                audit.registrar(
                    "CARGA",
                    f"Error en proceso {proceso}",
                    "ERROR",
                    {"fila": task["row_index"], "error": str(e)[:100]},
                )

        duracion_total = metricas.finalizar_tiempo("procesamiento_total") or 0.0

        logger.info("=" * 70)
        logger.info("RESUMEN DE EJECUCIÓN")
        logger.info("=" * 70)
        logger.info(f"  Total de tareas procesadas: {len(tasks)}")
        logger.info(f"  Exitosas: {exitosas} ({exitosas / len(tasks) * 100:.1f}%)")
        logger.info(f"  Fallidas: {fallidas} ({fallidas / len(tasks) * 100:.1f}%)")
        logger.info(f"  Duración total del procesamiento: {duracion_total:.2f}s")
        logger.info(f"  Tiempo promedio por tarea: {duracion_total / len(tasks):.2f}s")
        logger.info("=" * 70)

        resumen_metricas = metricas.obtener_resumen()
        audit.registrar(
            "SESION", "Ejecución completada", "FINALIZADO", resumen_metricas
        )

        if fallidas == 0:
            logger.info(
                "AUTOMATIZACIÓN COMPLETADA EXITOSAMENTE - 100% de tareas procesadas"
            )
        else:
            logger.warning(
                f"AUTOMATIZACIÓN COMPLETADA CON ADVERTENCIAS - {fallidas} tarea(s) fallida(s)"
            )

    except KeyboardInterrupt:
        logger.warning("Ejecución interrumpida por el usuario")
        audit.registrar("SESION", "Interrumpida por usuario", "INTERRUMPIDA")
        raise

    except Exception as e:
        logger.critical("=" * 70)
        logger.critical("ERROR CRÍTICO - LA EJECUCIÓN NO PUDO CONTINUAR")
        logger.critical("=" * 70)
        logger.critical(f"Causa: {type(e).__name__}: {e}")
        logger.critical("Acción sugerida: Revisar logs detallados y verificar:")
        logger.critical("  - Conexión a red")
        logger.critical("  - Disponibilidad del portal SAC")
        logger.critical("  - Credenciales en Excel de control (celdas M2, N2)")
        logger.critical("  - Permisos de acceso a carpetas de anexos")
        logger.critical("=" * 70)
        audit.registrar(
            "SESION",
            f"Error crítico: {type(e).__name__}",
            "FALLO_CRITICO",
            {"error": str(e)[:200]},
        )
        sys.exit(1)

    finally:
        duracion_ejecucion = time.time() - inicio_total

        if automator:
            logger.info("Cerrando conexión con portal SAC...")
            automator.close()

        if data_handler:
            logger.info("Guardando cambios en Excel de control...")
            data_handler.save()

        logger.info("Recursos liberados correctamente")
        logger.info(f"Duración total de la ejecución: {duracion_ejecucion:.2f}s")
        logger.info("=" * 70)
        logger.info("FIN DE LA EJECUCIÓN")
        logger.info("=" * 70)
        audit.registrar(
            "SESION",
            "Cierre de sesión",
            "OK",
            {"duracion_total_s": round(duracion_ejecucion, 2)},
        )


if __name__ == "__main__":
    main()
