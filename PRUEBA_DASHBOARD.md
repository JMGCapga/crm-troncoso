# 📊 PRUEBA - Dashboard Financiero Ejecutivo

## Acceso

### Para José Manuel (Director)
- **PIN:** `9900`
- **Esperado:** Al entrar, ve directamente el Dashboard Financiero (no la lista de entregas)

### Para Viridiana (Gerencia)
- **PIN:** `5678`
- **Esperado:** Al entrar, ve el Dashboard Financiero Ejecutivo

### Para otros operadores
- **PIN:** `1111`, `3333`, `4444`, `5555`
- **Esperado:** Ver la lista normal de entregas (no Dashboard)

---

## ✅ SECCIONES A VERIFICAR

### 1️⃣ LIQUIDEZ DEL DÍA
Muestra números de **hoy** en tiempo real.

**Datos que obtiene:**
- **Entradas:** Suma de `cortes` con fecha=hoy y status='aprobado' → campo `granTotal`
- **Salidas:** Suma de `salidas` con fecha=hoy y status='aprobado'
- **Neto:** Entradas - Salidas
- **Efectivo Estimado:** Suma de `efectivo` de cortes de hoy
- **Transfers Pendientes:** Cotizaciones cerradas hoy con `formaPago='transferencia'` sin corte confirmado

**Cómo verificar:**
1. Ver un corte aprobado de hoy en Firebase → debe aparecer en "Entradas"
2. Ver una salida aprobada de hoy → debe aparecer en "Salidas"
3. El neto debe ser: Entradas - Salidas
4. El efectivo debe coincidir con lo que cargó Viridiana en los cortes

---

### 2️⃣ SEMANA ACTUAL (lunes-hoy)
Muestra números acumulados de esta semana.

**Datos que obtiene:**
- **Ventas:** Cotizaciones con status='cerrado' desde lunes hasta hoy → campo `total`
- **Gastos:** Salidas en rango, excluyendo `tipo='nomina'` y `tipo='compra'`
- **Nómina:** `nomina_semanas` de esta semana → campo `totalEfectivo`
- **Compras:** `compras` en rango → campo `total`
- **Utilidad:** Ventas - Gastos - Nómina - Compras
- **Margen:** (Utilidad / Ventas) * 100
- **Comparativo:** Flecha verde ↑ si creció vs semana anterior, roja ↓ si bajó

**Cómo verificar:**
1. Contar cotizaciones cerradas esta semana en Firebase y comparar el total
2. El margen debe ser positivo si Utilidad > 0
3. La flecha debe ser verde si las ventas de esta semana > ventas de semana anterior

---

### 3️⃣ MES ACTUAL (Gráfica de barras)
Muestra el acumulado del mes con proyección.

**Datos que obtiene:**
- **Gráfica:** Una barra naranja por cada día del mes, altura proporcional a ventas de ese día
- **Acumulado:** Suma de cotizaciones cerradas este mes
- **Meta:** $800,000 (fija)
- **% Meta:** (Acumulado / Meta) * 100
- **Proyección:** (Acumulado / días transcurridos) * días totales del mes

**Cómo verificar:**
1. Contar todos los `cortes` cerrados del mes y comparar "Acumulado"
2. Si es 10 de julio y llevas $700,000, proyección debe ser: (700,000 / 10) * 31 ≈ $2,170,000
3. La gráfica debe tener barras más altas en días con más ventas

---

### 4️⃣ POR RAZÓN SOCIAL
Desglose de ventas por empresa.

**Datos que obtiene:**
- **Razones:** JMG (José Manuel), IZZ (Itzayana), CEM (Cemcoya)
- **Monto y %:** Suma de ventas por razón este mes
- **Orden:** De mayor a menor venta

**Cómo verificar:**
1. Sumar todas las cotizaciones de José Manuel este mes → debe coincidir con "JMG"
2. Los porcentajes deben sumar 100%
3. El más grande debe estar primero

---

### 5️⃣ PIPELINE DE VENTAS
Cotizaciones pendientes agrupadas por probabilidad.

**Datos que obtiene:**
- **🟢 Alta:** Cotizaciones con `status='pendiente'` o `'contactado'` y `probabilidad='alta'` → cuenta y suma `monto`
- **🟡 Media:** Igual pero `probabilidad='media'`
- **🔴 Baja:** Igual pero `probabilidad='baja'`
- **Tasa de cierre:** (cerradas / (cerradas + perdidas)) * 100 este mes
- **Tiempo promedio:** Promedio de días entre creación y cierre

