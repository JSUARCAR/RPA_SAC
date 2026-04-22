"""
Sistema de Logging Profesional para SAC Automation.
=================================================

Este módulo proporciona un sistema de logging de nivel empresarial con:
- Formato unificado estructurado con columnas
- Sanitización de información sensible
- Supresión automática de logs de librerías externas
- Rotación de archivos por tamaño
- Logging de auditoría separado
- Métricas de rendimiento
- Colores ANSI para consola

Autor: Equipo de Desarrollo Senior
Versión: 2.0.0
"""

import logging
import logging.handlers
import hashlib
import re
import os
import sys
import time
from datetime import datetime
from functools import wraps
from typing import Optional, Dict, Any


LIBRERIAS_SILENCIADAS = {
    "urllib3": logging.WARNING,
    "selenium": logging.WARNING,
    "selenium.webdriver": logging.WARNING,
    "webdriver_manager": logging.WARNING,
    "PIL": logging.WARNING,
    "openpyxl": logging.WARNING,
    "cachecontrol": logging.WARNING,
    "charset_normalizer": logging.WARNING,
    "certifi": logging.WARNING,
    "idna": logging.WARNING,
}


class ColoredFormatter(logging.Formatter):
    """
    Formateador con soporte para colores ANSI en consola.

    Proporciona salida visual diferenciada por nivel de log para
    facilitar la identificación rápida de eventos.
    """

    COLORES = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[35m",
        "AUDIT": "\033[34m",
        "RESET": "\033[0m",
    }

    SIMBOLOS_ASCII = {
        "DEBUG": "[D]",
        "INFO": "[I]",
        "WARNING": "[W]",
        "ERROR": "[E]",
        "CRITICAL": "[C]",
        "AUDIT": "[A]",
    }

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        use_colors: bool = True,
    ):
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors and sys.stdout.isatty()
        self._es_windows = sys.platform == "win32"

    def format(self, record: logging.LogRecord) -> str:
        simbolo = self.SIMBOLOS_ASCII.get(record.levelname, "[*]")

        if self.use_colors and not self._es_windows:
            color = self.COLORES.get(record.levelname, self.COLORES["RESET"])
            record.levelname = f"{color}{record.levelname}{self.COLORES['RESET']}"
            record.msg = f"{color}{simbolo}{self.COLORES['RESET']} {record.msg}"
        else:
            record.levelname = f"[{record.levelname}]"
            record.msg = f"{simbolo} {record.msg}"

        return super().format(record)


class EliteLogFormatter(logging.Formatter):
    """
    Formateador de logs estilo élite con estructura de columnas.

    Formato de salida:
    [TIMESTAMP] | [LEVEL] | [MODULE]      | [OPERATION]           | [MESSAGE]
    2026-04-14  | INFO   | WebAutomator  | login_sac              | Credenciales validadas correctamente

    Diseñado para facilitar:
    - Lectura rápida en terminal
    - Filtrado eficiente con grep/awk
    - Parsing por herramientas de monitoring
    """

    def __init__(self, include_metadata: bool = True):
        super().__init__()
        self.include_metadata = include_metadata

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3]
        level = f"[{record.levelname:<8}]"

        module = getattr(record, "log_module", record.module)
        module = f"[{module:<15}]"

        operation = getattr(record, "log_operation", "general")
        operation = f"[{operation:<20}]"

        message = record.getMessage()
        sanitized = SanitizadorLog.sanitizar(message)

        base_format = f"{timestamp} | {level} | {module} | {operation} | {sanitized}"

        if hasattr(record, "log_metadata") and record.log_metadata:
            import json

            metadata_str = json.dumps(record.log_metadata, ensure_ascii=False)
            base_format += f"\n  Metadata: {metadata_str}"

        if record.exc_info and record.levelno >= logging.ERROR:
            exc_text = self.formatException(record.exc_info)
            base_format += f"\n  Excepción: {self._resumir_excepcion(exc_text)}"

        return base_format

    def _resumir_excepcion(self, exc_text: str) -> str:
        """Resume una excepción a su mensaje esencial."""
        lines = exc_text.strip().split("\n")
        essential = lines[0] if lines else "Error desconocido"
        essential = re.sub(r'File ".*?"', "File [...]", essential)
        essential = re.sub(r"Line \d+", "Line [...]", essential)
        return essential[:150]


