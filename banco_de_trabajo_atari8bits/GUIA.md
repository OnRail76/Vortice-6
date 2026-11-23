# Banco de trabajo · juegos para Atari 8 bits

Lo que se usó para hacer **Vórtice 5**, **Zak Attack**, **Boloncio** y **Vórtice 6** y sirve para el próximo título:
herramientas, el flujo de trabajo de principio a fin y las lecciones aprendidas por el camino.

| Carpeta | Qué hay |
|---|---|
| `arnes/` | `run8.c`: el emulador sin pantalla con guiones (sección 3) |
| `plantilla/` | `hw.inc`, configuraciones de ld65 (`fases.cfg` es la de Vórtice 6), `build.sh`, `music.s` (reproductor de 4 voces) |
| `graficos/` | `canvas.py`, `pal.py`; `atpic.py` convierte ilustraciones a ANTIC E con 4 colores por franja |
| `audio/` | `musica.py` (compositor y empaquetador para `music.s`) y el análisis de temas de referencia |
| `cine/` | `cine.s` + `gencine.py`: intro y final (frases con fundido, ilustración con DLI, créditos con scroll fino) |
| `empaquetado/` | XEX, ATR sencillo, **disco multiprograma** (`boot_disco.s` + `mkdisk.py`) y **cartucho AtariMax 1 MB** (`cartldr.s`, `cartboot.s`, `mkcart.py`) |
| `analisis/` | capturas, bots, perfiles, `chkbul.py` (balas visibles) |
| `documentacion/` | atlas y manuales; `atlas_html.py` + `atlas_pdf.py` es el Atlas final de Vórtice 6 (HTML → PDF con Chrome) |
| `conversion_cpc/` | herramientas del port de Boloncio |

## 1. Montar las herramientas (Linux, una vez)

| Herramienta | Para qué | Cómo |
|---|---|---|
| cc65 2.19 (ca65 + ld65) | Ensamblar y enlazar | `git clone https://github.com/cc65/cc65 && make -C cc65` → binarios en `cc65/bin` |
| atari800 (libatari800) | Emulador sin pantalla para pruebas automáticas | `git clone https://github.com/atari800/atari800 && cd atari800 && ./autogen.sh && ./configure --target=libatari800 --disable-netsio && make CFLAGS="-O2 -Wno-error"` (con GCC reciente `-Werror` para la compilación por un `ULONG` redefinido) |
| `run8` | El arnés de pruebas (este banco) | `gcc -O2 -I atari800/src/libatari800 -I atari800/src -o run8 arnes/run8.c atari800/src/libatari800.a -lm` |
| Python 3 + Pillow + numpy | Gráficos, generadores, análisis | `pip install pillow numpy scipy` |
| Playwright + Chromium | Documentación HTML → PDF | `pip install playwright && playwright install chromium` |
| ffmpeg | Grabar la banda sonora a MP3 | paquete del sistema |

Para jugar de verdad: Altirra (Windows) o atari800 con pantalla.

## 2. El flujo de trabajo

```
gfx/*.py  ──►  tools/gen.py  ──►  src/data.s  ──►  ca65/ld65  ──►  main.bin
(dibujos en texto)  (charsets, mapas,   (generado)                     │
                     oleadas, jefes,                      mkxex.py ───┼──► .xex
                     música, textos)                      mkpack.py ──┴──► .atr + .car
```

1. **Dibujar en texto.** Sprites, tiles, escenarios y jefes son cuadrículas de caracteres
   en Python (`graficos/canvas.py` da rectángulos, elipses, trazos y espejo; `graficos/pal.py`
   convierte códigos de color $HL a RGB NTSC). La misma fuente sirve al juego y a los documentos.
2. **Generar los datos.** Un script convierte los dibujos en charsets de 1 KB, metatiles,
   mapas, tablas de enemigos, jefes partidos en dos juegos de caracteres y música en tablas.
   Comprueba los límites (128 caracteres por juego, sprites por franja…) y avisa si algo no cabe.
3. **Ensamblar.** `build.sh` regenera, ensambla, enlaza y empaqueta los tres formatos.
4. **Probar sin manos** con `run8` (sección 3).
5. **Medir** velocidad, sprites ocultos y duplicados (sección 4).
6. **Documentar** con los generadores de `documentacion/` (sección 5).

