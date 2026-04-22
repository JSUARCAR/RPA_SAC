"""
Estrategia de espera adaptativa con aprendizaje automático simple.

Este módulo implementa un sistema de espera que aprende de los tiempos de
carga históricos para optimizar los delays futuros, mejorando el rendimiento
de las operaciones de automatización web.
"""

from typing import List
import statistics


class AdaptiveWaitStrategy:
    """
    Estrategia de espera adaptativa con machine learning simple.

    Esta clase implementa un sistema de espera que aprende de los
    tiempos de carga históricos para optimizar los delays futuros.

    Parameters
    ----------
    Ninguno

    Attributes
    ----------
    wait_times : List[float]
        Historial de tiempos de espera registrados.
    success_rates : List[bool]
        Historial de éxito de operaciones asociadas a cada wait_time.
    learning_rate : float
        Tasa de aprendizaje para el ajuste de waits. Default: 0.1

    Examples
    --------
    >>> strategy = AdaptiveWaitStrategy()
    >>> strategy.record_attempt(2.5, success=True)
    >>> wait_time = strategy.predict_optimal_wait(base_wait=2.0)
    >>> print(f"Wait óptimo: {wait_time}")
    Wait óptimo: 2.05
    """

    def __init__(self):
        """
        Inicializa la estrategia de espera adaptativa.

        Inicializa los histogramas vacíos y establece la tasa de
        aprendizaje predeterminada a 0.1.
        """
        self.wait_times: List[float] = []
        self.success_rates: List[bool] = []
        self.learning_rate = 0.1

    def record_attempt(self, wait_time: float, success: bool) -> None:
        """
        Registra un intento para aprender del historial.

        Parameters
        ----------
        wait_time : float
            Tiempo de espera utilizado en segundos.
        success : bool
            True si la operación fue exitosa, False otherwise.

        Returns
        -------
        None

        Notes
        -----
        Mantiene solo las últimas 20 observaciones para evitar
        que el historial crezca indefinidamente.
        """
        self.wait_times.append(wait_time)
        self.success_rates.append(success)

        if len(self.wait_times) > 20:
            self.wait_times.pop(0)
            self.success_rates.pop(0)

    def predict_optimal_wait(self, base_wait: float = 2.0) -> float:
        """
        Predice el tiempo de espera óptimo basado en historial.

        Utiliza un algoritmo simple de media móvil ponderada para
        calcular el tiempo óptimo de espera.

        Parameters
        ----------
        base_wait : float, optional
            Tiempo de espera base en segundos. Default: 2.0

        Returns
        -------
        float
            Tiempo de espera óptimo predicho en segundos.

        Notes
        -----
        Si no hay datos históricos, retorna el base_wait.
        Si no hay exitos recientes, incrementa el base_wait en 50%.
        """
        if not self.wait_times:
            return base_wait

        successful_times = [t for t, s in zip(self.wait_times, self.success_rates) if s]

        if successful_times:
            optimal = statistics.mean(successful_times)
            return base_wait + self.learning_rate * (optimal - base_wait)

        return base_wait * 1.5
