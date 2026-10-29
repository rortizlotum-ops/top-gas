#!/usr/bin/env python3
"""Genera las rutas en moto por Mallorca (GPX para Wikiloc) y su resumen (rutas/resumen.json).

Uso:  python3 scripts/generar_rutas.py

El trazado se calcula sobre carreteras reales con Valhalla (valhalla1.openstreetmap.de),
perfil de moto y SIN autovías, forzando el paso por los puntos de cada ruta para que
siga las carreteras elegidas. El script avisa si algún tramo acaba en autovía.
"""
import json
import math
import time
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
GPX_DIR = ROOT / "rutas"
VALHALLA = "https://valhalla1.openstreetmap.de/route"

SALIDA = ("Gasolinera BP · Polígono de Marratxí", 39.6259, 2.7238)

# Lugares de paso (nombre -> (nombre, lat, lon)), comprobados con OpenStreetMap.
_LUGARES = """
Palma|39.5760|2.6553
Carretera de Galilea|39.6058|2.4967
Son Ferriol|39.5749|2.7168
Sant Jordi|39.5544|2.7779
Establiments|39.6201|2.6247
Cala Major|39.5542|2.6091
Palmanova|39.5225|2.5390
Santa Eugènia|39.6227|2.8366
Biniali|39.6404|2.8599
Pina|39.5992|2.9246
Randa|39.5268|2.9150
Port d'Andratx|39.5436|2.3866
Sant Elm (mirador de Sa Dragonera)|39.5791|2.3540
S'Arracó|39.5842|2.3900
Mirador Es Colomer|39.9235|3.1178
Coll dels Reis|39.8298|2.8425
Sa Calobra|39.8510|2.8063
Orient|39.7294|2.7408
Portals Nous|39.5350|2.5705
Santa Ponça|39.5148|2.4820
Calvià|39.5658|2.5047
Andratx|39.5756|2.4206
Puigpunyent|39.6247|2.5264
Galilea|39.6117|2.4839
Es Capdellà|39.5761|2.4617
Estellencs|39.6536|2.4800
Banyalbufar|39.6878|2.5147
Esporles|39.6692|2.5776
Valldemossa|39.7108|2.6225
Deià|39.7481|2.6492
Sóller|39.7667|2.7150
Port de Sóller|39.7975|2.6956
Fornalutx|39.7822|2.7408
Coll de Sóller|39.7358|2.6902
Bunyola|39.6961|2.6997
Embalse de Cúber|39.7880|2.8000
Embalse del Gorg Blau|39.8050|2.8193
Santuari de Lluc|39.8217|2.8847
Pollença|39.8772|3.0161
Port de Pollença|39.9075|3.0842
Alcúdia|39.8532|3.1213
Can Picafort|39.7650|3.1550
Son Serra de Marina|39.7360|3.2236
Colònia de Sant Pere|39.7380|3.2800
Artà|39.6936|3.3494
Capdepera|39.7022|3.4336
Cala Ratjada|39.7106|3.4602
Canyamel|39.6569|3.4398
Son Servera|39.6206|3.3606
Cala Millor|39.6047|3.3848
Sant Llorenç des Cardassar|39.6106|3.2839
Son Carrió|39.5863|3.3203
Manacor|39.5700|3.2094
Porto Cristo|39.5406|3.3308
Cales de Mallorca|39.4652|3.2799
Son Macià|39.5136|3.2166
Portocolom|39.4167|3.2583
Felanitx|39.4692|3.1481
Cala d'Or|39.3749|3.2303
Portopetro|39.3612|3.2092
Cala Figuera|39.3287|3.1683
Cala Llombards|39.3183|3.1359
Santanyí|39.3542|3.1283
Ses Salines|39.3378|3.0536
Colònia de Sant Jordi|39.3172|2.9936
Sa Ràpita|39.3663|2.9420
S'Estanyol|39.3626|2.9182
Cala Pi|39.3642|2.8387
S'Arenal|39.5008|2.7563
Llucmajor|39.4903|2.8908
Campos|39.4306|3.0194
Porreres|39.5147|3.0214
Montuïri|39.5667|2.9833
Algaida|39.5594|2.8950
Vilafranca de Bonany|39.5703|3.0890
Petra|39.6136|3.1122
Sant Joan|39.5971|3.0380
Sineu|39.6428|3.0114
Ariany|39.6508|3.1115
Maria de la Salut|39.6661|3.0752
Santa Margalida|39.7034|3.1027
Muro|39.7371|3.0567
Llubí|39.7003|3.0042
Sa Pobla|39.7697|3.0247
Búger|39.7591|2.9856
Campanet|39.7751|2.9651
Selva|39.7550|2.9006
Caimari|39.7419|2.8958
Mancor de la Vall|39.7501|2.8710
Inca|39.7211|2.9111
Lloseta|39.7186|2.8686
Alaró|39.7058|2.7922
Binissalem|39.6872|2.8439
Consell|39.6686|2.8134
Santa Maria del Camí|39.6503|2.7736
Sencelles|39.6476|2.8977
Costitx|39.6576|2.9497
Lloret de Vistalegre|39.6179|2.9752
Faro de Sa Mola|39.5317|2.3642
Faro de Cap Gros|39.7969|2.6847
Faro de Formentor|39.9619|3.2123
Faro d'Alcanada|39.8354|3.1712
Faro de Capdepera|39.7157|3.4775
Faro de Porto Cristo|39.5350|3.3402
Faro de Portocolom|39.4161|3.2731
Faro de Cap de ses Salines|39.2650|3.0536
Faro de Cap Blanc|39.3636|2.7896
Puig de Sant Miquel|39.5637|3.0081
Santuari de Cura|39.5276|2.9260
Santuari de Monti-sion|39.4961|3.0163
Santuari de Sant Salvador (Felanitx)|39.4555|3.1857
Castell de Santueri|39.4320|3.1878
Santuari de Consolació|39.5904|3.0345
Ermita de Bonany|39.5945|3.0873
Puig de Santa Magdalena|39.7211|2.9569
Ermita de la Victòria|39.8737|3.1711
Es Verger (Castell d'Alaró)|39.7294|2.7883
Santuari de Sant Salvador (Artà)|39.6964|3.3536
Ermita de Betlem|39.7372|3.3113
Castell de Capdepera|39.7045|3.4331
Castell de Bellver|39.5639|2.6188
Mirador de Na Burguesa|39.5659|2.5945
Coll de sa Gramola|39.6058|2.4096
Mirador de ses Ànimes|39.6837|2.5000
Ermita de la Trinitat|39.7296|2.6095
Son Marroig|39.7512|2.6290
Mirador de ses Barques|39.7908|2.7250
"""
P = {}
for _linea in _LUGARES.strip().splitlines():
    _n, _la, _lo = _linea.split("|")
    P[_n] = (_n, float(_la), float(_lo))

