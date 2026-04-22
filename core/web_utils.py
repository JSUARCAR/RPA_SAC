"""
Modulo de utilidades comunes para automatizacion web con Selenium.

Contiene logica reutilizable para manejo de excepciones,
configuracion de navegador y operaciones comunes.

Classes
-------
WebUtils
    Utilidades comunes para operaciones web con Selenium.

Examples
--------
>>> from core.web_utils import WebUtils
>>> driver = WebUtils.create_chrome_driver()
>>> WebUtils.safe_click(driver, "//button[@id='submit']")
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
    ElementClickInterceptedException,
)
from webdriver_manager.chrome import ChromeDriverManager


class WebUtils:
    """
    Utilidades comunes para operaciones web con Selenium.

    Proporciona metodos estaticos para interaccion segura con elementos
    web, incluyendo reintentos automaticos y manejo de excepciones.
    """

    @staticmethod
    def create_chrome_options():
        """
        Crea y configura opciones de Chrome para automatizacion.

        Returns
        -------
        ChromeOptions
            Opciones configuradas para el navegador Chrome.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--disable-web-security")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--disable-javascript")
        options.add_argument("--headless")
        return options

    @staticmethod
    def create_chrome_driver(options=None):
        """
        Crea una instancia de Chrome WebDriver con configuracion automatica.

        Parameters
        ----------
        options : ChromeOptions, optional
            Opciones de Chrome. Si es None, usa las predeterminadas.

        Returns
        -------
        WebDriver
            Instancia del driver de Chrome.
        """
        if options is None:
            options = WebUtils.create_chrome_options()

        try:
            service = webdriver.chrome.service.Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception as e:
            logging.error(f"Error al crear Chrome driver: {e}")
            raise

    @staticmethod
    def safe_click(driver, xpath, timeout=10, max_retries=3):
        """
        Realiza un clic seguro con manejo de excepciones y reintentos.

        Parameters
        ----------
        driver : WebDriver
            Instancia del WebDriver.
        xpath : str
            Selector XPath del elemento.
        timeout : int, optional
            Tiempo de espera en segundos. Default: 10.
        max_retries : int, optional
            Numero maximo de reintentos. Default: 3.

        Returns
        -------
        bool
            True si el clic fue exitoso, False en caso contrario.
        """
        wait = WebDriverWait(driver, timeout)

        for attempt in range(max_retries):
            try:
                element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                element.click()
                return True
            except StaleElementReferenceException:
                logging.debug(
                    f"Elemento obsoleto en intento {attempt + 1} para {xpath}, reintentando..."
                )
                time.sleep(0.5)
            except ElementClickInterceptedException:
                logging.debug(
                    f"Elemento interceptado en intento {attempt + 1} para {xpath}, esperando overlay..."
                )
                WebUtils.wait_for_overlay_to_disappear(driver)
                time.sleep(0.5)
            except TimeoutException:
                logging.warning(f"Timeout esperando elemento clickable: {xpath}")
                return False
            except Exception as e:
                logging.error(f"Error inesperado en clic: {e}")
                return False

        logging.error(f"Falló clic despues de {max_retries} intentos: {xpath}")
        return False

    @staticmethod
    def safe_send_keys(driver, xpath, text, timeout=10, max_retries=3):
        """
        Envia texto de forma segura con manejo de excepciones y reintentos.

        Parameters
        ----------
        driver : WebDriver
            Instancia del WebDriver.
        xpath : str
            Selector XPath del elemento.
        text : str
            Texto a enviar.
        timeout : int, optional
            Tiempo de espera en segundos. Default: 10.
        max_retries : int, optional
            Numero maximo de reintentos. Default: 3.

        Returns
        -------
        bool
            True si el envio fue exitoso, False en caso contrario.
        """
        wait = WebDriverWait(driver, timeout)

        for attempt in range(max_retries):
            try:
                element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                element.clear()
                element.send_keys(text)
                return True
            except StaleElementReferenceException:
                logging.debug(
                    f"Elemento obsoleto en intento {attempt + 1} para {xpath}, reintentando..."
                )
                time.sleep(0.5)
            except Exception as e:
                logging.error(f"Error enviando texto en intento {attempt + 1}: {e}")
                time.sleep(0.5)

        logging.error(
            f"Fallo envio de texto despues de {max_retries} intentos: {xpath}"
        )
        return False

    @staticmethod
    def wait_for_overlay_to_disappear(driver, timeout=10):
        """
        Espera a que los overlays o elementos de carga desaparezcan.

        Parameters
        ----------
        driver : WebDriver
            Instancia del WebDriver.
        timeout : int, optional
            Tiempo maximo de espera en segundos. Default: 10.
        """
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: len(
                    d.find_elements(
                        By.XPATH,
                        "//div[contains(@class, 'loading') or contains(@class, 'overlay')]",
                    )
                )
                == 0
            )
        except TimeoutException:
            logging.warning("Timeout esperando desaparecion de overlay")

    @staticmethod
    def wait_for_element(driver, xpath, timeout=10):
        """
        Espera a que un elemento este presente y visible.

        Parameters
        ----------
        driver : WebDriver
            Instancia del WebDriver.
        xpath : str
            Selector XPath del elemento.
        timeout : int, optional
            Tiempo de espera en segundos. Default: 10.

        Returns
        -------
        WebElement or None
            El elemento WebElement si se encuentra, None si timeout.
        """
        try:
            wait = WebDriverWait(driver, timeout)
            return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            logging.warning(f"Timeout esperando elemento: {xpath}")
            return None
