### 📘 Documento de Requerimientos de Software

**Proyecto:** QuickTask
**Versión:** 1.0
**Autor:** Ingeniero de Requisitos
**Fecha:** 28 de octubre de 2025

---

## 1. Descripción general del sistema

**QuickTask** es una aplicación de gestión de tareas personales que permite a los usuarios crear, editar, organizar y marcar tareas como completadas.
El objetivo principal del sistema es ofrecer una **interfaz intuitiva y eficiente** que facilite el control de actividades diarias y la mejora de la productividad individual.

El sistema estará disponible como **aplicación web y móvil**, sincronizando la información del usuario mediante una cuenta personal.

---

## 2. Actores principales

| Actor                   | Descripción                                                                                        |
| ----------------------- | -------------------------------------------------------------------------------------------------- |
| **Usuario**             | Persona que utiliza la aplicación para gestionar sus tareas personales.                            |
| **Sistema (QuickTask)** | Aplicación que procesa las acciones del usuario, almacena la información y muestra los resultados. |

---

## 3. Requerimientos funcionales

### 🔹 Gestión de cuentas

1. **RF1:** El sistema debe permitir al usuario registrarse mediante correo electrónico y contraseña.
2. **RF2:** El sistema debe permitir iniciar y cerrar sesión de forma segura.
3. **RF3:** El sistema debe permitir recuperar la contraseña mediante correo electrónico.

### 🔹 Gestión de tareas

4. **RF4:** El usuario debe poder **crear una nueva tarea** ingresando título, descripción y fecha opcional.
5. **RF5:** El usuario debe poder **editar los datos** de una tarea existente.
6. **RF6:** El usuario debe poder **marcar una tarea como completada** o **revertirla a pendiente**.
7. **RF7:** El usuario debe poder **eliminar una tarea** permanentemente.
8. **RF8:** El sistema debe permitir **filtrar tareas** por estado (pendiente, completada, todas).
9. **RF9:** El sistema debe permitir **ordenar tareas** por fecha de creación, prioridad o fecha límite.

### 🔹 Sincronización y notificaciones

10. **RF10:** El sistema debe sincronizar las tareas del usuario en tiempo real entre dispositivos.
11. **RF11:** El sistema debe permitir configurar **recordatorios** mediante notificaciones push o correo electrónico.

### 🔹 Interfaz y usabilidad

12. **RF12:** El sistema debe mostrar una **lista visual de tareas** agrupadas por estado o fecha.
13. **RF13:** El usuario debe poder **buscar tareas** por palabras clave.
14. **RF14:** El sistema debe ofrecer una **vista resumida del progreso**, mostrando el número de tareas completadas y pendientes.

---

## 4. Requerimientos no funcionales

| Categoría          | Requerimiento                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------------- |
| **Rendimiento**    | RNF1: La aplicación debe cargar la vista principal en menos de 3 segundos con conexión estándar (10 Mbps).          |
| **Disponibilidad** | RNF2: El sistema debe estar disponible al menos el 99% del tiempo mensual.                                          |
| **Escalabilidad**  | RNF3: Debe soportar al menos 10,000 usuarios simultáneos sin degradación perceptible.                               |
| **Usabilidad**     | RNF4: La interfaz debe ser intuitiva, con un diseño responsivo que se adapte a pantallas móviles y de escritorio.   |
| **Seguridad**      | RNF5: Las contraseñas deben almacenarse cifradas siguiendo estándares como bcrypt.                                  |
| **Privacidad**     | RNF6: Los datos del usuario no deben compartirse con terceros sin consentimiento explícito.                         |
| **Compatibilidad** | RNF7: La aplicación web debe ser compatible con los navegadores modernos (Chrome, Edge, Firefox, Safari).           |
| **Mantenibilidad** | RNF8: El código debe estar documentado y seguir un estándar de nomenclatura para facilitar futuras actualizaciones. |

---

## 5. Criterios de aceptación

| Función                                | Criterio de aceptación                                                                                                                                                                                          |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Crear tarea (RF4)**                  | Dado que el usuario está autenticado, cuando complete el formulario con un título válido y presione “Guardar”, entonces la tarea debe aparecer en la lista de tareas pendientes.                                |
| **Marcar tarea como completada (RF6)** | Dado que el usuario visualiza la lista de tareas, cuando seleccione una tarea pendiente y presione “Marcar como completada”, entonces el sistema debe actualizar su estado y moverla a la lista de completadas. |
| **Configurar recordatorio (RF11)**     | Dado que el usuario selecciona una tarea con fecha límite, cuando elija una hora de recordatorio, entonces el sistema debe enviar una notificación en la fecha y hora establecida.                              |

---

## 6. Suposiciones y restricciones

**Suposiciones:**

* El usuario dispone de conexión a internet para sincronizar sus tareas.
* Los dispositivos del usuario soportan notificaciones push.
* La autenticación se realizará mediante un servicio estándar (por ejemplo, Firebase Auth o similar).

**Restricciones:**

* El almacenamiento inicial estará limitado a **100 MB por usuario**.
* La aplicación móvil se desarrollará inicialmente solo para **Android**, con soporte para iOS en una fase posterior.
* El sistema debe estar desarrollado en un entorno **basado en la nube** (por ejemplo, AWS, Firebase o equivalente).

---

## 7. Riesgos y ambigüedades detectadas

1. **Falta de definición del modelo de negocio:** No se especifica si QuickTask será gratuita o tendrá planes premium.
2. **Sin detalles sobre prioridades de tareas:** No se aclara si habrá niveles de prioridad (alta, media, baja).
3. **Recordatorios:** Se necesita definir si las notificaciones serán locales, por correo, o ambas.
4. **Sincronización:** No se ha definido si se usará almacenamiento en la nube o una API personalizada.
5. **Diseño UX/UI:** No se especifican lineamientos visuales ni accesibilidad.