# Cada ruta: nombre, dificultad, salida (hora), descripción, puntos (nombre, lat, lon).
# Los puntos se recorren en orden; el primero y el último marcan salida y llegada.
RUTAS = [
    # ---------------- FÁCIL ----------------
    dict(nombre="Costa de Poniente: Andratx y Sant Elm", dificultad="Fácil", hora="09:00",
         desc="Ida por el interior (Establiments, Puigpunyent y la carretera de Galilea) hasta Andratx, el Port d'Andratx y Sant Elm, con vistas a Sa Dragonera. Vuelta por la costa de Calvià (Palmanova y Cala Major) y Palma.",
         puntos=[SALIDA, P["Establiments"], P["Puigpunyent"], P["Carretera de Galilea"], P["Es Capdellà"], P["Andratx"], P["Port d'Andratx"], P["Sant Elm (mirador de Sa Dragonera)"], P["S'Arracó"], P["Es Capdellà"], P["Calvià"], P["Palmanova"], P["Cala Major"], P["Palma"], SALIDA]),
    dict(nombre="Migjorn: Cap Blanc y Colònia de Sant Jordi", dificultad="Fácil", hora="09:00",
         desc='Ida por Sant Jordi y la carretera vieja de Llucmajor, faro de Cap Blanc, salinas de Es Trenc y café en Colònia de Sant Jordi. Vuelta por Campos, Porreres y Montuïri.',
         puntos=[SALIDA, P["Son Ferriol"], P["Sant Jordi"], P["Llucmajor"], P["Faro de Cap Blanc"], P["Ses Salines"], P["Colònia de Sant Jordi"], P["Campos"], P["Porreres"], P["Montuïri"], SALIDA]),
    dict(nombre="Pla de Mallorca: Sineu, Petra y Porreres", dificultad="Fácil", hora="09:00",
         desc='Ida por Sencelles y Costitx hasta Sineu y Petra; vuelta por Porreres, Montuïri y Algaida. Carreteras interiores tranquilas.',
         puntos=[SALIDA, P["Santa Maria del Camí"], P["Sencelles"], P["Costitx"], P["Sineu"], P["Petra"], P["Porreres"], P["Montuïri"], P["Algaida"], SALIDA]),
    dict(nombre="Levante: Porto Cristo, Portocolom y Santanyí", dificultad="Fácil", hora="09:00",
         desc='Ida por el Pla hasta Manacor y la costa este (Porto Cristo, Portocolom, Santanyí); vuelta por Campos, Llucmajor y Sant Jordi.',
         puntos=[SALIDA, P["Manacor"], P["Porto Cristo"], P["Portocolom"], P["Santanyí"], P["Campos"], P["Llucmajor"], P["Sant Jordi"], P["Son Ferriol"], SALIDA]),
    dict(nombre="Ruta Faros 1 · Sur: Cap Blanc, Ses Salines y Portocolom", dificultad="Fácil", hora="09:00",
         desc="Tres faros de la costa sur y levante por carreteras llanas y anchas: Cap Blanc sobre los acantilados, "
              "Cap de ses Salines en el punto más al sur de la isla y el faro de Portocolom a la entrada del puerto. "
              "Vuelta por Felanitx y Porreres.",
         puntos=[SALIDA, P["Son Ferriol"], P["Sant Jordi"], P["Llucmajor"], P["Faro de Cap Blanc"], P["Ses Salines"], P["Faro de Cap de ses Salines"], P["Santanyí"], P["Faro de Portocolom"], P["Felanitx"], P["Porreres"], P["Montuïri"], SALIDA]),
    # ---------------- MEDIA ----------------
    dict(nombre="Valldemossa, Deià y Sóller", dificultad="Media", hora="09:00",
         desc="El tramo más famoso de la Ma-10 con curvas enlazadas y miradores al mar. Vuelta por el Coll de Sóller (carretera vieja, 58 curvas).",
         puntos=[SALIDA, ("Valldemossa", 39.7108, 2.6225), ("Deià", 39.7481, 2.6492), ("Sóller", 39.7667, 2.7150),
                 ("Coll de Sóller", 39.7358, 2.6902), ("Bunyola", 39.6961, 2.6997), SALIDA]),
    dict(nombre="Galilea, Puigpunyent y Es Capdellà", dificultad="Media", hora="09:00",
         desc='Carretera estrecha y muy revirada por el interior de la Serra: Establiments, Puigpunyent y la carretera de Galilea hasta Es Capdellà. Vuelta por Calvià, la costa y Palma.',
         puntos=[SALIDA, P["Establiments"], P["Puigpunyent"], P["Carretera de Galilea"], P["Es Capdellà"], P["Calvià"], P["Palmanova"], P["Cala Major"], P["Palma"], SALIDA]),
    dict(nombre="Santuari de Cura (Puig de Randa)", dificultad="Media", hora="09:00",
         desc='Subida corta y revirada al Puig de Randa con vistas a toda la isla; ida por Algaida y vuelta por Llucmajor y Sant Jordi.',
         puntos=[SALIDA, P["Algaida"], P["Randa"], P["Santuari de Cura"], P["Llucmajor"], P["Sant Jordi"], P["Son Ferriol"], SALIDA]),
    dict(nombre="Serra de Llevant: Artà y Cala Ratjada", dificultad="Media", hora="09:00",
         desc='Ruta larga hacia el nordeste: ida por Algaida, Manacor y Son Servera hasta el faro y el puerto de Cala Ratjada; curvas de Capdepera a Artà y vuelta por Santa Margalida, Inca y la carretera vieja de Inca.',
         puntos=[SALIDA, P["Algaida"], P["Montuïri"], P["Manacor"], P["Sant Llorenç des Cardassar"], P["Son Servera"], P["Cala Ratjada"], P["Capdepera"], P["Artà"], P["Santa Margalida"], P["Llubí"], P["Inca"], P["Binissalem"], P["Santa Maria del Camí"], SALIDA]),
    dict(nombre="Cap de Formentor", dificultad="Media", hora="08:30",
         desc='Carretera espectacular hasta el faro. Ida por Inca y Pollença, vuelta por Alcúdia, sa Pobla y Llubí. Salir temprano: tramo estrecho, ciclistas y mucho tráfico a partir de media mañana.',
         puntos=[SALIDA, P["Santa Maria del Camí"], P["Binissalem"], P["Inca"], P["Pollença"], P["Port de Pollença"], P["Mirador Es Colomer"], P["Faro de Formentor"], P["Port de Pollença"], P["Alcúdia"], P["Sa Pobla"], P["Llubí"], P["Sencelles"], SALIDA]),
    # ---------------- DIFÍCIL ----------------
    dict(nombre="Orient y Castell d'Alaró", dificultad="Difícil", hora="09:00",
         desc="Carretera estrecha y bacheada por el valle de Orient, curvas cerradas sin visibilidad y bajada a Alaró. Muy técnica.",
         puntos=[SALIDA, ("Bunyola", 39.6961, 2.6997), ("Orient", 39.7294, 2.7408), ("Alaró", 39.7058, 2.7922),
                 ("Lloseta", 39.7186, 2.8686), ("Santa Maria del Camí", 39.6503, 2.7736), SALIDA]),
    dict(nombre="Ma-10 completa: Andratx – Pollença", dificultad="Difícil", hora="08:30",
         desc="La carretera de la Serra de Tramuntana entera: Estellencs, Banyalbufar, Deià, Sóller, Puig Major, Lluc y Pollença. Jornada completa, regreso por Inca.",
         puntos=[SALIDA, ("Andratx", 39.5756, 2.4206), ("Estellencs", 39.6536, 2.4800), ("Banyalbufar", 39.6878, 2.5147),
                 ("Valldemossa", 39.7108, 2.6225), ("Deià", 39.7481, 2.6492), ("Sóller", 39.7667, 2.7150),
                 ("Embalse de Cúber", 39.7880, 2.8000), ("Santuari de Lluc", 39.8217, 2.8847),
                 ("Pollença", 39.8772, 3.0161), ("Inca", 39.7211, 2.9111),
                 ("Binissalem", 39.6872, 2.8439), ("Santa Maria del Camí", 39.6503, 2.7736), SALIDA]),
    dict(nombre="Sa Calobra y Nus de sa Corbata", dificultad="Difícil", hora="08:30",
         desc='La carretera más famosa de la isla (Ma-2141): 12 km de horquillas y el Nus de sa Corbata, ida y vuelta desde el Coll dels Reis. Ida por Inca, Selva y Lluc; vuelta por el Puig Major, Sóller y el Coll de Sóller. Evitar horas de autocares.',
         puntos=[SALIDA, P["Santa Maria del Camí"], P["Binissalem"], P["Inca"], P["Selva"], P["Santuari de Lluc"], P["Coll dels Reis"], P["Sa Calobra"], P["Embalse del Gorg Blau"], P["Embalse de Cúber"], P["Sóller"], P["Coll de Sóller"], P["Bunyola"], SALIDA]),
    dict(nombre="Gran Vuelta Tramuntana: Sóller, Sa Calobra y Formentor", dificultad="Difícil", hora="08:30",
         desc="La ruta reina de la Tramuntana: Coll de Sóller, Puig Major, Sa Calobra y Formentor en un solo día. Solo para pilotos con experiencia.",
         puntos=[SALIDA, ("Coll de Sóller", 39.7358, 2.6902), ("Sóller", 39.7667, 2.7150), ("Fornalutx", 39.7822, 2.7408),
                 ("Embalse de Cúber", 39.7880, 2.8000), ("Sa Calobra", 39.8510, 2.8063),
                 ("Santuari de Lluc", 39.8217, 2.8847), ("Pollença", 39.8772, 3.0161),
                 ("Faro de Formentor", 39.9619, 3.2123), ("Port de Pollença", 39.9075, 3.0842),
                 ("Inca", 39.7211, 2.9111), ("Binissalem", 39.6872, 2.8439), ("Santa Maria del Camí", 39.6503, 2.7736), SALIDA]),
    dict(nombre="Ruta Faros 2 · Norte: Cap Gros y Formentor", dificultad="Difícil", hora="08:30",
         desc="Subida estrecha y empinada al faro de Cap Gros sobre el Port de Sóller, Ma-10 por el Puig Major y Lluc "
              "y final en el faro de Formentor. Coll de Sóller a la ida, carretera vieja por Inca a la vuelta. "
              "Jornada larga y muy revirada.",
         puntos=[SALIDA, ("Coll de Sóller", 39.7358, 2.6902), ("Sóller", 39.7667, 2.7150),
                 ("Port de Sóller", 39.7975, 2.6956), ("Faro de Cap Gros", 39.7969, 2.6847),
                 ("Sóller", 39.7667, 2.7150), ("Embalse de Cúber", 39.7880, 2.8000),
                 ("Santuari de Lluc", 39.8217, 2.8847), ("Pollença", 39.8772, 3.0161),
                 ("Faro de Formentor", 39.9619, 3.2123), ("Port de Pollença", 39.9075, 3.0842),
                 ("Inca", 39.7211, 2.9111), ("Binissalem", 39.6872, 2.8439),
                 ("Santa Maria del Camí", 39.6503, 2.7736), SALIDA]),
    # ================= RUTAS LARGAS (salida 08:30-09:00, vuelta a partir de las 15:00) =================
    # ---- Vueltas a Mallorca ----
    dict(nombre="Vuelta a Mallorca por la costa", dificultad="Difícil", hora="08:00",
         desc="La isla entera siguiendo la costa: Calvià y Andratx, toda la Ma-10 por la Serra de Tramuntana, "
              "bahías de Pollença y Alcúdia, Artà, la costa de Llevant y el Migjorn hasta s'Arenal. "
              "Es la ruta más larga: conviene salir a las 8:00 y contar con llegar por la tarde-noche.",
         puntos=[SALIDA, P["Portals Nous"], P["Palmanova"], P["Calvià"], P["Es Capdellà"], P["Andratx"], P["Estellencs"], P["Banyalbufar"],
                 P["Valldemossa"], P["Deià"], P["Sóller"], P["Embalse de Cúber"], P["Santuari de Lluc"], P["Pollença"],
                 P["Alcúdia"], P["Can Picafort"], P["Artà"], P["Capdepera"], P["Son Servera"], P["Porto Cristo"],
                 P["Portocolom"], P["Santanyí"], P["Colònia de Sant Jordi"], P["Sa Ràpita"], P["S'Estanyol"],
                 P["S'Arenal"], SALIDA]),
    dict(nombre="Vuelta a Mallorca por todos los faros", dificultad="Difícil", hora="08:00",
         desc="Vuelta completa pasando por los faros a los que se llega por carretera: Sa Mola, Cap Gros, Formentor, "
              "Alcanada, Capdepera, Porto Cristo, Portocolom, Cap de ses Salines y Cap Blanc. "
              "Jornada épica: salir a las 8:00, hacer paradas cortas y contar con volver de noche.",
         puntos=[SALIDA, P["Palma"], P["Cala Major"], P["Palmanova"], P["Calvià"], P["Es Capdellà"], P["Faro de Sa Mola"], P["Andratx"], P["Estellencs"], P["Valldemossa"],
                 P["Deià"], P["Port de Sóller"], P["Faro de Cap Gros"], P["Sóller"], P["Embalse de Cúber"],
                 P["Santuari de Lluc"], P["Pollença"], P["Faro de Formentor"], P["Port de Pollença"],
                 P["Faro d'Alcanada"], P["Can Picafort"], P["Artà"], P["Faro de Capdepera"], P["Son Servera"],
                 P["Faro de Porto Cristo"], P["Faro de Portocolom"], P["Santanyí"], P["Faro de Cap de ses Salines"],
                 P["Ses Salines"], P["Faro de Cap Blanc"], P["Llucmajor"], SALIDA]),
    dict(nombre="Media Vuelta Norte: de Andratx a Artà", dificultad="Difícil", hora="08:30",
         desc="La mitad norte de la vuelta a la isla: Ma-10 desde Andratx hasta Pollença, bahía de Alcúdia, "
              "Can Picafort y Artà. Regreso por el interior (Manacor, Petra y Sineu).",
         puntos=[SALIDA, P["Puigpunyent"], P["Andratx"], P["Estellencs"], P["Banyalbufar"], P["Valldemossa"],
                 P["Deià"], P["Sóller"], P["Embalse de Cúber"], P["Santuari de Lluc"], P["Pollença"], P["Alcúdia"],
                 P["Can Picafort"], P["Artà"], P["Petra"], P["Sineu"], SALIDA]),
    dict(nombre="Media Vuelta Sur: del Migjorn a Llevant", dificultad="Fácil", hora="09:00",
         desc="La mitad sur de la vuelta a la isla por carreteras cómodas: s'Arenal, Cap Blanc, Colònia de Sant Jordi, Santanyí, Cala d'Or, Portocolom, Porto Cristo y Artà. Vuelta por Santa Margalida y Sineu.",
         puntos=[SALIDA, P["Son Ferriol"], P["Sant Jordi"], P["S'Arenal"], P["Faro de Cap Blanc"], P["Colònia de Sant Jordi"], P["Santanyí"], P["Cala d'Or"], P["Portocolom"], P["Porto Cristo"], P["Son Servera"], P["Artà"], P["Santa Margalida"], P["Sineu"], SALIDA]),
    # ---- Faros ----
    dict(nombre="Ruta Faros 3 · Poniente: Sa Mola y Cap Gros", dificultad="Difícil", hora="08:30",
         desc="Faro de Sa Mola sobre el Port d'Andratx y faro de Cap Gros sobre el Port de Sóller, unidos por toda la Ma-10 "
              "de Poniente (Estellencs, Banyalbufar, Valldemossa y Deià). Vuelta por el Coll de Sóller.",
         puntos=[SALIDA, P["Palma"], P["Cala Major"], P["Palmanova"], P["Calvià"], P["Es Capdellà"], P["Faro de Sa Mola"], P["Andratx"], P["Estellencs"], P["Banyalbufar"],
                 P["Valldemossa"], P["Deià"], P["Port de Sóller"], P["Faro de Cap Gros"], P["Sóller"],
                 P["Coll de Sóller"], P["Bunyola"], SALIDA]),
    dict(nombre="Ruta Faros 4 · Llevant: Capdepera, Porto Cristo y Portocolom", dificultad="Fácil", hora="09:00",
         desc='Tres faros de la costa de Llevant por carreteras anchas: Capdepera (el punto más oriental de la isla), Porto Cristo y Portocolom. Ida por el Pla y Manacor, vuelta por Felanitx, Llucmajor y Sant Jordi.',
         puntos=[SALIDA, P["Manacor"], P["Artà"], P["Faro de Capdepera"], P["Son Servera"], P["Faro de Porto Cristo"], P["Faro de Portocolom"], P["Felanitx"], P["Llucmajor"], P["Sant Jordi"], P["Son Ferriol"], SALIDA]),
    dict(nombre="Ruta Faros 5 · Bahías del Norte: Formentor, Alcanada y Capdepera", dificultad="Media", hora="08:30",
         desc="Faro de Formentor al final de la península, faro de Alcanada frente a la bahía de Alcúdia y "
              "faro de Capdepera. Formentor es estrecho y con mucho tráfico: llegar temprano.",
         puntos=[SALIDA, P["Santa Maria del Camí"], P["Binissalem"], P["Inca"], P["Pollença"], P["Faro de Formentor"], P["Port de Pollença"], P["Faro d'Alcanada"],
                 P["Can Picafort"], P["Artà"], P["Faro de Capdepera"], P["Manacor"], P["Petra"], P["Sineu"], SALIDA]),
    # ---- Puigs ----
    dict(nombre="Ruta Puigs 1 · Pla: Cura, Sant Miquel, Monti-sion, Sant Salvador, Consolació y Bonany", dificultad="Media",
         hora="09:00",
         desc='Seis cimas y santuarios del Pla y el Migjorn: Puig de Randa (Cura), Puig de Sant Miquel (Montuïri), Monti-sion (Porreres), Sant Salvador (Felanitx), Consolació (Sant Joan) y Bonany (Petra). Subidas cortas, estrechas y reviradas con vistas a toda la isla. Vuelta por Sineu y Sencelles.',
         puntos=[SALIDA, P["Algaida"], P["Santuari de Cura"], P["Puig de Sant Miquel"], P["Santuari de Monti-sion"], P["Santuari de Sant Salvador (Felanitx)"], P["Santuari de Consolació"], P["Ermita de Bonany"], P["Sineu"], P["Sencelles"], P["Santa Maria del Camí"], SALIDA]),
    dict(nombre="Ruta Puigs 2 · Raiguer y Norte: Santa Magdalena, La Victòria, Lluc y Castell d'Alaró", dificultad="Difícil",
         hora="08:30",
         desc="Puig de Santa Magdalena (Inca), ermita de la Victòria sobre la bahía de Alcúdia, Santuari de Lluc "
              "y subida a Es Verger, al pie del Castell d'Alaró: el último tramo es muy estrecho y empinado.",
         puntos=[SALIDA, P["Santa Maria del Camí"], P["Binissalem"], P["Puig de Santa Magdalena"], P["Alcúdia"],
                 P["Ermita de la Victòria"], P["Pollença"], P["Santuari de Lluc"], P["Caimari"], P["Alaró"],
                 P["Es Verger (Castell d'Alaró)"], P["Alaró"], P["Santa Maria del Camí"], SALIDA]),
    dict(nombre="Ruta Puigs 3 · Llevant: Bonany, Castell de Capdepera, Sant Salvador d'Artà y Betlem", dificultad="Media",
         hora="09:00",
         desc='Puig de Bonany, castillo de Capdepera, santuario de Sant Salvador sobre Artà y ermita de Betlem (carretera estrecha de montaña). Ida por Sineu y Manacor, vuelta por Santa Margalida e Inca.',
         puntos=[SALIDA, P["Sineu"], P["Ermita de Bonany"], P["Manacor"], P["Son Servera"], P["Castell de Capdepera"], P["Artà"], P["Santuari de Sant Salvador (Artà)"], P["Ermita de Betlem"], P["Santa Margalida"], P["Llubí"], P["Inca"], P["Binissalem"], P["Santa Maria del Camí"], SALIDA]),
    dict(nombre="Ruta Puigs 4 · Gran Ruta de los Puigs", dificultad="Difícil", hora="08:30",
         desc="Siete subidas en un día: Cura, Monti-sion, Sant Salvador de Felanitx, Castell de Santueri, Bonany, "
              "Sant Salvador d'Artà y Santa Magdalena. Muchas horquillas estrechas y jornada larga.",
         puntos=[SALIDA, P["Santuari de Cura"], P["Santuari de Monti-sion"], P["Santuari de Sant Salvador (Felanitx)"],
                 P["Castell de Santueri"], P["Ermita de Bonany"], P["Santuari de Sant Salvador (Artà)"],
                 P["Santa Margalida"], P["Puig de Santa Magdalena"], P["Binissalem"], P["Santa Maria del Camí"], SALIDA]),
    dict(nombre="Ruta Puigs 5 · Ponent y Tramuntana: Na Burguesa, sa Gramola, Trinitat y Ses Barques", dificultad="Difícil",
         hora="08:30",
         desc="Miradores en altura del oeste: Na Burguesa sobre la bahía de Palma, Coll de sa Gramola, Mirador de ses Ànimes, "
              "ermita de la Trinitat (Valldemossa) y Mirador de ses Barques sobre Sóller. Vuelta por el Coll de Sóller.",
         puntos=[SALIDA, P["Mirador de Na Burguesa"], P["Calvià"], P["Andratx"], P["Coll de sa Gramola"],
                 P["Mirador de ses Ànimes"], P["Ermita de la Trinitat"], P["Deià"], P["Sóller"], P["Mirador de ses Barques"],
                 P["Sóller"], P["Coll de Sóller"], P["Bunyola"], SALIDA]),
    # ---- Temáticas ----
    dict(nombre="Ruta de los Castillos: Bellver, Santueri y Capdepera", dificultad="Media", hora="09:00",
         desc="Tres castillos: Bellver sobre Palma, Santueri en lo alto de Felanitx (subida estrecha) y el recinto "
              "amurallado de Capdepera. Vuelta por Artà y el Pla.",
         puntos=[SALIDA, P["Castell de Bellver"], P["Llucmajor"], P["Porreres"], P["Felanitx"], P["Castell de Santueri"],
                 P["Portocolom"], P["Porto Cristo"], P["Son Servera"], P["Castell de Capdepera"], P["Artà"],
                 P["Petra"], P["Sineu"], SALIDA]),
    dict(nombre="Calas del Sur: Cala Pi, Llombards, Cala Figuera y Cala d'Or", dificultad="Fácil", hora="09:00",
         desc="Las calas más bonitas del sur: Cala Pi, Cala Llombards, el puerto de Cala Figuera, Portopetro y Cala d'Or. "
              "Carreteras tranquilas y paradas a pie de mar. Vuelta por Felanitx.",
         puntos=[SALIDA, P["Son Ferriol"], P["Sant Jordi"], P["Llucmajor"], P["Cala Pi"], P["Campos"], P["Santanyí"], P["Cala Llombards"], P["Cala Figuera"], P["Portopetro"], P["Cala d'Or"], P["Felanitx"], P["Porreres"], P["Montuïri"], SALIDA]),
    dict(nombre="Pla de Mallorca completo: pueblos del interior", dificultad="Fácil", hora="09:00",
         desc='Los pueblos del corazón de la isla por carreteras locales sin tráfico: Sencelles, Costitx, Lloret, Sineu, Maria de la Salut, Santa Margalida, Muro y Llubí.',
         puntos=[SALIDA, P["Sencelles"], P["Costitx"], P["Lloret de Vistalegre"], P["Sineu"], P["Maria de la Salut"], P["Santa Margalida"], P["Muro"], P["Llubí"], P["Inca"], P["Binissalem"], P["Santa Maria del Camí"], SALIDA]),
    dict(nombre="Ruta del Vino: Binissalem, Pla y Felanitx", dificultad="Fácil", hora="09:00",
         desc="Las zonas de bodegas de la isla: denominación Binissalem (Santa Maria, Consell, Binissalem) y "
              "Pla i Llevant (Petra, Felanitx, Porreres, Algaida). Ruta tranquila para combinar con una visita.",
         puntos=[SALIDA, P["Santa Maria del Camí"], P["Consell"], P["Binissalem"], P["Sencelles"], P["Petra"],
                 P["Vilafranca de Bonany"], P["Felanitx"], P["Porreres"], P["Algaida"], SALIDA]),
    dict(nombre="Miradores de la Ma-10: de sa Gramola a Ses Barques", dificultad="Difícil", hora="08:30",
         desc="Todos los miradores de la carretera de la Serra: Coll de sa Gramola, ses Ànimes, Son Marroig, "
              "ses Barques, Gorg Blau y Lluc. Vuelta por Caimari y el Raiguer.",
         puntos=[SALIDA, P["Puigpunyent"], P["Andratx"], P["Coll de sa Gramola"], P["Mirador de ses Ànimes"],
                 P["Valldemossa"], P["Son Marroig"], P["Sóller"], P["Mirador de ses Barques"], P["Embalse del Gorg Blau"],
                 P["Santuari de Lluc"], P["Caimari"], P["Binissalem"], P["Santa Maria del Camí"], SALIDA]),
    dict(nombre="Raiguer completo: de Alaró a sa Pobla", dificultad="Media", hora="09:00",
         desc="Los pueblos al pie de la Tramuntana: Alaró, Lloseta, Mancor de la Vall, Selva, Caimari, Campanet, "
              "Búger y sa Pobla. Algún tramo estrecho entre pueblos de montaña.",
         puntos=[SALIDA, P["Alaró"], P["Lloseta"], P["Mancor de la Vall"], P["Selva"], P["Caimari"], P["Campanet"],
                 P["Búger"], P["Sa Pobla"], P["Muro"], P["Llubí"], P["Sencelles"], SALIDA]),
    dict(nombre="Costa Norte: Alcúdia, Son Serra y Colònia de Sant Pere", dificultad="Fácil", hora="09:00",
         desc='La bahía de Alcúdia de punta a punta: Alcúdia, Can Picafort, Son Serra de Marina y Colònia de Sant Pere, con final en Artà. Vuelta por el interior (Petra y Sineu).',
         puntos=[SALIDA, P["Santa Maria del Camí"], P["Binissalem"], P["Inca"], P["Sa Pobla"], P["Alcúdia"], P["Can Picafort"], P["Son Serra de Marina"], P["Colònia de Sant Pere"], P["Artà"], P["Petra"], P["Sineu"], SALIDA]),
    dict(nombre="Gran Ruta de Llevant: Cales de Mallorca, Canyamel y Cala Ratjada", dificultad="Fácil", hora="09:00",
         desc='Toda la costa de Llevant: Cales de Mallorca, Porto Cristo, Cala Millor, Canyamel y Cala Ratjada. Ida por Algaida y Manacor, vuelta por Artà, Santa Margalida e Inca.',
         puntos=[SALIDA, P["Algaida"], P["Montuïri"], P["Manacor"], P["Cales de Mallorca"], P["Porto Cristo"], P["Cala Millor"], P["Canyamel"], P["Cala Ratjada"], P["Artà"], P["Santa Margalida"], P["Llubí"], P["Inca"], P["Binissalem"], P["Santa Maria del Camí"], SALIDA]),
    dict(nombre="Tramuntana Sur: Calvià, Andratx, Estellencs y Esporles", dificultad="Media", hora="09:00",
         desc='La parte sur de la Serra en un bucle largo: ida por la costa de Calvià y Es Capdellà hasta Andratx; Coll de sa Gramola, Estellencs, Banyalbufar y vuelta por Esporles. Curvas continuas y poco tráfico.',
         puntos=[SALIDA, P["Palma"], P["Cala Major"], P["Palmanova"], P["Calvià"], P["Es Capdellà"], P["Andratx"], P["Coll de sa Gramola"], P["Estellencs"], P["Banyalbufar"], P["Esporles"], SALIDA]),
    dict(nombre="Valle de Sóller: Port de Sóller, Fornalutx, Deià y Valldemossa", dificultad="Media", hora="09:00",
         desc='Los pueblos del valle de los naranjos: Coll de Sóller, Sóller y Fornalutx, subida al Mirador de ses Barques y bajada al Port de Sóller. Vuelta por Deià, Valldemossa y Esporles.',
         puntos=[SALIDA, P["Bunyola"], P["Coll de Sóller"], P["Sóller"], P["Fornalutx"], P["Mirador de ses Barques"], P["Port de Sóller"], P["Deià"], P["Valldemossa"], P["Esporles"], SALIDA]),
    dict(nombre="Interior de Llevant: Vilafranca, Manacor y Son Macià", dificultad="Fácil", hora="09:00",
         desc='Carreteras secundarias del Llevant interior: Sant Joan, Vilafranca, Manacor, Son Macià y Felanitx. Vuelta por Llucmajor y Sant Jordi.',
         puntos=[SALIDA, P["Sant Joan"], P["Vilafranca de Bonany"], P["Manacor"], P["Son Macià"], P["Felanitx"], P["Llucmajor"], P["Sant Jordi"], P["Son Ferriol"], SALIDA]),
]

