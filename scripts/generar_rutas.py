#!/usr/bin/env python3
"""Genera las rutas en moto por Mallorca (GPX para Wikiloc) y su resumen (rutas/resumen.json).

Uso:  python3 scripts/generar_rutas.py

El trazado se calcula sobre carreteras reales con Valhalla (valhalla1.openstreetmap.de),
perfil de moto y SIN autovías, forzando el paso por los puntos de cada ruta para que
siga las carreteras elegidas. El script avisa si algún tramo acaba en autovía.
"""
import json
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
         desc="Carreteras anchas y bien asfaltadas por la costa suroeste. Vistas a Sa Dragonera desde Sant Elm. Ideal para empezar la temporada.",
         puntos=[SALIDA, ("Andratx", 39.5756, 2.4206), ("Port d'Andratx", 39.5436, 2.3866),
                 ("Sant Elm (mirador de Sa Dragonera)", 39.5791, 2.3540), ("S'Arracó", 39.5842, 2.3900),
                 ("Andratx", 39.5756, 2.4206), SALIDA]),
    dict(nombre="Migjorn: Cap Blanc y Colònia de Sant Jordi", dificultad="Fácil", hora="09:00",
         desc="Rectas y curvas suaves por el sur de la isla. Faro de Cap Blanc, salinas de Es Trenc y café en Colònia de Sant Jordi.",
         puntos=[SALIDA, ("Llucmajor", 39.4903, 2.8908), ("Faro de Cap Blanc", 39.3636, 2.7896),
                 ("Ses Salines", 39.3378, 3.0536), ("Colònia de Sant Jordi", 39.3172, 2.9936),
                 ("Campos", 39.4306, 3.0194), SALIDA]),
    dict(nombre="Pla de Mallorca: Sineu, Petra y Porreres", dificultad="Fácil", hora="09:00",
         desc="Carreteras interiores tranquilas entre pueblos del Pla, con poco tráfico el domingo por la mañana.",
         puntos=[SALIDA, ("Santa Maria del Camí", 39.6503, 2.7736), ("Sineu", 39.6428, 3.0114),
                 ("Petra", 39.6136, 3.1122), ("Porreres", 39.5147, 3.0214), ("Montuïri", 39.5667, 2.9833), SALIDA]),
    dict(nombre="Levante: Porto Cristo, Portocolom y Santanyí", dificultad="Fácil", hora="09:00",
         desc="Recorrido largo pero sencillo por la costa este: calas, puertos pesqueros y carreteras rápidas.",
         puntos=[SALIDA, ("Manacor", 39.5700, 3.2094), ("Porto Cristo", 39.5406, 3.3308),
                 ("Portocolom", 39.4167, 3.2583), ("Santanyí", 39.3542, 3.1283), ("Campos", 39.4306, 3.0194), SALIDA]),
    dict(nombre="Ruta Faros 1 · Sur: Cap Blanc, Ses Salines y Portocolom", dificultad="Fácil", hora="09:00",
         desc="Tres faros de la costa sur y levante por carreteras llanas y anchas: Cap Blanc sobre los acantilados, "
              "Cap de ses Salines en el punto más al sur de la isla y el faro de Portocolom a la entrada del puerto. "
              "Vuelta por Felanitx y Porreres.",
         puntos=[SALIDA, ("Llucmajor", 39.4903, 2.8908), ("Faro de Cap Blanc", 39.3636, 2.7896),
                 ("Ses Salines", 39.3378, 3.0536), ("Faro de Cap de ses Salines", 39.2650, 3.0536),
                 ("Santanyí", 39.3542, 3.1283), ("Faro de Portocolom", 39.4161, 3.2731),
                 ("Felanitx", 39.4692, 3.1481), ("Porreres", 39.5147, 3.0214), ("Montuïri", 39.5667, 2.9833), SALIDA]),
    # ---------------- MEDIA ----------------
    dict(nombre="Valldemossa, Deià y Sóller", dificultad="Media", hora="09:00",
         desc="El tramo más famoso de la Ma-10 con curvas enlazadas y miradores al mar. Vuelta por el Coll de Sóller (carretera vieja, 58 curvas).",
         puntos=[SALIDA, ("Valldemossa", 39.7108, 2.6225), ("Deià", 39.7481, 2.6492), ("Sóller", 39.7667, 2.7150),
                 ("Coll de Sóller", 39.7358, 2.6902), ("Bunyola", 39.6961, 2.6997), SALIDA]),
    dict(nombre="Galilea, Puigpunyent y Es Capdellà", dificultad="Media", hora="09:00",
         desc="Carretera estrecha y muy revirada por el interior de la Serra, con pueblos de montaña y poco tráfico.",
         puntos=[SALIDA, ("Puigpunyent", 39.6247, 2.5264), ("Galilea", 39.6117, 2.4839),
                 ("Es Capdellà", 39.5761, 2.4617), ("Calvià", 39.5658, 2.5047), SALIDA]),
    dict(nombre="Santuari de Cura (Puig de Randa)", dificultad="Media", hora="09:00",
         desc="Subida corta y revirada al Puig de Randa con vistas a toda la isla. Carretera estrecha en la parte final.",
         puntos=[SALIDA, ("Algaida", 39.5594, 2.8950), ("Randa", 39.5236, 2.9322),
                 ("Santuari de Cura", 39.5217, 2.9203), ("Llucmajor", 39.4903, 2.8908), SALIDA]),
    dict(nombre="Serra de Llevant: Artà y Cala Ratjada", dificultad="Media", hora="09:00",
         desc="Ruta larga hacia el nordeste: curvas de Artà a Capdepera, faro y puerto de Cala Ratjada, regreso por Son Servera.",
         puntos=[SALIDA, ("Manacor", 39.5700, 3.2094), ("Artà", 39.6936, 3.3494), ("Capdepera", 39.7022, 3.4336),
                 ("Cala Ratjada", 39.7127, 3.4630), ("Son Servera", 39.6206, 3.3606),
                 ("Sant Llorenç des Cardassar", 39.6106, 3.2839), SALIDA]),
    dict(nombre="Cap de Formentor", dificultad="Media", hora="08:30",
         desc="Carretera espectacular hasta el faro. Salir temprano: tramo estrecho, ciclistas y mucho tráfico a partir de media mañana.",
         puntos=[SALIDA, ("Santa Maria del Camí", 39.6503, 2.7736), ("Binissalem", 39.6872, 2.8439), ("Inca", 39.7211, 2.9111), ("Port de Pollença", 39.9075, 3.0842),
                 ("Mirador Es Colomer", 39.9235, 3.1178), ("Faro de Formentor", 39.9619, 3.2123),
                 ("Port de Pollença", 39.9075, 3.0842), ("Pollença", 39.8772, 3.0161),
                 ("Inca", 39.7211, 2.9111), ("Binissalem", 39.6872, 2.8439), ("Santa Maria del Camí", 39.6503, 2.7736), SALIDA]),
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
         desc="La carretera más famosa de la isla (Ma-2141): 12 km de horquillas y el Nus de sa Corbata. Ida y vuelta por el mismo sitio; evitar horas de autocares.",
         puntos=[SALIDA, ("Santa Maria del Camí", 39.6503, 2.7736), ("Binissalem", 39.6872, 2.8439), ("Inca", 39.7211, 2.9111), ("Selva", 39.7550, 2.9006), ("Santuari de Lluc", 39.8217, 2.8847),
                 ("Coll dels Reis", 39.8298, 2.8425), ("Sa Calobra", 39.8510, 2.8063),
                 ("Santuari de Lluc", 39.8217, 2.8847), ("Caimari", 39.7419, 2.8958),
                 ("Binissalem", 39.6872, 2.8439), ("Santa Maria del Camí", 39.6503, 2.7736), SALIDA]),
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
         puntos=[SALIDA, P["Portals Nous"], P["Santa Ponça"], P["Es Capdellà"], P["Andratx"], P["Estellencs"], P["Banyalbufar"],
                 P["Valldemossa"], P["Deià"], P["Sóller"], P["Embalse de Cúber"], P["Santuari de Lluc"], P["Pollença"],
                 P["Alcúdia"], P["Can Picafort"], P["Artà"], P["Capdepera"], P["Son Servera"], P["Porto Cristo"],
                 P["Portocolom"], P["Santanyí"], P["Colònia de Sant Jordi"], P["Sa Ràpita"], P["S'Estanyol"],
                 P["S'Arenal"], SALIDA]),
    dict(nombre="Vuelta a Mallorca por todos los faros", dificultad="Difícil", hora="08:00",
         desc="Vuelta completa pasando por los faros a los que se llega por carretera: Sa Mola, Cap Gros, Formentor, "
              "Alcanada, Capdepera, Porto Cristo, Portocolom, Cap de ses Salines y Cap Blanc. "
              "Jornada épica: salir a las 8:00, hacer paradas cortas y contar con volver de noche.",
         puntos=[SALIDA, P["Santa Ponça"], P["Es Capdellà"], P["Faro de Sa Mola"], P["Andratx"], P["Estellencs"], P["Valldemossa"],
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
         desc="La mitad sur de la vuelta a la isla por carreteras cómodas: s'Arenal, Cap Blanc, Colònia de Sant Jordi, "
              "Santanyí, Cala d'Or, Portocolom, Porto Cristo y Artà. Regreso por Manacor y el Pla.",
         puntos=[SALIDA, P["S'Arenal"], P["S'Estanyol"], P["Faro de Cap Blanc"], P["Colònia de Sant Jordi"],
                 P["Santanyí"], P["Cala d'Or"], P["Portocolom"], P["Porto Cristo"], P["Son Servera"], P["Artà"],
                 P["Manacor"], P["Petra"], P["Sineu"], SALIDA]),
    # ---- Faros ----
    dict(nombre="Ruta Faros 3 · Poniente: Sa Mola y Cap Gros", dificultad="Difícil", hora="08:30",
         desc="Faro de Sa Mola sobre el Port d'Andratx y faro de Cap Gros sobre el Port de Sóller, unidos por toda la Ma-10 "
              "de Poniente (Estellencs, Banyalbufar, Valldemossa y Deià). Vuelta por el Coll de Sóller.",
         puntos=[SALIDA, P["Santa Ponça"], P["Es Capdellà"], P["Faro de Sa Mola"], P["Andratx"], P["Estellencs"], P["Banyalbufar"],
                 P["Valldemossa"], P["Deià"], P["Port de Sóller"], P["Faro de Cap Gros"], P["Sóller"],
                 P["Coll de Sóller"], P["Bunyola"], SALIDA]),
    dict(nombre="Ruta Faros 4 · Llevant: Capdepera, Porto Cristo y Portocolom", dificultad="Fácil", hora="09:00",
         desc="Tres faros de la costa de Llevant por carreteras anchas: Capdepera (el punto más oriental de la isla), "
              "Porto Cristo y Portocolom. Ida por Manacor y Artà, vuelta por Felanitx.",
         puntos=[SALIDA, P["Manacor"], P["Artà"], P["Faro de Capdepera"], P["Son Servera"], P["Faro de Porto Cristo"],
                 P["Faro de Portocolom"], P["Felanitx"], P["Porreres"], P["Montuïri"], SALIDA]),
    dict(nombre="Ruta Faros 5 · Bahías del Norte: Formentor, Alcanada y Capdepera", dificultad="Media", hora="08:30",
         desc="Faro de Formentor al final de la península, faro de Alcanada frente a la bahía de Alcúdia y "
              "faro de Capdepera. Formentor es estrecho y con mucho tráfico: llegar temprano.",
         puntos=[SALIDA, P["Santa Maria del Camí"], P["Binissalem"], P["Inca"], P["Pollença"], P["Faro de Formentor"], P["Port de Pollença"], P["Faro d'Alcanada"],
                 P["Can Picafort"], P["Artà"], P["Faro de Capdepera"], P["Manacor"], P["Petra"], P["Sineu"], SALIDA]),
    # ---- Puigs ----
    dict(nombre="Ruta Puigs 1 · Pla: Sant Miquel, Cura, Monti-sion, Sant Salvador, Consolació y Bonany", dificultad="Media",
         hora="09:00",
         desc="Seis cimas y santuarios del Pla y el Migjorn: Puig de Sant Miquel (Montuïri), Puig de Randa (Cura), "
              "Monti-sion (Porreres), Sant Salvador (Felanitx), Consolació (Sant Joan) y Bonany (Petra). "
              "Subidas cortas, estrechas y reviradas con vistas a toda la isla.",
         puntos=[SALIDA, P["Puig de Sant Miquel"], P["Santuari de Cura"], P["Santuari de Monti-sion"],
                 P["Santuari de Sant Salvador (Felanitx)"], P["Santuari de Consolació"], P["Ermita de Bonany"],
                 P["Sineu"], SALIDA]),
    dict(nombre="Ruta Puigs 2 · Raiguer y Norte: Santa Magdalena, La Victòria, Lluc y Castell d'Alaró", dificultad="Difícil",
         hora="08:30",
         desc="Puig de Santa Magdalena (Inca), ermita de la Victòria sobre la bahía de Alcúdia, Santuari de Lluc "
              "y subida a Es Verger, al pie del Castell d'Alaró: el último tramo es muy estrecho y empinado.",
         puntos=[SALIDA, P["Santa Maria del Camí"], P["Binissalem"], P["Puig de Santa Magdalena"], P["Alcúdia"],
                 P["Ermita de la Victòria"], P["Pollença"], P["Santuari de Lluc"], P["Caimari"], P["Alaró"],
                 P["Es Verger (Castell d'Alaró)"], P["Alaró"], P["Santa Maria del Camí"], SALIDA]),
    dict(nombre="Ruta Puigs 3 · Llevant: Bonany, Sant Salvador d'Artà, Betlem y Castell de Capdepera", dificultad="Media",
         hora="09:00",
         desc="Puig de Bonany, santuario de Sant Salvador sobre Artà, ermita de Betlem (carretera estrecha de montaña) "
              "y castillo de Capdepera. Vuelta por Son Servera y Manacor.",
         puntos=[SALIDA, P["Sineu"], P["Ermita de Bonany"], P["Santuari de Sant Salvador (Artà)"], P["Ermita de Betlem"],
                 P["Artà"], P["Castell de Capdepera"], P["Son Servera"], P["Manacor"], P["Montuïri"], SALIDA]),
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
         puntos=[SALIDA, P["Llucmajor"], P["Cala Pi"], P["Campos"], P["Santanyí"], P["Cala Llombards"], P["Cala Figuera"],
                 P["Portopetro"], P["Cala d'Or"], P["Felanitx"], P["Porreres"], P["Montuïri"], SALIDA]),
    dict(nombre="Pla de Mallorca completo: pueblos del interior", dificultad="Fácil", hora="09:00",
         desc="Todos los pueblos del corazón de la isla por carreteras locales sin tráfico: Sencelles, Costitx, Lloret, "
              "Sineu, Maria de la Salut, Ariany, Petra, Santa Margalida, Muro y Llubí.",
         puntos=[SALIDA, P["Sencelles"], P["Costitx"], P["Lloret de Vistalegre"], P["Sineu"], P["Maria de la Salut"],
                 P["Ariany"], P["Petra"], P["Santa Margalida"], P["Muro"], P["Llubí"], P["Inca"], P["Binissalem"],
                 P["Santa Maria del Camí"], SALIDA]),
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
         desc="La bahía de Alcúdia de punta a punta: Alcúdia, Can Picafort, Son Serra de Marina y Colònia de Sant Pere, "
              "con final en Artà. Vuelta por Santa Margalida y Sineu.",
         puntos=[SALIDA, P["Santa Maria del Camí"], P["Binissalem"], P["Inca"], P["Sa Pobla"], P["Alcúdia"], P["Can Picafort"], P["Son Serra de Marina"],
                 P["Colònia de Sant Pere"], P["Artà"], P["Santa Margalida"], P["Sineu"], SALIDA]),
    dict(nombre="Gran Ruta de Llevant: Cales de Mallorca, Canyamel y Cala Ratjada", dificultad="Fácil", hora="09:00",
         desc="Toda la costa de Llevant: Porto Cristo, Cales de Mallorca, Cala Millor, Canyamel y Cala Ratjada. "
              "Vuelta por Artà y el Pla.",
         puntos=[SALIDA, P["Manacor"], P["Cales de Mallorca"], P["Porto Cristo"], P["Cala Millor"], P["Canyamel"],
                 P["Cala Ratjada"], P["Artà"], P["Petra"], P["Sineu"], SALIDA]),
    dict(nombre="Tramuntana Sur: Galilea, Andratx, Estellencs y Esporles", dificultad="Media", hora="09:00",
         desc="La parte sur de la Serra en un bucle largo: Puigpunyent, Galilea, Es Capdellà, Andratx, Estellencs, "
              "Banyalbufar y Esporles. Curvas continuas y poco tráfico.",
         puntos=[SALIDA, P["Puigpunyent"], P["Galilea"], P["Es Capdellà"], P["Andratx"], P["Coll de sa Gramola"],
                 P["Estellencs"], P["Banyalbufar"], P["Esporles"], SALIDA]),
    dict(nombre="Valle de Sóller: Port de Sóller, Fornalutx, Deià y Valldemossa", dificultad="Media", hora="09:00",
         desc="Los pueblos del valle de los naranjos: Coll de Sóller, Port de Sóller y Fornalutx, "
              "y vuelta por Deià, Valldemossa y Esporles.",
         puntos=[SALIDA, P["Bunyola"], P["Coll de Sóller"], P["Sóller"], P["Port de Sóller"], P["Fornalutx"],
                 P["Sóller"], P["Deià"], P["Valldemossa"], P["Esporles"], SALIDA]),
    dict(nombre="Interior de Llevant: Vilafranca, Sant Llorenç y Son Macià", dificultad="Fácil", hora="09:00",
         desc="Carreteras secundarias del Llevant interior: Sant Joan, Vilafranca, Manacor, Sant Llorenç, Son Carrió, "
              "Son Macià y Felanitx. Tranquila y sin complicaciones.",
         puntos=[SALIDA, P["Sant Joan"], P["Vilafranca de Bonany"], P["Manacor"], P["Sant Llorenç des Cardassar"],
                 P["Son Carrió"], P["Son Macià"], P["Felanitx"], P["Porreres"], P["Algaida"], SALIDA]),
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

    Valhalla admite 10 puntos por consulta: las rutas largas se calculan por trozos."""
    coords, dist, dur, autovia = [], 0.0, 0.0, []
    i = 0
    while i < len(puntos) - 1:
        trozo = puntos[i:i + 10]
        c, d, s, a = _calcular_trozo(trozo)
        coords.extend(c if not coords else c[1:])
        dist, dur, autovia = dist + d, dur + s, autovia + a
        i += len(trozo) - 1
        time.sleep(1.5)
    return coords, dist, dur, autovia


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
            coords, autovia = [], []
            for leg in trip["legs"]:
                shape = decode_polyline6(leg["shape"])
                coords.extend(shape if not coords else shape[1:])
                for m in leg["maneuvers"]:
                    if m.get("highway"):
                        autovia.append(", ".join(m.get("street_names", [])) or m["instruction"])
            s = trip["summary"]
            return coords, s["length"] * 1000, s["time"], autovia
        except Exception as e:  # noqa: BLE001
            if intento == 3:
                raise
            print("  reintentando:", e)
            time.sleep(2 ** (intento + 1))


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
        if nombre_pto in vistos:
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
