# Contexto del Negocio: SAC Automation

## 1. El Problema de Negocio

En la gestión de Peticiones, Quejas y Reclamos (PQR) en EPM, cada interacción con un cliente o proceso interno genera documentación que debe ser archivada en el **Sistema de Administración de Contratos (SAC)**. Esta documentación, conocida como "anexos", es fundamental para la trazabilidad, el cumplimiento normativo y la auditoría de los casos.

El proceso de carga de estos anexos se realizaba de forma **100% manual**. Un analista debía:

1.  Revisar una hoja de cálculo de Excel (el "control diario") para identificar los casos del día que requerían la carga de un anexo.
2.  Localizar el archivo correspondiente (un PDF, un correo `.msg`, etc.) en una carpeta de red compartida.
3.  Abrir un navegador web e iniciar sesión en la plataforma SAC.
4.  Navegar hasta el módulo de administración de procesos.
5.  Buscar manualmente cada número de proceso en la interfaz.
6.  Abrir el modal de carga de anexos.
7.  Completar un formulario con metadatos (título, descripción, tipo de documento).
8.  Subir el archivo.
9.  Esperar la confirmación y cerrar las ventanas modales.
10. Volver al archivo Excel y marcar la fila como "procesada", a menudo añadiendo la fecha y hora.

Este flujo de trabajo, repetido para docenas o cientos de casos diarios, presentaba varios problemas críticos:

- **Ineficiencia y Alto Costo Operativo:** Consumía una cantidad significativa de horas de trabajo de personal cualificado que podían dedicarse a tareas de mayor valor.
- **Propenso a Errores Humanos:** Errores de digitación al buscar un proceso, adjuntar el archivo incorrecto al caso equivocado, o marcar incorrectamente el estado en el Excel eran comunes.
- **Baja Velocidad de Respuesta:** La carga masiva de anexos podía tomar horas, retrasando la actualización del estado de los casos en el sistema oficial.
- **Falta de Trazabilidad Estandarizada:** El seguimiento del trabajo realizado dependía de la disciplina de cada analista para actualizar el archivo de control.

## 2. La Solución: Automatización Robótica de Procesos (RPA)

**SAC Automation** se concibió como una solución de RPA para abordar directamente estos problemas. El objetivo no es cambiar el proceso de negocio subyacente, sino **automatizar las tareas manuales y repetitivas** que lo componen.

El robot emula las acciones de un usuario humano, pero de una manera más rápida, precisa y sistemática:

- **Fuente de Verdad Única:** El archivo Excel sigue siendo la fuente de verdad para la cola de trabajo, pero ahora es leído por el robot.
- **Interacción Directa con los Sistemas:** El robot interactúa directamente con el sistema de archivos para encontrar los anexos y con la aplicación web SAC para cargarlos.
- **Registro Automático y Auditable:** Al finalizar cada operación, el robot actualiza el estado en el mismo archivo Excel y genera un log técnico detallado. Esto proporciona una trazabilidad inmediata y estandarizada.

## 3. Valor Aportado

- **Reducción de Costos:** Libera horas-hombre, permitiendo que el personal se enfoque en análisis, gestión y resolución de casos en lugar de tareas administrativas.
- **Mejora de la Calidad de los Datos:** Elimina prácticamente los errores humanos en la carga y registro de anexos, asegurando que el archivo correcto esté en el lugar correcto.
- **Aumento de la Eficiencia y Velocidad:** El robot puede procesar la cola de trabajo de forma continua y a una velocidad significativamente mayor que un humano.
- **Mejora en la Trazabilidad y Cumplimiento:** Proporciona un registro auditable y consistente de todas las cargas de anexos, facilitando auditorías y el seguimiento del cumplimiento.