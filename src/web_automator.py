"""
Módulo de automatización web implementando el patrón Page Object Model (POM).

Contiene clases Page Object para LoginPage, ProcessSearchPage y AttachmentPage,
proporcionando una abstracción de alto nivel para interactuar con el sistema SAC.

Classes
-------
BasePage
    Clase base para todas las páginas Page Object.
LoginPage
    Page Object para la página de login del sistema SAC.
ProcessSearchPage
    Page Object para la página de búsqueda de procesos.
AttachmentPage
    Page Object para la gestión de anexos.
WebAutomator
    Clase principal que coordina los Page Objects.

Functions
---------
Ninguna públicas.

Examples
--------
>>> from src.web_automator import WebAutomator
>>> automator = WebAutomator(config)
>>> automator.login(credentials)
>>> automator.completar_formulario(datos)
"""

import logging
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from core.web_utils import WebUtils
from src.adaptive_wait import AdaptiveWaitStrategy

# ==============================================================================
# Page Object Model - Clases Base
# ==============================================================================


class BasePage:
    """
    Clase base para todas las páginas Page Object.

    Proporciona métodos comunes y configuración compartida para
    todas las páginas del patrón Page Object Model (POM).

    Examples
    --------
    >>> class MiPagina(BasePage):
    ...     def mi_metodo(self):
    ...         return self.safe_click("//button")
    """

    def __init__(self, driver, config):
        """
        Inicializa la página base con driver y configuración.

        Parameters
        ----------
        driver : selenium.webdriver
            Instancia del WebDriver de Selenium.
        config : dict
            Diccionario de configuración con URLs y credenciales.
        """
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, 20)
        self.adaptive_wait = AdaptiveWaitStrategy()

    def safe_click(self, xpath, timeout=10):
        """
        Realiza un clic seguro en el elemento especificado.

        Delega a WebUtils.safe_click para manejar excepciones
        y reintentos automaticos.

        Parameters
        ----------
        xpath : str
            Selector XPath del elemento a hacer clic.
        timeout : int, optional
            Tiempo maximo de espera en segundos. Default: 10.

        Returns
        -------
        bool
            True si el clic fue exitoso, False en caso contrario.
        """
        return WebUtils.safe_click(self.driver, xpath, timeout)

    def safe_send_keys(self, xpath, text, timeout=10):
        """
        Envía texto al elemento especificado de forma segura.

        Delega a WebUtils.safe_send_keys para manejar excepciones
        y reintentos automaticos.

        Parameters
        ----------
        xpath : str
            Selector XPath del elemento de entrada.
        text : str
            Texto a enviar al elemento.
        timeout : int, optional
            Tiempo maximo de espera en segundos. Default: 10.

        Returns
        -------
        bool
            True si el envio fue exitoso, False en caso contrario.
        """
        return WebUtils.safe_send_keys(self.driver, xpath, text, timeout)

    def wait_for_element(self, xpath, timeout=10):
        """
        Espera hasta que el elemento este presente y visible.

        Parameters
        ----------
        xpath : str
            Selector XPath del elemento a esperar.
        timeout : int, optional
            Tiempo maximo de espera en segundos. Default: 10.

        Returns
        -------
        WebElement or None
            El elemento WebElement si se encuentra, None si timeout.
        """
        return WebUtils.wait_for_element(self.driver, xpath, timeout)


