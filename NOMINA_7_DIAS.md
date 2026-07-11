# 📅 Nómina de 7 Días - Guía de Cambios

## ✅ Se ha actualizado a **nómina de 7 días**

La nómina ahora calcula descuentos y conceptos basado en **7 días de trabajo por semana**, en lugar de 6.

---

## 🧮 Cómo Cambió el Cálculo

### Antes (6 días):
```
Descuento por falta = (Sueldo / 6) × Faltas
Ejemplo: ($2000 / 6) × 1 falta = $333.33
```

### Ahora (7 días):
```
Descuento por falta = (Sueldo / 7) × Faltas
Ejemplo: ($2000 / 7) × 1 falta = $285.71
```

---

## 📊 Comparación de Descuentos

### Ejemplo: Francisco con sueldo $3,400 y 1 falta

| Días | Fórmula | Descuento |
|------|---------|-----------|
| 6 días | 3,400 ÷ 6 × 1 | **$566.67** |
| 7 días | 3,400 ÷ 7 × 1 | **$485.71** |
| Diferencia | — | **$81** menos descuento |

---

## 🔧 Cómo Funciona Ahora

### Paso 1: Configuración (Primera vez)
```
1. Ve a ⚙️ Config. Empleados
2. Todos los empleados tienen "Días/Sem" = 7 (por defecto)
3. Si alguno trabaja diferente, puedes cambiar el valor
   - Ej: Alguien que solo trabaja lunes-viernes = 5 días
   - Ej: Alguien medio tiempo = 3 días
4. Guarda
```

### Paso 2: Nómina (Cada semana)
```
1. Ve a 📝 Nueva Nómina
2. Registra faltas (número de días)
3. Sistema calcula automáticamente:
   - descuentoFaltas = (sueldoSemanal / diasSemana) × faltas
   - Para 7 días: descuentoFaltas = (sueldo / 7) × faltas
4. El resto de descuentos (Caja, Préstamo, etc.) igual que antes
```

---

## 📝 Ejemplo Completo

### Empleado: Ivette
**Configuración:**
- Sueldo: $2,000
- Días/Semana: 7
- Caja Ahorro: $100

**Nómina de esta semana:**
- Faltas: 2 días
- Otros descuentos: $0
- Bonos: $0

**Cálculo:**
```
Descuento faltas = (2,000 / 7) × 2 = $571.43
Total Descuentos = 571.43 + 100 (caja) + 0 (otros) = $671.43
Neto = 2,000 - 671.43 + 0 = $1,328.57
Efectivo = 1,328.57 (sin IMSS)
```

---

## 🎯 Casos Especiales

### ¿Qué si alguien trabaja 6 días?
```
1. Ve a ⚙️ Config. Empleados
2. En columna "Días/Sem" cambia de 7 a 6
3. Para ese empleado se calculará:
   - descuentoFaltas = (sueldo / 6) × faltas
```

### ¿Qué si alguien trabaja 5 días (lunes-viernes)?
```
1. Ve a ⚙️ Config. Empleados
2. Cambia a 5
3. Descuentos se calcularán sobre 5 días
```

### ¿Qué si tiene jornada especial?
```
- Puedes ajustar el valor en Config. para cada empleado
- El sistema es flexible y usa el valor de cada uno
```

---

## 🔄 Impacto en Cálculos

### Total Descuentos (Fórmula Completa)
```
TotalDescuentos = DescFaltas + PrestamoSemanal + PrestamoFijo + CajaAhorro + OtrosDescuentos

Donde:
DescFaltas = (sueldoSemanal / diasSemana) × faltas

Para 7 días:
DescFaltas = (sueldoSemanal / 7) × faltas
```

### Ejemplo Completo: Carlos

```
Datos:
- Sueldo: $3,200
- Días: 7
- Caja: $100
- Prest. Fijo: $200
- Faltas esta semana: 1

Cálculo:
DescFaltas = (3,200 / 7) × 1 = $457.14
TotalDesc = 457.14 + 0 + 200 + 100 + 0 = $757.14
Neto = 3,200 - 757.14 + 0 = $2,442.86
```

---

## ✅ Verificar en el CRM

### Quick Test:
```
1. Abre http://localhost:8000/index.html
2. PIN: 5678
3. 👷 Nómina → ⚙️ Config. Empleados
4. Verifica que todos muestren "7" en columna "Días/Sem"
5. 📝 Nueva Nómina
6. Registra 1 falta para Ivette ($2000 sueldo)
7. Verifica: Desc. Faltas = $285.71 (2000/7 = 285.71)
8. ✅ Correcto
```

---

## 📊 Comparación: 6 días vs 7 días

### Escenario: Todos con sueldo promedio $2,500 y 1 falta

| Empleado | Días | Desc. Faltas | Diferencia |
|----------|------|--------------|-----------|
| Ivette | 7 | $357.14 | — |
| Francisco | 7 | $357.14 | — |
| Carlos | 7 | $357.14 | — |
| **Total semana (6 empleados) con 1 falta c/u** | | | |
| Con 6 días | 6 | $2,500.00 | **Más alto** |
| Con 7 días | 7 | $2,142.86 | **Más bajo** |
| Ahorro semanal | — | — | **$357.14** |

---

## 🔐 ¿Por qué 7 días?

En México, la ley laboral considera:
- Semana = 7 días naturales
- Descanso semanal = 1 día (generalmente domingo)
- Jornada máxima = 8 horas/día
- Semana laboral = Lunes a Domingo (7 días disponibles)

Aunque muchos trabajan 6 días (lunes-sábado) o menos, el cálculo de proporcionales debe basarse en 7 días como referencia.

---

## 🛠️ Cómo Cambiar si Necesitas

### Si necesitas volver a 6 días:

1. **Opción 1: Cambiar por empleado**
   - ⚙️ Config. Empleados
   - Cada empleado puede tener diferente valor

2. **Opción 2: Cambiar por defecto (todos a la vez)**
   - Editar `index.html`
   - Buscar: `diasSemana: 7`
   - Cambiar a: `diasSemana: 6`

---

## 📝 Impacto en Documentación

Todos los ejemplos en la documentación ahora usan:
```
Descuento = (sueldo / 7) × faltas
```

En lugar de:
```
Descuento = (sueldo / 6) × faltas
```

---

## ✨ Ventajas de 7 Días

✅ Correcto según ley laboral mexicana  
✅ Flexible: cada empleado puede tener diferente valor  
✅ Preciso: descuentos proporcionales correctos  
✅ Auditable: se guarda el valor de días en Firebase  
✅ Justo: menor castigo por faltas (285 vs 333 en ejemplo)

---

## 🎯 Resumen Rápido

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| Días semana | 6 (fijo) | 7 (configurable) |
| Descuento/falta | $333.33 ($2000) | $285.71 ($2000) |
| Flexibilidad | No | Sí, por empleado |
| Cálculo | Hardcodeado | Dinámico |
| Legal | Aproximado | Correcto |

---

## 🧪 Ejercicio de Verificación

**Datos de prueba:**
```
Empleado: Agustín
Sueldo: $2,900
Faltas: 1
Días: 7
```

**Cálculo esperado:**
```
Desc. Faltas = 2,900 ÷ 7 × 1 = $414.29
```

**Verificación:**
1. Ingresa datos en Nueva Nómina
2. Verifica que muestre $414.29
3. ✅ Correcto

---

**¡La nómina ya es de 7 días! 🎉**

Todos los cálculos ahora son:
```
descuentoFaltas = (sueldoSemanal / 7) × faltas
```

¿Necesitas cambiar algún empleado a diferente cantidad de días?
