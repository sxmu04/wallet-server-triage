# 🏦 Proyecto: Core Bancario "SecureWallet" - Auditoría y Refactorización Nivel Avanzado

¡Atención equipo de Ingeniería de Software ADSO! 

Hemos heredado el prototipo de un Microservidor de Transacciones Financieras de una Fintech aliada. El sistema está escrito en Python puro para optimizar recursos de infraestructura, pero el código actual viola múltiples principios de diseño seguro, escalabilidad y mantenibilidad. El cliente reporta pérdidas de dinero inexplicables en simulaciones de alta concurrencia y vulnerabilidades severas en auditorías de caja negra.

Su misión es auditar el código, identificar los fallos de arquitectura y reescribir el sistema bajo estándares de calidad industrial utilizando un flujo de trabajo colaborativo profesional en GitHub.

---

## 🛠️ Flujo de Trabajo Obligatorio (Git & GitHub)

Para este proyecto **NO deben crear un repositorio desde cero**. Trabajaremos simulando un entorno de desarrollo real donde se contribuye a un repositorio central de la organización:

1. **Hacer un Fork:** Un integrante por equipo debe hacer clic en el botón **Fork** (en la esquina superior derecha de este repositorio de la instrucción) para crear una copia exacta de este proyecto en su perfil personal de GitHub.
2. **Clonar el Fork:** Copien la URL de su propio Fork clonado y descárguenlo en sus entornos locales de Linux:
   ```bash
   git clone [https://github.com/sxmu04/securewallet-backend.git](https://github.com/sxmu04/securewallet-backend.git)
   ```
3. Trabajar en Ramas (Branches): No tiren código directamente en la rama main. Creen ramas específicas para cada hito del plan de mejora utilizando el estándar GitFlow:

    ```bash
    git checkout -b feature/arquitectura-mvc
    # o para corregir un bug específico:
    git checkout -b bugfix/condicion-carrera
   ```

4. Integración: Una vez solucionado un módulo, suban la rama a su Fork y realicen un Pull Request (PR) hacia la rama main del repositorio de su propio equipo para revisar los cambios antes de fusionar.

---
## 🎯 El Reto Técnico
Deberán aplicar ingeniería inversa leyendo el archivo wallet_server.py. Para aprobar la auditoría de calidad, el software refactorizado debe cumplir con las siguientes especificaciones obligatorias:

1. Desacoplamiento de Arquitectura (Capas Limpias)
El archivo actual maneja la red, las reglas de negocio, la lógica transaccional y la persistencia en archivos dentro de un solo bloque de código.

    * Deben separar el sistema en el patrón clean arquitechture (vista en formación).

    * El enrutador HTTP no debe conocer cómo se calculan los saldos ni cómo se guardan los datos en el JSON. Cada archivo debe tener una única responsabilidad.

2. Blindaje de Reglas de Negocio (Lógica Financiera)
El sistema actual procesa dinero. Deben auditar la lógica del flujo de transferencias para evitar fraudes y comportamientos inesperados:

    * Validación Estricta de Tipos: Aseguren que el sistema rechace montos de transferencia que pongan en riesgo la integridad matemática del saldo (caracteres extraños, desbordamientos, inyecciones de datos o signos matemáticos inválidos).

    * Validación de Estados Cruzados: Una transacción no puede involucrar entidades financieras con restricciones luegos o estados de bloqueo. Ambas partes del flujo deben estar validadas antes de mover un solo centavo.

3. El Problema de la Concurrencia y Persistencia
El backend lee y escribe un archivo de texto (accounts.json) directamente en medio del flujo de ejecución del hilo del servidor.

    * Investiguen qué ocurre cuando ocurren dos peticiones HTTP idénticas en la misma fracción de segundo afectando a la misma entidad. El código base actual tiene una latencia artificial para simular este fallo de producción.

    * Implementen un mecanismo técnico (ej. Bloqueos de hilos/Mutex con la librería threading de Python o colas de procesamiento de transacciones) para asegurar que la persistencia financiera sea atómica e inmutable ante solicitudes simultáneas.

4. Seguridad Estructural
El API expone endpoints administrativos de alto riesgo sin capas de control.

    * Implementen un sistema de interceptores o utilitarios que actúen como un Middleware de Seguridad, validando cabeceras específicas o un token de simulación antes de dar acceso a métodos críticos de alteración de estados del sistema.

---
## 📋 Entregables de la Auditoría
Cada equipo debe presentar al finalizar:

1. Documento de Triage Técnico: Un reporte formal (añadido en una carpeta /docs o en las Issues del repo) que liste los 5 hallazgos arquitectónicos y de seguridad más graves del código original, explicando el impacto técnico de cada uno de ellos si se desplegara a producción.

2. Repositorio Modularizado: El código definitivo atomizado en componentes con responsabilidades únicas según el estándar de arquitectura propuesto por el instructor.

3. Mesa de Pruebas (Postman / Thunder Client): Una colección de pruebas que demuestre escenarios límite (Edge Cases) que el sistema ahora maneja correctamente (ej. peticiones malformadas mitigadas con códigos HTTP adecuados como 400, 422 o 401).

---
## 🚀 Ejecución Local Base
1. Asegúrense de contar con su entorno listo.
2. Corran el servicio base para iniciar la auditoría:
```bash
    python3 wallet_server.py
   ```
3. El servidor iniciará en el puerto 8500. Analicen el código fuente para determinar las rutas de acceso existentes y los parámetros que requiere recibir en el cuerpo de las peticiones.