# Numeración propia en cada dificultad (fáciles 1, 2, 3…; medias 1, 2, 3…; difíciles 1, 2, 3…),
# respetando el orden de la lista. Colores: verde = fácil, amarillo = media, rojo = difícil.
# "num" es el número de la ruta dentro de su dificultad; "id" (p. ej. "dificil-03") la identifica de forma única.
_PREFIJO = {"Fácil": "facil", "Media": "media", "Difícil": "dificil"}
RUTAS.sort(key=lambda r: list(_PREFIJO).index(r["dificultad"]))
_contador = {d: 0 for d in _PREFIJO}
for _r in RUTAS:
    _contador[_r["dificultad"]] += 1
    _r["num"] = _contador[_r["dificultad"]]
    _r["id"] = f"{_PREFIJO[_r['dificultad']]}-{_r['num']:02d}"

VELOCIDAD_MEDIA_KMH = 45  # para estimar el tiempo de conducción sin paradas


def decode_polyline6(s):
    coords, i, lat, lon = [], 0, 0, 0
    while i < len(s):
        for eje in (0, 1):
            shift = result = 0
            while True:
                b = ord(s[i]) - 63
                i += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            delta = ~(result >> 1) if result & 1 else result >> 1
            if eje == 0:
                lat += delta
            else:
                lon += delta
        coords.append([lon / 1e6, lat / 1e6])
    return coords


