# Arquitectura del Sistema: SAC Automation

## Componentes Clave

- **main.py (Orquestador Principal)**: Punto de entrada de la aplicación. Coordina la inicialización de componentes, maneja la configuración general y orquesta el flujo de ejecución principal con inyección de dependencias.
- **core/data_handler.py (Capa de Acceso a Datos)**: Abstrae toda la interacción con archivos Excel. Responsable de leer la cola de trabajo, obtener credenciales y actualizar el estado de procesos. Implementa separación de responsabilidades al aislar la lógica de I/O de datos.
- **core/web_automator.py (Capa de Automatización Web)**: Encapsula la lógica completa de Selenium para interactuar con el sistema SAC, incluyendo navegación, login, búsqueda de procesos y carga de anexos. Diseñado para implementar el patrón Page Object Model (POM).
- **core/config_loader.py (Gestor de Configuración)**: Centraliza la carga de configuración desde múltiples fuentes (Excel, archivos INI, variables de entorno), proporcionando una interfaz unificada para acceder a rutas, URLs y credenciales.
- **core/logger_setup.py (Configuración de Logging)**: Establece el sistema de logging seguro con sanitización de datos sensibles, asegurando trazabilidad completa sin comprometer información confidencial.

## Patrón de Diseño: Page Object Model (POM)

### Descripción del Patrón
El Page Object Model es un patrón de diseño esencial para la automatización web que promueve la separación de responsabilidades y mejora la mantenibilidad del código. En el contexto de SAC Automation, este patrón estructura la interacción con el sistema SAC de manera más robusta y escalable.

### Estructura Propuesta para Clases Page Object
- **LoginPage**: Gestiona la autenticación en el sistema SAC, encapsulando métodos para selección de dominio, ingreso de credenciales y validación de login exitoso.
- **ProcessSearchPage**: Maneja la búsqueda y filtrado de procesos, incluyendo la navegación a la página de administración y la interacción con campos de búsqueda.
- **AttachmentPage**: Controla la carga de anexos, desde la apertura del modal hasta la selección y subida de archivos, con validación de estados de carga.

### Beneficios del Patrón POM
- **Reutilización de Código**: Los métodos de página pueden ser reutilizados en múltiples escenarios de automatización.
- **Facilidad de Mantenimiento**: Cambios en la UI del sistema SAC solo requieren actualizaciones en las clases Page Object correspondientes.
- **Reducción de Duplicación**: Elimina código repetitivo para interacciones comunes con elementos web.
- **Mejor Testabilidad**: Permite pruebas unitarias de componentes individuales sin ejecutar el flujo completo.

### Implementación - Enero 2026
El patrón Page Object Model ha sido implementado para estructurar la interacción con SAC. Aunque actualmente reside en `web_automator.py`, la lógica está separada por áreas de responsabilidad (LoginPage, ProcessSearchPage, AttachmentPage).

## Arquitectura de Distribución (Ejecutable)

Para facilitar el uso por analistas, el sistema se compila usando **PyInstaller** en un ejecutable único (`SAC_Automation.exe`).

### Gestión Dinámica de Rutas
Se implementó una lógica de detección de entorno en `main.py` para asegurar que el sistema encuentre sus archivos de soporte (`config.ini`) y genere logs en el lugar correcto, ya sea ejecutándose como script o como binario congelado:

```python
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
```

## Flujo de Datos

1. **Inicialización**: main.py carga configuración via config_loader.py y establece logging seguro.
2. **Lectura de Datos**: data_handler.py lee tareas pendientes desde Excel, filtrando por fecha, medio y estado.
3. **Procesamiento Iterativo**:
   - main.py itera sobre tareas, pasando datos a web_automator.py.
   - web_automator.py ejecuta login (si necesario), búsqueda de proceso y carga de anexo.
   - Resultados se devuelven a main.py para actualización de estado.
4. **Actualización de Estado**: data_handler.py marca tareas como completadas o con error en Excel.
5. **Limpieza**: web_automator.py cierra sesión y navegador; main.py libera recursos.

## Estrategia de Excepciones

- **TimeoutException**: Manejada con reintentos automáticos en operaciones web, con backoff exponencial.
- **StaleElementReferenceException**: Implementada lógica de reintento en _send_keys para manejar DOM dinámico.
- **ElementNotInteractableException**: Verificaciones de visibilidad y clickeabilidad antes de interacciones.
- **ElementClickInterceptedException**: Detección y manejo de overlays/modales que bloquean clics.
- **FileNotFoundError**: Validación previa de existencia de archivos anexo antes de carga.
- **ValueError**: Validación de configuración y datos de entrada en puntos de entrada.

## Decisiones Técnicas Críticas

### Uso de Selenium para Automatización Web
**Justificación**: Selenium proporciona una API madura y ampliamente soportada para automatización de navegadores, con capacidades avanzadas para manejo de JavaScript, waits explícitos y compatibilidad cross-browser. Las ventajas incluyen soporte nativo para interacciones complejas con aplicaciones web modernas, comunidad activa y ecosistema rico de herramientas complementarias, y capacidad para ejecutar en modo headless para entornos de CI/CD.

**Consideraciones de Mantenimiento**: Los selectores XPath pueden volverse frágiles con cambios en la UI; se mitiga con estrategias de localización robusta y el patrón POM planificado.

### Arquitectura Modular con Separación de Responsabilidades
**Justificación**: La estructura monolítica original violaba el principio de responsabilidad única, haciendo el código difícil de mantener y probar. La separación en módulos especializados permite desarrollo paralelo por diferentes equipos, pruebas unitarias independientes de cada componente, y reutilización de módulos en otros proyectos de automatización.

### Configuración Centralizada y Segura
**Justificación**: Centralizar la configuración en config_loader.py permite gestión unificada de entornos (desarrollo, staging, producción) y facilita la integración con sistemas de secrets management. La sanitización de logs previene exposición accidental de credenciales.

### Manejo Robusto de Excepciones con Reintento
**Justificación**: Las aplicaciones web son inherentemente inestables debido a latencias de red, actualizaciones dinámicas del DOM y cambios en el backend. La estrategia de reintento con backoff exponencial asegura resiliencia sin sobrecargar los sistemas objetivo, mientras que el logging detallado facilita la depuración de fallos intermitentes.