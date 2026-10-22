# top-gas · Rutas en moto por Mallorca 🏍️

38 rutas en moto por Mallorca en formato **GPX, listas para subir a Wikiloc**, numeradas por dificultad y con un nombre que describe el recorrido.

Todas salen y vuelven a la **Gasolinera BP del polígono de Marratxí** (Es Figueral – Can Farineta, junto a la Ma-13A). El trazado va por carreteras reales y **evita autovías y autopistas** (Ma-1, Ma-13, Ma-19, Ma-20…). Se calculó con Valhalla sobre OpenStreetMap, con el perfil de moto, obligándolo a pasar por los puntos de cada ruta. Para ir hacia Inca se usa la carretera vieja por Santa Maria y Binissalem.

## Contenido

| Fichero | Qué es |
|---|---|
| `rutas/*.gpx` | Un GPX por ruta: el track y los waypoints de los puntos de interés |
| `rutas/resumen.json` | Resumen en datos de todas las rutas: km, horas y fichero |
| `scripts/generar_rutas.py` | Script que genera todo lo anterior (`python3 scripts/generar_rutas.py`) |

## Criterios de dificultad

- 🟢 **Fácil**: carreteras anchas y bien asfaltadas, con curvas suaves y poco desnivel. Apta para cualquier moto y para quien empieza.
- 🟡 **Media**: tramos de montaña con curvas enlazadas, algún paso estrecho o mucho tráfico turístico. Hace falta soltura en curva.
- 🔴 **Difícil**: horquillas cerradas, carreteras estrechas o bacheadas, desniveles fuertes y jornadas largas por la Serra de Tramuntana. Para pilotos con experiencia.

## Catálogo por dificultad

Las rutas están numeradas por dificultad: **1–13 fáciles, 14–25 medias y 26–38 difíciles**.

Además de rutas sueltas hay varias series:

- **Vueltas a Mallorca**: la vuelta completa por la costa, la vuelta por todos los faros y dos medias vueltas (norte y sur).
- **Ruta Faros 1–5**: faros de la isla a los que se llega por carretera, agrupados por zonas.
- **Ruta Puigs 1–5**: subidas a puigs, santuarios y miradores en altura; más o menos cimas según la distancia.
- **Temáticas**: castillos, calas, Pla, vino, miradores de la Ma-10, Raiguer, Llevant…

### 🟢 Fácil
| # | Ruta | Salida | Km | Conducción* | GPX |
|---|---|---|---|---|---|
| 01 | Costa de Poniente: Andratx y Sant Elm | 09:00 | 127 | 2 h 49 min | [GPX](rutas/01-facil-costa-de-poniente-andratx-y-sant-elm.gpx) |
| 02 | Migjorn: Cap Blanc y Colònia de Sant Jordi | 09:00 | 165 | 3 h 40 min | [GPX](rutas/02-facil-migjorn-cap-blanc-y-colonia-de-sant-jordi.gpx) |
| 03 | Pla de Mallorca: Sineu, Petra y Porreres | 09:00 | 100 | 2 h 13 min | [GPX](rutas/03-facil-pla-de-mallorca-sineu-petra-y-porreres.gpx) |
| 04 | Levante: Porto Cristo, Portocolom y Santanyí | 09:00 | 177 | 3 h 56 min | [GPX](rutas/04-facil-levante-porto-cristo-portocolom-y-santanyi.gpx) |
| 05 | Ruta Faros 1 · Sur: Cap Blanc, Ses Salines y Portocolom | 09:00 | 202 | 4 h 29 min | [GPX](rutas/05-facil-ruta-faros-1-sur-cap-blanc-ses-salines-y-portocolom.gpx) |
| 06 | Media Vuelta Sur: del Migjorn a Llevant | 09:00 | 257 | 5 h 43 min | [GPX](rutas/06-facil-media-vuelta-sur-del-migjorn-a-llevant.gpx) |
| 07 | Ruta Faros 4 · Llevant: Capdepera, Porto Cristo y Portocolom | 09:00 | 209 | 4 h 39 min | [GPX](rutas/07-facil-ruta-faros-4-llevant-capdepera-porto-cristo-y-portocolom.gpx) |
| 08 | Calas del Sur: Cala Pi, Llombards, Cala Figuera y Cala d'Or | 09:00 | 192 | 4 h 16 min | [GPX](rutas/08-facil-calas-del-sur-cala-pi-llombards-cala-figuera-y-cala-d-or.gpx) |
| 09 | Pla de Mallorca completo: pueblos del interior | 09:00 | 115 | 2 h 33 min | [GPX](rutas/09-facil-pla-de-mallorca-completo-pueblos-del-interior.gpx) |
| 10 | Ruta del Vino: Binissalem, Pla y Felanitx | 09:00 | 122 | 2 h 43 min | [GPX](rutas/10-facil-ruta-del-vino-binissalem-pla-y-felanitx.gpx) |
| 11 | Costa Norte: Alcúdia, Son Serra y Colònia de Sant Pere | 09:00 | 182 | 4 h 03 min | [GPX](rutas/11-facil-costa-norte-alcudia-son-serra-y-colonia-de-sant-pere.gpx) |
| 12 | Gran Ruta de Llevant: Cales de Mallorca, Canyamel y Cala Ratjada | 09:00 | 207 | 4 h 36 min | [GPX](rutas/12-facil-gran-ruta-de-llevant-cales-de-mallorca-canyamel-y-cala-ratjada.gpx) |
| 13 | Interior de Llevant: Vilafranca, Sant Llorenç y Son Macià | 09:00 | 153 | 3 h 24 min | [GPX](rutas/13-facil-interior-de-llevant-vilafranca-sant-llorenc-y-son-macia.gpx) |

