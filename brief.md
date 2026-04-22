# Brief del Proyecto: SAC Automation

**SAC Automation** es un robot de software (RPA) desarrollado en Python que automatiza la carga masiva de anexos en el **Sistema de Administración de Contratos (SAC)** de EPM.

El sistema lee un archivo Excel que actúa como cola de trabajo, extrae los datos de los procesos a intervenir, y utiliza Selenium para controlar un navegador web, iniciar sesión en SAC, buscar cada proceso y adjuntar los archivos correspondientes.

El objetivo principal es **eliminar la carga manual de trabajo**, reducir errores humanos y acelerar el tiempo de respuesta en la gestión de PQR (Peticiones, Quejas y Reclamos), mejorando la eficiencia operativa y la trazabilidad de los anexos.