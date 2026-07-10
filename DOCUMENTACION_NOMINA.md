# 📘 Documentación Técnica - Módulo de Nómina Semanal

## 📐 Arquitectura

El módulo de Nómina Semanal es parte del CRM Materiales Troncoso y utiliza:
- **Frontend:** HTML + CSS + JavaScript vanilla
- **Backend:** Firebase Firestore + Storage
- **Autenticación:** PIN de 4 dígitos

---

## 🗂️ Estructura de Datos

### 1. Colección `empleados`

Almacena el catálogo de empleados con sueldos base e información IMSS.

```javascript
{
  nombre: "Ivette",
  imss: false,
  diasSemana: 6,
  sueldoSemanal: 2000,
  montoIMSS: 0,
  activo: true,
  timestamp: 1626234567890
}
```

**Campos:**
- `nombre` (string): Nombre del empleado
- `imss` (boolean): ¿Tiene seguro IMSS?
- `diasSemana` (number): Días laborales (típicamente 6)
- `sueldoSemanal` (number): Sueldo base semanal
- `montoIMSS` (number): Monto que transfiere José Manuel por IMSS
- `activo` (boolean): Si está activo en nómina
- `timestamp` (number): Fecha de creación

---

### 2. Colección `nomina_semanas`

Registro de cada nómina semanal procesada.

```javascript
{
  semana: "2026-W28",
  fechaInicio: "2026-07-07",
  fechaSabado: "2026-07-12",
  timestamp: 1626234567890,
  procesadoPor: "Viridiana",
  status: "procesada",
  
  empleados: [
    {
      nombre: "Ivette",
      empleadoId: "emp_001",
      imss: false,
      sueldoSemanal: 2000,
      faltas: 1,
      descuentoFaltas: 333.33,
      prestamo: 0,
      otrosDescuentos: 0,
      otrosDescuentosNota: "",
      bonos: 0,
      totalDescuentos: 333.33,
      netoAPagar: 1666.67,
      montoIMSS: 0,
      efectivoViri: 1666.67,
      pagado: false
    }
    // ... más empleados
  ],
  
  totalNomina: 11500.50,
  totalIMSS: 900.00,
  totalEfectivo: 10600.50,
  notas: "Observaciones generales"
}
```

**Campos principales:**
- `semana` (string): Código ISO (YYYY-Www)
- `status` (string): "borrador" → "procesada"
- `empleados` (array): Detalles de pago por empleado
- `totalNomina`: Suma de todos los netos a pagar
- `totalIMSS`: Suma de transferencias IMSS (José Manuel)
- `totalEfectivo`: Suma de efectivo que paga Viridiana

---

### 3. Colección `prestamos`

Seguimiento de préstamos activos.

```javascript
{
  empleado: "Francisco",
  montoTotal: 1000,
  montoSemanal: 200,
  saldoPendiente: 600,
  fechaInicio: "2026-07-01",
  activo: true,
  autorizadoPor: "Jose Manuel",
  notas: "Préstamo para gastos",
  timestamp: 1626234567890
}
```

**Campos:**
- `empleado` (string): Nombre del empleado
- `montoTotal`: Monto inicial del préstamo
- `montoSemanal`: Descuento semanal acordado
- `saldoPendiente`: Lo que falta pagar
- `activo` (boolean): Se marca `false` cuando `saldoPendiente <= 0`

---

### 4. Colección `salidas` (registro ampliado)

Cuando se procesa una nómina, se crea un registro de salida:

```javascript
{
  fecha: "2026-07-12",
  timestamp: 1626234567890,
  tipo: "nomina",
  tipoLabel: "👷 Pago nómina semanal",
  monto: 10600.50,
  concepto: "Nómina semana 2026-W28 — 6 empleados",
  rs: "JMG",
  rsNombre: "José Manuel Garín",
  factura: "no",
  registradoPor: "Viridiana",
  status: "aprobado",
  nominaId: "ref_a1b2c3"
}
```

---

## 🧮 Cálculos Automáticos

### Descuento por Faltas

```javascript
descuentoFaltas = (sueldoSemanal / diasSemana) * faltas
```

Ejemplo:
- Sueldo: $2000
- Días/semana: 6
- Faltas: 1
- **Descuento: (2000 / 6) × 1 = $333.33**

### Total Descuentos

```javascript
totalDescuentos = descuentoFaltas + prestamo + otrosDescuentos
```

### Neto a Pagar

```javascript
netoAPagar = sueldoSemanal - totalDescuentos + bonos
```

### Efectivo que paga Viridiana

```javascript
if (imss) {
  efectivoViri = netoAPagar - montoIMSS
} else {
  efectivoViri = netoAPagar
}

// Si el resultado es negativo (muchos descuentos):
if (efectivoViri < 0) efectivoViri = 0
```

### Totales de la Semana

```javascript
totalNomina = SUM(netoAPagar para todos)
totalIMSS = SUM(montoIMSS para empleados con IMSS)
totalEfectivo = SUM(efectivoViri para todos)
```