class SanitizadorLog:
    """
    Sanitizador de información sensible para logs.

    Reemplaza automáticamente:
    - Rutas de archivos con hashes anónimos
    - Credenciales (usuarios, contraseñas, claves)
    - Tokens y sesiones
    - Direcciones IP y datos personales

    Implementa protecciones contra CWE-532 (Information Exposure Through Log Files).
    """

    _cache_rutas: Dict[str, str] = {}

    @classmethod
    def sanitizar(cls, mensaje: str) -> str:
        """Sanitiza un mensaje de log completo."""
        if not mensaje:
            return mensaje

        resultado = mensaje

        resultado = cls._sanitizar_rutas(resultado)
        resultado = cls._sanitizar_credenciales(resultado)
        resultado = cls._sanitizar_sensibles(resultado)

        return resultado

    @classmethod
    def _sanitizar_rutas(cls, texto: str) -> str:
        """Reemplaza rutas absolutas con hashes anónimos."""

        def replace_path(match):
            ruta = match.group(0)
            if ruta in cls._cache_rutas:
                return cls._cache_rutas[ruta]

            hash_ruta = hashlib.sha256(ruta.encode()).hexdigest()[:12]
            resultado = f"[📁:{hash_ruta}]"
            cls._cache_rutas[ruta] = resultado
            return resultado

        patron = r"[A-Za-z]:[\\\/][^\s'\"<>|]+|[/\w]+/[.\w/]+"
        return re.sub(patron, replace_path, texto)

    @classmethod
    def _sanitizar_credenciales(cls, texto: str) -> str:
        """Oculta credenciales sensibles."""
        patrones = [
            (r"user(?:uario)?[:=]\s*[\w@.]+", "[👤-USUARIO]"),
            (r"password|contraseña|passwd|pwd[:=]\s*\S+", "[🔐-CLAVE]"),
            (r"token[:=]\s*[\w\-.]+", "[🎫-TOKEN]"),
            (r"session(?:_id)?[:=]\s*[\w\-]+", "[🔑-SESIÓN]"),
            (r"api[_-]?key[:=]\s*[\w\-]+", "[🔑-APIKEY]"),
            (r"secret[:=]\s*\S+", "[🔐-SECRETO]"),
        ]

        for patron, reemplazo in patrones:
            texto = re.sub(patron, reemplazo, texto, flags=re.IGNORECASE)

        return texto

    @classmethod
    def _sanitizar_sensibles(cls, texto: str) -> str:
        """Oculta otros datos sensibles comunes."""
        patrones = [
            (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[📱-TELÉFONO]"),
            (r"\b\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\b", "[🌐-IP]"),
            (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[📧-EMAIL]"),
            (r"\b\d{5,}\b", "[🔢-ID]"),
        ]

        for patron, reemplazo in patrones:
            texto = re.sub(patron, reemplazo, texto)

        return texto


class AuditLogger:
    """
    Logger especializado para auditoría de operaciones de negocio.

    Registra eventos de alto nivel para compliance y trazabilidad:
    - Inicio/fin de procesos
    - Operaciones CRUD
    - Autenticaciones
    - Transferencias de datos

    Configurado para escritura inmediata (no buffering).
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._inicializado = False
        return cls._instance

    def __init__(self):
        if self._inicializado:
            return
        self._inicializado = True
        self.logger = logging.getLogger("sac_audit")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

    def configurar(self, log_file: str):
        """Configura el handler de archivo para auditoría."""
        audit_handler = logging.FileHandler(
            log_file.replace(".log", "_audit.log"), mode="a", encoding="utf-8"
        )
        audit_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        audit_handler.setFormatter(formatter)

        if not any(isinstance(h, logging.FileHandler) for h in self.logger.handlers):
            self.logger.addHandler(audit_handler)

    def registrar(
        self,
        operacion: str,
        detalle: str,
        estado: str = "OK",
        metadata: Optional[Dict] = None,
    ):
        """Registra un evento de auditoría."""
        timestamp = datetime.now().isoformat()
        meta_str = f" | Meta: {metadata}" if metadata else ""
        mensaje = f"{operacion} | {detalle} | Estado: {estado}{meta_str}"
        self.logger.info(mensaje)


class MetricasLogger:
    """
    Registrador de métricas de rendimiento.

    Calcula y almacena:
    - Tiempo de ejecución por operación
    - Throughput (operaciones/segundo)
    - Tasas de éxito/error
    - Uso de memoria (si disponible)
    """

    def __init__(self):
        self.metrica_inicio: Dict[str, float] = {}
        self.metrica_contador: Dict[str, int] = {"exitos": 0, "errores": 0}
        self.metrica_tiempos: Dict[str, list] = {}

    def iniciar_tiempo(self, operacion: str):
        """Marca el inicio de una operación."""
        self.metrica_inicio[operacion] = time.time()

    def finalizar_tiempo(self, operacion: str) -> Optional[float]:
        """Marca el fin y retorna la duración."""
        if operacion not in self.metrica_inicio:
            return None

        duracion = time.time() - self.metrica_inicio[operacion]

        if operacion not in self.metrica_tiempos:
            self.metrica_tiempos[operacion] = []
        self.metrica_tiempos[operacion].append(duracion)

        del self.metrica_inicio[operacion]
        return duracion

    def registrar_exito(self):
        """Incrementa contador de éxitos."""
        self.metrica_contador["exitos"] += 1

    def registrar_error(self):
        """Incrementa contador de errores."""
        self.metrica_contador["errores"] += 1

    def obtener_resumen(self) -> Dict[str, Any]:
        """Retorna resumen de métricas."""
        total_ops = self.metrica_contador["exitos"] + self.metrica_contador["errores"]
        tasa_exito = (
            (self.metrica_contador["exitos"] / total_ops * 100) if total_ops > 0 else 0
        )

        resumen = {
            "total_operaciones": total_ops,
            "exitos": self.metrica_contador["exitos"],
            "errores": self.metrica_contador["errores"],
            "tasa_exito_pct": round(tasa_exito, 2),
            "tiempos_promedio": {},
        }

        for op, tiempos in self.metrica_tiempos.items():
            if tiempos:
                resumen["tiempos_promedio"][op] = round(sum(tiempos) / len(tiempos), 3)

        return resumen


def medir_tiempo(operacion: str):
    """Decorador para medir tiempo de ejecución de funciones."""

    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            inicio = time.time()
            try:
                resultado = func(*args, **kwargs)
                duracion = time.time() - inicio
                logging.getLogger().debug(f"⏱ {operacion} | Duración: {duracion:.3f}s")
                return resultado
            except Exception as e:
                duracion = time.time() - inicio
                logging.getLogger().debug(
                    f"⏱ {operacion} | Duración hasta error: {duracion:.3f}s | Error: {e}"
                )
                raise

        return wrapper

    return decorador


class EliteLoggerAdapter(logging.LoggerAdapter):
    """
    Adapter que añade contexto estructurado a los logs.

    Permite agregar información de contexto como:
    - Módulo origen
    - Operación específica
    - Metadata adicional
    """

    def process(self, msg, kwargs):
        extra = kwargs.get("extra", {})

        module = extra.get("module", self.extra.get("module", "SYSTEM"))
        operation = extra.get("operation", self.extra.get("operation", "general"))
        metadata = extra.get("metadata", self.extra.get("metadata"))

        kwargs["extra"] = {
            "log_module": module,
            "log_operation": operation,
            "log_metadata": metadata,
        }
        return msg, kwargs


_global_audit_logger = AuditLogger()
_global_metricas = MetricasLogger()


def setup_logging(
    log_file: str = "sac_automation.log",
    level: int = logging.INFO,
    verbose: bool = False,
) -> logging.Logger:
    """
    Configura el sistema de logging profesional para SAC Automation.

    Esta función configura un sistema de logging completo con:
    1. Handler de archivo con rotación automática (10MB por archivo, 5 backups)
    2. Handler de consola con colores ANSI
    3. Supresión automática de logs de librerías externas
    4. Logger de auditoría separado
    5. Sanitización de información sensible

    Parameters
    ----------
    log_file : str
        Ruta del archivo de log principal.
    level : int
        Nivel mínimo de log (default: INFO).
    verbose : bool
        Si True, activa modo DEBUG en consola.

    Returns
    -------
    logging.Logger
        Logger raíz configurado.

    Examples
    --------
    >>> logger = setup_logging("app.log", verbose=True)
    >>> logger.info("Aplicación iniciada")
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    _silenciar_librerias_externas()

    log_dir = os.path.dirname(log_file) or "."
    os.makedirs(log_dir, exist_ok=True)

    file_formatter = EliteLogFormatter()

    rotating_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    rotating_handler.setLevel(level)
    rotating_handler.setFormatter(file_formatter)
    root_logger.addHandler(rotating_handler)

    console_level = logging.DEBUG if verbose else logging.INFO
    console_formatter = ColoredFormatter(
        "%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S", use_colors=True
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    _global_audit_logger.configurar(log_file)

    root_logger.info(
        "+====================================================================+\n"
        "|         SISTEMA DE LOGGING CONFIGURADO - v2.0                   |\n"
        "|  +----------------------------------------------------------+  |\n"
        "|  | Nivel archivo: INFO  | Nivel consola: {} |  |\n"
        "|  +----------------------------------------------------------+  |\n"
        "|  Modulos activos: Principal, WebAutomator, DataHandler       |\n"
        "+====================================================================+".format(
            "DEBUG" if verbose else "INFO"
        )
    )

    return root_logger


def _silenciar_librerias_externas():
    """Silencia los logs de librerías de terceros para reducir ruido."""
    for nombre_logger, nivel in LIBRERIAS_SILENCIADAS.items():
        logger = logging.getLogger(nombre_logger)
        logger.setLevel(nivel)

        if not logger.handlers:
            handler_nulo = logging.NullHandler()
            logger.addHandler(handler_nulo)


def get_logger(nombre: str) -> logging.LoggerAdapter:
    """
    Obtiene un logger configurado con contexto estructurado.

    Parameters
    ----------
    nombre : str
        Nombre del módulo/componente.

    Returns
    -------
    EliteLoggerAdapter
        Logger con capacidades de contexto estructurado.

    Examples
    --------
    >>> logger = get_logger('WebAutomator')
    >>> logger.info("Login exitoso", extra={'operation': 'autenticacion'})
    """
    logger = logging.getLogger(nombre)
    return EliteLoggerAdapter(logger, {"module": nombre})


def get_audit_logger() -> AuditLogger:
    """Obtiene la instancia global del logger de auditoría."""
    return _global_audit_logger


def get_metricas() -> MetricasLogger:
    """Obtiene la instancia global del registrador de métricas."""
    return _global_metricas
