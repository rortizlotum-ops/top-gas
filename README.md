# top-gas · Rutas en moto por Mallorca 🏍️

15 rutas en moto por Mallorca en formato **GPX, listas para subir a Wikiloc**, numeradas por dificultad. Las fechas de cada ruta se van asignando en el **calendario de domingos**.

Todas salen y vuelven a la **Gasolinera BP del polígono de Marratxí** (Es Figueral – Can Farineta, junto a la Ma-13A). El trazado va por carreteras reales y **evita autovías y autopistas** (Ma-1, Ma-13, Ma-19, Ma-20…). Se calculó con Valhalla sobre OpenStreetMap, con el perfil de moto, obligándolo a pasar por los puntos de cada ruta. Para ir hacia Inca se usa la carretera vieja por Santa Maria y Binissalem.

## Contenido

| Fichero | Qué es |
|---|---|
| `rutas/*.gpx` | Un GPX por ruta: el track y los waypoints de los puntos de interés |
| `calendario-domingos.ics` | Calendario con una ruta cada domingo (Google Calendar, Apple, Outlook…) |
| `rutas/resumen.json` | Resumen en datos de las 15 rutas: km, horas, fichero y fecha si ya la tiene |
| `scripts/generar_rutas.py` | Script que genera todo lo anterior (`python3 scripts/generar_rutas.py`) |

## Criterios de dificultad

- 🟢 **Fácil**: carreteras anchas y bien asfaltadas, con curvas suaves y poco desnivel. Apta para cualquier moto y para quien empieza.
- 🟡 **Media**: tramos de montaña con curvas enlazadas, algún paso estrecho o mucho tráfico turístico. Hace falta soltura en curva.
- 🔴 **Difícil**: horquillas cerradas, carreteras estrechas o bacheadas, desniveles fuertes y jornadas largas por la Serra de Tramuntana. Para pilotos con experiencia.

## Catálogo por dificultad

Las rutas están numeradas por dificultad: **1–5 fáciles, 6–10 medias y 11–15 difíciles**.

### 🟢 Fácil
| # | Ruta | Km | Conducción* | GPX |
|---|---|---|---|---|
| 01 | Costa de Poniente: Andratx y Sant Elm | 127 | 2 h 49 min | [GPX](rutas/01-facil-costa-de-poniente-andratx-y-sant-elm.gpx) |
| 02 | Migjorn: Cap Blanc y Colònia de Sant Jordi | 165 | 3 h 40 min | [GPX](rutas/02-facil-migjorn-cap-blanc-y-colonia-de-sant-jordi.gpx) |
| 03 | Pla de Mallorca: Sineu, Petra y Porreres | 99 | 2 h 12 min | [GPX](rutas/03-facil-pla-de-mallorca-sineu-petra-y-porreres.gpx) |
| 04 | Levante: Porto Cristo, Portocolom y Santanyí | 177 | 3 h 56 min | [GPX](rutas/04-facil-levante-porto-cristo-portocolom-y-santanyi.gpx) |
| 05 | Faros del Sur: Cap Blanc, Ses Salines y Portocolom | 202 | 4 h 29 min | [GPX](rutas/05-facil-faros-del-sur-cap-blanc-ses-salines-y-portocolom.gpx) |

### 🟡 Media
| # | Ruta | Km | Conducción* | GPX |
|---|---|---|---|---|
| 06 | Valldemossa, Deià y Sóller | 69 | 1 h 32 min | [GPX](rutas/06-media-valldemossa-deia-y-soller.gpx) |
| 07 | Galilea, Puigpunyent y Es Capdellà | 93 | 2 h 04 min | [GPX](rutas/07-media-galilea-puigpunyent-y-es-capdella.gpx) |
| 08 | Santuari de Cura (Puig de Randa) | 73 | 1 h 37 min | [GPX](rutas/08-media-santuari-de-cura-puig-de-randa.gpx) |
| 09 | Serra de Llevant: Artà y Cala Ratjada | 170 | 3 h 47 min | [GPX](rutas/09-media-serra-de-llevant-arta-y-cala-ratjada.gpx) |
| 10 | Cap de Formentor | 156 | 3 h 28 min | [GPX](rutas/10-media-cap-de-formentor.gpx) |

