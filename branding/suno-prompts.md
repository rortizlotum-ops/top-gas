# TOP GAS — Prompts de Suno (música instrumental)

Identidad sonora del grupo motero **Top Gas**: estética Top Gun (aviación 80s, rojo/blanco/negro,
estrellas, alas) cruzada con mundo custom/rocker (V-twin, cromo, carretera, cuero).

Traducción a música: **hard rock sureño / biker rock** con un guiño **cinemático ochentero**
(sintes de metal, caja con gated reverb, épica de cabecera de película).

> Usa siempre **Custom Mode** + interruptor **Instrumental ON**.
> El campo *Style* de Suno funciona mejor con descripciones densas en comas, sin frases largas.

---

## 1) CABECERA / INTRO DEL CANAL — 25 SEGUNDOS

Objetivo: **25 s exactos**, explosivo desde el primer compás y con final seco. Nada de introducción
ambiental ni de subidas lentas: el gancho tiene que aparecer antes del segundo 5.

Referencia estética: *main title* de película de aviación de mediados de los 80 — guitarra solista
con delay largo y trémolo, sintes de metal, caja con gated reverb, secuencia de bajo en semicorcheas.

> **Importante:** no escribas en Suno el nombre de la película, del compositor ni del guitarrista.
> Suno rechaza el prompt. Se consigue el mismo sonido **describiendo los elementos**, que es lo que
> hacen los prompts de abajo.

### Campo *Style of Music*

```
Instrumental 80s cinematic rock anthem, aviation action-movie main title energy, 128 BPM, 4/4,
E minor lifting into a triumphant major-key hook. Soaring lead electric guitar carrying the melody
with long stereo delay, wide vibrato and whammy bar dives; palm-muted chugging power chords
underneath; punchy analog synth brass stabs; driving sequenced 16th-note synth bass; gated reverb
snare and electronic toms; shimmering FM bell pad on top. Arrangement is short and explosive:
two bar swell, four bar riff, six bar lead guitar theme, one bar hard stop. Total length 25
seconds. High energy from the very first beat, heroic, triumphant, chrome and jet fuel. Big loud
bright 1986 arena production, tape saturation, wide stereo.
```

### Campo *Style* (versión corta si tu Suno limita a ~200 caracteres)

```
Instrumental 80s cinematic aviation rock anthem, soaring delayed lead guitar, synth brass stabs,
sequenced synth bass, gated reverb snare, palm-muted power chords, 128 BPM, heroic and explosive,
25 second main title, hard stop.
```

### Campo de letra (estructura con tiempos, 128 BPM → 1 compás = 1,9 s)

```
[0:00 Intro - 2 bars: synth brass swell + electronic tom fill, no fade in]
[0:04 Main Riff - 4 bars: palm-muted power chords + sequenced synth bass, full drums]
[0:11 Lead Theme - 6 bars: soaring lead guitar melody over the riff, highest energy]
[0:22 Ending - 1 bar: final power chord, crash cymbal, hard stop]
[End]
```

### Exclude Styles / negativos

```
vocals, singing, rap, long intro, ambient intro, fade in, fade out, slow build, quiet opening,
sparse verse, ballad, lo-fi, trap hi-hats, EDM drop, tempo change, orchestral only
```

### Cómo conseguir que dure 25 s de verdad

Suno **no garantiza la duración**: le pidas lo que le pidas, suele entregar entre 1 y 3 minutos.
El prompt de arriba sube mucho las probabilidades de una pista corta, pero el método fiable es:

1. Genera **6–8 versiones** con ese prompt.
2. Descarta las que empiecen suave: te interesa la que entra a saco en el segundo 0.
3. Recorta **0:00 → 0:25** (en Suno, *Edit → Crop/Trim* si tu plan lo tiene; si no, en Audacity,
   CapCut o el propio editor de YouTube).
4. El corte cae casi siempre a mitad de compás: alinéalo con el primer golpe de caja del compás 14
   y pega encima un **crash con cola de reverb** para cerrar. Queda como final compuesto, no cortado.
5. Alternativa limpia: genera la pista completa, localiza el punto de máxima energía (suele estar
   sobre 0:45–1:10) y monta la cabecera con **4 s de swell + 20 s de ese tramo + crash final**.

### Títulos sugeridos
`Top Gas Anthem` · `Afterburner` · `Ignition` · `Full Throttle Theme`

---

## 1B) CABECERA — VARIANTE ROCKERA (25 s, guitarras al frente)

Misma función y misma duración que la 1), pero la épica la llevan **las guitarras y no los sintes**.
Sube el tempo, entra Hammond en lugar de teclado ochentero, batería acústica sin procesar y bajo
tocado. Es la versión que mejor casa con el lado custom del logo: más garaje, más cuero, menos cabina.

### Campo *Style of Music*

```
Instrumental hard rock main title, 136 BPM, 4/4, key E, guitar driven with no synthesizers.
Two Marshall stacked electric guitars playing a harmonized twin lead melody in thirds as the main
hook, thick distorted power chord riff underneath, bluesy slide guitar fills, dirty Hammond organ
holding the chords, loud fingered electric bass, hard hitting acoustic drum kit with open hi-hat,
cowbell on the accents and a tom fill intro, natural room reverb. Arrangement is short and
explosive: two bar drum and guitar pickup, four bar riff, seven bar twin lead theme, one bar hard
stop. Total length 25 seconds. Swaggering, heroic, triumphant, full throttle. Raw analog 70s and
80s rock production, tape saturation, real amps, no click track feel, loud and live.
```

