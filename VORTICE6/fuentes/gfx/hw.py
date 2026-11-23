"""VÓRTICE 6 · reglas del hardware y paletas (NTSC).

Pantalla de juego
  - Marcador superior: 1 línea ANTIC 2 (fuente de la ROM).
  - Campo: 20 filas ANTIC 4 (4x8 píxeles de 1 color clock, 4 colores + fondo), HSCROL.
      píxel '.'=fondo(COLBK) '1'=PF0 '2'=PF1 '3'=PF2 '4'=PF3 (carácter invertido: sustituye a PF2)
      Una celda de 4x8 no puede mezclar '3' y '4'.
  - Marcador inferior: 1 línea ANTIC 2.
  - 128 caracteres por juego; un juego por fase y otro por jefe.

Sprites (PMG de 1 línea, prioridad players sobre campo, modo OR en parejas)
  - P0+P1: VÓRTICE 6. P1 desplazado 4 cc a la derecha: 12 cc de ancho, 3 colores
      'a' = solo P0, 'b' = solo P1, 'c' = los dos (color = P0 OR P1)
  - P2, P3: enemigos voladores, multiplexados por franjas con DLI (1 color cada uno).
      Dos enemigos que comparten franja usan P2 y P3; P2+P3 superpuestos = objeto de 3 colores
      (cápsulas P/S, ojo de los jefes).
  - M0/M1: disparos de la nave (ancho x4 = 8 cc).  M2/M3: balas enemigas.
"""

ROWS = 20          # filas de campo
SHIP_P1_OFS = 4    # desplazamiento de P1 respecto a P0

SHIP = dict(p0=0x9C, p1=0x0E)        # v4: cian azulado (alas, motores, cola del láser) + blanco (morro, punta del láser) -> OR $9E
SHIELD = dict(p0=0x1C, p1=0x0E)      # con escudo la nave se vuelve dorada

# ---------------------------------------------------------------- paletas de fase
# bk: color de fondo por fila de campo (DLI); el resto, por fase
PHASES = [
  dict(key='desguace', nombre='EL DESGUACE ESPACIAL', jefe='FERRUM-9', lema='EL COMPACTADOR SOBERANO',
       pf0=0x04, pf1=0x36, pf2=0x0C, pf3=0xAC,
       bk=[0x00]*20,
       luz=0x0E),
  dict(key='oceanos', nombre='LOS OCEANOS ASTRALES', jefe='THALASSA', lema='LA MADRE DE LAS MAREAS',
       pf0=0x84, pf1=0xA8, pf2=0xBC, pf3=0x0E,
       bk=[0x80, 0x80, 0x80, 0x80, 0x82, 0x82, 0x82, 0x82, 0x92, 0x92, 0x92, 0x92, 0x94, 0x94, 0x94, 0x94, 0x84, 0x84, 0x82, 0x80],
       luz=0xAE),
  dict(key='hades', nombre='EL FUEGO INFERNAL DE HADES', jefe='EL TRIPTICO DE HADES', lema='ALTAR DE TRES ROSTROS',
       pf0=0x42, pf1=0x36, pf2=0x2C, pf3=0x0E,
       bk=[0x00]*4 + [0x30]*4 + [0x00]*6 + [0x30, 0x30, 0x32, 0x32, 0x42, 0x42],
       luz=0x2E),
  dict(key='saturno', nombre='EL SARCOFAGO DE SATURNO', jefe='SATURNUS', lema='EL OFICIANTE VACIO',
       pf0=0x64, pf1=0x28, pf2=0xBA, pf3=0x58,
       bk=[0x00]*4 + [0x60, 0x60, 0x70, 0x70, 0x60, 0x60, 0x70, 0x70, 0x60, 0x60, 0x00, 0x00] + [0x00]*4,
       luz=0x2E),
  dict(key='viviente', nombre='LA NAVE VIVIENTE', jefe='EL CORAZON NULO', lema='NUCLEO DE LA NAVE VIVIENTE',
       pf0=0x42, pf1=0x46, pf2=0xFC, pf3=0xDA,
       bk=[0x40, 0x40, 0x00, 0x00] + [0x00]*12 + [0x00, 0x00, 0x40, 0x40],
       luz=0xDC),
]
# Nombre completo para documentos (la fuente de la ROM no tiene tildes; el atlas sí)
NOMBRES_DOC = ['EL DESGUACE ESPACIAL', 'LOS OCÉANOS ASTRALES', 'EL FUEGO INFERNAL DE HADES',
               'EL SARCÓFAGO DE SACRIFICIOS DE SATURNO', 'LA NAVE VIVIENTE']
JEFES_DOC = ['FERRUM-9', 'THALASSA', 'EL TRÍPTICO DE HADES', 'SATURNUS', 'EL CORAZÓN NULO']
LEMAS_DOC = ['El compactador soberano', 'La madre de las mareas', 'Altar de tres rostros',
             'El oficiante vacío', 'Núcleo de la Nave Viviente']
