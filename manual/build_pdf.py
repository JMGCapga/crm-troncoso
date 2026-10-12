#!/usr/bin/env python3
"""Genera el PDF de un manual a partir de manual/<depto>.json y sus capturas.

Uso:   python3 manual/build_pdf.py ventas
Salida: manual/Manual-Ventas.pdf

El mismo JSON alimenta la pestaña "📖 Manual" del CRM: se edita el JSON y se
regeneran las dos versiones. Requiere:  pip install reportlab
"""
import json
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, Image, KeepTogether, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

AQUI = os.path.dirname(os.path.abspath(__file__))
NARANJA = colors.HexColor('#E8500A')
OSCURO = colors.HexColor('#1A1A1A')
GRIS = colors.HexColor('#6B6560')
CREMA = colors.HexColor('#F5F2EE')
AMARILLO = colors.HexColor('#FFF6E5')


def limpio(txt):
    """Helvetica solo trae el juego de caracteres de Windows (cp1252): se quitan emojis y se cambian las flechas."""
    txt = txt.replace('→', '>').replace('←', '<').replace('✓', 'v').replace('✂', '').replace('−', '-')   # el signo menos matemático no existe en Helvetica
    return ''.join(c for c in txt if ord(c) < 0x10000 and _cp1252(c)).strip()


def _cp1252(c):
    try:
        c.encode('cp1252')
        return True
    except UnicodeEncodeError:
        return False


def marcado(txt):
    """Escapa XML y convierte **negritas** a <b>."""
    t = limpio(txt).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)


EST = {
    'portada_t': ParagraphStyle('portada_t', fontName='Helvetica-Bold', fontSize=34, leading=38, textColor=OSCURO),
    'portada_s': ParagraphStyle('portada_s', fontName='Helvetica', fontSize=14, leading=18, textColor=GRIS),
    'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=17, leading=21, textColor=NARANJA, spaceBefore=6, spaceAfter=4),
    'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=OSCURO, spaceBefore=8, spaceAfter=4),
    'cuerpo': ParagraphStyle('cuerpo', fontName='Helvetica', fontSize=10.5, leading=14.5, textColor=OSCURO, alignment=TA_LEFT),
    'cuando': ParagraphStyle('cuando', fontName='Helvetica-Oblique', fontSize=10, leading=13, textColor=GRIS, spaceAfter=6, keepWithNext=1),
    'leyenda': ParagraphStyle('leyenda', fontName='Helvetica', fontSize=8.5, leading=11, textColor=GRIS, spaceAfter=8),
    'caja': ParagraphStyle('caja', fontName='Helvetica', fontSize=10, leading=13.5, textColor=OSCURO),
    'toc1': ParagraphStyle('toc1', fontName='Helvetica', fontSize=11, leading=17, textColor=OSCURO),
}


class Doc(BaseDocTemplate):
    def __init__(self, ruta, titulo, **kw):
        super().__init__(ruta, pagesize=letter, leftMargin=2 * cm, rightMargin=2 * cm,
                         topMargin=2 * cm, bottomMargin=2 * cm, title=titulo, author='Materiales Troncoso', **kw)
        self.titulo_pie = titulo
        marco = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='f')
        self.addPageTemplates([PageTemplate(id='p', frames=[marco], onPage=self._pie)])

    def _pie(self, canv, doc):
        canv.saveState()
        canv.setStrokeColor(NARANJA)
        canv.setLineWidth(1.2)
        canv.line(doc.leftMargin, 1.5 * cm, doc.leftMargin + doc.width, 1.5 * cm)
        canv.setFont('Helvetica', 8)
        canv.setFillColor(GRIS)
        canv.drawString(doc.leftMargin, 1.05 * cm, 'Materiales Troncoso  ·  ' + limpio(self.titulo_pie))
        canv.drawRightString(doc.leftMargin + doc.width, 1.05 * cm, 'Página %d' % doc.page)
        canv.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == 'h1_toc':
            self.notify('TOCEntry', (0, flowable.getPlainText(), self.page))


def imagen(ruta_img, ancho_max):
    from reportlab.lib.utils import ImageReader
    w, h = ImageReader(ruta_img).getSize()
    ancho = min(ancho_max, 13.6 * cm)
    alto = ancho * h / w
    tope = 12 * cm if h > w * 1.2 else 10 * cm   # capturas de celular (verticales) pueden ser un poco más altas
    if alto > tope:
        alto = tope
        ancho = alto * w / h
    im = Image(ruta_img, width=ancho, height=alto)
    marco = Table([[im]], colWidths=[ancho + 4])
    marco.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#D8D0C8')),
                               ('LEFTPADDING', (0, 0), (-1, -1), 2), ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                               ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
    marco.hAlign = 'LEFT'
    return marco


def caja(titulo, lineas, fondo, borde):
    contenido = [Paragraph('<b>%s</b>' % marcado(titulo), EST['caja'])]
    for l in lineas:
        contenido.append(Paragraph('•&nbsp;&nbsp;' + marcado(l), EST['caja']))
    t = Table([[contenido]], colWidths=[17.4 * cm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), fondo), ('LINEBEFORE', (0, 0), (0, -1), 3, borde),
                           ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                           ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    return t