def calcular_ruta(puntos):
    """Devuelve (coords [lon, lat], metros, segundos, tramos en autovía).

    Cada tramo entre dos puntos consecutivos se calcula por separado, para poder comprobarlo
    (y sustituirlo por el de OSRM si el mapa de Valhalla tiene un corte que no existe)."""
    puntos = simplificar_pasos(puntos)
    resultado = _unir_tramos(puntos)
    # Si la ruta entra en un pueblo de paso y sale por el mismo sitio, el punto del pueblo se lleva al
    # cruce donde empezaba ese entrar y salir, y se vuelve a calcular.
    cambios = {}
    for _, largo, _, lugar, cruce in tramos_repetidos(resultado[0], puntos, detalle=True):
        if largo <= 1500 and not es_parada(lugar[0]) and lugar[0] != SALIDA[0]:
            cambios[lugar] = (lugar[0], round(cruce[0], 5), round(cruce[1], 5))
    if cambios:
        resultado = _unir_tramos([cambios.get(p, p) for p in puntos])
    return resultado


def _unir_tramos(puntos):
    coords, dist, dur, autovia = [], 0.0, 0.0, []
    for a, b in zip(puntos, puntos[1:]):
        c, d, s, au = _calcular_trozo([a, b])
        coords.extend(c if not coords else c[1:])
        dist, dur, autovia = dist + d, dur + s, autovia + au
        time.sleep(1)
    return coords, dist, dur, autovia


