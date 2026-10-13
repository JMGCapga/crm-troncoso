# Seguridad del CRM — cómo está armada

**Idea:** el código del CRM es público (GitHub Pages), así que nada secreto vive en él. Quien protege los datos son las **reglas de Firestore/Storage** y las **cuentas de Firebase Auth** del personal.

## Archivos
- `firestore.rules` y `storage.rules` — las reglas. Solo entran las 8 cuentas del personal (`<nombre>@troncoso-crm.com`). Nómina, empleados y préstamos: solo Director y Gerencia.
- `cuentas.py` — crea las cuentas con un PIN al azar (se imprime una sola vez, no se guarda).
- `pruebas/` — 657 pruebas contra el emulador. Correr: `cd seguridad/pruebas && npm install && npm test` (necesita Java y `firebase-tools`).
- `firebase.json` — configuración del emulador.
- `encuesta-troncoso.patch` — el cambio que hay que aplicar al repo `encuesta-troncoso` (`git apply`): la página usa `encuestas_respondidas/{folio}` y ya no lee la colección de evaluaciones.

## Dos accesos SIN cuenta (a propósito)
1. **Encuesta del cliente** (`encuesta-troncoso`): solo puede *crear* una evaluación y preguntar por UN folio (`encuestas_respondidas/{folio}`). No puede leer ni listar nada.
2. **Link de WhatsApp para aprobar fondeos**: abre UN fondeo por su id (20 caracteres al azar) y lo cierra una sola vez como aprobado/rechazado. No puede buscar por folio ni cambiar montos.

## Instalar (fuera de horario)
1. Firebase Console → Authentication → Método de acceso → activar **Correo electrónico/contraseña**.
2. `python3 seguridad/cuentas.py crear todas --contactos <archivo-con-teléfonos.json>` → anota los 8 PIN (no subir ese archivo a git). Formato del archivo: `{"josemanuel":"52...","viridiana":"52...","francisco":"52...","agustin":"52...","carlos":"52..."}`.
3. Subir el CRM y la encuesta (`encuesta-troncoso`) a GitHub; esperar 1–2 min a que GitHub Pages publique.
4. Probar que cada quien entra con su PIN.
5. Publicar reglas: Firestore → Reglas (pegar `firestore.rules`) y Storage → Reglas (pegar `storage.rules`) → Publicar.
6. Verificar: sin sesión y con sesión anónima las lecturas dan 403.
7. Opcional, un día después: desactivar el proveedor *Anónimo* en Authentication y quitar `signInAnonymously` de la encuesta y del link de fondeos.

## Regresar atrás
Firebase Console → Firestore → Reglas → **Historial** → restaurar la versión anterior (igual en Storage). El CRM nuevo sigue funcionando con las reglas viejas.

## PIN olvidado
Borrar el usuario en Authentication → Users y correr `python3 seguridad/cuentas.py crear <nombre>` (genera un PIN nuevo). Cada quien puede cambiar el suyo con el botón de la llave (arriba, junto a Salir).

## Qué no cubre
- Un compañero con cuenta ve lo de todos (salvo nómina/empleados/préstamos/razones fiscales). Restringir más por rol es una fase 2.
- La historia de Git conserva datos viejos (PINs ya cambiados, CLABEs y teléfonos). Purgarla requiere reescribir el historial.
