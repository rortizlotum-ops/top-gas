# top-gas · Rutas en moto por Mallorca 🏍️

13 rutas en moto por Mallorca en formato **GPX, listas para subir a Wikiloc**. Están clasificadas por dificultad y repartidas en un **calendario de domingos** (del 18 de octubre de 2026 al 10 de enero de 2027).

Todas salen y vuelven a **Palma (Plaça d'Espanya)**. El trazado va por carreteras reales y **evita autovías y autopistas** (Ma-1, Ma-13, Ma-19, Ma-20…). Se calculó con Valhalla sobre OpenStreetMap, con el perfil de moto, obligándolo a pasar por los puntos de cada ruta. Para ir hacia Inca se usa la carretera vieja por Santa Maria y Binissalem.

## Contenido

| Fichero | Qué es |
|---|---|
| `rutas/*.gpx` | Un GPX por ruta: el track y los waypoints de los puntos de interés |
| `calendario-domingos.ics` | Calendario con una ruta cada domingo (Google Calendar, Apple, Outlook…) |
| `rutas/resumen.json` | Resumen en datos: fecha, km, horas y fichero |
| `scripts/generar_rutas.py` | Script que genera todo lo anterior (`python3 scripts/generar_rutas.py`) |

## Criterios de dificultad

- 🟢 **Fácil**: carreteras anchas y bien asfaltadas, con curvas suaves y poco desnivel. Apta para cualquier moto y para quien empieza.
- 🟡 **Media**: tramos de montaña con curvas enlazadas, algún paso estrecho o mucho tráfico turístico. Hace falta soltura en curva.
- 🔴 **Difícil**: horquillas cerradas, carreteras estrechas o bacheadas, desniveles fuertes y jornadas largas por la Serra de Tramuntana. Para pilotos con experiencia.

## Catálogo por dificultad

### 🟢 Fácil
| # | Ruta | Km | Conducción* | GPX |
|---|---|---|---|---|
| 01 | Costa de Poniente: Andratx y Sant Elm | 89 | 1 h 59 min | [GPX](rutas/01-facil-costa-de-poniente-andratx-y-sant-elm.gpx) |
| 02 | Migjorn: Cap Blanc y Colònia de Sant Jordi | 168 | 3 h 44 min | [GPX](rutas/02-facil-migjorn-cap-blanc-y-colonia-de-sant-jordi.gpx) |
| 03 | Pla de Mallorca: Sineu, Petra y Porreres | 122 | 2 h 43 min | [GPX](rutas/03-facil-pla-de-mallorca-sineu-petra-y-porreres.gpx) |
| 04 | Levante: Porto Cristo, Portocolom y Santanyí | 189 | 4 h 12 min | [GPX](rutas/04-facil-levante-porto-cristo-portocolom-y-santanyi.gpx) |

### 🟡 Media
| # | Ruta | Km | Conducción* | GPX |
|---|---|---|---|---|
| 05 | Valldemossa, Deià y Sóller (vuelta por el Coll de Sóller) | 72 | 1 h 36 min | [GPX](rutas/05-media-valldemossa-deia-y-soller.gpx) |
| 06 | Galilea, Puigpunyent y Es Capdellà | 59 | 1 h 19 min | [GPX](rutas/06-media-galilea-puigpunyent-y-es-capdella.gpx) |
| 07 | Santuari de Cura (Puig de Randa) | 75 | 1 h 40 min | [GPX](rutas/07-media-santuari-de-cura-puig-de-randa.gpx) |
| 08 | Serra de Llevant: Artà y Cala Ratjada | 183 | 4 h 04 min | [GPX](rutas/08-media-serra-de-llevant-arta-y-cala-ratjada.gpx) |
| 09 | Cap de Formentor | 180 | 4 h 00 min | [GPX](rutas/09-media-cap-de-formentor.gpx) |

### 🔴 Difícil
| # | Ruta | Km | Conducción* | GPX |
|---|---|---|---|---|
| 10 | Orient y Castell d'Alaró | 73 | 1 h 37 min | [GPX](rutas/10-dificil-orient-y-castell-d-alaro.gpx) |
| 11 | Ma-10 completa: Andratx – Pollença | 206 | 4 h 35 min | [GPX](rutas/11-dificil-ma-10-completa-andratx-pollenca.gpx) |
| 12 | Sa Calobra y Nus de sa Corbata | 153 | 3 h 24 min | [GPX](rutas/12-dificil-sa-calobra-y-nus-de-sa-corbata.gpx) |
| 13 | Gran Vuelta Tramuntana: Sóller, Sa Calobra y Formentor | 223 | 4 h 57 min | [GPX](rutas/13-dificil-gran-vuelta-tramuntana-soller-sa-calobra-y-formentor.gpx) |

\* Tiempo de conducción estimado sin paradas. Calculado a una media de 45 km/h, un ritmo tranquilo de moto por carreteras secundarias. En el calendario cada evento dura más porque incluye paradas y café.

## 📅 Calendario de domingos

La dificultad va subiendo poco a poco y se van alternando zonas. Las rutas largas de la Tramuntana quedan para diciembre y enero, cuando hay menos turistas y ciclistas.

| Domingo | Salida | Dificultad | Ruta | Km |
|---|---|---|---|---|
| 18 oct 2026 | 09:30 | 🟢 Fácil | 01 · Costa de Poniente: Andratx y Sant Elm | 89 |
| 25 oct 2026 | 09:30 | 🟢 Fácil | 02 · Migjorn: Cap Blanc y Colònia de Sant Jordi | 168 |
| 1 nov 2026 | 09:00 | 🟡 Media | 05 · Valldemossa, Deià y Sóller | 72 |
| 8 nov 2026 | 09:30 | 🟢 Fácil | 03 · Pla de Mallorca: Sineu, Petra y Porreres | 122 |
| 15 nov 2026 | 09:30 | 🟡 Media | 06 · Galilea, Puigpunyent y Es Capdellà | 59 |
| 22 nov 2026 | 09:00 | 🟢 Fácil | 04 · Levante: Porto Cristo, Portocolom y Santanyí | 189 |
| 29 nov 2026 | 10:00 | 🟡 Media | 07 · Santuari de Cura (Puig de Randa) | 75 |
| 6 dic 2026 | 09:00 | 🔴 Difícil | 10 · Orient y Castell d'Alaró | 73 |
| 13 dic 2026 | 09:00 | 🟡 Media | 08 · Serra de Llevant: Artà y Cala Ratjada | 183 |
| 20 dic 2026 | 08:30 | 🟡 Media | 09 · Cap de Formentor | 180 |
| 27 dic 2026 | 08:00 | 🔴 Difícil | 12 · Sa Calobra y Nus de sa Corbata | 153 |
| 3 ene 2027 | 08:00 | 🔴 Difícil | 11 · Ma-10 completa: Andratx – Pollença | 206 |
| 10 ene 2027 | 07:30 | 🔴 Difícil | 13 · Gran Vuelta Tramuntana | 223 |

Para meterlo en tu agenda, importa `calendario-domingos.ics`. En Google Calendar: *Configuración → Importar y exportar → Importar*.

## Cómo subir una ruta a Wikiloc

1. Entra en wikiloc.com con tu cuenta y pulsa **Subir → Subir ruta**.
2. Elige el fichero `.gpx` de la ruta.
3. Pon como actividad **Moto** y elige la dificultad (Fácil / Moderado / Difícil) según la tabla.
4. El nombre y la descripción ya vienen en el GPX; revisa y publica.

Wikiloc también funciona como *"Seguir ruta"* en la app del móvil, así que puedes llevarla en el manillar.

## Avisos

- Algunas carreteras (Formentor, Sa Calobra) pueden **cerrarse o restringirse** para vehículos privados en temporada alta. Consulta al Consell de Mallorca antes de salir.
- En la Tramuntana hay muchos **ciclistas**, sobre todo los domingos por la mañana. Adelanta con margen.
- Si llueve en diciembre o enero, cambia las rutas difíciles por una fácil del sur o del Pla.
- El recorrido lo calcula un planificador automático. Antes de salir, revisa el track en el mapa de Wikiloc.