class LoginPage(BasePage):
    """
    Page Object para la página de login del sistema SAC.

    Maneja la autenticación y selección de dominio del usuario
    en el sistema de administración de contratos.

    Examples
    --------
    >>> page = LoginPage(driver, config)
    >>> page.login({"user": "jsuarcar", "password": "secret"})
    """

    # Selectores XPath para elementos de login
    DOMAIN_SELECT = "//*[@id='ContentPlaceHolder1_ddlDominios']/option[3]"
    USERNAME_INPUT = "//*[@id='ContentPlaceHolder1_txtUsuario']"
    PASSWORD_INPUT = "//*[@id='txtPassword']"
    LOGIN_BUTTON = "//*[@id='ContentPlaceHolder1_btnLogin']"

    def login(self, credentials):
        """
        Realiza el proceso completo de login en el sistema SAC.

        Ejecuta la secuencia de autenticacion incluyendo navegacion,
        seleccion de dominio, ingreso de credenciales y confirmacion.

        Parameters
        ----------
        credentials : dict
            Diccionario con claves 'user' y 'password' para autenticacion.

        Returns
        -------
        bool
            True si el login fue exitoso.

        Raises
        ------
        ValueError
            Si las credenciales no estan completas.
        Exception
            Si ocurre un error durante el proceso de login.
        """
        logging.info("Iniciando proceso de login en SAC...")
        user = credentials.get("user")
        password = credentials.get("password")

        if not user or not password:
            raise ValueError("Usuario o contraseña no proporcionados.")

        try:
            # Navegar a la página de login
            self.driver.get(self.config.get("sac_url"))
            wait_time = self.adaptive_wait.predict_optimal_wait(3.0)
            time.sleep(wait_time)
            self.adaptive_wait.record_attempt(wait_time, True)

            # Seleccionar dominio
            if not self.safe_click(self.DOMAIN_SELECT):
                raise Exception("No se pudo seleccionar el dominio")
            wait_time = self.adaptive_wait.predict_optimal_wait(2.0)
            time.sleep(wait_time)
            self.adaptive_wait.record_attempt(wait_time, True)

            # Ingresar usuario
            if not self.safe_send_keys(self.USERNAME_INPUT, user):
                raise Exception("No se pudo ingresar el usuario")
            wait_time = self.adaptive_wait.predict_optimal_wait(2.0)
            time.sleep(wait_time)
            self.adaptive_wait.record_attempt(wait_time, True)

            # Ingresar contraseña
            if not self.safe_send_keys(self.PASSWORD_INPUT, password):
                raise Exception("No se pudo ingresar la contraseña")
            wait_time = self.adaptive_wait.predict_optimal_wait(2.0)
            time.sleep(wait_time)
            self.adaptive_wait.record_attempt(wait_time, True)

            # Hacer clic en login
            if not self.safe_click(self.LOGIN_BUTTON):
                raise Exception("No se pudo hacer clic en el botón de login")
            wait_time = self.adaptive_wait.predict_optimal_wait(3.0)
            time.sleep(wait_time)
            self.adaptive_wait.record_attempt(wait_time, True)

            logging.info("Login en SAC completado exitosamente.")
            return True

        except Exception as e:
            logging.error(f"Error durante el login: {e}")
            raise


class ProcessSearchPage(BasePage):
    """
    Page Object para la página de busqueda de procesos en SAC.

    Maneja la navegacion a administracion y busqueda de procesos
    especificos por numero de proceso.

    Examples
    --------
    >>> page = ProcessSearchPage(driver, config)
    >>> page.navigate_to_admin()
    >>> page.search_process("13280955")
    """

    # Selectores XPath para búsqueda de procesos
    FILTER_BUTTON = (
        "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_btnFiltrarProcesos']/span"
    )
    PROCESS_FILTER_INPUT = (
        "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_txtFiltroNumeroProceso']"
    )
    SEARCH_BUTTON = (
        "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_btnBuscarFiltrosProcesos']"
    )
    ATTACHMENTS_BUTTON = (
        "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_btnAnexos']/span"
    )

    def navigate_to_admin(self):
        """
        Navega a la pagina de administracion de procesos en SAC.

        Carga la URL de administracion configurada y espera
        a que la pagina este lista usando espera adaptativa.

        Returns
        -------
        None
        """
        logging.info("Navegando a pagina de administracion...")
        self.driver.get(self.config.get("sac_admin_url"))
        wait_time = self.adaptive_wait.predict_optimal_wait(5.0)
        time.sleep(wait_time)
        self.adaptive_wait.record_attempt(wait_time, True)

    def search_process(self, process_number):
        """
        Busca un proceso especifico por numero de proceso.

        Abre el filtro de busqueda, ingresa el numero de proceso
        y espera a que el boton de anexos este disponible.

        Parameters
        ----------
        process_number : str
            Numero unico del proceso SAC a buscar.

        Returns
        -------
        bool
            True si el proceso fue encontrado y cargado correctamente.

        Raises
        ------
        Exception
            Si no se puede abrir el filtro, buscar o encontrar resultados.
        """
        logging.info(f"Buscando proceso SAC: {process_number}")

        try:
            # Abrir filtros
            if not self.safe_click(self.FILTER_BUTTON):
                raise Exception("No se pudo abrir el filtro de procesos")

            # Ingresar número de proceso
            if not self.safe_send_keys(self.PROCESS_FILTER_INPUT, process_number):
                raise Exception("No se pudo ingresar el número de proceso")

            # Ejecutar búsqueda
            if not self.safe_click(self.SEARCH_BUTTON):
                raise Exception("No se pudo ejecutar la búsqueda")

            # Esperar resultados
            if not self.wait_for_element(self.ATTACHMENTS_BUTTON):
                raise Exception("No se encontraron resultados para el proceso")

            logging.info(f"Proceso {process_number} encontrado exitosamente.")
            return True

        except Exception as e:
            logging.error(f"Error buscando proceso {process_number}: {e}")
            raise