## 3. El arnés `run8`

Ejecuta un .xex/.atr/.car en atari800 sin pantalla siguiendo un guion de texto:

```
in  F0 F1 joy trig start   # entre los cuadros F0 y F1: joy (1 arriba, 2 abajo, 4 izq., 8 der.; se suman), fuego 0/1, START 0/1
shot F nombre.raw          # captura de pantalla en el cuadro F (384×240, códigos de color)
mem  F 0080 128 z.bin      # volcado de memoria (dirección en hex, longitud en decimal)
end  F                     # último cuadro
```

- `WAV=salida.raw run8 juego.xex guion` graba el sonido (PCM 16 bits, 44.100 Hz, mono).
- `shot.py` convierte capturas a PNG; `memq.py` lee variables por nombre con el fichero de etiquetas.
- Con una versión invulnerable (`-D CHEAT=1`) un bot recorre el juego entero en un minuto de reloj.

## 4. Medir

| Script | Qué da |
|---|---|
| `fullrun.py` | Guion de partida completa: elige dificultad, juega en zigzag con fuego y vuelca memoria cada N cuadros |
| `allstats.sh` + `stats.py` | Por tramo (fase/jefe y sector): velocidad (vueltas de lógica por cuadro), balas, balas/disparos/sprites que se quedan sin dibujar, duplicados |
| `nodprof.sh` + `prof.py` | Coste en ciclos de cada rutina, con sondas `PROF n` (VCOUNT + cuadro) y DMA apagado |

Una vuelta de lógica que pasa de un cuadro tarda dos: el juego va al 50 % en ese momento.
Lo que importa es que casi todas las vueltas quepan en un cuadro, no la media.

## 5. Documentar

- `render_assets.py`: sprites, tiles, cráteres y jefes desde los mismos `gfx/*.py`, más recortes de capturas reales.
- `build_atlas.py` (A4 apaisado) y `build_manual.py` (A5) escriben HTML; `make_pdf.py` lo pasa a PDF.
- `common.py` reúne los textos compartidos (créditos, historia, lema, datos de sectores).

## 6. Lecciones aprendidas (Vórtice 5)

**Pantalla y DLI**
- Tablas DLI de más de 256 bytes con índice Y dan la vuelta: una tabla por campo (32 bytes), rutinas A/B con direccionamiento absoluto.
- Con VSCROL = 7 la primera línea mide un scanline y su DLI llega dentro de la anterior: deja una línea en blanco tras el marcador y carga la línea 0 en la VBI.
- Pon el bit de DLI solo en la línea anterior a una línea que cambia algo, con una máscara de cambios por línea. Un barrido desenrollado de la máscara vale más que ordenar listas.
- Doble búfer: dos display lists y dos juegos de tablas; la lógica prepara el cuadro siguiente y la VBI solo cambia punteros.
- La PMG de resolución de una línea deja libre $B000–$B2FF: buen sitio para tablas de trabajo.

**Sprites**
- Multiplexar P2/P3 por franjas y los 4 misiles como un solo recurso compartido entre disparos y balas.
- **Turnos**: lo que no cupo en un cuadro va primero en el siguiente. Así nada queda invisible dos cuadros seguidos; como mucho parpadea.
- Un sprite que no cambió (posición, gráfico, player) no se borra ni se repinta. Que cada objeto conserve su player.
- Recorre los objetos en el orden en que suelen estar ya (el reparto de huecos lo marca): la ordenación por inserción sale casi gratis.

**Rendimiento**
- VBI inmediata propia en juego (copiar sombras a mano) en vez de pasar por el SO.
- No toques los LMS si el scroll no se movió; cachea lo que solo cambia con el scroll.
- Colisiones contra listas compactas de lo que está vivo y en pantalla.
- Si un tramo sigue lento, a veces la solución es de diseño: espaciar las oleadas.

**Sonido**
- Lo que corre en la VBI necesita sus propios temporales de página cero.
- Nunca cortes en seco: bucles que cierran en el acorde que lleva al principio y fundido en cada cambio de pista.
- AUDCTL $78 (dos voces de 16 bits) para pantallas; $28 en juego (bajo de 16 bits, melodía de 8, efectos en su canal).

