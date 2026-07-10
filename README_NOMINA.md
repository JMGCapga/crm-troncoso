# 👷 Módulo de Nómina Semanal - Materiales Troncoso

## 🎯 Resumen Ejecutivo

Se ha implementado **exitosamente** el módulo de Nómina Semanal en el CRM Materiales Troncoso. Este módulo permite a **Viridiana (Gerencia)** y **José Manuel (Director)** gestionar la nómina semanal de manera digital, reemplazando el sistema manual actual.

### ✨ Características Principales

- ✅ **Configuración de empleados** con sueldos y datos IMSS
- ✅ **Cálculos automáticos** de descuentos por faltas
- ✅ **Gestión de préstamos** con seguimiento de saldo pendiente
- ✅ **Procesamiento de nómina** que genera registros en "Salidas"
- ✅ **Historial completo** de nóminas procesadas
- ✅ **Integración con Firebase** para almacenamiento persistente

---

## 📁 Archivos Modificados/Creados

### Modificados:
```
crm-troncoso-real/index.html
├── Agregado: tab "👷 Nómina"
├── Agregado: panel-nomina con 4 sub-pantallas
└── Agregado: ~500 líneas de funciones JavaScript
```

### Creados (Documentación):
```
PRUEBA_MODULO_NOMINA.md          → Guía completa de pruebas
DOCUMENTACION_NOMINA.md           → Documentación técnica detallada
README_NOMINA.md                  → Este archivo
```

---

## 🚀 Cómo Usar

### 1. Acceder al Módulo

```
1. Abre: http://localhost:8000/index.html (o tu URL del CRM)
2. Ingresa PIN: 5678 (Viridiana) o 9900 (José Manuel)
3. Haz clic en el tab "👷 Nómina"
```

### 2. Configurar Empleados (Primera vez)

En la sub-pantalla **"⚙️ Config. Empleados"**:

1. Se cargan automáticamente 6 empleados:
   - Ivette (sin IMSS)
   - Erika (con IMSS)
   - Carlos J. Escobar (sin IMSS)
   - Francisco (con IMSS)
   - Agustín Lara (sin IMSS)
   - Viridiana (con IMSS)

2. Ingresa el **sueldo semanal** de cada uno
3. Si tiene IMSS, ingresa el **monto IMSS** que transfiere José Manuel
4. Haz clic en **"💾 Guardar Configuración"**

### 3. Crear Nueva Nómina

En la sub-pantalla **"📝 Nueva Nómina"**:

1. Se auto-calcula:
   - Semana ISO (ej: 2026-W28)
   - Lunes de esta semana
   - Sábado (día de pago)

2. Para cada empleado, puedes ingresar:
   - **Faltas:** Número de días faltados (se calcula descuento automático)
   - **Otros Desc.:** Descuentos adicionales
   - **Bonos:** Bonificaciones extras

3. Los **Préstamos** se cargan automáticamente si hay activos

4. La tabla recalcula automáticamente:
   - Descuento por faltas
   - Total descuentos
   - Neto a pagar
   - Efectivo que paga Viridiana (neto - IMSS)

5. Haz clic en **"💾 Guardar borrador"** para guardar sin procesar

### 4. Procesar la Nómina

Una vez revisada:

1. Haz clic en **"✅ PROCESAR NÓMINA"**

**Esto automáticamente:**
- ✓ Marca la nómina como "procesada"
- ✓ Crea un registro en la colección "salidas"
- ✓ Descuenta los préstamos (reduce saldo pendiente)
- ✓ Marca préstamos como liquidados si saldo = 0

### 5. Gestionar Préstamos

En la sub-pantalla **"💳 Préstamos"**:

1. **Ver activos:** Muestra todos los préstamos en curso con:
   - Barra de progreso de porcentaje pagado
   - Saldo pendiente
   - Descuento semanal

2. **Crear nuevo:**
   - Haz clic en **"+ Nuevo Préstamo"**
   - Selecciona empleado
   - Ingresa monto total
   - Ingresa monto semanal (descuento)
   - Guarda

