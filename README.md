# top-gas · Rutas en moto por Mallorca 🏍️

38 rutas en moto por Mallorca en formato **GPX, listas para subir a Wikiloc**, numeradas por dificultad y con un nombre que describe el recorrido.

Todas salen y vuelven a la **Gasolinera BP del polígono de Marratxí** (Es Figueral – Can Farineta, junto a la Ma-13A). El trazado va por carreteras reales y **evita autovías y autopistas** (Ma-1, Ma-13, Ma-19, Ma-20…). Se calcula con Valhalla sobre OpenStreetMap con el perfil de moto; si su mapa tiene un corte que no existe, ese tramo se toma de OSRM.

Además, las rutas están pensadas para que no haya dudas en ruta:

- **Pueblos de paso**: se cruzan o se bordean por el camino más directo; nunca se entra al centro para volver a salir por el mismo sitio. Solo se visitan las paradas (faros, santuarios, miradores, calas, castillos…).
- **Vuelta por otro camino**: la vuelta no repite la ida. Solo coinciden los últimos kilómetros junto a Marratxí, donde confluyen todas las carreteras, y las idas y vueltas obligadas a una parada en fondo de saco (un faro, Sa Calobra…).
- **GPX limpios**: en el GPX solo se marcan la gasolinera y las paradas, no los pueblos de paso.

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

Cada dificultad tiene su propia numeración desde el 1, y se distinguen por el color:

- 🟢 **Fácil (verde)**: rutas 1 a 13
- 🟡 **Media (amarilla)**: rutas 1 a 12
- 🔴 **Difícil (roja)**: rutas 1 a 13

Así, «la 3 roja» es la ruta Difícil 3. En los ficheros GPX el nombre empieza por la dificultad y el número (por ejemplo, *Difícil 3 · Sa Calobra y Nus de sa Corbata*).

Además de rutas sueltas hay varias series:

- **Vueltas a Mallorca**: la vuelta completa por la costa, la vuelta por todos los faros y dos medias vueltas (norte y sur).
- **Ruta Faros 1–5**: faros de la isla a los que se llega por carretera, agrupados por zonas.
- **Ruta Puigs 1–5**: subidas a puigs, santuarios y miradores en altura; más o menos cimas según la distancia.
- **Temáticas**: castillos, calas, Pla, vino, miradores de la Ma-10, Raiguer, Llevant…

### 🟢 Fácil (verdes)
| # | Ruta | Salida | Km | Conducción* | GPX |
|---|---|---|---|---|---|
| 1 | Costa de Poniente: Andratx y Sant Elm | 09:00 | 129 | 2 h 52 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-01-costa-de-poniente-andratx-y-sant-elm.gpx) |
| 2 | Migjorn: Cap Blanc y Colònia de Sant Jordi | 09:00 | 161 | 3 h 35 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-02-migjorn-cap-blanc-y-colonia-de-sant-jordi.gpx) |
| 3 | Pla de Mallorca: Sineu, Petra y Porreres | 09:00 | 97 | 2 h 09 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-03-pla-de-mallorca-sineu-petra-y-porreres.gpx) |
| 4 | Levante: Porto Cristo, Portocolom y Santanyí | 09:00 | 164 | 3 h 39 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-04-levante-porto-cristo-portocolom-y-santanyi.gpx) |
| 5 | Ruta Faros 1 · Sur: Cap Blanc, Ses Salines y Portocolom | 09:00 | 203 | 4 h 31 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-05-ruta-faros-1-sur-cap-blanc-ses-salines-y-portocolom.gpx) |
| 6 | Media Vuelta Sur: del Migjorn a Llevant | 09:00 | 237 | 5 h 16 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-06-media-vuelta-sur-del-migjorn-a-llevant.gpx) |
| 7 | Ruta Faros 4 · Llevant: Capdepera, Porto Cristo y Portocolom | 09:00 | 208 | 4 h 37 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-07-ruta-faros-4-llevant-capdepera-porto-cristo-y-portocolom.gpx) |
| 8 | Calas del Sur: Cala Pi, Llombards, Cala Figuera y Cala d'Or | 09:00 | 198 | 4 h 24 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-08-calas-del-sur-cala-pi-llombards-cala-figuera-y-cala-d-or.gpx) |
| 9 | Pla de Mallorca completo: pueblos del interior | 09:00 | 94 | 2 h 05 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-09-pla-de-mallorca-completo-pueblos-del-interior.gpx) |
| 10 | Ruta del Vino: Binissalem, Pla y Felanitx | 09:00 | 118 | 2 h 37 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-10-ruta-del-vino-binissalem-pla-y-felanitx.gpx) |
| 11 | Costa Norte: Alcúdia, Son Serra y Colònia de Sant Pere | 09:00 | 176 | 3 h 55 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-11-costa-norte-alcudia-son-serra-y-colonia-de-sant-pere.gpx) |
| 12 | Gran Ruta de Llevant: Cales de Mallorca, Canyamel y Cala Ratjada | 09:00 | 216 | 4 h 48 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-12-gran-ruta-de-llevant-cales-de-mallorca-canyamel-y-cala-ratjada.gpx) |
| 13 | Interior de Llevant: Vilafranca, Manacor y Son Macià | 09:00 | 124 | 2 h 45 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/facil-13-interior-de-llevant-vilafranca-manacor-y-son-macia.gpx) |