**Juego justo**
- Ninguna bala nace dentro de una zona alrededor de la nave; tope de balas según la dificultad.
- Una bala nueva no nace encima de otra igual; un enemigo que devuelve disparos, con enfriamiento.

**Formatos**
- ATR autoarrancable sin DOS: tope de 255 sectores (~32 KB); vigílalo.
- Cartucho AtariMax 128 KB: el banco 0 copia los demás a RAM y desconecta el cartucho.
- Desconecta el BASIC de los XL/XE (PORTB) si usas $A000–$BFFF.

## 7. Lista para el próximo título

1. Copia `plantilla/` (build.sh, vortice5.cfg, cart.s) y los empaquetadores.
2. Define paleta y reglas del hardware antes de dibujar (cuántos colores, sprites por franja, tamaño de jefes).
3. Dibuja en `gfx/` con `canvas.py`; haz que el generador compruebe los límites.
4. Haz una versión con `CHEAT` y `PROF` desde el primer día; mide en cada cambio grande.
5. Prueba los tres formatos al final de cada ronda.

## 8. Lecciones aprendidas (Zak Attack, run and gun con scroll horizontal)

**Pantalla**
- ANTIC 4 + HSCROL sobre un anillo de 64 columnas por fila (128 bytes, cada columna escrita dos veces): la ventana de 48 bytes nunca da la vuelta y basta tocar el byte bajo de 22 LMS en la VBI.
- HSCROL = 3 − (camx & 3); HPOS del píxel 0 del campo = 45 con este montaje.
- Fondo repetido cada 16 columnas + primer plano en tramos [fila, n, códigos]: 5 fases en ~8 KB.
- El generador comprueba que el fondo no use caracteres sólidos (en el tren, las colinas eran "suelo" invisible).
- Una DLI bajo el marcador cambia juego de caracteres y colores; otra en la última fila devuelve el borde a negro.
- Logotipo con juego de caracteres propio (41 celdas) y degradado por DLI línea a línea en el título.

**Errores que costaron**
- Otra vez el temporal compartido entre VBI y programa principal: la VBI usa SOLO sus variables (`vbt`). El síntoma fue fondo corrupto en la segunda vuelta.
- Una rutina de sonido que pisa X/Y dentro de un bucle de colisiones produjo puntuaciones BCD imposibles ("063<00"). `play_sfx` conserva X e Y.
- `cld` al principio de la VBI: puede llegar en medio de una suma BCD.
- Jefes: comprobar con números que el punto débil queda a la altura de los disparos (pies − 12 de pie, − 5 agachado, ~−60 saltando).

**Pruebas**
- `bot.py` + `runbot.sh`: corre, salta, se para a disparar y a veces se gira; con `-D CHEAT=1` los fosos lo devuelven arriba y no pierde vidas. Recorre las 5 fases en ~23 000 cuadros.
- `zp.py`: lee variables de página cero por nombre desde un volcado de `run8`.
- Contador `lagcnt` de cuadros perdidos: < 1 %, casi todo en cambios de fase.
- `atlas.py`: atlas gráfico desde los mismos datos del juego (pantallas simuladas), antes de programar nada.

**Segunda ronda (pruebas de Tony en atari800 de verdad)**
- Calibra la posición de los sprites contra el decorado desde el primer día: captura cruda, busca el color del sprite y el de un tile conocido y compara con las coordenadas del mundo. Aquí el sprite iba 9 color clocks a la derecha (Zak "se metía" en las cajas) y el campo visible empieza en camx + 12.
- Ninguna rutina devuelve intacto un puntero de página cero que no sea suyo: `aim_bullet` usaba `ptr3` y el bucle de torretas guardaba ahí su índice. Con el índice basura escribía fuera de las tablas: colores rotos (cielo rosa) y cuelgue.
- Aritmética con signo: `lsr` sobre un valor negativo lo convierte en uno enorme (el pescado aparecía abajo del todo). Usa `cmp #$80 / ror`.
- Recogibles: si no hay hueco de sprite, el evento espera; los enemigos se pierden, el pescado no.
- Enemigos de tierra con prueba de pared (`move_xw`): el soldado se para, el perro salta.
- Bot aleatorio (`randbot.py`) para buscar cuelgues: cuidado con los falsos positivos en pantallas de texto y GAME OVER.
- Música de marcha: batería en el canal de efectos (bombo con barrido de tono, caja y charles de ruido); un golpe de batería tapa el sonido del disparo, nunca una explosión o un golpe a Zak.

