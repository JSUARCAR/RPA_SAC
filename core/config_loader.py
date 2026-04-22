"""
Modulo responsable de cargar y proveer toda la configuracion necesaria.

Abstrae el origen de la configuracion, actualmente desde un archivo Excel
usando la hoja 'PARAMETROS_LOCALES'.

Classes
-------
ConfigLoader
    Carga y gestiona la configuracion desde el archivo Excel.

Functions
---------
Ninguna publicas.

Examples
--------
>>> from core.config_loader import ConfigLoader
>>> loader = ConfigLoader("Control_PQR.xlsx")
>>> url = loader.get("sac_url")
"""

from openpyxl import load_workbook
import os


class ConfigLoader:
    """
    Carga y gestiona la configuracion desde la hoja PARAMETROS_LOCALES.

    Proporciona acceso centralizado a la configuracion de la aplicacion
    incluyendo URLs del sistema SAC, rutas de archivos y credenciales.

    Attributes
    ----------
    _config : dict
        Diccionario interno con la configuracion cargada.

    Examples
    --------
    >>> loader = ConfigLoader("Control_PQR.xlsx")
    >>> url = loader.get("sac_url")
    >>> print(url)
    https://sac.corp.epm.com.co/GEN/Vistas/Login/LOGIN_GEN.aspx
    """

    def __init__(self, excel_path: str):
        """
        Inicializa el cargador de configuración.

        Parameters
        ----------
        excel_path : str
            Ruta al archivo Excel de control.

        Raises
        ------
        ValueError
            Si el archivo Excel no existe o no tiene la hoja requerida.
        """
        self._config = self._load_config_from_excel(excel_path)

    def _load_config_from_excel(self, excel_path: str) -> dict:
        """
        Carga la configuración desde la hoja 'PARAMETROS_LOCALES'.

        Parameters
        ----------
        excel_path : str
            Ruta al archivo Excel.

        Returns
        -------
        dict
            Diccionario con la configuración cargada.

        Raises
        ------
        ValueError
            Si el archivo no existe o la hoja no se encuentra.

        Notes
        -----
        Las celdas esperadas en PARAMETROS_LOCALES son:
        - K2: anexos_correo_path
        - K3: anexos_mercurio_path
        - M2: user
        - N2: password
        """
        try:
            workbook = load_workbook(excel_path, data_only=True)
            sheet = workbook["PARAMETROS_LOCALES"]

            config = {
                "anexos_mercurio_path": sheet["K3"].value,
                "anexos_correo_path": sheet["K2"].value,
                "sac_url": "https://sac.corp.epm.com.co/GEN/Vistas/Login/LOGIN_GEN.aspx",
                "sac_admin_url": "https://sac.corp.epm.com.co/SAC/Vistas/App/PRO_ADMPRO.aspx",
                "user": sheet["M2"].value,
                "password": sheet["N2"].value,
            }
            return config
        except FileNotFoundError:
            raise ValueError(
                f"El archivo de configuración Excel no se encontró en: {excel_path}"
            )
        except KeyError:
            raise ValueError(
                "La hoja 'PARAMETROS_LOCALES' no se encontró en el archivo Excel."
            )
        except Exception as e:
            raise ValueError(f"Error cargando la configuración desde Excel: {e}")

    def get(self, key: str):
        """
        Obtiene un valor de configuración por su clave.

        Parameters
        ----------
        key : str
            La clave del valor de configuración.

        Returns
        -------
        any
            El valor de configuración o None si la clave no existe.
        """
        return self._config.get(key)

    @property
    def all_configs(self) -> dict:
        """
        Retorna todo el diccionario de configuración.

        Returns
        -------
        dict
            Copia del diccionario de configuración completo.
        """
        return self._config.copy()