### 🟡 Media
| # | Ruta | Salida | Km | Conducción* | GPX |
|---|---|---|---|---|---|
| 14 | Valldemossa, Deià y Sóller | 09:00 | 69 | 1 h 32 min | [GPX](rutas/14-media-valldemossa-deia-y-soller.gpx) |
| 15 | Galilea, Puigpunyent y Es Capdellà | 09:00 | 93 | 2 h 04 min | [GPX](rutas/15-media-galilea-puigpunyent-y-es-capdella.gpx) |
| 16 | Santuari de Cura (Puig de Randa) | 09:00 | 73 | 1 h 37 min | [GPX](rutas/16-media-santuari-de-cura-puig-de-randa.gpx) |
| 17 | Serra de Llevant: Artà y Cala Ratjada | 09:00 | 171 | 3 h 48 min | [GPX](rutas/17-media-serra-de-llevant-arta-y-cala-ratjada.gpx) |
| 18 | Cap de Formentor | 08:30 | 155 | 3 h 27 min | [GPX](rutas/18-media-cap-de-formentor.gpx) |
| 19 | Ruta Faros 5 · Bahías del Norte: Formentor, Alcanada y Capdepera | 08:30 | 251 | 5 h 35 min | [GPX](rutas/19-media-ruta-faros-5-bahias-del-norte-formentor-alcanada-y-capdepera.gpx) |
| 20 | Ruta Puigs 1 · Pla: Sant Miquel, Cura, Monti-sion, Sant Salvador, Consolació y Bonany | 09:00 | 194 | 4 h 19 min | [GPX](rutas/20-media-ruta-puigs-1-pla-sant-miquel-cura-monti-sion-sant-salvador-consolacio-y-bonany.gpx) |
| 21 | Ruta Puigs 3 · Llevant: Bonany, Sant Salvador d'Artà, Betlem y Castell de Capdepera | 09:00 | 196 | 4 h 21 min | [GPX](rutas/21-media-ruta-puigs-3-llevant-bonany-sant-salvador-d-arta-betlem-y-castell-de-capdepera.gpx) |
| 22 | Ruta de los Castillos: Bellver, Santueri y Capdepera | 09:00 | 228 | 5 h 04 min | [GPX](rutas/22-media-ruta-de-los-castillos-bellver-santueri-y-capdepera.gpx) |
| 23 | Raiguer completo: de Alaró a sa Pobla | 09:00 | 96 | 2 h 08 min | [GPX](rutas/23-media-raiguer-completo-de-alaro-a-sa-pobla.gpx) |
| 24 | Tramuntana Sur: Galilea, Andratx, Estellencs y Esporles | 09:00 | 113 | 2 h 31 min | [GPX](rutas/24-media-tramuntana-sur-galilea-andratx-estellencs-y-esporles.gpx) |
| 25 | Valle de Sóller: Port de Sóller, Fornalutx, Deià y Valldemossa | 09:00 | 103 | 2 h 17 min | [GPX](rutas/25-media-valle-de-soller-port-de-soller-fornalutx-deia-y-valldemossa.gpx) |

