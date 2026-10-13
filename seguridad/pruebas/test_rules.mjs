// Pruebas de las reglas de Firestore y Storage contra el emulador (no toca producción).
// Correr:  cd seguridad/pruebas && npm install && npm test   (necesita Java y firebase-tools)
import fs from 'fs';
import { fileURLToPath } from 'url';
import { initializeTestEnvironment, assertSucceeds, assertFails } from '@firebase/rules-unit-testing';
import { setLogLevel, doc, getDoc, getDocs, setDoc, updateDoc, addDoc, collection, deleteDoc, writeBatch } from 'firebase/firestore';
import { ref, uploadString, getBytes } from 'firebase/storage';

const DOM = '@troncoso-crm.com';
const STAFF = ['ivette', 'erika', 'francisco', 'agustin', 'carlos', 'viridiana', 'josemanuel', 'taller'];
const ADMIN = ['josemanuel', 'viridiana'];

const aqui = fileURLToPath(new URL('.', import.meta.url));
const htmlSrc = fs.readFileSync(aqui + '../../index.html', 'utf8');
const reglasFS = fs.readFileSync(aqui + '../firestore.rules', 'utf8');
const reglasST = fs.readFileSync(aqui + '../storage.rules', 'utf8');

setLogLevel('silent');
let ok = 0, mal = 0;
function chk(nombre, cond, extra) {
  if (cond) { ok++; } else { mal++; console.log('  ✗ FALLÓ:', nombre, extra || ''); }
}
async function pasa(nombre, p) { try { await assertSucceeds(p); ok++; } catch (e) { mal++; console.log('  ✗ DEBÍA PASAR:', nombre, '→', String(e.message || e).slice(0, 140)); } }
async function falla(nombre, p) { try { await assertFails(p); ok++; } catch (e) { mal++; console.log('  ✗ DEBÍA FALLAR:', nombre); } }

const env = await initializeTestEnvironment({
  projectId: 'demo-troncoso',
  firestore: { rules: reglasFS, host: '127.0.0.1', port: 8080 },
  storage: { rules: reglasST, host: '127.0.0.1', port: 9199 }
});

const ctxStaff = (n) => env.authenticatedContext('uid-' + n, { email: n + DOM, firebase: { sign_in_provider: 'password' } });
const ctxAnon = () => env.authenticatedContext('uid-anon', { firebase: { sign_in_provider: 'anonymous' } });
const ctxIntruso = () => env.authenticatedContext('uid-hack', { email: 'hacker@gmail.com', firebase: { sign_in_provider: 'password' } });
const ctxIntrusoCasi = () => env.authenticatedContext('uid-hack2', { email: 'ivette@otrodominio.com', firebase: { sign_in_provider: 'password' } });
const ctxSinEmail = () => env.authenticatedContext('uid-x', { firebase: { sign_in_provider: 'password' } });
const ctxSinSesion = () => env.unauthenticatedContext();

