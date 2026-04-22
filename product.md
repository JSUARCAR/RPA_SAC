# Documento de Producto: SAC Automation

## 1. Propósito del Producto

**SAC Automation** es una solución de Robotic Process Automation (RPA) diseñada para **automatizar integralmente el proceso de carga de anexos** en el Sistema de Administración de Contratos (SAC) de EPM.

El propósito fundamental es transformar una tarea manual, repetitiva y propensa a errores en un flujo de trabajo automatizado, eficiente y auditable. El sistema actúa como un "asistente digital" que lee una cola de trabajo desde un archivo Excel, interactúa con la interfaz web de SAC y ejecuta la carga de documentos sin intervención humana.

## 2. Objetivos y Experiencia de Usuario (UX)

El usuario principal de esta herramienta es un analista o gestor de PQR que actualmente realiza este proceso manualmente. La experiencia de usuario debe centrarse en:

- **Trazabilidad y Auditabilidad:** El usuario debe tener visibilidad completa sobre las acciones del robot. El sistema debe generar un registro claro de cada operación, tanto en el archivo Excel de control (marcando el estado de cada fila) como en un archivo de log (`sac_automation.log`) para diagnóstico de errores.
- **Eficiencia y Ahorro de Tiempo:** El objetivo principal es liberar al usuario de horas de trabajo manual, permitiéndole centrarse en tareas de mayor valor. El robot debe procesar la carga de anexos de forma masiva y a una velocidad superior a la de un humano.
- **Confiabilidad y Manejo de Errores:** El sistema debe ser robusto. Si un anexo no se encuentra o si ocurre un error durante la carga, el robot debe registrar el fallo claramente en el Excel y continuar con el siguiente ítem, en lugar de detenerse por completo.
- **Mínima Configuración:** La ejecución debe ser simple, idealmente con un solo clic (a través de `run_sac_automation.bat`), sin requerir conocimientos técnicos avanzados por parte del usuario final.

## 3. Funcionalidades Clave (Features)

- **Procesamiento por Lotes desde Excel:** Lee y procesa múltiples registros desde una hoja de cálculo (`CONTROL_DIARIO_PQR`).
- **Autenticación Segura:** Inicia sesión en el sistema SAC utilizando credenciales almacenadas en el mismo archivo Excel.
- **Navegación y Búsqueda Automatizada:** Navega a la sección correcta de SAC, busca procesos específicos por su número de identificación.
- **Carga Dinámica de Anexos:** Localiza los archivos (PDF, MSG, etc.) en rutas de red predefinidas y los adjunta al proceso correspondiente en SAC.
- **Actualización de Estado en Tiempo Real:** Modifica el archivo Excel para reflejar el resultado de cada operación (éxito o fallo) y añade una marca de tiempo.
- **Logging Detallado:** Genera un archivo de log (`sac_automation.log`) con el detalle técnico de la ejecución para facilitar el debugging.
- **Gestión Automática de Entorno:** El script de inicio (`run_sac_automation.bat`) gestiona la creación del entorno virtual y la instalación de dependencias.