### 🔴 Difícil
| # | Ruta | Salida | Km | Conducción* | GPX |
|---|---|---|---|---|---|
| 26 | Orient y Castell d'Alaró | 09:00 | 60 | 1 h 20 min | [GPX](rutas/26-dificil-orient-y-castell-d-alaro.gpx) |
| 27 | Ma-10 completa: Andratx – Pollença | 08:30 | 218 | 4 h 51 min | [GPX](rutas/27-dificil-ma-10-completa-andratx-pollenca.gpx) |
| 28 | Sa Calobra y Nus de sa Corbata | 08:30 | 128 | 2 h 51 min | [GPX](rutas/28-dificil-sa-calobra-y-nus-de-sa-corbata.gpx) |
| 29 | Gran Vuelta Tramuntana: Sóller, Sa Calobra y Formentor | 08:30 | 215 | 4 h 47 min | [GPX](rutas/29-dificil-gran-vuelta-tramuntana-soller-sa-calobra-y-formentor.gpx) |
| 30 | Ruta Faros 2 · Norte: Cap Gros y Formentor | 08:30 | 204 | 4 h 32 min | [GPX](rutas/30-dificil-ruta-faros-2-norte-cap-gros-y-formentor.gpx) |
| 31 | Vuelta a Mallorca por la costa | 08:00 | 383 | 8 h 31 min | [GPX](rutas/31-dificil-vuelta-a-mallorca-por-la-costa.gpx) |
| 32 | Vuelta a Mallorca por todos los faros | 08:00 | 512 | 11 h 23 min | [GPX](rutas/32-dificil-vuelta-a-mallorca-por-todos-los-faros.gpx) |
| 33 | Media Vuelta Norte: de Andratx a Artà | 08:30 | 294 | 6 h 32 min | [GPX](rutas/33-dificil-media-vuelta-norte-de-andratx-a-arta.gpx) |
| 34 | Ruta Faros 3 · Poniente: Sa Mola y Cap Gros | 08:30 | 181 | 4 h 01 min | [GPX](rutas/34-dificil-ruta-faros-3-poniente-sa-mola-y-cap-gros.gpx) |
| 35 | Ruta Puigs 2 · Raiguer y Norte: Santa Magdalena, La Victòria, Lluc y Castell d'Alaró | 08:30 | 156 | 3 h 28 min | [GPX](rutas/35-dificil-ruta-puigs-2-raiguer-y-norte-santa-magdalena-la-victoria-lluc-y-castell-d-alaro.gpx) |
| 36 | Ruta Puigs 4 · Gran Ruta de los Puigs | 08:30 | 238 | 5 h 17 min | [GPX](rutas/36-dificil-ruta-puigs-4-gran-ruta-de-los-puigs.gpx) |
| 37 | Ruta Puigs 5 · Ponent y Tramuntana: Na Burguesa, sa Gramola, Trinitat y Ses Barques | 08:30 | 160 | 3 h 33 min | [GPX](rutas/37-dificil-ruta-puigs-5-ponent-y-tramuntana-na-burguesa-sa-gramola-trinitat-y-ses-barques.gpx) |
| 38 | Miradores de la Ma-10: de sa Gramola a Ses Barques | 08:30 | 188 | 4 h 11 min | [GPX](rutas/38-dificil-miradores-de-la-ma-10-de-sa-gramola-a-ses-barques.gpx) |

\* Tiempo de conducción estimado sin paradas, a una media de 45 km/h (ritmo tranquilo de moto por carreteras secundarias). Con paradas, las rutas largas salen a las 8:30–9:00 y vuelven a partir de las 15:00. Las dos vueltas completas son jornadas excepcionales: salida a las 8:00 y vuelta por la tarde-noche.

## Cómo subir una ruta a Wikiloc

1. Entra en wikiloc.com con tu cuenta y pulsa **Subir → Subir ruta**.
2. Elige el fichero `.gpx` de la ruta.
3. Pon como actividad **Moto** y elige la dificultad (Fácil / Moderado / Difícil) según la tabla.
4. El nombre y la descripción ya vienen en el GPX; revisa y publica.

Wikiloc también funciona como *"Seguir ruta"* en la app del móvil, así que puedes llevarla en el manillar.

## Avisos

- Algunas carreteras (Formentor, Sa Calobra) pueden **cerrarse o restringirse** para vehículos privados en temporada alta. Consulta al Consell de Mallorca antes de salir.
- En la Tramuntana hay muchos **ciclistas**, sobre todo los fines de semana por la mañana. Adelanta con margen.
- Si llueve, cambia las rutas difíciles por una fácil del sur o del Pla.
- El recorrido lo calcula un planificador automático. Antes de salir, revisa el track en el mapa de Wikiloc.