### Campo *Style* (versión corta)

```
Instrumental hard rock main title, harmonized twin lead guitars, thick power chord riff, slide
guitar, dirty Hammond organ, acoustic drums with cowbell, 136 BPM, key E, no synths, explosive
25 second intro, hard stop.
```

### Campo de letra (estructura con tiempos, 136 BPM → 1 compás = 1,76 s)

```
[0:00 Intro - 2 bars: tom fill into a screaming guitar pickup, no fade in]
[0:03 Main Riff - 4 bars: thick power chord riff, bass and drums lock in, cowbell]
[0:10 Twin Lead Theme - 7 bars: harmonized twin guitars play the main melody, highest energy]
[0:22 Ending - 1 bar: final open chord, crash cymbal, hard stop]
[End]
```

### Exclude Styles / negativos

```
vocals, singing, synthesizer, synth bass, synth brass, gated reverb snare, electronic drums, 80s
pop, long intro, fade in, fade out, slow build, quiet opening, ballad, lo-fi, trap hi-hats, EDM
```

> Si aun así se te cuela algún teclado, añade también `keyboard, piano, strings` a los negativos.
> Y si quieres un punto intermedio entre 1) y 1B), quita `synthesizer` del exclude y deja solo
> `synth bass, gated reverb snare`: conservas un golpe de sinte en los acentos con la base rockera.

### Títulos sugeridos
`Top Gas Overdrive` · `Kickstart` · `Twin Lead` · `Redline Theme`

---

## 2) FONDO INSTRUMENTAL PARA LOS VÍDEOS

Objetivo: acompañar sin molestar. Se pone **debajo de la voz, de motores y de cámara onboard**.
La regla de oro: nada de solos, nada de saltos de dinámica, hueco en los medios para la locución,
y que pueda repetirse en bucle sin cansar.

### Campo *Style of Music* (versión corta, segura)

```
Laid-back instrumental blues rock groove bed, dirty palm-muted overdriven guitar, subtle slide,
warm walking bass, relaxed live drums with rimshots, faint Hammond organ pad, 98 BPM, A minor,
steady hypnotic cruising feel, no solos, no dynamic jumps, loopable, mixed low with midrange space
for voiceover.
```

### Campo *Style of Music* (versión larga / v4.5+)

```
Background instrumental bed for motorcycle road videos. Genre: laid-back southern blues rock with
a touch of desert stoner groove. Tempo 95-102 BPM, key A minor, 4/4, steady and hypnotic, cruising
not racing. Instrumentation: gritty rhythm guitar with light overdrive and palm muting holding a
simple repeating two-bar riff, a distant lazy slide guitar adding colour, warm round bass locked
with the kick, relaxed live drum kit with rimshot backbeat and light ride, a faint Hammond organ
pad underneath, occasional tambourine. Arrangement: flat and consistent from start to finish, no
build ups, no drops, no guitar solos, no big fills, no silence. Production: warm analog, slightly
dry, restrained low end, carved midrange so a voiceover sits on top, moderate stereo width, quiet
and unobtrusive mix. Mood: confident, easy, open road, sunny asphalt, relaxed rider.
```

### Campo de letra (estructura)

```
[Intro: guitar riff alone, 2 bars]
[Groove: full band, steady, low intensity]
[Groove Variation: same energy, slide guitar colour]
[Groove: return to main riff]
[Outro: riff fades on last bar, clean loop point]
```

### Exclude Styles / negativos

```
vocals, singing, guitar solo, shredding, build up, drop, crescendo, orchestral hits, dramatic,
aggressive metal, double kick, trap hi-hats, EDM, silence, tempo change, key change
```

### Títulos sugeridos
`Cruise Control` · `Asphalt Idle` · `Two Lanes` · `Top Gas Groove`

---

## Variantes útiles del fondo (mismo ADN, distinto uso)

| Uso | Qué cambiar en el prompt |
|---|---|
| Rutas tranquilas / paisaje | `acoustic slide guitar, dobro, brushes on snare, 88 BPM, dusty desert americana` |
| Presentación de motos / detalle | `heavier fuzz riff, stoner rock, 105 BPM, thick bass, still no solos` |
| Quedadas / ambiente de grupo | `rock and roll shuffle, boogie piano, upbeat, 110 BPM, party garage feel` |
| Despedida / cierre de vídeo | `slow blues outro, clean reverb guitar, 72 BPM, warm and nostalgic, ends on a held chord` |

---

## Consejos de uso en Suno

1. **Instrumental ON** siempre: si no, mete voces aunque el prompt diga *instrumental*.
2. Genera **4–6 versiones** de cada uno y quédate con la que tenga mejor riff; el riff es lo que
   convierte una pista en "la sintonía de Top Gas".
3. Cuando tengas la cabecera buena, usa **Extend / Cover** sobre esa misma pista para sacar el
   fondo de los vídeos: así ambas comparten el mismo tema melódico y el canal suena coherente.
4. Para la cabecera, si quieres el rugido del V-twin, **no lo pidas a Suno** (lo hace mal):
   graba tu moto y móntalo encima en la edición, justo antes del primer acorde.
5. Sube ligeramente el *Style Influence* y baja *Weirdness* para el fondo (quieres previsibilidad);
   al revés para la cabecera si buscas un riff más original.
6. Exporta la cabecera con **final seco** (sin fade) y el fondo en **bucle limpio**.