**Tercera ronda (puntería, dificultad, avisos)**
- Joystick de un botón y apuntar: "plantarse con FIRE" (FIRE desde quieto fija a Zak y la palanca apunta) conserva correr-saltar-disparar y añade diagonales en el suelo.
- Otra vez registros pisados: una rutina auxiliar (`scale_hp`) cambiaba Y en medio de un bucle que leía datos con (ptr),Y → todas las piezas del jefe mal colocadas. Toda rutina auxiliar guarda lo que toca.
- Los flancos de la palanca en una variable propia: `put_line` reutilizaba `tmp+2` y el menú cambiaba de dificultad solo.
- Inicializa explícitamente lo que vive en BSS (la dificultad salía con basura del cargador).
- Aviso de jefe genérico: la pieza que va a atacar invierte sus caracteres (bit 7) cada 4 cuadros y se restaura al terminar; proyectiles "en espera" (contador en el hueco del enemigo) para escombros y barridos.

## 9. Lecciones aprendidas (Boloncio, port desde Amstrad CPC)

**Origen**
- Un `.cpr` de GX4000 puede ser solo un BASIC de CPC metido en un disco ROM: mira el directorio AMSDOS
  antes de pensar en hardware Plus (`conversion_cpc/extract.py` + `detok.py`).
- Los decorados hechos con PRINT y salto de línea se reconstruyen fielmente simulando la pantalla del CPC
  (`rooms.py`); copiar a mano las cadenas largas lleva a errores.
- Leer los listados con lupa: errores de tecleo de revista (un token `LIST` colado en un LOCATE),
  variables que nunca se asignan (`OB$`), `+0.5` en variables enteras.

**Pantalla**
- MODE 0 del CPC (20 columnas de 8x8, 1 color por carácter) = ANTIC 6 casi uno a uno: 64 códigos y 4 colores
  (bits 6-7). El protagonista en PMG libera caracteres y le da color propio.
- Colores: tinta CPC (n = 9G + 3R + B, niveles 0/128/255) → código Atari más cercano en `pal.bin`.
- La colisión "leer el carácter de la pantalla" del BASIC se porta con una tabla de clase por código
  (libre, sólido, mortal, llave, pareja).

**Errores que costaron (cartucho)**
- Con la VBI del SO (no una propia), al desconectar el cartucho AtariMax el SO XL ve TRIG3 ≠ GINTLK
  y bloquea la máquina: copiar TRIG3 en GINTLK ($03FA) al arrancar.
- El cargador del cartucho copia sobre $2000-$9FFF y machaca la display list del SO con $FF (DLI en
  cada línea). Si se activa NMIEN=$C0 antes de poner una DL propia, las DLI se anidan y desbordan la pila.
  Activar la DLI solo con la DL del juego ya puesta; parar ANTIC (DMACTL=0) al empezar.
- Probar siempre los tres formatos: el .xex y el .atr iban bien y el .car no.

**Pruebas**
- Compilación BOT: el juego lee las acciones de una tabla generada por un BFS (`route.py`) en vez de
  la palanca; así no hay desfases entre el guion de `run8` y los pasos de la lógica. Con CHEAT y
  monstruos "atravesables" recorre las 8 salas, abre puertas y llega a la pantalla final sin manos.
- Compilación con `-D STARTROOM=n` para capturar cada sala directamente.

## 10. Lecciones aprendidas (Vórtice 6, visor de láminas desde un GDD)

**Herramientas**
- En una sesión nueva sin cc65 ni atari800: `git clone` de GitHub y compilar como en la sección 1 (unos 3 minutos). No hace falta escribir ensamblador ni emulador propios.