3. **Liquidar:**
   - Haz clic en **"✓ Liquidar"** cuando esté pagado

### 6. Ver Historial

En la sub-pantalla **"📊 Historial"**:

- Filtra por: Todas | Este mes | Este trimestre
- Muestra todas las nóminas procesadas
- Haz clic para ver detalles

---

## 🔢 Fórmulas de Cálculo

### Descuento por Faltas
```
descuento = (sueldo_semanal / días_semana) × faltas
```

Ejemplo: Sueldo $2000, 6 días/semana, 1 falta
```
descuento = (2000 / 6) × 1 = $333.33
```

### Neto a Pagar
```
neto = sueldo - descuentos + bonos
```

### Efectivo que paga Viridiana
```
Si tiene IMSS:
  efectivo = neto - montoIMSS
Si no tiene IMSS:
  efectivo = neto
```

### Totales Semanales
```
totalNomina = suma de todos los netos
totalIMSS = suma de montos IMSS (José Manuel transfiere)
totalEfectivo = suma de efectivo a pagar (Viridiana)
```

---

## 🗄️ Datos en Firebase

### Colecciones Creadas

#### `empleados`
Almacena datos de cada empleado:
```json
{
  "nombre": "Ivette",
  "imss": false,
  "diasSemana": 6,
  "sueldoSemanal": 2000,
  "montoIMSS": 0,
  "activo": true,
  "timestamp": 1626234567890
}
```

#### `nomina_semanas`
Registro de cada nómina procesada:
```json
{
  "semana": "2026-W28",
  "fechaInicio": "2026-07-07",
  "fechaSabado": "2026-07-12",
  "status": "procesada",
  "empleados": [...],
  "totalNomina": 12000,
  "totalIMSS": 900,
  "totalEfectivo": 11100
}
```

#### `prestamos`
Seguimiento de préstamos activos:
```json
{
  "empleado": "Francisco",
  "montoTotal": 1000,
  "montoSemanal": 200,
  "saldoPendiente": 600,
  "activo": true,
  "autorizadoPor": "Jose Manuel"
}
```

---

## 👥 Control de Acceso

**Solo pueden usar el módulo:**
- **Viridiana (5678)** - Rol: Gerencia
  - Captura sueldos
  - Registra faltas y descuentos
  - Procesa nómina
  - Ve historial completo

- **José Manuel (9900)** - Rol: Director
  - Ve resumen de IMSS
  - Ve historial de nóminas
  - (En futuras versiones: dashboard ejecutivo)

**No pueden ver:**
- Operadores (Francisco, Agustín, Carlos)
- Otros roles

---

## 🧪 Pruebas

### Cómo Verificar que Funciona

Sigue la guía completa: **PRUEBA_MODULO_NOMINA.md**

Resumen rápido:
```
1. Accede como Viridiana (5678)
2. Ve el tab "👷 Nómina"
3. Configura empleados con sueldos
4. Crea nueva nómina (automática para esta semana)
5. Registra 1 falta en Ivette → verifica descuento automático
6. Crea un préstamo de $1000 con $200 semanal
7. Procesa nómina → verifica que se cree en "Salidas"
8. Accede como José Manuel (9900) → ve la nómina
9. Limpia datos de prueba en Firebase
```

---

## 🔗 Integración con Otros Módulos

### Con "Salidas" (📤)
Cuando procesas una nómina, automáticamente se crea un registro en Salidas:
- **Tipo:** Nómina
- **Monto:** Total Efectivo
- **Fecha:** Sábado de la semana
- **Status:** Aprobado

### Con "Compras" (🛒)
No hay interacción directa, pero ambos escriben a Firebase independientemente.

### Con "Corte de Caja" (💰)
El total de efectivo de nómina se resta del corte del sábado.

---

## 🛠️ Mantenimiento

### Agregar un Empleado