### 🟡 Media (amarillas)
| # | Ruta | Salida | Km | Conducción* | GPX |
|---|---|---|---|---|---|
| 1 | Valldemossa, Deià y Sóller | 09:00 | 62 | 1 h 23 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/media-01-valldemossa-deia-y-soller.gpx) |
| 2 | Galilea, Puigpunyent y Es Capdellà | 09:00 | 88 | 1 h 57 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/media-02-galilea-puigpunyent-y-es-capdella.gpx) |
| 3 | Santuari de Cura (Puig de Randa) | 09:00 | 72 | 1 h 36 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/media-03-santuari-de-cura-puig-de-randa.gpx) |
| 4 | Serra de Llevant: Artà y Cala Ratjada | 09:00 | 180 | 4 h 00 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/media-04-serra-de-llevant-arta-y-cala-ratjada.gpx) |
| 5 | Cap de Formentor | 08:30 | 162 | 3 h 36 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/media-05-cap-de-formentor.gpx) |
| 6 | Ruta Faros 5 · Bahías del Norte: Formentor, Alcanada y Capdepera | 08:30 | 242 | 5 h 23 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/media-06-ruta-faros-5-bahias-del-norte-formentor-alcanada-y-capdepera.gpx) |
| 7 | Ruta Puigs 1 · Pla: Cura, Sant Miquel, Monti-sion, Sant Salvador, Consolació y Bonany | 09:00 | 177 | 3 h 56 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/media-07-ruta-puigs-1-pla-cura-sant-miquel-monti-sion-sant-salvador-consolacio-y-bonany.gpx) |
| 8 | Ruta Puigs 3 · Llevant: Bonany, Castell de Capdepera, Sant Salvador d'Artà y Betlem | 09:00 | 190 | 4 h 13 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/media-08-ruta-puigs-3-llevant-bonany-castell-de-capdepera-sant-salvador-d-arta-y-betlem.gpx) |
| 9 | Ruta de los Castillos: Bellver, Santueri y Capdepera | 09:00 | 231 | 5 h 08 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/media-09-ruta-de-los-castillos-bellver-santueri-y-capdepera.gpx) |
| 10 | Raiguer completo: de Alaró a sa Pobla | 09:00 | 93 | 2 h 04 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/media-10-raiguer-completo-de-alaro-a-sa-pobla.gpx) |
| 11 | Tramuntana Sur: Calvià, Andratx, Estellencs y Esporles | 09:00 | 95 | 2 h 07 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/media-11-tramuntana-sur-calvia-andratx-estellencs-y-esporles.gpx) |
| 12 | Valle de Sóller: Port de Sóller, Fornalutx, Deià y Valldemossa | 09:00 | 93 | 2 h 04 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/media-12-valle-de-soller-port-de-soller-fornalutx-deia-y-valldemossa.gpx) |