**Cómo verificar:**
1. Contar cotizaciones pendientes/contactadas en Firebase por probabilidad
2. Si hay 10 cerradas y 2 perdidas este mes → tasa debe ser 83%
3. El tiempo debe ser > 0 si hay cierres

---

### 6️⃣ ALERTAS
Avisos automáticos de cosas que necesitan atención.

**Alertas que muestra:**
1. ⚠️ Cotizaciones sin seguimiento > 48 horas
2. ⚠️ Compras a crédito próximas a vencer (próximos 7 días)
3. ⚠️ Transfers pendientes de confirmar
4. ⚠️ Fondeos pendientes de aprobación
5. ⚠️ Notas de crédito pendientes

**Cómo verificar:**
1. Crear una cotización con fecha de ayer → debe aparecer alerta
2. Crear un fondeo con status='pendiente' → debe aparecer alerta
3. Si no hay alertas, muestra "✓ Sin alertas"

---

### 7️⃣ RESUMEN ANUAL (Gráfica de barras)
Ventas de cada mes del 2026.

**Datos que obtiene:**
- **Gráfica:** Barras naranja para cada mes (E, F, M, A, M, J, J, A, S, O, N, D)
- **Mejor mes:** Mes con más ventas y su monto
- **Promedio mensual:** Acumulado / 12
- **Acumulado 2026:** Suma de todos los meses

**Cómo verificar:**
1. Contar cotizaciones de cada mes en Firebase
2. El mejor mes debe tener la barra más alta
3. El acumulado debe ser la suma de todos los meses

---

## 🔄 ACTUALIZAR DATOS

- **Botón verde "🔄 Actualizar":** Recarga todos los datos de Firebase
- **Timestamp:** Muestra la hora de la última actualización
- Los datos se cargan automáticamente al entrar al dashboard

---

## 🎯 CHECKLIST DE VERIFICACIÓN

- [ ] José Manuel entra con PIN 9900 → ve Dashboard
- [ ] Viridiana entra con PIN 5678 → ve Dashboard
- [ ] Otros operadores entran → ven lista de entregas (no dashboard)
- [ ] Liquidez del Día carga y muestra números reales
- [ ] Semana Actual calcula utilidad y margen correctamente
- [ ] Gráfica del mes se dibuja correctamente
- [ ] Razones Sociales suma 100%
- [ ] Pipeline cuenta cotizaciones correctamente
- [ ] Alertas muestra avisos reales
- [ ] Resumen Anual dibuja gráfica
- [ ] Botón Actualizar funciona
- [ ] Timestamp se actualiza
- [ ] Diseño se ve bien en móvil (iPhone José Manuel)
- [ ] Sin errores en la consola de navegador (F12 → Console)

---

## 📋 NOTAS IMPORTANTES

1. **Firebase:** Todos los datos vienen en tiempo real desde la BD. No necesita refrescar la página.
2. **Sin librerías externas:** Las gráficas se dibujan con SVG puro, sin Chart.js
3. **Seguridad:** Solo Jose Manuel (9900) y Viridiana (5678) ven el dashboard completo
4. **Móvil:** Optimizado para pantalla de José Manuel (responsive design)
5. **Sin listeners:** No usa `onSnapshot()`, solo `get()` para no gastar cuota de Firebase

---

## ❌ POSIBLES ERRORES A REVISAR

Si algo no funciona:

1. **"Sin datos" en secciones:** 
   - Revisar que existan registros en Firebase con las fechas correctas
   - Las fechas en Firebase deben estar en formato `YYYY-MM-DD`

2. **Gráficas no aparecen:**
   - Abrir F12 → Console para ver si hay errores de JavaScript
   - Las gráficas se dibujan con SVG - no debería haber problemas

3. **Números incorrectos:**
   - Verificar que los campos en Firebase coincidan con los nombres esperados:
     - `cotizaciones.total` (no `monto` o `importe`)
     - `cortes.granTotal` y `cortes.efectivo`
     - `salidas.monto`
     - `nomina_semanas.totalEfectivo`
     - `compras.total`

4. **No entra al dashboard:**
   - Revisar que la lógica de login esté correcta (PINs 9900 y 5678)
   - Ver consola del navegador (F12) para errores

---

## 📞 PARA JOSÉ MANUEL

Si ves algo que no funciona:
1. Abre la consola (F12 en Chrome/Safari → Console)
2. Describe qué sección falla y qué número esperabas
3. Comparte los números reales de Firebase para comparar