// ── 0. Todas las colecciones que usa el CRM están declaradas en las reglas ──
const usadas = new Set();
for (const m of htmlSrc.matchAll(/collection\('([^']+)'\)/g)) usadas.add(m[1]);
['cotizaciones', 'pedidos', 'tickets'].forEach(c => usadas.add(c));
const declaradas = new Set([...reglasFS.matchAll(/match \/([a-z_]+)\/\{/g)].map(m => m[1]));
console.log('Colecciones que usa index.html:', usadas.size, '· declaradas en reglas:', declaradas.size);
for (const c of usadas) chk('colección sin regla: ' + c, declaradas.has(c));

// sembrar datos como administrador del emulador (se salta las reglas)
await env.withSecurityRulesDisabled(async (ctx) => {
  const d = ctx.firestore();
  for (const c of declaradas) await setDoc(doc(d, c, 'semilla'), { x: 1, nombre: 'dato de prueba' });
  await setDoc(doc(d, 'fondeos', 'FONDEO_PENDIENTE_ABC123'), { folio: 'FND-001', status: 'pendiente', tokenUsado: false, tokenAprobacion: 'tok', monto: 500, motivo: 'prueba', whatsappViriEnviado: false });
  await setDoc(doc(d, 'fondeos', 'FONDEO_PENDIENTE_2'), { folio: 'FND-002', status: 'pendiente', tokenUsado: false, tokenAprobacion: 'tok2', monto: 700, motivo: 'prueba' });
  await setDoc(doc(d, 'fondeos', 'FONDEO_YA_APROBADO'), { folio: 'FND-003', status: 'aprobado', tokenUsado: true, monto: 900 });
});

// ── 1. Quienes NO deben entrar: nada de nada ──
console.log('\n1) Intrusos (sin sesión, anónimo, correo ajeno, sin correo)');
const intrusos = { sinSesion: ctxSinSesion(), anonimo: ctxAnon(), correoAjeno: ctxIntruso(), dominioParecido: ctxIntrusoCasi(), sinCorreo: ctxSinEmail() };
const sensibles = ['clientes', 'pedidos', 'nomina_semanas', 'empleados', 'prestamos', 'razones_sociales', 'salidas', 'cuentas_cobrar', 'cotizaciones', 'permisos_roles', 'config_contactos', 'productos', 'tickets', 'alertas'];
for (const [quien, ctx] of Object.entries(intrusos)) {
  const d = ctx.firestore();
  for (const c of sensibles) {
    await falla(quien + ' lee ' + c, getDoc(doc(d, c, 'semilla')));
    await falla(quien + ' lista ' + c, getDocs(collection(d, c)));
    await falla(quien + ' escribe ' + c, setDoc(doc(d, c, 'nuevo'), { x: 1 }));
    await falla(quien + ' borra ' + c, deleteDoc(doc(d, c, 'semilla')));
  }
  await falla(quien + ' lista fondeos', getDocs(collection(d, 'fondeos')));
  await falla(quien + ' lista encuestas', getDocs(collection(d, 'encuestas')));
  await falla(quien + ' lee encuesta', getDoc(doc(d, 'encuestas', 'semilla')));
  await falla(quien + ' lista encuestas_respondidas', getDocs(collection(d, 'encuestas_respondidas')));
}

// ── 2. Personal: trabaja normal ──
console.log('\n2) Personal con cuenta');
for (const n of STAFF) {
  const d = ctxStaff(n).firestore();
  for (const c of ['clientes', 'pedidos', 'salidas', 'cotizaciones', 'productos', 'fondeos', 'alertas', 'encuestas', 'kilometraje']) {
    await pasa(n + ' lee ' + c, getDoc(doc(d, c, 'semilla')));
    await pasa(n + ' lista ' + c, getDocs(collection(d, c)));
  }
  await pasa(n + ' escribe pedidos', setDoc(doc(d, 'pedidos', 'p_' + n), { id: 'NV-1', cliente: 'x' }));
  await pasa(n + ' actualiza pedidos', updateDoc(doc(d, 'pedidos', 'p_' + n), { estado: 'entregado' }));
  await pasa(n + ' lee razones_sociales', getDoc(doc(d, 'razones_sociales', 'semilla')));
  await pasa(n + ' lee permisos_roles', getDoc(doc(d, 'permisos_roles', 'semilla')));
  await pasa(n + ' lee config_contactos', getDoc(doc(d, 'config_contactos', 'semilla')));
}

// ── 3. Solo Director y Gerencia ──
console.log('\n3) Nómina / empleados / préstamos / razones / permisos solo para Director y Gerencia');
for (const n of STAFF) {
  const d = ctxStaff(n).firestore();
  const esAdm = ADMIN.includes(n);
  for (const c of ['nomina_semanas', 'empleados', 'prestamos']) {
    const leer = () => getDoc(doc(d, c, 'semilla'));
    const escribir = () => setDoc(doc(d, c, 'w_' + n), { x: 1 });
    if (esAdm) { await pasa(n + ' lee ' + c, leer()); await pasa(n + ' escribe ' + c, escribir()); }
    else { await falla(n + ' lee ' + c, leer()); await falla(n + ' escribe ' + c, escribir()); }
  }
  for (const c of ['razones_sociales', 'permisos_roles', 'config_contactos']) {
    const escribir = () => setDoc(doc(d, c, 'w_' + n), { x: 1 });
    if (esAdm) await pasa(n + ' escribe ' + c, escribir()); else await falla(n + ' escribe ' + c, escribir());
  }
}

// ── 4. Link mágico de fondeos (sin sesión) ──
console.log('\n4) Link de WhatsApp de fondeos');
{
  const d = ctxSinSesion().firestore();
  await pasa('abre UN fondeo por id', getDoc(doc(d, 'fondeos', 'FONDEO_PENDIENTE_ABC123')));
  await falla('no lista fondeos', getDocs(collection(d, 'fondeos')));
  await falla('no consulta por folio', getDocs(collection(d, 'fondeos'), ));
  await falla('no cambia el monto', updateDoc(doc(d, 'fondeos', 'FONDEO_PENDIENTE_ABC123'), { monto: 9999999 }));
  await falla('no aprueba y cambia monto a la vez', updateDoc(doc(d, 'fondeos', 'FONDEO_PENDIENTE_ABC123'), { status: 'aprobado', tokenUsado: true, monto: 1 }));
  await falla('no se salta tokenUsado', updateDoc(doc(d, 'fondeos', 'FONDEO_PENDIENTE_ABC123'), { status: 'aprobado' }));
  await falla('no pone estado raro', updateDoc(doc(d, 'fondeos', 'FONDEO_PENDIENTE_ABC123'), { status: 'cancelado', tokenUsado: true }));
  await falla('no crea fondeos', setDoc(doc(d, 'fondeos', 'inventado'), { status: 'pendiente' }));
  await falla('no borra fondeos', deleteDoc(doc(d, 'fondeos', 'FONDEO_PENDIENTE_ABC123')));
  await pasa('aprueba el fondeo pendiente', updateDoc(doc(d, 'fondeos', 'FONDEO_PENDIENTE_ABC123'), { status: 'aprobado', aprobadoPor: 'Jose Manuel', timestampAprobacion: 1, tokenUsado: true, motivoRechazo: null }));
  await falla('no vuelve a procesar el mismo', updateDoc(doc(d, 'fondeos', 'FONDEO_PENDIENTE_ABC123'), { status: 'rechazado', tokenUsado: true }));
  await pasa('marca aviso a Viri enviado', updateDoc(doc(d, 'fondeos', 'FONDEO_PENDIENTE_ABC123'), { whatsappViriEnviado: true }));
  await falla('fondeo ya aprobado no se reabre', updateDoc(doc(d, 'fondeos', 'FONDEO_YA_APROBADO'), { status: 'rechazado', tokenUsado: true }));
  await pasa('rechaza el otro pendiente', updateDoc(doc(d, 'fondeos', 'FONDEO_PENDIENTE_2'), { status: 'rechazado', aprobadoPor: 'Jose Manuel', timestampAprobacion: 2, tokenUsado: true, motivoRechazo: 'no' }));
}

// ── 5. Encuesta del cliente (sin sesión) ──
console.log('\n5) Encuesta post-entrega');
{
  const d = ctxSinSesion().firestore();
  const buena = { pedidoId: 'NV-0123', cliente: 'Juan', fecha: '2026-10-12', timestamp: Date.now(), 'llegóATiempo': true, productosCorrectos: true, cantidadesCorrectas: true, descargaSinDanos: false, atencionBuena: true, comentarios: 'todo bien', puntuacion: 4, 'dejóResena': false };
  await pasa('crea encuesta válida', addDoc(collection(d, 'encuestas'), buena));
  await pasa('crea encuesta con respuestas sin contestar (null)', addDoc(collection(d, 'encuestas'), Object.assign({}, buena, { 'llegóATiempo': null })));
  await falla('encuesta con campo extra', addDoc(collection(d, 'encuestas'), Object.assign({}, buena, { admin: true })));
  await falla('encuesta con dejóResena true', addDoc(collection(d, 'encuestas'), Object.assign({}, buena, { 'dejóResena': true })));
  await falla('encuesta con comentario enorme', addDoc(collection(d, 'encuestas'), Object.assign({}, buena, { comentarios: 'x'.repeat(5000) })));
  await falla('encuesta sin pedidoId', addDoc(collection(d, 'encuestas'), Object.assign({}, buena, { pedidoId: '' })));
  await falla('no lee encuestas', getDocs(collection(d, 'encuestas')));
  await falla('no edita encuestas', updateDoc(doc(d, 'encuestas', 'semilla'), { puntuacion: 5 }));
  await falla('no borra encuestas', deleteDoc(doc(d, 'encuestas', 'semilla')));
  await pasa('pregunta si el folio ya respondió', getDoc(doc(d, 'encuestas_respondidas', 'NV-0123')));
  await pasa('marca el folio respondido', setDoc(doc(d, 'encuestas_respondidas', 'NV-0123'), { pedidoId: 'NV-0123', timestamp: 1 }));
  await falla('no marca un folio con otro id', setDoc(doc(d, 'encuestas_respondidas', 'NV-9999'), { pedidoId: 'NV-0000', timestamp: 1 }));
  await falla('no mete campos de más en la marca', setDoc(doc(d, 'encuestas_respondidas', 'NV-8888'), { pedidoId: 'NV-8888', timestamp: 1, admin: true }));
  await falla('no reescribe la marca', setDoc(doc(d, 'encuestas_respondidas', 'NV-0123'), { pedidoId: 'NV-0123', timestamp: 2 }));
  await pasa('lote: encuesta + marca juntas (como lo hará la página)', (async () => {
    const b = writeBatch(d);
    b.set(doc(collection(d, 'encuestas')), Object.assign({}, buena, { pedidoId: 'NV-5555' }));
    b.set(doc(d, 'encuestas_respondidas', 'NV-5555'), { pedidoId: 'NV-5555', timestamp: 3 });
    await b.commit();
  })());
  const st = ctxStaff('josemanuel').firestore();
  await pasa('el CRM lee encuestas por fecha', getDocs(collection(st, 'encuestas')));
}

// ── 6. Storage ──
console.log('\n6) Storage (constancias fiscales)');
{
  const pdf = 'JVBERi0xLjQK';
  const s = (ctx) => ctx.storage();
  await pasa('Ivette sube constancia de cliente', uploadString(ref(s(ctxStaff('ivette')), 'fiscal/clientes/c1/csf.pdf'), pdf, 'base64'));
  await pasa('Erika lee constancia de cliente', getBytes(ref(s(ctxStaff('erika')), 'fiscal/clientes/c1/csf.pdf')));
  await falla('Ivette NO sube a razones_sociales', uploadString(ref(s(ctxStaff('ivette')), 'fiscal/razones_sociales/JMG/csf.pdf'), pdf, 'base64'));
  await pasa('Viri sube a razones_sociales', uploadString(ref(s(ctxStaff('viridiana')), 'fiscal/razones_sociales/JMG/csf.pdf'), pdf, 'base64'));
  await pasa('Ivette lee razones_sociales', getBytes(ref(s(ctxStaff('ivette')), 'fiscal/razones_sociales/JMG/csf.pdf')));
  for (const [q, ctx] of Object.entries(intrusos)) {
    await falla(q + ' lee constancia cliente', getBytes(ref(s(ctx), 'fiscal/clientes/c1/csf.pdf')));
    await falla(q + ' lee razones_sociales', getBytes(ref(s(ctx), 'fiscal/razones_sociales/JMG/csf.pdf')));
    await falla(q + ' sube archivo', uploadString(ref(s(ctx), 'fiscal/clientes/c1/hack.pdf'), pdf, 'base64'));
    await falla(q + ' sube en ruta libre', uploadString(ref(s(ctx), 'cualquier/cosa.txt'), 'hola'));
  }
  await falla('personal no sube en ruta no declarada', uploadString(ref(s(ctxStaff('josemanuel')), 'otra/cosa.txt'), 'hola'));
}

await env.cleanup();
console.log('\nRESULTADO: ' + ok + ' pruebas correctas · ' + mal + ' fallidas');
process.exit(mal ? 1 : 0);