# Paradas: lugares que se visitan (faros, santuarios, miradores, calas…), a los que se llega aunque
# haya que volver por el mismo camino. Todo lo demás (pueblos, collados…) son puntos de paso: la ruta
# debe cruzarlos o bordearlos sin entrar y salir por el mismo sitio (lo vigila tramos_repetidos).
_PREFIJOS_PARADA = ("Faro", "Santuari", "Ermita", "Castell", "Mirador", "Puig ", "Es Verger", "Son Marroig",
                    "Sa Calobra", "Sant Elm", "Cala ", "Cales", "Canyamel", "Colònia", "Son Serra",
                    "Port d'Andratx", "Port de Sóller", "Portopetro")


def es_parada(nombre):
    return nombre.startswith(_PREFIJOS_PARADA) and nombre != "Cala Millor"


OSRM = "https://router.project-osrm.org/route/v1/driving/"
AUTOVIAS = {"Ma-1", "Ma-13", "Ma-19", "Ma-20", "Ma-30"}


def _osrm_tramo(a, b):
    """Tramo a->b según OSRM: (coords, metros, segundos, carreteras usadas) o None."""
    url = f"{OSRM}{a[2]},{a[1]};{b[2]},{b[1]}?overview=full&geometries=geojson&steps=true"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "top-gas-rutas-moto/1.0"}),
                                    timeout=60) as r:
            d = json.load(r)
        ruta = d["routes"][0]
    except Exception:  # noqa: BLE001
        return None
    refs = {ref.strip() for leg in ruta["legs"] for s in leg["steps"] for ref in (s.get("ref") or "").split(";")}
    return ruta["geometry"]["coordinates"], ruta["distance"], ruta["duration"], refs