1. En Firebase Console, ve a `empleados`
2. Agregar documento nuevo:
```json
{
  "nombre": "Nuevo Empleado",
  "imss": true/false,
  "diasSemana": 6,
  "sueldoSemanal": 0,
  "montoIMSS": 0,
  "activo": true,
  "timestamp": Date.now()
}
```
3. Recarga el CRM

### Modificar Sueldo Base

1. Ve a "⚙️ Config. Empleados"
2. Modifica el campo de sueldo semanal
3. Haz clic fuera del campo (se guarda automático)

### Ver Detalles de una Nómina Procesada

1. Ve a "📊 Historial"
2. Haz clic en una fila
3. Se muestra un alert con los detalles (en futuras versiones: modal mejor)

---

## 🐛 Troubleshooting

### "No tienes permisos para acceder"
→ Solo Viridiana (5678) y José Manuel (9900) pueden ver el módulo

### "Sin conexión a Firebase"
→ Verifica que el badge de sincronización (header) esté verde
→ Comprueba tu conexión a internet

### Los empleados no aparecen
→ Primera carga toma ~1 segundo para crear seed
→ Espera un momento y recarga

### No se guarda la nómina
→ Verifica que Firebase esté conectado
→ Abre la consola (F12) para ver errores

### Los préstamos no aparecen en nómina
→ Verifica que estén en estado "activo: true"
→ Recarga la pantalla de nueva nómina

---

## 📊 Resumen de Cambios

| Aspecto | Antes | Después |
|---------|-------|---------|
| Nómina | Manual (archivo local) | Digital en Firebase |
| Disponibilidad | Solo en la tienda | Accesible desde celular/tablet |
| Cálculos | Manuales | Automáticos |
| Histórico | Archivos dispersos | Centralizado en Firebase |
| Préstamos | Control manual | Seguimiento automático |
| Reportes | PDF descargado | Vistas en tiempo real |

---

## 📞 Contacto y Soporte

Si hay problemas o dudas:

1. **Consola del navegador** (F12): Revisa los errores
2. **Firebase Console**: Verifica estado de colecciones
3. **Revisa documentación**: DOCUMENTACION_NOMINA.md

---

## 📝 Checklist de Deploy

Antes de usar en producción:

- [ ] Backup de datos actuales en Firebase
- [ ] Probar con datos de prueba (PRUEBA_MODULO_NOMINA.md)
- [ ] Verificar permisos de usuarios (Viridiana y José Manuel)
- [ ] Entrenar a Viridiana en uso del módulo
- [ ] Limpiar datos de prueba
- [ ] Hacer deploy a producción
- [ ] Monitorear primeras 2 semanas de uso

---

## 🎓 Capacitación para Viridiana

Puntos clave a entender:

1. **Los sueldos se guardan una sola vez** → Actualiza cuando cambie
2. **Cada sábado se crea una nueva nómina** → Automática
3. **Los descuentos se calculan automáticamente** → No edites "Desc. Faltas"
4. **Procesar = confirmar y crear movimiento** → No se puede deshacer fácilmente
5. **Los préstamos se descargan automáticamente** → No sumar manual
6. **El total de efectivo se usa en Corte de Caja** → Es lo que retira del banco

---

## 🚀 Versiones Futuras

Ideas para mejorar:

- [ ] Exportar nómina a PDF
- [ ] Generar archivo de transferencias bancarias
- [ ] Notificar a empleados por SMS
- [ ] Cálculo automático de ISR
- [ ] Integración con asistencia
- [ ] Múltiples monedas
- [ ] Cargas sociales (Seguro Social, INFONAVIT)
- [ ] Dashboard ejecutivo para José Manuel

---

## 📦 Versión

**Versión:** 1.0  
**Fecha:** 2026-07-10  
**Estado:** ✅ Completo y Funcional  
**Próxima Revisión:** 2026-07-24  

---

**¡Listo para usar! 🎉**

Para comenzar: Abre el CRM, accede como Viridiana (5678), haz clic en "👷 Nómina" y sigue la guía de pruebas.
