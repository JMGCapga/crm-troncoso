# ✨ Nuevos Campos Agregados a Nómina Semanal

Se han agregado **5 nuevos campos** basados en tu archivo Excel "Resumen de Nómina".

---

## 📋 Nuevos Campos por Sección

### 1️⃣ En Configuración de Empleados

#### **CAJA DE AHORRO** 💰
- **Qué es:** Descuento semanal fijo que el empleado autoriza para ahorrar
- **Ejemplo:** $100 por semana
- **Cómo usar:**
  1. Ve a "⚙️ Config. Empleados"
  2. Ingresa el monto en la columna "Caja Ahorro"
  3. Se aplicará automáticamente cada semana

#### **PREST. FIJO** 🏦
- **Qué es:** Préstamo fijo de la empresa, diferente de préstamos puntuales
- **Ejemplo:** $200 por semana (distinto a "Préstamo Semanal variable")
- **Cómo usar:**
  1. Ve a "⚙️ Config. Empleados"
  2. Ingresa el monto en la columna "Prest. Fijo"
  3. Se descuenta automáticamente cada nómina

---

### 2️⃣ En Nueva Nómina (Tabla de Detalle)

#### **PAGO VIA TRANSFERENCIA** 🏧
- **Qué es:** Opción de pagar al empleado por transferencia bancaria en lugar de efectivo
- **Ejemplo:** $500 por transferencia
- **Cómo usar:**
  1. Ve a "📝 Nueva Nómina"
  2. En la columna "Transferencia", ingresa el monto a transferir
  3. El resto se paga en efectivo
  4. **Nota:** Suma de efectivo + transferencia = neto total

#### **OBSERVACIONES** 📝
- **Qué es:** Campo libre para notas sobre ese empleado en esa nómina
- **Ejemplos:**
  - "Falta justificada - médico"
  - "Bono performance $500"
  - "Retrasó entrega de documento"
  - "IMSS pagado por separado"
- **Cómo usar:**
  1. Haz clic en la columna "Observ." de cada empleado
  2. Escribe tu nota
  3. Se guarda automático

#### **TOTAL DESCUENTOS** (Nueva columna calculada)
- **Qué es:** Suma visible de todos los descuentos
- **Incluye:**
  - Descuento por faltas
  - Préstamo semanal (variable)
  - Préstamo fijo
  - Caja de ahorro
  - Otros descuentos
- **Cómo leerla:** Información, no se edita

---

## 🧮 Fórmula de Cálculo Actualizada

### Antes:
```
Neto = Sueldo - (DescFaltas + Préstamo + OtrosDesc) + Bonos
```

### Ahora:
```
TotalDescuentos = DescFaltas + PrestamoSemanal + PrestamoFijo + CajaAhorro + OtrosDescuentos
Neto = Sueldo - TotalDescuentos + Bonos
Efectivo = Neto - IMSS - TransferenciaABancaria
```

---

## 📊 Ejemplo Completo

### Empleado: Francisco Escobar

**Configuración:**
- Sueldo semanal: $3,400
- IMSS: $0
- Caja Ahorro: $100 (cada semana)
- Prest. Fijo: $200 (cada semana)

**Nómina de esta semana:**
- Faltas: 0
- Desc. Faltas: $0
- Prest. Semanal: $500 (préstamo adicional)
- Prest. Fijo: $200 (automático)
- Caja Ahorro: $100 (automático)
- Otros Desc: $0
- Bonos: $0

**Cálculo:**
```
Total Descuentos = 0 + 500 + 200 + 100 + 0 = $800
Neto = 3,400 - 800 + 0 = $2,600
Efectivo = 2,600 (sin IMSS)
Transferencia: $0 (todo en efectivo)
```

---

## 🔄 Diferencia: Préstamo Semanal vs Préstamo Fijo

### Préstamo Semanal (Variable) 📋
- **Dónde:** Tab "💳 Préstamos" (crear nuevo)
- **Cantidad:** Única al momento
- **Descuento:** Se aplicaautomáticamente en nómina
- **Seguimiento:** Barra de progreso de liquidación
- **Fin:** Cuando saldo = $0

### Préstamo Fijo 🏢
- **Dónde:** "⚙️ Config. Empleados"
- **Cantidad:** Permanente por empleado
- **Descuento:** Automático cada semana
- **Seguimiento:** Se aplica sin control de saldo
- **Fin:** Cuando cambies el monto a $0

**Ejemplo de uso combinado:**
- Francisco tiene préstamo fijo de $200/semana (de la empresa)
- Francisco solicita préstamo adicional de $1,000 (variable)
  - Descuento: $200 fijo + $500 semanal = $700 total
  - Cuando liquida el adicional, quedan solo los $200 fijos

