# Documento de Producto: SAC Automation

## Propósito del Producto

**SAC Automation** es una solución de Robotic Process Automation (RPA) diseñada para **automatizar integralmente el proceso de carga de anexos** en el Sistema de Administración de Contratos (SAC) de EPM.

El propósito fundamental es transformar una tarea manual, repetitiva y propensa a errores en un flujo de trabajo automatizado, eficiente y auditable. El sistema actúa como un "asistente digital" que lee una cola de trabajo desde un archivo Excel, interactúa con la interfaz web de SAC y ejecuta la carga de documentos sin intervención humana.

## Problemas que Resuelve

- **Ineficiencia Operativa**: Eliminación de horas de trabajo manual en carga de anexos
- **Errores Humanos**: Reducción significativa de errores en la asignación de documentos
- **Trazabilidad**: Registro automático y auditable de todas las operaciones
- **Velocidad de Respuesta**: Procesamiento masivo más rápido que intervención manual

## Experiencia de Usuario (UX)

El usuario principal es un analista o gestor de PQR que actualmente realiza este proceso manualmente. La experiencia se centra en:

- **Simplicidad**: Ejecución con un solo clic mediante `run_sac_automation.bat` o a través del ejecutable profesional `SAC_Automation.exe`.
- **Identidad**: Aplicación con ícono personalizado y ejecución silenciosa (sin consola) para una experiencia premium.
- **Trazabilidad Completa**: Visibilidad en Excel y logs de todas las operaciones
- **Confiabilidad**: Continuación del proceso ante errores individuales
- **Transparencia**: Logging detallado para diagnóstico y auditoría

## Funcionalidades Clave

- **Procesamiento por Lotes desde Excel**: Lectura automática de cola de trabajo
- **Autenticación Segura**: Login automático en SAC con credenciales protegidas
- **Navegación Automatizada**: Búsqueda precisa de procesos por número SAC
- **Carga Dinámica de Anexos**: Localización automática de archivos (PDF, MSG, EML)
- **Actualización de Estado**: Marcado automático de resultados en Excel
- **Logging Seguro**: Registros sanitizados sin exposición de datos sensibles
- **Gestión de Errores Robusta**: Reintentos y manejo de excepciones

## Beneficios Esperados

- **Reducción de Costos**: Liberación de horas-hombre para tareas de mayor valor
- **Mejora de Calidad**: Eliminación de errores humanos en carga de documentos
- **Aumento de Eficiencia**: Procesamiento continuo y veloz
- **Cumplimiento Mejorado**: Trazabilidad auditable y consistente