class AttachmentPage(BasePage):
    """
    Page Object para la gestion de anexos en SAC.

    Maneja la carga, configuracion y guardado de archivos adjuntos
    en los procesos del sistema de administracion de contratos.

    Examples
    --------
    >>> page = AttachmentPage(driver, config)
    >>> page.open_attachments_section()
    >>> page.fill_attachment_form({"asunto": "Reclamo"})
    """

    # Selectores XPath para gestión de anexos
    ATTACHMENTS_BUTTON = (
        "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_btnAnexos']/span"
    )
    INSERT_ATTACHMENT_BUTTON = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_lbtInsertarAnexo']"
    TITLE_INPUT = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_txtTituloIng']"
    DESCRIPTION_INPUT = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_txtDescripcionIng']"
    DOCUMENT_GROUP_INPUT = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_txtGrupoDocumentoIng']"
    DOCUMENT_TYPE_INPUT = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_txtTipoDocumentoIng']"
    FILE_INPUT = (
        "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_inpArchivo']"
    )
    UPLOAD_BUTTON = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_udpCargueArchivo']/div/div/div/div[4]/div/div/a/span"
    SAVE_BUTTON = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_lbtGuardarAnexo']/i"
    CLOSE_MODAL_BUTTON = "//*[@id='btnCerrarModal1']"
    CLOSE_ATTACHMENTS_BUTTON = "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_ucGenAnexosCtrl_lbtCerrarAnexosCon']/span"

    def open_attachments_section(self):
        """
        Abre la seccion de anexos del proceso actual.

        Hace clic en el boton de anexos del proceso y espera
        a que cargue la seccion correspondiente.

        Returns
        -------
        None

        Raises
        ------
        Exception
            Si no se puede abrir la seccion de anexos.
        """
        logging.info("Abriendo seccion de anexos...")
        if not self.safe_click(self.ATTACHMENTS_BUTTON):
            raise Exception("No se pudo abrir la seccion de anexos")

    def insert_new_attachment(self):
        """
        Inicia el proceso de inserciÃ³n de un nuevo anexo.

        Hace clic en el boton para insertar un nuevo anexo
        dentro de la seccion de anexos abierta.

        Returns
        -------
        None

        Raises
        ------
        Exception
            Si no se puede iniciar la inserciÃ³n del anexo.
        """
        logging.info("Insertando nuevo anexo...")
        if not self.safe_click(self.INSERT_ATTACHMENT_BUTTON):
            raise Exception("No se pudo iniciar inserciÃ³n de anexo")

    def fill_attachment_form(self, data):
        """
        Completa el formulario de carga de anexo.

        Llena los campos de titulo, descripcion, grupo de documento
        y tipo de documento con los valores correspondientes.

        Parameters
        ----------
        data : dict
            Datos del anexo conteniendo 'asunto' u otras claves relevantes.

        Returns
        -------
        None

        Raises
        ------
        Exception
            Si no se puede completar alguno de los campos del formulario.
        """
        logging.info("Completando formulario de anexo...")

        title = str(data.get("asunto", "Anexo"))
        description = str(data.get("asunto", "Anexo"))

        # Llenar campos del formulario
        if not self.safe_send_keys(self.TITLE_INPUT, title):
            raise Exception("No se pudo ingresar el título")
        if not self.safe_send_keys(self.DESCRIPTION_INPUT, description):
            raise Exception("No se pudo ingresar la descripción")
        if not self.safe_send_keys(self.DOCUMENT_GROUP_INPUT, "17"):
            raise Exception("No se pudo ingresar el grupo de documento")
        # Esperar a que el segundo overlay de carga desaparezca
        self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))

        self.safe_click(self.DOCUMENT_TYPE_INPUT)
        time.sleep(2)  # Pausa para que el formulario procese
        if not self.safe_send_keys(self.DOCUMENT_TYPE_INPUT, "234"):
            raise Exception("No se pudo ingresar el tipo de documento")

    def upload_file(self, file_path):
        """
        Selecciona y carga el archivo anexo en el formulario.

        Ubica el input de archivo, lo hace visible si es necesario,
        envia la ruta del archivo y ejecuta la carga.

        Parameters
        ----------
        file_path : str
            Ruta completa del archivo a cargar.

        Returns
        -------
        None

        Raises
        ------
        Exception
            Si no se puede cargar el archivo en el formulario.
        """
        logging.info(f"Cargando archivo: {file_path}")

        try:
            file_input = self.driver.find_element(By.XPATH, self.FILE_INPUT)
            file_input.send_keys(file_path)

            # Ejecutar carga
            if not self.safe_click(self.UPLOAD_BUTTON):
                raise Exception("No se pudo ejecutar la carga del archivo")

        except Exception as e:
            logging.error(f"Error cargando archivo {file_path}: {e}")
            raise

    def save_attachment(self):
        """
        Guarda el anexo y cierra los modales de confirmacion.

        Ejecuta el guardado del anexo, espera el procesamiento,
        cierra el modal de confirmacion y cierra la seccion de anexos.

        Returns
        -------
        None
        """
        logging.info("Guardando anexo...")

        # Guardar anexo
        if not self.safe_click(self.SAVE_BUTTON):
            raise Exception("No se pudo guardar el anexo")

        # Cerrar modales
        wait_time = self.adaptive_wait.predict_optimal_wait(2.0)
        time.sleep(wait_time)  # Esperar procesamiento
        self.adaptive_wait.record_attempt(wait_time, True)
        self.safe_click(self.CLOSE_MODAL_BUTTON)
        self.safe_click(self.CLOSE_ATTACHMENTS_BUTTON)

        logging.info("Anexo guardado exitosamente.")

    def find_attachment_file(self, data):
        """
        Busca el archivo anexo basado en los datos de la tarea.

        Busca el archivo en los directorios configurados (Mercurio y correos)
        usando el numero de PQR o numero de proceso SAC.

        Parameters
        ----------
        data : dict
            Datos de la tarea con claves 'no_pqr' y/o 'proceso_sac'.

        Returns
        -------
        str or None
            Ruta completa del archivo encontrado, o None si no existe.
        """
        no_pqr = str(data.get("no_pqr", "")).strip()
        proceso_sac = str(data.get("proceso_sac", "")).strip()

        search_keys = [key for key in [no_pqr, proceso_sac] if key]
        if not search_keys:
            logging.warning(
                "La tarea no tiene 'no_pqr' ni 'proceso_sac' para buscar el archivo."
            )
            return None

        base_paths = [
            self.config.get("anexos_mercurio_path"),
            self.config.get("anexos_correo_path"),
        ]
        extensions = [".pdf", ".msg", ".eml"]

        for key in search_keys:
            for base_path in base_paths:
                if not base_path:
                    continue
                for ext in extensions:
                    file_path = os.path.join(base_path, key + ext)
                    if os.path.exists(file_path):
                        logging.info(f"Archivo anexo encontrado en: {file_path}")
                        return file_path

        logging.warning(
            f"No se pudo encontrar el archivo anexo para las claves: {search_keys}"
        )
        return None


