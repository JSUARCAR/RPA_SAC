"""
Módulo de automatización web para el sistema SAC.

Este módulo encapsula toda la lógica de Selenium para interactuar
con el sistema de Administración de Contratos (SAC) de EPM.

Classes
-------
WebAutomator
    Clase principal que gestiona la interacción con el navegador y
    la automatización del sitio web SAC.
"""

import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    InvalidSessionIdException,
    ElementClickInterceptedException,
)
from webdriver_manager.chrome import ChromeDriverManager
import re


class WebAutomator:
    """
    Gestiona la interacción con el navegador y la automatización web.

    Proporciona métodos para login, búsqueda de procesos, carga de anexos
    y gestión de archivos adjuntos en el sistema SAC.
    """

    XP_BTN_DOMINIO = "//*[@id='ContentPlaceHolder1_ddlDominios']/option[3]"
    XP_INPUT_USUARIO = "//*[@id='ContentPlaceHolder1_txtUsuario']"
    XP_INPUT_CLAVE = "//*[@id='txtPassword']"
    XP_BTN_LOGIN = "//*[@id='ContentPlaceHolder1_btnLogin']"
    XP_FILTRAR_PROCESO = (
        "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_btnFiltrarProcesos']/span"
    )
    XP_INPUT_NUM_PROCESO = (
        "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_txtFiltroNumeroProceso']"
    )
    XP_BTN_BUSCAR_PROCESO = (
        "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_btnBuscarFiltrosProcesos']"
    )
    XP_BTN_ANEXOS = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_btnAnexos']/span"
    XP_BTN_ACEPTAR = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_ucMensajeConfirmacion_lbtAceptar']"
    XP_MODAL_CONFIRMACION = '//*[@id="ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_ucMensajeConfirmacion_udpMensajeConfirmacion"]/div'
    XP_BTN_INSERTAR_ANEXO = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_lbtInsertarAnexo']"
    XP_INPUT_TITULO = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_txtTituloIng']"
    XP_INPUT_DESC = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_txtDescripcionIng']"
    XP_INPUT_GRUPO = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_txtGrupoDocumentoIng']"
    XP_INPUT_TIPO_DOC = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_txtTipoDocumentoIng']"
    XP_INPUT_ARCHIVO = (
        "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_inpArchivo']"
    )
    XP_BTN_CARGAR_ARCHIVO = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_udpCargueArchivo']/div/div/div/div[4]/div/div/a/span"
    XP_BTN_TITULO_ANEXO_ACEPTAR = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_udpTituloAnexosCon']//button[contains(@id,'Aceptar')]"
    XP_BTN_TITULO_ANEXO_CERRAR = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_udpTituloAnexosCon']//button[contains(@id,'Cerrar')]"
    XP_MODAL_TITULO = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_udpTituloAnexosCon']"
    XP_BTN_GUARDAR_ANEXO = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_lbtGuardarAnexo']/i"
    XP_BTN_CERRAR_MODAL1 = "//*[@id='btnCerrarModal1']"
    XP_BTN_CERRAR_ANEXOS = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_lbtCerrarAnexosCon']/span"
    XP_BTN_SALIR = "//*[@id='btnSalir']"

    def __init__(self, config):
        self.config = config
        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, 20)
        logging.info("Automatizador web inicializado correctamente")

    def _init_driver(self):
        """Inicializa el WebDriver de Chrome con configuración optimizada."""
        logger = logging.getLogger("WebAutomator")

        logger.debug("Configurando opciones del navegador Chrome...")
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--disable-web-security")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--allow-running-insecure-content")

        try:
            logger.info("Inicializando ChromeDriver...")
            chromedriver_path = ChromeDriverManager().install()
            logger.info(f"ChromeDriver listo: [📁:{chromedriver_path[:12]}...]")

            service = webdriver.chrome.service.Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
            self._verify_browser_version(driver)

            logger.info("Navegador Chrome iniciado correctamente")
            return driver

        except Exception as e:
            logger.critical(f"Fallo al inicializar ChromeDriver: {type(e).__name__}")
            logger.critical(
                "Acción sugerida: Verificar instalación de Chrome y permisos del sistema"
            )
            raise

    def _verify_browser_version(self, driver):
        """Verifica compatibilidad entre Chrome y ChromeDriver."""
        logger = logging.getLogger("WebAutomator")

        try:
            chrome_version = driver.capabilities.get("browserVersion", "unknown")
            chromedriver_version = driver.capabilities.get("chrome", {}).get(
                "chromedriverVersion", "unknown"
            )

            if chromedriver_version != "unknown":
                chromedriver_major = str(chromedriver_version).split(".")[0]
                chrome_major = str(chrome_version).split(".")[0]

                if chrome_major != chromedriver_major:
                    logger.warning(
                        f"⚠ Versión incompatibles | Chrome: {chrome_version} | ChromeDriver: {chromedriver_version}"
                    )
                    logger.warning(
                        "Esto puede causar errores de sesión. Considere actualizar webdriver-manager"
                    )
                else:
                    logger.debug(f"✓ Versiones compatibles | Chrome: {chrome_version}")
        except Exception:
            logger.debug("No se pudo verificar la versión del navegador")

    def _click(self, xpath, max_retries=2):
        """Realiza un clic en un elemento identificado por XPath con reintento automático."""
        logger = logging.getLogger("WebAutomator")

        for attempt in range(1, max_retries + 1):
            try:
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                element.click()
                return
            except StaleElementReferenceException:
                if attempt < max_retries:
                    logger.debug(f"Elemento desactualizado, reintentando clic...")
                    time.sleep(0.5)
                else:
                    raise
            except ElementClickInterceptedException as e:
                if attempt < max_retries:
                    logger.debug(
                        f"Clic bloqueado por overlay, intentando con JavaScript..."
                    )
                    self._js_click(xpath)
                    return
                else:
                    logger.warning(f"No se pudo hacer clic en elemento: {xpath}")
                    raise

    def _send_keys(self, xpath, text):
        """Envía texto a un elemento de entrada con validación y reintento automático."""
        logger = logging.getLogger("WebAutomator")
        max_retries = 3

        for attempt in range(max_retries):
            try:
                element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                element.clear()
                element.send_keys(text)
                return
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    logger.debug(
                        f"Reintentando envío de datos (intento {attempt + 2}/{max_retries})..."
                    )
                    time.sleep(0.5)
                else:
                    logger.error(f"Fallo después de {max_retries} intentos")
                    raise

    def _wait_for_overlay_to_disappear(self, timeout=30):
        """Espera hasta que el overlay de carga desaparezca."""
        logger = logging.getLogger("WebAutomator")

        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.invisibility_of_element_located((By.ID, "loading")))
            logger.debug("Overlay de carga cerrado")
        except TimeoutException:
            logger.warning("Overlay de carga no desapareció en el tiempo esperado")

    def _js_click(self, xpath):
        """Realiza un clic usando JavaScript para evitar problemas de overlay."""
        logger = logging.getLogger("WebAutomator")
        logger.debug(f"Ejecutando clic via JavaScript: {xpath[:50]}...")
        element = self.driver.find_element(By.XPATH, xpath)
        self.driver.execute_script("arguments[0].click();", element)

    def _cerrar_modales_residuales(self):
        """Cierra cualquier modal que haya quedado abierto de operaciones anteriores."""
        logger = logging.getLogger("WebAutomator")

        MODALES_IDS = [
            "ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_panModalAnexosCon",
            "ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_udpTituloAnexosCon",
            "ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_udpMensajeConfirmacion",
        ]

        try:
            for modal_id in MODALES_IDS:
                script = f"""
                    var modal = document.getElementById('{modal_id}');
                    if (modal && modal.classList.contains('show')) {{
                        modal.classList.remove('show');
                        modal.style.display = 'none';
                    }}
                """
                self.driver.execute_script(script)
        except Exception as e:
            logger.debug(f"Error al cerrar modales residuales: {type(e).__name__}")

    def _manejar_modal_titulo_anexo(self):
        """Maneja el modal de título de anexo que aparece después de adjuntar archivo."""
        logger = logging.getLogger("WebAutomator")

        logger.debug("Verificando si aparece modal de título de anexo...")

        try:
            wait = WebDriverWait(self.driver, 10)

            if wait.until(
                EC.visibility_of_element_located((By.XPATH, self.XP_MODAL_TITULO))
            ):
                logger.debug("Modal de título detectado, procesando...")

                try:
                    logger.debug("Intentando cerrar modal con botón de aceptar...")
                    self._js_click(self.XP_BTN_TITULO_ANEXO_ACEPTAR)
                except Exception:
                    try:
                        logger.debug("Intentando cerrar modal con botón cerrar...")
                        self._js_click(self.XP_BTN_TITULO_ANEXO_CERRAR)
                    except Exception:
                        logger.debug("Cerrando modal via JavaScript...")
                        self.driver.execute_script("""
                            var modal = document.getElementById('ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_udpTituloAnexosCon');
                            if (modal) {
                                modal.classList.remove('show');
                                modal.style.display = 'none';
                                modal.style.visibility = 'hidden';
                            }
                        """)

                time.sleep(2)
                self._wait_for_overlay_to_disappear()
                logger.debug("Modal de título cerrado correctamente")

        except TimeoutException:
            logger.debug("Modal de título no appeared, continuando...")
            pass

    def login(self):
        """Realiza el proceso de autenticación en el sistema SAC."""
        logger = logging.getLogger("WebAutomator")
        user = self.config.get("user")
        password = self.config.get("password")

        logger.info("Validando credenciales de acceso...")

        if not user or not password:
            logger.critical("Credenciales no encontradas en configuración")
            logger.critical(
                "Verificar celdas M2 (usuario) y N2 (contraseña) en PARAMETROS_LOCALES"
            )
            raise ValueError("Credenciales faltantes en la configuración")

        user_str = str(user).strip()
        password_str = str(password).strip()

        if len(password_str) < 4:
            logger.warning(
                f"Contraseña con longitud inusual: {len(password_str)} caracteres"
            )

        if not user_str or not password_str:
            logger.critical("Usuario o contraseña están vacíos")
            raise ValueError("Credenciales inválidas: campos vacíos")

        try:
            sac_url = self.config.get("sac_url")
            logger.info(f"Conectando con portal SAC: {sac_url}")
            self.driver.get(sac_url)
            time.sleep(3)

            logger.debug("Seleccionando dominio de autenticación...")
            self._click(self.XP_BTN_DOMINIO)
            time.sleep(2)

            logger.debug(f"Ingresando credenciales de usuario: [{user_str[:3]}***]")
            self._send_keys(self.XP_INPUT_USUARIO, user_str)
            time.sleep(2)

            logger.debug("Ingresando contraseña...")
            self._send_keys(self.XP_INPUT_CLAVE, password_str)
            time.sleep(2)

            logger.debug("Enviando formulario de autenticación...")
            self._click(self.XP_BTN_LOGIN)
            time.sleep(3)

            logger.info("✓ Autenticación en SAC completada exitosamente")

        except TimeoutException:
            logger.error(
                "Timeout durante autenticación: elementos de login no cargaron"
            )
            logger.error(
                "Causa probable: página lenta, red lenta, o portal SAC no disponible"
            )
            logger.error(
                "Acción sugerida: Verificar conectividad y disponibilidad del portal"
            )
            raise
        except Exception as e:
            logger.error(f"Fallo durante el proceso de login: {type(e).__name__}: {e}")
            logger.error(
                "Acción sugerida: Revisar credenciales y estado del portal SAC"
            )
            raise

    def process_task(self, task):
        """Procesa una tarea de carga de anexo completa."""
        logger = logging.getLogger("WebAutomator")

        num_proceso = task["proceso_sac"]
        logger.debug(f"Iniciando carga de anexo para proceso: {num_proceso}")

        self._cerrar_modales_residuales()
        self._buscar_proceso(num_proceso)
        self._cargar_anexo(task)
        self._cerrar_modales_seguro()

        logger.info(f"Anexo cargado exitosamente para proceso {num_proceso}")

    def _verify_session_active(self):
        """Verifica si la sesión del navegador sigue activa."""
        logger = logging.getLogger("WebAutomator")

        try:
            self.driver.current_url
            return True
        except InvalidSessionIdException:
            logger.warning("Sesión del navegador expirada")
            return False

    def _reinit_driver_and_login(self):
        """Re-inicializa el driver y autentica nuevamente tras pérdida de sesión."""
        logger = logging.getLogger("WebAutomator")

        logger.info("Re-estableciendo conexión con SAC...")
        try:
            if self.driver:
                try:
                    self.driver.quit()
                except Exception:
                    pass

            self.driver = self._init_driver()
            self.wait = WebDriverWait(self.driver, 20)
            self.login()
            logger.info("✓ Sesión re-establecida exitosamente")
            return True
        except Exception as e:
            logger.error(f"No se pudo recuperar la sesión: {type(e).__name__}")
            raise

    def _buscar_proceso(self, num_proceso):
        """Busca un proceso específico en el sistema SAC con reintento automático."""
        logger = logging.getLogger("WebAutomator")
        max_retries = 3

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(
                    f"Buscando proceso {num_proceso} (intento {attempt}/{max_retries})..."
                )

                if not self._verify_session_active():
                    self._reinit_driver_and_login()

                sac_admin_url = self.config.get("sac_admin_url")
                logger.debug(
                    f"Navegando a módulo de administración: [{sac_admin_url[:50]}...]"
                )
                self.driver.get(sac_admin_url)
                time.sleep(5)

                self._wait_for_overlay_to_disappear()

                self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, self.XP_INPUT_NUM_PROCESO)
                    )
                )

                logger.debug("Ingresando número de proceso...")
                self._click(self.XP_FILTRAR_PROCESO)
                self._send_keys(self.XP_INPUT_NUM_PROCESO, num_proceso)
                self._click(self.XP_BTN_BUSCAR_PROCESO)
                self._wait_for_overlay_to_disappear()

                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, self.XP_BTN_ANEXOS))
                )
                logger.info(f"✓ Proceso {num_proceso} localizado correctamente")
                return

            except InvalidSessionIdException:
                logger.warning(
                    f"Pérdida de sesión detectada (intento {attempt}/{max_retries})"
                )
                if attempt < max_retries:
                    logger.info("Reintentando operación...")
                    self._reinit_driver_and_login()
                else:
                    logger.critical(f"Sesión perdida después de {max_retries} intentos")
                    logger.critical(
                        "Acción sugerida: Verificar estabilidad de red y sesión activa en portal SAC"
                    )
                    raise

            except TimeoutException:
                logger.warning(
                    f"Timeout esperando respuesta del servidor (intento {attempt}/{max_retries})"
                )
                if attempt < max_retries:
                    logger.info("Reintentando navegación...")
                    time.sleep(3)
                else:
                    logger.error(
                        "No se pudo completar la búsqueda después de múltiples intentos"
                    )
                    raise

    def _cargar_anexo(self, task):
        """Carga el archivo anexo para la tarea dada en el sistema SAC."""
        import os

        logger = logging.getLogger("WebAutomator")

        proceso_sac = task["proceso_sac"]
        logger.info(f"Iniciando carga de anexo para proceso {proceso_sac}...")

        self._click(self.XP_BTN_ANEXOS)

        try:
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, self.XP_BTN_ACEPTAR))
            ).click()
        except Exception:
            logger.debug("Modal de confirmación no apareció, continuando...")
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, self.XP_BTN_INSERTAR_ANEXO))
            ).click()

        self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.XP_INPUT_TITULO))
        )

        texto_anexo = (
            f"[ANEXO USUARIO | {task.get('medio', '')} - {task.get('asunto', 'Anexo')}]"
        )
        logger.debug(f"Estableciendo título del anexo: {texto_anexo}")
        self._send_keys(self.XP_INPUT_TITULO, texto_anexo)
        self._send_keys(self.XP_INPUT_DESC, texto_anexo)

        input_grupo = self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.XP_INPUT_GRUPO))
        )
        if not input_grupo.get_attribute("value"):
            logger.debug("Asignando grupo de documento por defecto: 17")
            self._send_keys(self.XP_INPUT_GRUPO, "17")

        self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))
        self._click(self.XP_INPUT_TIPO_DOC)
        time.sleep(2)

        self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))
        self._send_keys(self.XP_INPUT_TIPO_DOC, "234")
        time.sleep(2)

        self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))

        ruta_archivo = self._find_attachment_file(task)
        if not ruta_archivo:
            logger.error(f"Archivo anexo no encontrado para proceso {proceso_sac}")
            logger.error(
                f"Búsqueda realizada con claves: no_pqr={task.get('no_pqr')}, proceso_sac={proceso_sac}"
            )
            raise FileNotFoundError(
                f"No se encontró archivo anexo para proceso {proceso_sac}"
            )

        logger.info(
            f"Preparando archivo para carga: [{ruta_archivo.split(os.sep)[-1]}]"
        )
        input_archivo = self.driver.find_element(By.XPATH, self.XP_INPUT_ARCHIVO)
        if not input_archivo.is_displayed():
            self.driver.execute_script(
                "arguments[0].style.display = 'block';", input_archivo
            )

        logger.debug("Adjuntando archivo al formulario...")
        input_archivo.send_keys(ruta_archivo)
        time.sleep(2)

        self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))
        logger.debug("Iniciando subida de archivo al servidor...")
        self._click(self.XP_BTN_CARGAR_ARCHIVO)

        self._manejar_modal_titulo_anexo()

        self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))
        logger.debug("Guardando anexo en sistema...")
        self._click(self.XP_BTN_GUARDAR_ANEXO)

        self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))
        time.sleep(2)
        self._cerrar_modales_seguro()

        logger.info(f"✓ Anexo cargado correctamente para proceso {proceso_sac}")

    def _find_attachment_file(self, task):
        """Busca el archivo anexo basado en el radicado o número de proceso."""
        import os

        logger = logging.getLogger("WebAutomator")

        no_pqr = str(task.get("no_pqr", "")).strip()
        proceso_sac = str(task.get("proceso_sac", "")).strip()

        search_keys = [key for key in [no_pqr, proceso_sac] if key]
        if not search_keys:
            logger.warning("Tarea sin identificadores para búsqueda de archivo")
            return None

        base_paths = [
            self.config.get("anexos_mercurio_path"),
            self.config.get("anexos_correo_path"),
        ]
        extensions = [".pdf", ".msg", ".eml"]

        logger.debug(f"Buscando archivo con claves: {search_keys}")

        for key in search_keys:
            for base_path in base_paths:
                if not base_path:
                    continue
                for ext in extensions:
                    file_path = os.path.join(base_path, key + ext)
                    if os.path.exists(file_path):
                        logger.info(f"✓ Archivo localizado: [{key}{ext}]")
                        return file_path

        logger.warning(f"Archivo no encontrado para claves: {search_keys}")
        logger.warning(f"Rutas verificadas: {[p for p in base_paths if p]}")
        return None

    def _cerrar_modales_seguro(self):
        """Cierra los modales de anexos de forma segura con fallback a JavaScript."""
        logger = logging.getLogger("WebAutomator")

        self._wait_for_overlay_to_disappear()

        try:
            self._click(self.XP_BTN_CERRAR_MODAL1)
        except Exception:
            logger.debug("Modal de confirmación ya cerrado o no presente")

        time.sleep(0.5)
        self._wait_for_overlay_to_disappear()

        try:
            self._click(self.XP_BTN_CERRAR_ANEXOS)
        except ElementClickInterceptedException:
            logger.debug("Modal bloqueado, intentando cierre forzado con JavaScript...")
            self.driver.execute_script("""
                var modal = document.getElementById('ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_panModalAnexosCon');
                if (modal) {
                    modal.classList.remove('show');
                    modal.style.display = 'none';
                }
            """)
            time.sleep(1)
        except Exception:
            logger.debug("Modal de anexos ya cerrado o no presente")

        self._wait_for_overlay_to_disappear()

    def close(self):
        """Cierra la sesión en SAC y el navegador."""
        logger = logging.getLogger("WebAutomator")

        if self.driver:
            self._cerrar_modales_residuales()
            try:
                logger.info("Cerrando sesión en portal SAC...")
                self._js_click(self.XP_BTN_SALIR)
            except Exception as e:
                logger.warning(f"Cierre de sesión irregular: {type(e).__name__}")
            finally:
                self.driver.quit()
                logger.info("✓ Navegador cerrado correctamente")
