# Conversión desde Amstrad CPC (usado en Boloncio)
- `extract.py juego.cpr carpeta`: abre un cartucho .cpr (RIFF "AMS!", bancos de 16 KB) que lleve un disco
  AMSDOS en ROM (directorio en $C000 del cartucho) y saca los ficheros con su cabecera.
- `detok.py FICHERO.BAS`: lista Locomotive BASIC tokenizado (salta la cabecera AMSDOS de 128 bytes).
- `rooms.py`: ejemplo de "pantalla CPC simulada" (LOCATE/PRINT/PEN con salto de línea a 20 columnas)
  para reconstruir los decorados que el BASIC dibuja con PRINT.
- `route.py`: BFS con la misma lógica por pasos del juego; da una ruta por sala y alimenta la compilación BOT.
- `route_full.py`: igual pero simulando monstruos y gotas paso a paso (BFS sobre héroe + tiempo); compara reglas.