class WebAutomator:
    """
    Clase principal del automatizador web implementando POM.

    Coordina las diferentes paginas (LoginPage, ProcessSearchPage,
    AttachmentPage) y proporciona una interfaz unificada para la
    automatizacion del sistema SAC.

    Examples
    --------
    >>> automator = WebAutomator(config)
    >>> automator.login(credentials)
    >>> automator.completar_formulario(datos)
    """

    def __init__(self, config):
        """
        Inicializa el automatizador web con configuracion POM.

        Crea el driver de Chrome, instancia los Page Objects
        y configura la espera adaptativa.

        Parameters
        ----------
        config : dict
            Configuracion necesaria para la automatizacion,
            incluyendo URLs y credenciales.
        """
        self.config = config
        self.driver = WebUtils.create_chrome_driver()
        self.wait = WebDriverWait(self.driver, 20)

        # Inicializar Page Objects
        self.login_page = LoginPage(self.driver, config)
        self.process_search_page = ProcessSearchPage(self.driver, config)
        self.attachment_page = AttachmentPage(self.driver, config)
        self.adaptive_wait = AdaptiveWaitStrategy()

        logging.info("Automatizador web inicializado con patrón POM.")

    def init_session(self):
        """
        Inicializa y abre la sesion del navegador.

        Prepara el entorno para iniciar la interaccion
        con el sistema SAC.

        Returns
        -------
        None
        """
        logging.info("Sesion del navegador inicializada.")

    def close_session(self):
        """
        Cierra la sesion del navegador de forma segura.

        Finaliza el WebDriver y libera los recursos
        del navegador.

        Returns
        -------
        None
        """
        if self.driver:
            self.driver.quit()
            logging.info("Sesion del navegador cerrada correctamente.")

    def login(self, credentials):
        """
        Realiza el proceso de login usando LoginPage.

        Delega al Page Object LoginPage para ejecutar el proceso
        de autenticacion completo.

        Parameters
        ----------
        credentials : dict
            Diccionario con claves 'user' y 'password'.

        Returns
        -------
        bool
            True si el login fue exitoso.
        """
        return self.login_page.login(credentials)

    def completar_formulario(self, datos):
        """
        Completa el formulario de carga de anexo usando Page Objects.

        Coordina la navegacion a admin, busqueda del proceso,
        apertura de anexos y carga del archivo.

        Parameters
        ----------
        datos : dict
            Datos necesarios para completar el formulario,
            incluyendo 'proceso_sac' y datos del anexo.

        Returns
        -------
        None

        Raises
        ------
        FileNotFoundError
            Si no se encuentra el archivo anexo.
        Exception
            Si ocurre un error durante el proceso de carga.
        """
        logging.info("Completando formulario de carga de anexo...")

        try:
            # Navegar a administración y buscar proceso
            self.process_search_page.navigate_to_admin()
            num_proceso = datos.get("proceso_sac")
            self.process_search_page.search_process(num_proceso)

            # Gestionar anexo
            self.attachment_page.open_attachments_section()
            self.attachment_page.insert_new_attachment()
            self.attachment_page.fill_attachment_form(datos)

            # Buscar y cargar archivo
            file_path = self.attachment_page.find_attachment_file(datos)
            if not file_path:
                raise FileNotFoundError(
                    f"No se encontró el archivo anexo para la tarea: {datos}"
                )

            self.attachment_page.upload_file(file_path)
            self.attachment_page.save_attachment()

            logging.info("Formulario completado exitosamente.")

        except Exception as e:
            logging.error(f"Error completando formulario: {e}")
            raise

    # Métodos legacy para compatibilidad - DEPRECATED
    # Estos métodos se mantienen por compatibilidad pero delegan a los Page Objects

    def _click(self, xpath):
        """
        Metodo legacy para compatibilidad hacia atras.

        Delega a WebUtils.safe_click para mantener compatibilidad
        con codigo existente.

        Parameters
        ----------
        xpath : str
            Selector XPath del elemento.

        Returns
        -------
        bool
            Resultado del clic.
        """
        logging.warning("_click method is deprecated. Use Page Objects instead.")
        return WebUtils.safe_click(self.driver, xpath)

    def _send_keys(self, xpath, text):
        """
        Metodo legacy para compatibilidad hacia atras.

        Delega a WebUtils.safe_send_keys para mantener compatibilidad
        con codigo existente.

        Parameters
        ----------
        xpath : str
            Selector XPath del elemento.
        text : str
            Texto a enviar.

        Returns
        -------
        bool
            Resultado del envio de texto.
        """
        logging.warning("_send_keys method is deprecated. Use Page Objects instead.")
        return WebUtils.safe_send_keys(self.driver, xpath, text)