---

## 🔐 Control de Acceso

**Solo pueden ver/usar el módulo:**
- `role: 'Gerencia'` → Viridiana (5678)
- `role: 'Director'` → José Manuel (9900)

Los demás usuarios ven: ⚠️ "No tienes permisos para acceder a este módulo"

---

## 🔄 Flujo de Procesamiento

```
1. CONFIGURACIÓN (sub-tab 1)
   ↓
   Empleados + sueldos guardados en Firebase
   ↓
2. NUEVA NÓMINA (sub-tab 2)
   ↓
   Ingresa faltas, descuentos, bonos
   ↓
   Guarda borrador
   ↓
3. PROCESAR NÓMINA (botón ✅)
   ↓
   ├─ Actualiza nomina_semanas (status = "procesada")
   ├─ Crea registro en colección "salidas"
   ├─ Descuenta préstamos
   └─ Marca prestamoactivo = false si saldoPendiente <= 0
   ↓
4. HISTORIAL (sub-tab 4)
   ↓
   Muestra nóminas procesadas
```

---

## 📱 UI/UX

### Componentes Principales

#### Sub-Tabs de Navegación
```html
<!-- Al hacer clic, cambian entre las 4 sub-pantallas -->
⚙️ Config. Empleados | 📝 Nueva Nómina | 💳 Préstamos | 📊 Historial
```

#### Tabla de Empleados
- Editable en línea
- Cálculos en tiempo real
- Validación de rangos

#### Tabla de Nómina
- Columnas calculadas automáticamente
- Totales actualizados en vivo
- Resaltado de valores importantes (IMSS, Efectivo)

---

## 🚀 Funciones Clave

### `iniciarNomina()`
Punto de entrada. Verifica permisos y carga datos.

### `cargarEmpleados()`
Carga empleados de Firebase. Si no hay, crea seed de 6 empleados.

### `cargarNominaDeEstaSemana()`
Busca si ya existe nómina para esta semana ISO. Si no, crea una nueva.

### `crearNominaNueva()`
Inicializa nómina con empleados y sueldos actuales.

### `renderTablaEmpleados()`
Renderiza tabla HTML con inputs para faltas, descuentos, bonos.

### `procesarNomina()`
Procesa la nómina:
1. Cambia status a "procesada"
2. Crea registro en "salidas"
3. Descuenta préstamos activos
4. Marca préstamos liquidados como inactivos

### `cargarPrestamos()`
Carga préstamos activos y asigna descuentos a empleados en nómina.

### `guardarPrestamo()`
Crea nuevo préstamo en Firebase.

### `semanaISO() / lunesDeEstaSemana() / sabadoDeEstaSemana()`
Funciones de utilidad para fechas ISO 8601.

---

## 🐛 Consideraciones Técnicas

### Validaciones
- No se permite procesar nómina sin empleados configurados
- Los descuentos no pueden ser negativos
- Se valida que `montoSemanal <= montoTotal` en préstamos

### Manejo de Errores
- Toast notifications para errores
- Try/catch en llamadas Firebase
- Mensajes claros al usuario

### Rendimiento
- Carga de empleados: máximo 200 documentos
- Historial: máximo 20 registros
- Índices recomendados en Firebase:
  - `empleados`: `nombre` (asc)
  - `nomina_semanas`: `semana` (asc), `status` (asc)
  - `prestamos`: `activo` (asc)

---

## 🔌 Integración con Otros Módulos

### Con "Salidas"
Cuando procesas nómina, automáticamente se crea un registro en Salidas:
- Tipo: "nomina"
- Monto: Total Efectivo
- RS: "JMG" (José Manuel Garín)
- Status: "aprobado"

---

## 📝 Ejemplos de Datos de Prueba

```javascript
// Empleado sin IMSS
{
  nombre: "Ivette",
  imss: false,
  diasSemana: 6,
  sueldoSemanal: 2000
}

// Empleado con IMSS
{
  nombre: "Erika",
  imss: true,
  diasSemana: 6,
  sueldoSemanal: 2200,
  montoIMSS: 400
}
```

---

## 🔮 Mejoras Futuras

1. **Vista diferenciada para José Manuel**: Dashboard con solo info de IMSS
2. **Exportar nómina a PDF**: Generación de reportes
3. **Integración bancaria**: Generar archivos de transferencia
4. **Notificaciones**: SMS/WhatsApp a empleados sobre pago
5. **Control de asistencia**: Integración con módulo de asistencia
6. **Retenciones de ISR**: Cálculo automático de impuestos
7. **Múltiples formas de pago**: No solo efectivo + IMSS

---

## 📞 Soporte

Para problemas:
1. Verifica que Firebase esté conectado (green dot en header)
2. Revisa la consola del navegador (F12 → Console)
3. Asegúrate de que el usuario tenga permisos (rol Gerencia o Director)
4. Limpia caché y recarga la página

---

**Versión:** 1.0  
**Última actualización:** 2026-07-10  
**Mantenedor:** Claude Code  
