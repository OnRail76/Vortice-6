# VÓRTICE 6 · CORAZÓN DEL VACÍO

Euroshooter de scroll horizontal para Atari XL/XE (64 KB). Tiene cinco fases, cinco jefes y tres dificultades.

© 2026 · Tony C. Ware

- **Dirigido y diseñado por:** Tony C. Ware
- **Gráficos, fases y música:** Tony C. Ware
- **Programa y asistencia:** GPT y Claude

## Contenido del paquete

| Fichero | Qué es |
|---|---|
| `vortice6.atr` | **Juego completo en disco.** Doble densidad (180 KB) y autoarrancable, sin DOS (701 de 717 sectores). Incluye la intro, las 5 fases encadenadas y el final. |
| `vortice6.car` | **Juego completo en cartucho.** Formato AtariMax 8 Mbit (1 MB, tipo CAR 42), con cargas instantáneas. |
| `VORTICE6_Atlas.pdf` | El Atlas del proyecto: carátulas, historia, instrucciones ilustradas, fases, enemigos, jefes, Unidad Cero, memoria técnica, inspiración y créditos. |
| `xex/` | La intro, cada fase y el final por separado, en `.xex`. Cada fase también va en `.atr` de densidad simple. |
| `xex/prueba/` | Cada fase con la nave invencible, para verla entera. |
| `musica/` | Los temas grabados del emulador. |
| `capturas/` | Pantallas de la versión final. |
| `fuentes/` | Todo el código y los dibujos. `build_disco.sh` reconstruye todo: XEX, disco y cartucho. |

## Para jugar

- **Disco:** enciende el Atari con `vortice6.atr` en la unidad 1. Necesita una disquetera de doble densidad (XF551, 1050 ampliada), SIO2SD, SIO2PC, FujiNet o un emulador.
- **Cartucho:** en un emulador, elige el tipo *AtariMax 8 Mbit*. En un Atari real, grábalo en un cartucho flash AtariMax de 8 Mbit o compatible.
- **Controles:**
  - Joystick en el puerto 1 para mover la nave.
  - FIRE para disparar; si lo mantienes pulsado, el disparo es automático.
  - En el título, izquierda y derecha cambian la dificultad.
- El juego está pensado para NTSC (60 Hz). En PAL funciona, algo más lento.

Las instrucciones completas están en el Atlas.

## Cambios de esta versión (revisión final)

- **Panel de mando:** el título del disco y del cartucho es ahora el panel de la nave. Tiene:
  - un monitor con barrido;
  - la ruta de los 5 mundos, que recorre la Vórtice 6;
  - luces de consola;
  - EUROSHOOTER EN 8 BITS REDEFINIDO latiendo bajo el logotipo.

  Izquierda y derecha cambian la dificultad; FIRE despega. Si nadie toca nada unos 40 s, vuelve la intro.
- **Intro:** dura un minuto e incluye la historia, que se escribe letra a letra. FIRE la salta.
- **Truco de los créditos:** en el panel, arriba, arriba y FIRE muestra solo los créditos del final y vuelve al panel.
- **Créditos:** ya suben suaves, sin dar saltos.
- **Arreglo:** el MODO INVENCIBLE podía quedarse puesto en el título al volver de una partida completa. Ahora el truco se apaga al terminar el juego y el récord siempre se ve.
- **Jefes:**
  - THALASSA llama a sus crías.
  - El Tríptico hace llover escoria.
  - El Corazón Nulo alterna su aspiración con la sangre nueva.
  - FERRUM-9 y SATURNUS no cambian.
- **Oleadas:** cinco patrones nuevos (por detrás, bucle, patrulla, carga y escalera).
- **Unidad Cero:** solo aparece donde hay sitio y se le puede disparar, y se retira si el decorado se le echa encima.
- **Puertas de rayos de Saturno:** se encienden y se apagan; ya no se destruyen.
- **Pinzas y muros de fuego:** dejan siempre su hueco en medio.
- **Fase 2:** el leviatán del abismo ya se ve.
- **Atlas:** nuevas ilustraciones (ficha técnica, piloto, nave en vuelo nocturno y carátula pintada) y páginas de oleadas y del panel.

## Probado

Todo se ha probado en el emulador atari800:

- Partida automática encadenada en disco y en cartucho: intro, panel, las 5 fases, final y vuelta al panel con el récord. Se comprobó que pasan bien los puntos, las naves, el láser, el escudo, la dificultad y el récord.
- De un GAME OVER, vuelta al panel; y si el panel se queda quieto, vuelve la intro.
- Las balas enemigas siguen viéndose en las 5 fases con las oleadas nuevas.
- Arranque en PAL: panel de mando y partida.
- Desde `fuentes/`, el disco, el cartucho y los XEX se reconstruyen idénticos byte a byte.

No se ha probado en un Atari real.