**Pantalla**
- Los textos de los marcadores (ANTIC 2 con LMS) también cuentan para el límite de 4 KB: un marcador que empezaba en $7FEC salió corrupto. El generador coloca filas *y* textos con la misma comprobación.
- Datos primero: los juegos de caracteres en $2000 quedan alineados a 1 KB sin relleno; el RUNAD y el salto del ATR se leen de la etiqueta `start` en `game.lbl` (`mkxex.py`, `mkatr.py`).
- PMG en $A000 y DL + tablas en $A800 con el BASIC desconectado por PORTB al arrancar (y en el segmento INIT del .xex).
- Escenario de 64 columnas + 48 repetidas por fila: scroll infinito, la VBI solo suma el desplazamiento grueso a 20 LMS. Filas iguales se comparten (151 filas únicas para 10 láminas).
- DLI con 15 tablas (una por campo) y dos rutas: ligera por fila (fondo + P2/P3) y completa en los cambios de zona (juego de caracteres, PF0-3, los 4 players). En la galería, los 4 players se multiplexan por bandas.

**Sprites**
- Nave de 12 píxeles y 3 colores con solo P0+P1: P1 desplazado 4 cc y PRIOR $21 (modo OR). Columnas 0-3 solo P0, 8-11 solo P1, 4-7 los tres colores.
- Cápsulas y balas de jefe como pareja P2+P3 en OR (cáscara + letra).

**Documentación**
- Atlas en PIL directamente (sin Playwright): páginas A4 apaisadas a 150 ppp → PDF con `save_all`. Capturas de `run8` + dibujos desde los mismos `gfx/*.py`.
- Cuando el GDD y la lámina se contradicen (armas, número de enemigos, PAL/NTSC), decidir con el usuario antes de dibujar y dejarlo escrito en el atlas.

## 11. Lecciones aprendidas (Vórtice 6, fase 1 jugable)

**Lo que pidió Tony al probar** (y es la norma para los shooters): balas siempre visibles, sin parpadeos, sin sprites cortados ni corruptos. Las torretas de decorado no compensan: mejor enemigos voladores.

- Multiplexar "a quien quepa" por fila da parpadeo. Lo correcto: franjas fijas con 2 huecos y objetos confinados a su franja; el generador de oleadas reparte entre la franja y su vecina, y lo que no cabe espera.
- El color de los misiles M2/M3 sale de COLPM2/COLPM3 de esa franja: en franjas sin enemigo hay que poner un color de bala vivo (si no, bala negra sobre fondo negro). Todos los enemigos con luminancia alta.
- Doble búfer de verdad también para la PMG: dos zonas de 2 KB (PMBASE en la VBI) y HPOS de P0/P1/M0-3 congelados por búfer. Los misiles se borran enteros y se repintan cada cuadro: adiós a las balas fantasma que dejaba "desactivar sin borrar".
- `lda (src,x)` NO es "(src) + x": indexa el puntero. Usado como contador de bucle copia basura (sprites "peinados"). Para copiar: `(src),y` con el destino en la misma Y.
- `tools/chkbul.py`: comprueba en las capturas crudas de `run8` que cada bala enemiga activa (según la memoria) tiene píxeles visibles en su sitio.
- `tools/fixbr.py`: convierte los saltos condicionales fuera de alcance que señala ca65 en salto invertido + jmp.

## 12. Lecciones aprendidas (Vórtice 6 completo: 5 fases, intro, final, disco y cartucho)

**Un programa por fase**
- Cuando el juego no cabe en 64 KB: un programa por fase (más intro y final), todos cargados en $2000 y con la misma interfaz.
  Cada uno monta solo su música, su jefe y el código de sus enemigos (`.if FASE = n`).
- Un **bloque compartido** en la página 5 ($0580) pasa la partida de un programa a otro: firma $56, dificultad, «encadenado»,
  puntos, vidas, láser, escudo, récord, truco y «arrancado desde el cargador».
- Un **cargador residente** en $0710 con interfaz fija (A = número de programa) sirve igual para el disco y el cartucho:
  los programas no saben de dónde vienen.
- **Error que costó:** al terminar el final, el bloque seguía marcado como «encadenado» y la fase 1 empezaba directamente con los puntos
  de la partida anterior. Quien termina la partida (final o GAME OVER) limpia `P_CHAIN` antes de volver al título.

