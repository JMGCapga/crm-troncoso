#!/usr/bin/env python3
"""Crea las cuentas de Firebase del personal (correo interno + PIN al azar) y, opcionalmente,
guarda los teléfonos en Firestore (config_contactos/staff).

Uso:
  python3 seguridad/cuentas.py crear todas
  python3 seguridad/cuentas.py crear erika ivette
  python3 seguridad/cuentas.py crear todas --contactos /ruta/contactos.json   (teléfonos; NO subir ese archivo a git)
  agregar --emulador para probar contra el emulador local sin tocar producción

Los PIN se imprimen UNA vez en pantalla y no se guardan en ningún lado.
Reiniciar el PIN de alguien que lo olvidó: borrar su usuario en la Consola de Firebase
(Authentication > Users) y volver a correr "crear <nombre>" (genera un PIN nuevo).
Solo usa la apiKey pública que ya está en index.html; las reglas son las que protegen los datos.
"""
import json, re, secrets, sys, urllib.request, urllib.error, pathlib

DOMINIO = '@troncoso-crm.com'
# nombre -> longitud del PIN (Director y Gerencia: 8 dígitos)
PERSONAL = {'ivette': 6, 'erika': 6, 'francisco': 6, 'agustin': 6, 'carlos': 6,
            'viridiana': 8, 'josemanuel': 8, 'taller': 6}
ADMIN_CONTACTOS = 'josemanuel'   # con esta cuenta se escribe config_contactos (solo Director/Gerencia pueden)

AQUI = pathlib.Path(__file__).resolve().parent
API_KEY = re.search(r'apiKey:\s*"([^"]+)"', (AQUI.parent / 'index.html').read_text(encoding='utf-8')).group(1)


def pin_debil(p):
    if len(set(p)) <= 2:
        return True
    asc, desc = '01234567890123456789', '98765432109876543210'
    for i in range(len(p) - 3):                       # tramos de 4 seguidos: 1234, 4321
        if p[i:i + 4] in asc or p[i:i + 4] in desc:
            return True
    return p[:len(p) // 2] == p[len(p) // 2:]         # 123123


def pin_nuevo(largo):
    while True:
        p = ''.join(secrets.choice('0123456789') for _ in range(largo))
        if not pin_debil(p):
            return p


def post(url, cuerpo, token=None, metodo='POST'):
    datos = json.dumps(cuerpo).encode('utf-8')
    req = urllib.request.Request(url, data=datos, method=metodo, headers={'Content-Type': 'application/json'})
    if token:
        req.add_header('Authorization', 'Bearer ' + token)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode('utf-8') or '{}')
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode('utf-8'))
        except Exception:
            return e.code, {}


def main():
    args = sys.argv[1:]
    emulador = '--emulador' in args
    contactos = None
    if '--contactos' in args:
        contactos = json.loads(pathlib.Path(args[args.index('--contactos') + 1]).read_text(encoding='utf-8'))
    pos = [a for a in args if not a.startswith('--') and (not contactos or a != args[args.index('--contactos') + 1])]
    if len(pos) < 2 or pos[0] != 'crear':
        print(__doc__); sys.exit(1)
    nombres = list(PERSONAL) if pos[1] == 'todas' else pos[1:]
    for n in nombres:
        if n not in PERSONAL:
            print('Nombre desconocido:', n, '· válidos:', ', '.join(PERSONAL)); sys.exit(1)

    if emulador:
        auth = 'http://127.0.0.1:9099/identitytoolkit.googleapis.com/v1/accounts:%s?key=fake'
        fs = 'http://127.0.0.1:8080/v1/projects/demo-troncoso/databases/(default)/documents/config_contactos/staff'
    else:
        auth = 'https://identitytoolkit.googleapis.com/v1/accounts:%s?key=' + API_KEY
        fs = 'https://firestore.googleapis.com/v1/projects/troncoso--sistema/databases/(default)/documents/config_contactos/staff'

    print('Destino:', 'EMULADOR (prueba)' if emulador else 'PRODUCCIÓN')
    nuevos = {}
    for n in nombres:
        pin = pin_nuevo(PERSONAL[n])
        st, j = post(auth % 'signUp', {'email': n + DOMINIO, 'password': pin, 'returnSecureToken': False})
        if st == 200:
            nuevos[n] = pin
            print('  creada  %-11s PIN %s' % (n, pin))
        else:
            msg = (j.get('error') or {}).get('message', str(st))
            if msg == 'EMAIL_EXISTS':
                print('  YA EXISTE %-9s (para reiniciar su PIN: borrar el usuario en la Consola y volver a crear)' % n)
            elif msg == 'OPERATION_NOT_ALLOWED':
                print('  ERROR: falta activar "Correo electrónico/contraseña" en Firebase > Authentication > Método de acceso'); sys.exit(2)
            else:
                print('  ERROR con', n, '->', msg)

    if contactos:
        if ADMIN_CONTACTOS not in nuevos:
            print('Para guardar teléfonos hay que crear josemanuel en esta misma corrida (su PIN abre la sesión).')
        else:
            st, j = post(auth % 'signInWithPassword', {'email': ADMIN_CONTACTOS + DOMINIO, 'password': nuevos[ADMIN_CONTACTOS], 'returnSecureToken': True})
            token = j.get('idToken')
            campos = {k: {'stringValue': str(v)} for k, v in contactos.items()}
            st, j = post(fs, {'fields': campos}, token=token, metodo='PATCH')
            print('  teléfonos guardados en config_contactos/staff' if st == 200 else '  ERROR guardando teléfonos: %s %s' % (st, j))
    print('\nListo. Entrega cada PIN en persona o por mensaje directo; no se vuelve a mostrar.')


if __name__ == '__main__':
    main()