### 🔴 Difícil
| # | Ruta | Km | Conducción* | GPX |
|---|---|---|---|---|
| 11 | Orient y Castell d'Alaró | 60 | 1 h 20 min | [GPX](rutas/11-dificil-orient-y-castell-d-alaro.gpx) |
| 12 | Ma-10 completa: Andratx – Pollença | 217 | 4 h 49 min | [GPX](rutas/12-dificil-ma-10-completa-andratx-pollenca.gpx) |
| 13 | Sa Calobra y Nus de sa Corbata | 128 | 2 h 51 min | [GPX](rutas/13-dificil-sa-calobra-y-nus-de-sa-corbata.gpx) |
| 14 | Gran Vuelta Tramuntana: Sóller, Sa Calobra y Formentor | 214 | 4 h 45 min | [GPX](rutas/14-dificil-gran-vuelta-tramuntana-soller-sa-calobra-y-formentor.gpx) |
| 15 | Faros del Norte: Cap Gros y Formentor | 204 | 4 h 32 min | [GPX](rutas/15-dificil-faros-del-norte-cap-gros-y-formentor.gpx) |

\* Tiempo de conducción estimado sin paradas. Calculado a una media de 45 km/h, un ritmo tranquilo de moto por carreteras secundarias. En el calendario cada evento dura más porque incluye paradas y café.

## 📅 Calendario de domingos

| Domingo | Salida | Dificultad | Ruta | Km |
|---|---|---|---|---|
| 18 oct 2026 | 09:30 | 🟢 Fácil | 01 · Costa de Poniente: Andratx y Sant Elm | 127 |
| 25 oct 2026 | 09:30 | 🟢 Fácil | 02 · Migjorn: Cap Blanc y Colònia de Sant Jordi | 165 |
| 1 nov 2026 | 09:00 | 🟡 Media | 06 · Valldemossa, Deià y Sóller | 69 |
| 8 nov 2026 | 09:30 | 🟢 Fácil | 03 · Pla de Mallorca: Sineu, Petra y Porreres | 99 |
| 15 nov 2026 | 09:30 | 🟡 Media | 07 · Galilea, Puigpunyent y Es Capdellà | 93 |
| 22 nov 2026 | 09:00 | 🟢 Fácil | 04 · Levante: Porto Cristo, Portocolom y Santanyí | 177 |
| 29 nov 2026 | 10:00 | 🟡 Media | 08 · Santuari de Cura (Puig de Randa) | 73 |
| 6 dic 2026 | 09:00 | 🔴 Difícil | 11 · Orient y Castell d'Alaró | 60 |
| 13 dic 2026 | 09:00 | 🟡 Media | 09 · Serra de Llevant: Artà y Cala Ratjada | 170 |
| 20 dic 2026 | 08:30 | 🟡 Media | 10 · Cap de Formentor | 156 |
| 27 dic 2026 | 08:00 | 🔴 Difícil | 13 · Sa Calobra y Nus de sa Corbata | 128 |
| 3 ene 2027 | 08:00 | 🔴 Difícil | 12 · Ma-10 completa: Andratx – Pollença | 217 |
| 10 ene 2027 | 07:30 | 🔴 Difícil | 14 · Gran Vuelta Tramuntana: Sóller, Sa Calobra y Formentor | 214 |

Este reparto de fechas está pendiente de revisar: las rutas 05 y 15 todavía no tienen día asignado.

Para meterlo en tu agenda, importa `calendario-domingos.ics`. En Google Calendar: *Configuración → Importar y exportar → Importar*. Cada evento lleva el enlace de descarga directa de su GPX para Wikiloc (funciona cuando el repositorio es público).

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
