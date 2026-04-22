# Reglas Personalizadas para Architect Mode - Archivo architecture.md

## Regla 1: Profundidad - Liderazgo Técnico
La documentación de arquitectura generada en `architecture.md` debe enfocarse en el liderazgo técnico y la planificación estratégica, detallando la justificación de las decisiones clave tomadas durante el desarrollo. Esto incluye:
- Explicación detallada del uso de tecnologías como Selenium para automatización web, incluyendo ventajas y consideraciones de mantenimiento.
- Justificación de la estructura modular adoptada en componentes como `data_handler.py`, `web_automator.py` y `config_loader.py`, enfatizando principios de separación de responsabilidades y escalabilidad.
- Análisis de trade-offs técnicos y cómo estas decisiones contribuyen a la robustez y mantenibilidad del sistema a largo plazo.

## Regla 2: Consistencia - Patrones de Diseño
El archivo `architecture.md` debe incluir una sección dedicada y detallada sobre el patrón de diseño a utilizar para la interacción web, específicamente el Page Object Model (POM), incluso si la implementación completa aún no existe. Esta sección debe cubrir:
- Descripción del patrón POM y su aplicación en el contexto de la automatización SAC.
- Estructura propuesta para las clases Page Object, incluyendo métodos y propiedades para interactuar con elementos web.
- Beneficios del patrón en términos de reutilización de código, facilidad de mantenimiento y reducción de duplicación.
- Plan de implementación futura, incluyendo cómo se integrará con los módulos existentes como `web_automator.py`.

## Regla 3: Formato - Estándar de Documentación
Asegurar que todas las secciones principales del `architecture.md` estén claramente separadas con títulos Markdown apropiados (usando `#`, `##`, `###`) y utilicen listas para mejorar la claridad y legibilidad. Las secciones obligatorias incluyen:
- **Componentes Clave**: Lista numerada o con viñetas de los componentes principales del sistema.
- **Flujo de Datos**: Diagrama o descripción paso a paso en formato de lista del flujo de información entre módulos.
- **Estrategia de Excepciones**: Lista de tipos de excepciones manejadas y estrategias de recuperación.
- Uso consistente de listas para enumerar características, beneficios y consideraciones en todas las secciones.

Estas reglas son **obligatorias** para el Agente Kilo Code al generar o actualizar el contenido del archivo `architecture.md` en **Architect Mode**. Cualquier modificación debe adherirse estrictamente a estos estándares para mantener la calidad y consistencia de la documentación arquitectónica.