**Disco multiprograma** (`boot_disco.s`, `mkdisk.py`)
- ATR de doble densidad (720 sectores de 256 bytes; los 3 primeros de 128). Arranque propio de 3 sectores en $0700, sin DOS.
- El cargador lee por el SIO del SO (SIOV) sector a sector y salta a la etiqueta `start` del programa, sacada de su `.lbl`.
- Antes de cargar: DMA y DLI fuera, vectores de VBI del SO de vuelta (SETVBV con SYSVBV/XITVBV) y POKEY en silencio.

**Cartucho AtariMax 8 Mbit** (`cartldr.s`, `cartboot.s`, `mkcart.py`)
- 128 bancos de 8 KB en $A000–$BFFF; $D500+n elige banco y $D580 desconecta. CAR tipo 42.
- El banco de arranque copia el mismo cargador a $0700; los datos van por páginas desde el banco 1.
- **NMIEN = 0 mientras se conecta o desconecta el cartucho**, y `TRIG3 → GINTLK` al terminar: si una VBI del SO XL ve TRIG3 ≠ GINTLK, cuelga la máquina.
- El tipo «viejo» arranca en el banco 127 y el «nuevo» en el 0: el banco de arranque va repetido en los dos.
- Con todo en RAM por debajo de $A000 se copia directamente con el cartucho conectado; si algo cargara en $A000–$BFFF haría falta un búfer en RAM baja.

**Intro y final** (`cine/`)
- Ilustración en ANTIC E (160 × 192) con 4 colores por franja de 4 líneas cambiados por DLI. La DLI va en la línea 2 de cada franja:
  `WSYNC`, prepara los registros, `WSYNC` y los escribe al empezar la franja siguiente. Hecha de una vez, los colores llegaban una línea tarde.
- La imagen se parte en dos LMS para no cruzar un límite de 4 KB ($5010 y $6000).
- `atpic.py`: convierte una carátula con un negro fijo + 3 colores por franja (o 4 libres) y Floyd–Steinberg en serpentina;
  penaliza cambiar de color entre franjas. Retocar a mano lo que importa (ojos, logotipos).
- La DLI con temporales propios (`d1`, `d2`): compartirlos con el fundido corrompía los colores.
- Destello sobre la ilustración: un jugador en resolución de una línea (PMBASE libre por encima del programa) y un efecto de sonido
  escrito en la VBI *después* del reproductor, en el canal 4, para que pise la música solo mientras suena.
- Créditos: ANTIC 2 con desplazamiento fino vertical, la DL se rehace por línea; que entren desde abajo con la pantalla vacía y sin que FIRE los salte.

**Música**
- `musica.py` compone por patrones e instrumentos (envolvente, arpegio, temblor, sonido fijo de batería) y genera `musdata.s`.
- Mide la afinación grabando con `WAV=` y elige la tonalidad de cada tema para que el bajo de 8 bits caiga en notas afinadas.
- Variables `V6FASE` (tema de fase + jefe) y `V6TEMAS` (temas sueltos, para grabar MP3).

**Pruebas**
- Para recorrer el juego entero encadenado: compilar con `-D FASTCLEAR` (el jefe cae al llegar a su arena) y `-D PRUEBA` (invencible)
  mediante un `ca65` envoltorio en `CC65=…`, sin tocar los scripts; luego reconstruir la versión normal.
- Partida automática de la intro al título en disco y en cartucho, comprobando el bloque compartido con `mem`.
- `run8 … -pal` para comprobar que arranca en PAL.
- Reconstruir desde una copia limpia del paquete de fuentes y comparar con `cmp`: el entregable debe salir idéntico byte a byte.

**Documentación: el Atlas final**
- HTML + CSS a A4 y PDF con Playwright usando el Chrome del sistema (`atlas_pdf.py`): fuentes OTF (Inter) que reportlab no carga.
- `atlas_title.py`: rótulos con la fuente del juego en degradado, como imágenes pixeladas.
- `atlas_sprites.py`: los sprites desde los mismos datos que el juego (letras a/b/c = P2, P3 y la mezcla en OR), con proporción de píxel NTSC (6 × 4).
- Capturas nuevas de la versión final con guiones de `run8` de las versiones `_PRUEBA`; repasar las hojas de contactos y elegir a mano.
- Comprobar la maqueta rasterizando el PDF (`pdftoppm`): títulos largos que se salen, imágenes que pisan el pie de página.