def _calcular_trozo(puntos):
    body = json.dumps({
        "locations": [{"lat": lat, "lon": lon, "type": "break"} for _, lat, lon in puntos],
        "costing": "motorcycle",
        # use_highways=0: evitar autovías y autopistas; use_trails=0: nada de pistas sin asfaltar
        "costing_options": {"motorcycle": {"use_highways": 0, "use_trails": 0, "use_ferry": 0}},
        "units": "kilometers",
    }).encode()
    for intento in range(4):
        try:
            req = urllib.request.Request(VALHALLA, data=body, headers={
                "Content-Type": "application/json", "User-Agent": "top-gas-rutas-moto/1.0"})
            with urllib.request.urlopen(req, timeout=90) as r:
                trip = json.load(r)["trip"]
            coords, autovia, metros, segundos = [], [], 0.0, 0.0
            for k, leg in enumerate(trip["legs"]):
                shape = decode_polyline6(leg["shape"])
                largo, tiempo = leg["summary"]["length"] * 1000, leg["summary"]["time"]
                tramo_autovia = [", ".join(m.get("street_names", [])) or m["instruction"]
                                 for m in leg["maneuvers"] if m.get("highway")]
                # Salvaguarda: si el mapa de Valhalla tiene un corte que no existe (rodeo absurdo),
                # se usa el tramo de OSRM siempre que no pase por autovía.
                a, b = puntos[k], puntos[k + 1]
                recta = math.dist((a[1] * 110.57, a[2] * 85.2), (b[1] * 110.57, b[2] * 85.2)) * 1000
                if largo > 2 * recta + 2000:
                    alt = _osrm_tramo(a, b)
                    if alt and alt[1] * 1.4 + 2000 < largo and not (alt[3] & AUTOVIAS):
                        print(f"    tramo {a[0]} -> {b[0]}: Valhalla {largo / 1000:.1f} km, se usa OSRM {alt[1] / 1000:.1f} km")
                        shape, largo, tiempo, tramo_autovia = alt[0], alt[1], alt[2], []
                coords.extend(shape if not coords else shape[1:])
                autovia += tramo_autovia
                metros += largo
                segundos += tiempo
            return coords, metros, segundos, autovia
        except Exception as e:  # noqa: BLE001
            if intento == 3:
                raise
            print("  reintentando:", e)
            time.sleep(2 ** (intento + 1))