def paso(num, p, carpeta_img, antes=None):
    texto = Paragraph(marcado(p['t']), EST['cuerpo'])
    numero = Table([[str(num)]], colWidths=[0.62 * cm], rowHeights=[0.62 * cm])
    numero.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), NARANJA), ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 9),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('ROUNDEDCORNERS', [6, 6, 6, 6]),
                                ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                                ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    fila = Table([[numero, texto]], colWidths=[0.95 * cm, 16.4 * cm])
    fila.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                              ('TOPPADDING', (0, 0), (-1, -1), 1), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    piezas = list(antes or []) + [fila]   # 'antes' = título de la tarea: viaja pegado a su primer paso
    if p.get('img'):
        t = Table([[imagen(os.path.join(carpeta_img, p['img']), 15.5 * cm)]], colWidths=[17.4 * cm])
        t.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 28), ('TOPPADDING', (0, 0), (-1, -1), 2),
                               ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
        piezas.append(t)
        if p.get('leyenda'):
            piezas.append(Table([[Paragraph(marcado(p['leyenda']), EST['leyenda'])]], colWidths=[17.4 * cm],
                                style=TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 28)])))
    piezas.append(Spacer(1, 4))
    return KeepTogether(piezas)


def construir(depto):
    ruta_json = os.path.join(AQUI, depto + '.json')
    with open(ruta_json, encoding='utf-8') as f:
        m = json.load(f)
    carpeta_img = os.path.join(AQUI, 'img', depto)
    salida = os.path.join(AQUI, 'Manual-%s.pdf' % m['departamento'])
    doc = Doc(salida, m['titulo'])
    h1_toc = ParagraphStyle('h1_toc', parent=EST['h1'], keepWithNext=1)   # el título de cada tarea nunca queda solo al pie
    historia = []

    # Portada
    historia += [Spacer(1, 5 * cm),
                 Table([['']], colWidths=[17.4 * cm], rowHeights=[0.35 * cm],
                       style=TableStyle([('BACKGROUND', (0, 0), (-1, -1), NARANJA)])),
                 Spacer(1, 0.8 * cm),
                 Paragraph(marcado(m['titulo'].upper()), EST['portada_t']),
                 Spacer(1, 0.3 * cm),
                 Paragraph('Materiales Troncoso  ·  CRM', EST['portada_s']),
                 Spacer(1, 0.2 * cm),
                 Paragraph('Para: %s  ·  Actualizado: %s' % (marcado(m['para']), marcado(m['actualizado'])), EST['portada_s']),
                 Spacer(1, 0.2 * cm),
                 Paragraph(marcado(m['url']), EST['portada_s']),
                 Spacer(1, 2 * cm),
                 Paragraph(marcado(m['intro']), EST['cuerpo']),
                 PageBreak()]

    # Índice
    historia.append(Paragraph('Contenido', EST['h1']))
    toc = TableOfContents()
    toc.levelStyles = [EST['toc1']]
    toc.dotsMinLevel = 0
    historia += [toc, Spacer(1, 0.6 * cm), caja(m['reglas_titulo'], m['reglas'], AMARILLO, NARANJA), PageBreak()]

    # Tareas
    for i, t in enumerate(m['tareas'], 1):
        historia.append(CondPageBreak(9 * cm))
        cabecera = [Spacer(1, 10), Paragraph('%d. %s' % (i, marcado(t['titulo'])), h1_toc),
                    Paragraph('Cuándo: ' + marcado(t['cuando']), EST['cuando'])]
        for n, p in enumerate(t['pasos'], 1):
            historia.append(paso(n, p, carpeta_img, cabecera if n == 1 else None))
        if t.get('cuidado'):
            historia.append(Spacer(1, 3))
            historia.append(caja('Cuidado', t['cuidado'], AMARILLO, NARANJA))
        if t.get('ayuda'):
            historia.append(Spacer(1, 4))
            historia.append(Paragraph('<b>Si necesitas ayuda:</b> ' + marcado(t['ayuda']), EST['cuerpo']))
        historia.append(Spacer(1, 14))

    # Problemas frecuentes
    historia.append(CondPageBreak(10 * cm))
    historia.append(Paragraph('Problemas frecuentes', h1_toc))
    filas = [[Paragraph('<b>%s</b>' % marcado(p['p']), EST['caja']), Paragraph(marcado(p['r']), EST['caja'])] for p in m['problemas']]
    tabla = Table(filas, colWidths=[6.2 * cm, 11.2 * cm])
    tabla.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, CREMA]),
                               ('LINEBELOW', (0, 0), (-1, -1), 0.4, colors.HexColor('#D8D0C8')),
                               ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    historia.append(tabla)

    doc.multiBuild(historia)
    print('PDF listo:', salida, '(%d KB)' % (os.path.getsize(salida) // 1024))


if __name__ == '__main__':
    construir(sys.argv[1] if len(sys.argv) > 1 else 'ventas')