**Lo que pidió Tony** (norma para los siguientes)
- Créditos: «2026 - TONY C. WARE». En Vórtice 6, además: dirigido y diseñado, gráficos, fases y música por Tony; programa y asistencia, GPT y Claude.
- Nada de «prototipo» ni de sistema de vídeo en las pantallas de un juego terminado.
- Paquetes sin scripts de publicación.

## 13. Lecciones aprendidas (Vórtice 6, revisión final: panel de mando, jefes, oleadas)

**Panel de mando (menú) en mapa de bits**
- `graficos/menu_art.py`: el panel se dibuja en Python a 160 × 192 con 4 colores por franja de 4 líneas, decidiendo la paleta franja a franja
  (lo que va en la misma franja comparte colores: planetas y rótulos se ordenan en vertical para que cada uno tenga los suyos).
  Fuente pequeña 3x5 (`graficos/font3.py`): 4 píxeles = 1 byte en ANTIC E, así los rótulos variables se copian por bytes.
- Se guarda comprimido (RLE sencillo: 7,5 KB → 4,2 KB) y se descomprime en RAM al entrar; las piezas que cambian (dificultad, aviso, cifras
  del récord) son bloques recortados que se copian encima.
- Los efectos son solo colores por franja recalculados cada vuelta: barrido del monitor (COLBK más claro con estela), destellos, luces.
- **Error que costó:** la lógica del menú tardaba más de un cuadro y todo lo que dependía de `frame and #1` (fundido, barrido) no avanzaba
  nunca: el fundido se quedaba en negro y solo se veía media pantalla. Los contadores de efectos avanzan por vuelta, no por paridad del cuadro.
- **Error que costó:** con DLI en la línea 2 de cada franja hay 48 DLI y la última prepara una franja 48 que no existe: bajo la imagen salía
  una banda de color con basura de la memoria (el programa anterior la había dejado allí). Poner a cero la entrada 48 de las tablas.
- El BSS de un programa cargado por el cargador NO está a cero: lo que dejó la fase anterior sigue ahí. Inicializar todo lo que se lea.
- Los nombres de etiqueta no pueden ser mnemónicos (`STX`) ni repetir temporales de la música (`mt`).

**Flujo del disco con panel**
- Programa 0 = intro + historia + panel. El panel deja el bloque compartido listo (dificultad, vidas, láser 1, truco) con `P_CHAIN = 1` y
  carga la fase 1. GAME OVER y el final cargan el programa 0 con `P_CHAIN = $80`: directo al panel, sin intro. El final apaga el truco.

**Jefes y oleadas**
- Ataques distintos por jefe con el mismo esqueleto (aviso común, fase especial, exposición): invocar enemigos con `newobj` desde la boca
  del jefe, o hacer caer rocas como caracteres sólidos de la pantalla del jefe (la colisión con el decorado ya mata).
- Patrones de oleada como capa encima del enemigo (`OPAT`): por detrás (nunca en la franja de la nave), bucle, patrulla, carga con aviso y
  escalera. Al convertir el objeto en explosión hay que borrar su patrón.
- Enemigo grande que se planta: antes de nacer, comprobar con `solidat` que su sitio y la línea de tiro desde la nave estén libres; en vuelo,
  mirar el decorado que se le acerca y retirarse a tiempo. Si no hay sitio en ~5 s, perder esa oleada para no bloquear las siguientes.
- Créditos con desplazamiento fino vertical que «botaban»: el programa rehacía la lista y escribía VSCROL a destiempo. Solución: una lista fija
  (una sola dirección LMS y líneas seguidas en memoria) y la VBI cambia juntas la dirección y VSCROL antes de que se pinte el cuadro.
- Truco «solo créditos»: el panel carga el programa del final con `P_CHAIN = $81`; el final ve la marca, enseña solo los créditos y vuelve al panel.