def _distancia_minima_m(coords, punto):
    kx, ky = 111320 * math.cos(math.radians(39.6)), 110570
    return min(math.dist((lon * kx, lat * ky), (punto[2] * kx, punto[1] * ky)) for lon, lat in coords)


def simplificar_pasos(puntos, margen_m=1200):
    """Quita los pueblos de paso que no hacen falta para marcar el camino.

    Si la ruta del punto anterior al siguiente ya pasa a menos de `margen_m` del pueblo (cruzándolo o
    bordeándolo) y no usa autovía, el pueblo deja de ser un punto obligado. Así la ruta no entra hasta
    el centro para volver a salir por el mismo sitio."""
    final, saltados = [puntos[0]], []
    for i in range(1, len(puntos) - 1):
        p = puntos[i]
        if not es_parada(p[0]):
            coords, _, _, autovia = _calcular_trozo([final[-1], puntos[i + 1]])
            # el camino directo tiene que seguir pasando por todos los pueblos que se saltan
            if not autovia and all(_distancia_minima_m(coords, q) < margen_m for q in saltados + [p]):
                saltados.append(p)
                continue
        final.append(p)
        saltados = []
    final.append(puntos[-1])
    return final


def tramos_repetidos(coords, puntos, minimo_m=300, detalle=False):
    """Tramos que la ruta recorre dos veces (ida y vuelta por la misma carretera).

    Devuelve [(km_en_ruta, longitud_m, lugar_mas_cercano)]. No cuenta las idas y vueltas obligadas a una
    parada en fondo de saco (faros, santuarios…) ni los tramos a menos de 8 km de la gasolinera, donde confluyen todas las carreteras."""
    kx, ky = 111320 * math.cos(math.radians(39.6)), 110570
    xy = [(lon * kx, lat * ky) for lon, lat in coords]
    # remuestrear cada 25 m
    pts, acum = [xy[0]], [0.0]
    for a, b in zip(xy, xy[1:]):
        d = math.dist(a, b)
        n = int(d // 25)
        for k in range(1, n + 1):
            pts.append((a[0] + (b[0] - a[0]) * k * 25 / d, a[1] + (b[1] - a[1]) * k * 25 / d))
            acum.append(acum[-1] + 25)
    total = acum[-1]
    celdas = {}
    for i, (x, y) in enumerate(pts):
        celdas.setdefault((int(x // 50), int(y // 50)), []).append(i)
    dup = [False] * len(pts)
    previo = [None] * len(pts)  # índice de la primera pasada por ese mismo sitio
    for i, (x, y) in enumerate(pts):
        cx, cy = int(x // 50), int(y // 50)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in celdas.get((cx + dx, cy + dy), ()):
                    # solo la segunda pasada: un punto ya recorrido al menos 400 m antes
                    if acum[i] - acum[j] > 400 and math.dist(pts[i], pts[j]) < 20:
                        dup[i] = True
                        previo[i] = j if previo[i] is None else max(previo[i], j)
    # posición en la ruta de cada parada (el punto del recorrido más cercano)
    pos_paradas = []
    for n, lat, lon in puntos:
        if es_parada(n):
            q = (lon * kx, lat * ky)
            pos_paradas.append(min(range(len(pts)), key=lambda k: math.dist(pts[k], q)))
    salida = (SALIDA[2] * kx, SALIDA[1] * ky)
    res, i = [], 0
    while i < len(pts):
        if not dup[i]:
            i += 1
            continue
        j = i
        while True:  # juntar trozos separados por huecos de menos de 250 m
            while j + 1 < len(pts) and dup[j + 1]:
                j += 1
            k = j + 1
            while k < len(pts) and not dup[k] and acum[k] - acum[j] < 250:
                k += 1
            if k < len(pts) and dup[k] and acum[k] - acum[j] < 250:
                j = k
            else:
                break
        largo = acum[j] - acum[i]
        tramo = pts[i:j + 1]
        # Ida y vuelta obligada a una parada en fondo de saco: la segunda pasada empieza justo
        # después de dar la vuelta en la parada.
        giro = max(previo[k] for k in range(i, j + 1) if previo[k] is not None)
        cerca_parada = (any(acum[giro] - 3000 <= acum[p] <= acum[i] + 1000 for p in pos_paradas)
                        and acum[i] - acum[giro] < 6000)
        # Cerca de la gasolinera todas las carreteras confluyen: no se cuenta lo que queda a menos de 8 km.
        junto_salida = max(math.dist(q, salida) for q in tramo) < 8000
        if largo >= minimo_m and not cerca_parada and not junto_salida:
            mx, my = tramo[len(tramo) // 2]
            lugar = min(puntos, key=lambda p: math.dist((p[2] * kx, p[1] * ky), (mx, my)))
            # cruce donde empieza la primera pasada por este tramo (donde se entra y luego se vuelve a salir)
            ini = min(previo[k] for k in range(i, j + 1) if previo[k] is not None)
            cruce = (pts[ini][1] / ky, pts[ini][0] / kx)
            res.append((round(acum[i] / 1000, 1), round(largo), lugar[0], lugar, cruce))
        i = j + 1
    return res if detalle else [r[:3] for r in res]


def slug(texto):
    import unicodedata
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return "-".join("".join(c if c.isalnum() else " " for c in t).split())


def gpx(ruta, coords, dist_km):
    nombre = f"{ruta['dificultad']} {ruta['num']} · {ruta['nombre']}"
    desc = f"{ruta['desc']} Dificultad: {ruta['dificultad']}. Distancia aprox.: {dist_km:.0f} km."
    lineas = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gpx version="1.1" creator="top-gas" xmlns="http://www.topografix.com/GPX/1/1" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">',
        f"  <metadata><name>{escape(nombre)}</name><desc>{escape(desc)}</desc>"
        f"<keywords>moto, mallorca, {escape(ruta['dificultad'].lower())}</keywords></metadata>",
    ]
    vistos = set()
    for nombre_pto, lat, lon in ruta["puntos"]:
        # solo las paradas y la gasolinera: los pueblos de paso no se marcan para no confundir
        if not (es_parada(nombre_pto) or nombre_pto == SALIDA[0]) or nombre_pto in vistos:
            continue
        vistos.add(nombre_pto)
        lineas.append(f'  <wpt lat="{lat:.6f}" lon="{lon:.6f}"><name>{escape(nombre_pto)}</name></wpt>')
    lineas.append(f"  <trk><name>{escape(nombre)}</name><desc>{escape(desc)}</desc><type>Moto</type><trkseg>")
    for lon, lat in coords:
        lineas.append(f'    <trkpt lat="{lat:.6f}" lon="{lon:.6f}"/>')
    lineas.append("  </trkseg></trk>")
    lineas.append("</gpx>")
    return "\n".join(lineas) + "\n"


def main():
    GPX_DIR.mkdir(exist_ok=True)
    for viejo in GPX_DIR.glob("*.gpx"):
        viejo.unlink()
    info = {}
    for ruta in RUTAS:
        print("Calculando", ruta["id"], ruta["nombre"])
        coords, dist, _, autovia = calcular_ruta(ruta["puntos"])
        if autovia:
            print("  AVISO, tramos en autovía:", autovia)
        for km, largo, lugar in tramos_repetidos(coords, ruta["puntos"]):
            print(f"  AVISO, tramo repetido: {largo} m en el km {km} (cerca de {lugar})")
        fichero = f"{ruta['id']}-{slug(ruta['nombre'])}.gpx"
        (GPX_DIR / fichero).write_text(gpx(ruta, coords, dist / 1000), encoding="utf-8")
        # El tiempo del planificador es muy prudente; se usa una media fija de moto por secundarias.
        info[ruta["id"]] = (ruta, dist / 1000, dist / 1000 / VELOCIDAD_MEDIA_KMH, fichero)
        time.sleep(1)

    # Resumen en JSON (catálogo completo)
    resumen = [dict(id=rid, num=r["num"], nombre=r["nombre"], dificultad=r["dificultad"], km=round(km),
                    horas_conduccion=round(h, 1), salida=r["hora"], gpx=f)
               for rid, (r, km, h, f) in info.items()]
    (ROOT / "rutas" / "resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2) + "\n",
                                                 encoding="utf-8")
    for e in resumen:
        print(e)


if __name__ == "__main__":
    main()