---

## 📱 Cómo Usar los Nuevos Campos

### Paso 1: Configurar Valores Fijos (Primera vez)
```
1. Ve a "⚙️ Config. Empleados"
2. Para cada empleado, ingresa:
   - Caja Ahorro (si aplica): $100
   - Prest. Fijo (si aplica): $200
3. Clic "💾 Guardar Configuración"
```

### Paso 2: Crear Nómina (Cada semana)
```
1. Ve a "📝 Nueva Nómina"
2. Para cada empleado:
   - Registra faltas si las hay
   - Los descuentos fijos se cargan automático
   - Si hay pago por transferencia, ingresa monto
   - Si hay observación especial, escribe en "Observ."
3. Verifica Total Descuentos (suma visible)
4. Revisa Neto y Efectivo
```

### Paso 3: Procesar
```
1. Haz clic "✅ PROCESAR NÓMINA"
2. Se guarda todo (incluyendo observaciones)
3. Se crea registro en Salidas
4. Los préstamos se descargan automático
```

---

## 🧮 Ejercicios Prácticos

### Ejercicio 1: Francisco con Caja Ahorro
**Datos:**
- Sueldo: $3,200
- Caja Ahorro configurada: $150
- Esta semana: 0 faltas, 0 bonos

**Resultado esperado:**
```
Total Desc = Desc_Faltas(0) + Prest_Sem(0) + Prest_Fijo(0) + Caja(150) + Otros(0) = $150
Neto = 3,200 - 150 + 0 = $3,050
```

### Ejercicio 2: Agustín con Múltiples Descuentos
**Datos:**
- Sueldo: $2,900
- Caja Ahorro: $100 (configurada)
- Prest. Fijo: $200 (configurado)
- Esta semana: 1 falta (6 días laborales)
- Otros descuentos: $50
- Bonos: $200

**Cálculo:**
```
Desc_Faltas = (2,900 / 6) × 1 = $483.33
Total Desc = 483.33 + 0 + 200 + 100 + 50 = $833.33
Neto = 2,900 - 833.33 + 200 = $2,266.67
```

---

## 💾 Dónde se Guardan los Datos

### Firebase Collection `empleados`
```json
{
  "nombre": "Francisco",
  "sueldoSemanal": 3400,
  "cajaAhorro": 100,
  "prestamoFijo": 200,
  "imss": false,
  "montoIMSS": 0
}
```

### Firebase Collection `nomina_semanas`
```json
{
  "empleados": [
    {
      "nombre": "Francisco",
      "cajaAhorro": 100,
      "prestamoFijo": 200,
      "prestamoSemanal": 500,
      "pagoTransferencia": 500,
      "observaciones": "Falta justificada - médico",
      "totalDescuentos": 1300,
      "netoAPagar": 2100
    }
  ]
}
```

---

## ✅ Verificar que Funciona

1. **Ingresa Caja Ahorro para un empleado:**
   - Ve a Config. Empleados
   - Coloca $100 en "Caja Ahorro" para Ivette
   - Guarda

2. **Crea nueva nómina:**
   - Ve a "📝 Nueva Nómina"
   - En la tabla de Ivette, verifica:
     - Caja Ahorro: $100 (automático)
     - Total Descuentos: incluye $100

3. **Escribe observación:**
   - En la columna "Observ." de Ivette
   - Escribe "Test de caja ahorro"
   - Verifica que se guarde al salir del campo

4. **Procesa nómina:**
   - Haz clic "✅ PROCESAR NÓMINA"
   - Entra en Firebase Console
   - Ve a `nomina_semanas` → último documento
   - Verifica que contenga `cajaAhorro`, `observaciones`, etc.

---

## 🎯 Resumen de Cambios

| Campo | Anterior | Ahora |
|-------|----------|-------|
| Config empleados | 4 columnas | 6 columnas |
| Tabla nómina | 10 columnas | 15 columnas |
| Descuentos incluidos | 3 tipos | 5 tipos |
| Datos guardados | Básicos | + observaciones |
| Opciones pago | Efectivo | Efectivo + Transferencia |

---

## 🚀 Próximas Mejoras Sugeridas

1. ✅ (Hecho) Caja de ahorro y préstamo fijo
2. ✅ (Hecho) Observaciones por empleado
3. ✅ (Hecho) Pago por transferencia
4. ⏳ (Futuro) Reportes desagregados (caja ahorro total, etc.)
5. ⏳ (Futuro) Control de liquidación de caja
6. ⏳ (Futuro) Comparativo con archivo Excel

---

**¡Los nuevos campos están listos para usar! 🎉**

Próximo paso: Prueba con los datos de tu Excel para verificar que los resultados coincidan.