### 🔴 Difícil (rojas)
| # | Ruta | Salida | Km | Conducción* | GPX |
|---|---|---|---|---|---|
| 1 | Orient y Castell d'Alaró | 09:00 | 57 | 1 h 16 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-01-orient-y-castell-d-alaro.gpx) |
| 2 | Ma-10 completa: Andratx – Pollença | 08:30 | 208 | 4 h 37 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-02-ma-10-completa-andratx-pollenca.gpx) |
| 3 | Sa Calobra y Nus de sa Corbata | 08:30 | 121 | 2 h 41 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-03-sa-calobra-y-nus-de-sa-corbata.gpx) |
| 4 | Gran Vuelta Tramuntana: Sóller, Sa Calobra y Formentor | 08:30 | 198 | 4 h 24 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-04-gran-vuelta-tramuntana-soller-sa-calobra-y-formentor.gpx) |
| 5 | Ruta Faros 2 · Norte: Cap Gros y Formentor | 08:30 | 188 | 4 h 11 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-05-ruta-faros-2-norte-cap-gros-y-formentor.gpx) |
| 6 | Vuelta a Mallorca por la costa | 08:00 | 360 | 8 h 00 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-06-vuelta-a-mallorca-por-la-costa.gpx) |
| 7 | Vuelta a Mallorca por todos los faros | 08:00 | 486 | 10 h 48 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-07-vuelta-a-mallorca-por-todos-los-faros.gpx) |
| 8 | Media Vuelta Norte: de Andratx a Artà | 08:30 | 282 | 6 h 16 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-08-media-vuelta-norte-de-andratx-a-arta.gpx) |
| 9 | Ruta Faros 3 · Poniente: Sa Mola y Cap Gros | 08:30 | 151 | 3 h 21 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-09-ruta-faros-3-poniente-sa-mola-y-cap-gros.gpx) |
| 10 | Ruta Puigs 2 · Raiguer y Norte: Santa Magdalena, La Victòria, Lluc y Castell d'Alaró | 08:30 | 148 | 3 h 17 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-10-ruta-puigs-2-raiguer-y-norte-santa-magdalena-la-victoria-lluc-y-castell-d-alaro.gpx) |
| 11 | Ruta Puigs 4 · Gran Ruta de los Puigs | 08:30 | 236 | 5 h 15 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-11-ruta-puigs-4-gran-ruta-de-los-puigs.gpx) |
| 12 | Ruta Puigs 5 · Ponent y Tramuntana: Na Burguesa, sa Gramola, Trinitat y Ses Barques | 08:30 | 150 | 3 h 20 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-12-ruta-puigs-5-ponent-y-tramuntana-na-burguesa-sa-gramola-trinitat-y-ses-barques.gpx) |
| 13 | Miradores de la Ma-10: de sa Gramola a Ses Barques | 08:30 | 181 | 4 h 01 min | [Descargar](https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/dificil-13-miradores-de-la-ma-10-de-sa-gramola-a-ses-barques.gpx) |

\* Tiempo de conducción estimado sin paradas, a una media de 45 km/h (ritmo tranquilo de moto por carreteras secundarias). Con paradas, las rutas largas salen a las 8:30–9:00 y vuelven a partir de las 15:00. Las dos vueltas completas son jornadas excepcionales: salida a las 8:00 y vuelta por la tarde-noche.

## Cómo subir una ruta a Wikiloc

1. Pulsa **Descargar** en la ruta (aquí o en la web del catálogo). Se baja el archivo `.gpx` directamente al móvil u ordenador.
2. Entra en wikiloc.com con tu cuenta y pulsa **Subir → Subir ruta**.
3. Elige el archivo `.gpx` que acabas de descargar (en el móvil suele estar en la carpeta *Descargas*).
4. Pon como actividad **Moto** y elige la dificultad (Fácil / Moderado / Difícil). El nombre y la descripción ya vienen en el GPX; revisa y publica.

Todos los GPX están también en la página de descargas del repositorio: https://github.com/rortizlotum-ops/top-gas/releases/tag/gpx

Wikiloc también funciona como *"Seguir ruta"* en la app del móvil, así que puedes llevarla en el manillar.

## Avisos

- Algunas carreteras (Formentor, Sa Calobra) pueden **cerrarse o restringirse** para vehículos privados en temporada alta. Consulta al Consell de Mallorca antes de salir.
- En la Tramuntana hay muchos **ciclistas**, sobre todo los fines de semana por la mañana. Adelanta con margen.
- Si llueve, cambia las rutas difíciles por una fácil del sur o del Pla.
- El recorrido lo calcula un planificador automático. Antes de salir, revisa el track en el mapa de Wikiloc.
