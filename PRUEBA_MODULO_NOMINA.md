# 🧪 Prueba del Módulo de Nómina Semanal

## ✅ Checklist de Verificación

Sigue estos pasos para verificar que el módulo de Nómina funciona correctamente.

---

## 🔐 Paso 1: Acceder como Viridiana (5678)

1. Abre http://localhost:8000/index.html (o la URL del CRM)
2. Ingresa el PIN: **5678** (Viridiana - Gerencia)
3. Verifica que veas el nuevo tab **👷 Nómina** en la barra de tabs

**Resultado esperado:** Deberías ver los tabs incluyendo "👷 Nómina" junto a "🛒 Compras"

---

## ⚙️ Paso 2: Configurar Empleados

1. Haz clic en el tab **👷 Nómina**
2. Deberías ver la sub-pantalla **"⚙️ Config. Empleados"** abierta por defecto
3. Verifica que aparezca una tabla con 6 empleados:
   - Ivette (sin IMSS)
   - Erika (con IMSS)
   - Carlos J. Escobar (sin IMSS)
   - Francisco (con IMSS)
   - Agustín Lara (sin IMSS)
   - Viridiana (con IMSS)

4. **Ingresa sueldos de prueba:**
   - Ivette: **2000**
   - Erika: **2200** (IMSS: **400**)
   - Carlos J. Escobar: **2000**
   - Francisco: **2200** (IMSS: **400**)
   - Agustín Lara: **1800**
   - Viridiana: **2500** (IMSS: **500**)

5. Haz clic en **"💾 Guardar Configuración"**

**Resultado esperado:** Los datos se guardan en Firebase en la colección `empleados`

---

## 📝 Paso 3: Crear Nueva Nómina Semanal

1. Haz clic en el tab **"📝 Nueva Nómina"**
2. Verifica que aparezcan:
   - Semana ISO actual (ej: 2026-W28)
   - Lunes de esta semana
   - Sábado (día de pago)

3. Verifica que haya una **tabla de nómina** con columnas:
   - Empleado | Sueldo | Faltas | Desc. Faltas | Préstamo | Otros Desc. | Bonos | Neto | IMSS | Efectivo Viri

4. **Prueba de Faltas - Registra 1 falta para Ivette:**
   - Campo "Faltas" en la fila de Ivette: ingresa **1**
   - El campo "Desc. Faltas" debe calcularse automáticamente
   - Para Ivette (6 días/semana, sueldo $2000): Desc. = $2000/6 × 1 = ~$333

   **Resultado esperado:** El descuento se calcula automáticamente

5. **Prueba de Bonos - Agrega $100 de bono a Francisco:**
   - Campo "Bonos" en la fila de Francisco: ingresa **100**
   
   **Resultado esperado:** El neto se recalcula incluyendo el bono

6. Verifica que los **totales se actualicen** en la parte inferior:
   - Total Nómina
   - Total IMSS
   - Total Efectivo (lo que paga Viridiana en efectivo)

7. Haz clic en **"💾 Guardar borrador"**

**Resultado esperado:** La nómina se guarda en Firebase sin procesar aún

---

## 💳 Paso 4: Crear un Préstamo

1. Haz clic en el tab **"💳 Préstamos"**
2. Haz clic en **"+ Nuevo Préstamo"**
3. Completa el formulario:
   - **Empleado:** Francisco
   - **Monto Total:** 1000
   - **Monto Semanal:** 200
   - **Notas:** (opcional)

4. Haz clic en **"✓ Guardar Préstamo"**

**Resultado esperado:** 
- El préstamo se crea en Firebase colección `prestamos`
- Aparece en la lista de "Préstamos Activos"
- Muestra barra de progreso de 0% pagado

---

## ✅ Paso 5: Procesar la Nómina

1. Vuelve al tab **"📝 Nueva Nómina"**
2. Verifica que ahora el **préstamo de Francisco** ($200) aparezca en la columna "Préstamo"
3. **Calcula mentalmente el neto para Francisco:**
   - Sueldo: $2200
   - Descuentos: $200 (préstamo) + $100 (otros desc. si agregaste) = $300
   - Bonos: $100
   - Neto: $2200 - $300 + $100 = $2000
   - IMSS: $400
   - Efectivo Viri: $2000 - $400 = $1600

4. Haz clic en **"✅ PROCESAR NÓMINA"**

**Resultado esperado:**
- Se crea un registro en `salidas` con:
  - tipo: "nomina"
  - monto: Total Efectivo
  - fecha: Sábado de la semana
- El préstamo de Francisco se decrementa en $200
- Se muestra mensaje ✅ "Nómina procesada"

---

## 👀 Paso 6: Ver como José Manuel (9900)

1. Haz clic en **"Salir"**
2. Ingresa el PIN: **9900** (José Manuel - Director)
3. Haz clic en el tab **👷 Nómina**

**Resultado esperado:**
- José Manuel ve solo información de IMSS
- Ve cuánto debe transferir por IMSS esta semana
- (En esta versión, ve la misma pantalla que Viridiana, pero en futuras versiones podría tener una vista diferente)

---

## 📊 Paso 7: Ver Historial

1. (Siguiendo como Viridiana) Haz clic en el tab **"📊 Historial"**
2. Verifica que aparezca la semana actual con:
   - Semana (ISO)
   - Cantidad de empleados
   - Total de efectivo pagado

3. Haz clic en una fila para ver detalles (opcional)

**Resultado esperado:** El historial muestra las nóminas procesadas

---

## 🧹 Paso 8: Limpiar Datos de Prueba

Para que todo esté limpio después de la prueba:

1. **Elimina desde Firebase Console:**
   - Colección `empleados` - borra todos los documentos
   - Colección `nomina_semanas` - borra todos los documentos
   - Colección `prestamos` - borra todos los documentos
   - Colección `salidas` - borra el registro de nómina creado

O ejecuta este script en la consola de Firestore:

```javascript
// Eliminar empleados
db.collection('empleados').get().then(snap => {
  snap.forEach(doc => doc.ref.delete());
});

// Eliminar nóminas
db.collection('nomina_semanas').get().then(snap => {
  snap.forEach(doc => doc.ref.delete());
});

// Eliminar préstamos
db.collection('prestamos').get().then(snap => {
  snap.forEach(doc => doc.ref.delete());
});
```

---

## 📋 Resumen de lo que se testea:

| Aspecto | ✓ Verificado |
|---------|--------------|
| Tab visible en el CRM | |
| Permisos (solo Viridiana y José Manuel) | |
| Carga de empleados desde Firebase | |
| Configuración de sueldos | |
| Cálculo automático de descuentos por faltas | |
| Integración con préstamos | |
| Procesamiento de nómina | |
| Generación de registro en Salidas | |
| Historial de nóminas | |

---

## 🔗 URLs útiles:

- **CRM:** http://localhost:8000/index.html
- **Firebase Console:** https://console.firebase.google.com/project/troncoso--sistema

---

## 💡 Notas:

- El módulo usa las mismas colecciones de Firebase que el resto del CRM
- Los cálculos son automáticos cuando cambias faltas, bonos u otros descuentos
- Los préstamos se descargan automáticamente cuando procesas la nómina
- El módulo crea automáticamente un registro en "Salidas" cuando procesas

---

**¡Listo para probar! 🚀**
