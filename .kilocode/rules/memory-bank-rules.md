# Reglas Personalizadas para Architect Mode - Archivo memory-bank-rules.md

## Regla 1: Inicialización del Memory Bank
El archivo `brief.md` debe ser creado y mantenido **manualmente** por los desarrolladores. Este archivo sirve como base para inicializar y generar automáticamente los otros archivos del Memory Bank: `product.md`, `context.md`, `architecture.md` y `tag.md`. Kilo Code no debe modificar `brief.md` directamente; cualquier actualización debe provenir de los desarrolladores humanos.

## Regla 2: Generación Automática de Archivos
Kilo Code debe generar y mantener automáticamente los archivos `product.md`, `context.md`, `architecture.md` y `tag.md` basándose en el contenido de `brief.md`. La generación debe ocurrir cuando se detecte un cambio en `brief.md` o cuando se solicite explícitamente la actualización del Memory Bank. Cada archivo debe derivarse lógicamente del `brief.md`, expandiendo la información proporcionada hacia aspectos específicos del proyecto.

## Regla 3: Contenido Específico por Archivo
- **`product.md`**: Debe describir el producto o solución final, incluyendo funcionalidades clave, beneficios para el usuario y alcance del proyecto, derivado de la visión inicial en `brief.md`.
- **`context.md`**: Debe proporcionar el contexto del proyecto, incluyendo antecedentes, stakeholders, restricciones y entorno operativo, basado en la información contextual implícita o explícita en `brief.md`.
- **`architecture.md`**: Debe detallar la arquitectura técnica, componentes, patrones de diseño y decisiones clave, justificando elecciones basadas en los requisitos del `brief.md`.
- **`tag.md`**: Debe contener etiquetas y metadatos relevantes para categorización, búsqueda y navegación del proyecto, extraídos o inferidos del `brief.md`.

## Regla 4: Mantenimiento y Actualización
Kilo Code debe actualizar los archivos del Memory Bank automáticamente cuando se modifique `brief.md`, asegurando consistencia y coherencia entre todos los archivos. Las actualizaciones deben preservar la información existente a menos que sea contradictoria con el nuevo `brief.md`. Si se detectan inconsistencias, Kilo Code debe proponer cambios pero no aplicarlos sin aprobación.

## Regla 5: Formato y Estándares
Todos los archivos del Memory Bank deben seguir un formato Markdown consistente, con secciones claramente separadas usando títulos (`#`, `##`, `###`) y listas para mejorar la legibilidad. El contenido debe ser técnico, preciso y alineado con las mejores prácticas de documentación. Kilo Code debe evitar duplicaciones innecesarias y mantener un tono profesional y objetivo.

Estas reglas son **obligatorias** para el Agente Kilo Code al generar, actualizar o mantener los archivos del Memory Bank en **Architect Mode**. Cualquier acción relacionada con el Memory Bank debe adherirse estrictamente a estos estándares para garantizar la calidad, consistencia y utilidad de la documentación del proyecto.