#!/usr/bin/env python3
"""Genera las rutas en moto por Mallorca (GPX para Wikiloc) y el calendario de domingos (ICS).

Uso:  python3 scripts/generar_rutas.py

El trazado se calcula sobre carreteras reales con Valhalla (valhalla1.openstreetmap.de),
perfil de moto y SIN autovías, forzando el paso por los puntos de cada ruta para que
siga las carreteras elegidas. El script avisa si algún tramo acaba en autovía.
"""
import json
import math
import time
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
GPX_DIR = ROOT / "rutas"
VALHALLA = "https://valhalla1.openstreetmap.de/route"

PALMA = ("Palma (Plaça d'Espanya)", 39.5760, 2.6553)

# Cada ruta: id, nombre, dificultad, salida (hora), descripción, puntos (nombre, lat, lon).
# Los puntos se recorren en orden; el primero y el último marcan salida y llegada.
RUTAS = [
    # ---------------- FÁCIL ----------------
    dict(id="01", nombre="Costa de Poniente: Andratx y Sant Elm", dificultad="Fácil", hora="09:30",
         desc="Carreteras anchas y bien asfaltadas por la costa suroeste. Vistas a Sa Dragonera desde Sant Elm. Ideal para empezar la temporada.",
         puntos=[PALMA, ("Andratx", 39.5756, 2.4206), ("Port d'Andratx", 39.5436, 2.3866),
                 ("Sant Elm (mirador de Sa Dragonera)", 39.5791, 2.3540), ("S'Arracó", 39.5842, 2.3900),
                 ("Andratx", 39.5756, 2.4206), PALMA]),
    dict(id="02", nombre="Migjorn: Cap Blanc y Colònia de Sant Jordi", dificultad="Fácil", hora="09:30",
         desc="Rectas y curvas suaves por el sur de la isla. Faro de Cap Blanc, salinas de Es Trenc y café en Colònia de Sant Jordi.",
         puntos=[PALMA, ("Llucmajor", 39.4903, 2.8908), ("Faro de Cap Blanc", 39.3636, 2.7896),
                 ("Ses Salines", 39.3378, 3.0536), ("Colònia de Sant Jordi", 39.3172, 2.9936),
                 ("Campos", 39.4306, 3.0194), PALMA]),
    dict(id="03", nombre="Pla de Mallorca: Sineu, Petra y Porreres", dificultad="Fácil", hora="09:30",
         desc="Carreteras interiores tranquilas entre pueblos del Pla, con poco tráfico el domingo por la mañana.",
         puntos=[PALMA, ("Santa Maria del Camí", 39.6503, 2.7736), ("Sineu", 39.6428, 3.0114),
                 ("Petra", 39.6136, 3.1122), ("Porreres", 39.5147, 3.0214), ("Montuïri", 39.5667, 2.9833), PALMA]),
    dict(id="04", nombre="Levante: Porto Cristo, Portocolom y Santanyí", dificultad="Fácil", hora="09:00",
         desc="Recorrido largo pero sencillo por la costa este: calas, puertos pesqueros y carreteras rápidas.",
         puntos=[PALMA, ("Manacor", 39.5700, 3.2094), ("Porto Cristo", 39.5406, 3.3308),
                 ("Portocolom", 39.4167, 3.2583), ("Santanyí", 39.3542, 3.1283), ("Campos", 39.4306, 3.0194), PALMA]),
    # ---------------- MEDIA ----------------
    dict(id="05", nombre="Valldemossa, Deià y Sóller", dificultad="Media", hora="09:00",
         desc="El tramo más famoso de la Ma-10 con curvas enlazadas y miradores al mar. Vuelta por el Coll de Sóller (carretera vieja, 58 curvas).",
         puntos=[PALMA, ("Valldemossa", 39.7108, 2.6225), ("Deià", 39.7481, 2.6492), ("Sóller", 39.7667, 2.7150),
                 ("Coll de Sóller", 39.7358, 2.6902), ("Bunyola", 39.6961, 2.6997), PALMA]),
    dict(id="06", nombre="Galilea, Puigpunyent y Es Capdellà", dificultad="Media", hora="09:30",
         desc="Carretera estrecha y muy revirada por el interior de la Serra, con pueblos de montaña y poco tráfico.",
         puntos=[PALMA, ("Puigpunyent", 39.6247, 2.5264), ("Galilea", 39.6117, 2.4839),
                 ("Es Capdellà", 39.5761, 2.4617), ("Calvià", 39.5658, 2.5047), PALMA]),
    dict(id="07", nombre="Santuari de Cura (Puig de Randa)", dificultad="Media", hora="10:00",
         desc="Subida corta y revirada al Puig de Randa con vistas a toda la isla. Carretera estrecha en la parte final.",
         puntos=[PALMA, ("Algaida", 39.5594, 2.8950), ("Randa", 39.5236, 2.9322),
                 ("Santuari de Cura", 39.5217, 2.9203), ("Llucmajor", 39.4903, 2.8908), PALMA]),
    dict(id="08", nombre="Serra de Llevant: Artà y Cala Ratjada", dificultad="Media", hora="09:00",
         desc="Ruta larga hacia el nordeste: curvas de Artà a Capdepera, faro y puerto de Cala Ratjada, regreso por Son Servera.",
         puntos=[PALMA, ("Manacor", 39.5700, 3.2094), ("Artà", 39.6936, 3.3494), ("Capdepera", 39.7022, 3.4336),
                 ("Cala Ratjada", 39.7127, 3.4630), ("Son Servera", 39.6206, 3.3606),
                 ("Sant Llorenç des Cardassar", 39.6106, 3.2839), PALMA]),
    dict(id="09", nombre="Cap de Formentor", dificultad="Media", hora="08:30",
         desc="Carretera espectacular hasta el faro. Salir temprano: tramo estrecho, ciclistas y mucho tráfico a partir de media mañana.",
         puntos=[PALMA, ("Santa Maria del Camí", 39.6503, 2.7736), ("Binissalem", 39.6872, 2.8439), ("Inca", 39.7211, 2.9111), ("Port de Pollença", 39.9075, 3.0842),
                 ("Mirador Es Colomer", 39.9235, 3.1178), ("Faro de Formentor", 39.9619, 3.2123),
                 ("Port de Pollença", 39.9075, 3.0842), ("Pollença", 39.8772, 3.0161),
                 ("Inca", 39.7211, 2.9111), ("Binissalem", 39.6872, 2.8439), ("Santa Maria del Camí", 39.6503, 2.7736), PALMA]),
    # ---------------- DIFÍCIL ----------------
    dict(id="10", nombre="Orient y Castell d'Alaró", dificultad="Difícil", hora="09:00",
         desc="Carretera estrecha y bacheada por el valle de Orient, curvas cerradas sin visibilidad y bajada a Alaró. Muy técnica.",
         puntos=[PALMA, ("Bunyola", 39.6961, 2.6997), ("Orient", 39.7294, 2.7408), ("Alaró", 39.7058, 2.7922),
                 ("Lloseta", 39.7186, 2.8686), ("Santa Maria del Camí", 39.6503, 2.7736), PALMA]),
    dict(id="11", nombre="Ma-10 completa: Andratx – Pollença", dificultad="Difícil", hora="08:00",
         desc="La carretera de la Serra de Tramuntana entera: Estellencs, Banyalbufar, Deià, Sóller, Puig Major, Lluc y Pollença. Jornada completa, regreso por Inca.",
         puntos=[PALMA, ("Andratx", 39.5756, 2.4206), ("Estellencs", 39.6536, 2.4800), ("Banyalbufar", 39.6878, 2.5147),
                 ("Valldemossa", 39.7108, 2.6225), ("Deià", 39.7481, 2.6492), ("Sóller", 39.7667, 2.7150),
                 ("Embalse de Cúber", 39.7880, 2.8000), ("Santuari de Lluc", 39.8217, 2.8847),
                 ("Pollença", 39.8772, 3.0161), ("Inca", 39.7211, 2.9111),
                 ("Binissalem", 39.6872, 2.8439), ("Santa Maria del Camí", 39.6503, 2.7736), PALMA]),
    dict(id="12", nombre="Sa Calobra y Nus de sa Corbata", dificultad="Difícil", hora="08:00",
         desc="La carretera más famosa de la isla (Ma-2141): 12 km de horquillas y el Nus de sa Corbata. Ida y vuelta por el mismo sitio; evitar horas de autocares.",
         puntos=[PALMA, ("Santa Maria del Camí", 39.6503, 2.7736), ("Binissalem", 39.6872, 2.8439), ("Inca", 39.7211, 2.9111), ("Selva", 39.7550, 2.9006), ("Santuari de Lluc", 39.8217, 2.8847),
                 ("Coll dels Reis", 39.8298, 2.8425), ("Sa Calobra", 39.8510, 2.8063),
                 ("Santuari de Lluc", 39.8217, 2.8847), ("Caimari", 39.7419, 2.8958),
                 ("Binissalem", 39.6872, 2.8439), ("Santa Maria del Camí", 39.6503, 2.7736), PALMA]),
    dict(id="13", nombre="Gran Vuelta Tramuntana: Sóller, Sa Calobra y Formentor", dificultad="Difícil", hora="07:30",
         desc="La ruta reina para cerrar el año: Coll de Sóller, Puig Major, Sa Calobra y Formentor en un solo día. Solo para pilotos con experiencia.",
         puntos=[PALMA, ("Coll de Sóller", 39.7358, 2.6902), ("Sóller", 39.7667, 2.7150), ("Fornalutx", 39.7822, 2.7408),
                 ("Embalse de Cúber", 39.7880, 2.8000), ("Sa Calobra", 39.8510, 2.8063),
                 ("Santuari de Lluc", 39.8217, 2.8847), ("Pollença", 39.8772, 3.0161),
                 ("Faro de Formentor", 39.9619, 3.2123), ("Port de Pollença", 39.9075, 3.0842),
                 ("Inca", 39.7211, 2.9111), ("Binissalem", 39.6872, 2.8439), ("Santa Maria del Camí", 39.6503, 2.7736), PALMA]),
]

# Orden del calendario: progresivo en dificultad, mezclando para no repetir zonas seguidas.
ORDEN_CALENDARIO = ["01", "02", "05", "03", "06", "04", "07", "10", "08", "09", "12", "11", "13"]
PRIMER_DOMINGO = date(2026, 10, 18)
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
    nombre = f"{ruta['id']} · {ruta['nombre']} ({ruta['dificultad']})"
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


def ics(eventos):
    ahora = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//top-gas//Rutas moto Mallorca//ES",
           "CALSCALE:GREGORIAN", "X-WR-CALNAME:Rutas en moto por Mallorca (domingos)",
           "X-WR-TIMEZONE:Europe/Madrid",
           "BEGIN:VTIMEZONE", "TZID:Europe/Madrid",
           "BEGIN:DAYLIGHT", "TZOFFSETFROM:+0100", "TZOFFSETTO:+0200", "TZNAME:CEST",
           "DTSTART:19700329T020000", "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU", "END:DAYLIGHT",
           "BEGIN:STANDARD", "TZOFFSETFROM:+0200", "TZOFFSETTO:+0100", "TZNAME:CET",
           "DTSTART:19701025T030000", "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU", "END:STANDARD",
           "END:VTIMEZONE"]
    for dia, ruta, dist_km, horas, fichero in eventos:
        h, m = map(int, ruta["hora"].split(":"))
        inicio = datetime(dia.year, dia.month, dia.day, h, m)
        fin = inicio + timedelta(hours=math.ceil(horas * 1.5 + 1))  # paradas incluidas
        desc = (f"Dificultad: {ruta['dificultad']}\\nDistancia: {dist_km:.0f} km\\n{ruta['desc']}\\n"
                f"GPX para Wikiloc: rutas/{fichero}").replace(",", "\\,").replace(";", "\\;")
        out += ["BEGIN:VEVENT", f"UID:top-gas-ruta-{ruta['id']}-{dia:%Y%m%d}@top-gas", f"DTSTAMP:{ahora}",
                f"DTSTART;TZID=Europe/Madrid:{inicio:%Y%m%dT%H%M%S}",
                f"DTEND;TZID=Europe/Madrid:{fin:%Y%m%dT%H%M%S}",
                f"SUMMARY:🏍️ [{ruta['dificultad']}] {ruta['nombre']}".replace(",", "\\,"),
                f"LOCATION:{PALMA[0]}".replace(",", "\\,"), f"DESCRIPTION:{desc}", "END:VEVENT"]
    out.append("END:VCALENDAR")
    # plegado de líneas >75 octetos (RFC 5545)
    plegado = []
    for linea in out:
        b = linea.encode()
        while len(b) > 75:
            corte = 75
            while (b[corte] & 0xC0) == 0x80:
                corte -= 1
            plegado.append(b[:corte].decode())
            b = b" " + b[corte:]
        plegado.append(b.decode())
    return "\r\n".join(plegado) + "\r\n"


def main():
    GPX_DIR.mkdir(exist_ok=True)
    info = {}
    for ruta in RUTAS:
        print("Calculando", ruta["id"], ruta["nombre"])
        coords, dist, _, autovia = calcular_ruta(ruta["puntos"])
        if autovia:
            print("  AVISO, tramos en autovía:", autovia)
        fichero = f"{ruta['id']}-{slug(ruta['dificultad'])}-{slug(ruta['nombre'])}.gpx"
        (GPX_DIR / fichero).write_text(gpx(ruta, coords, dist / 1000), encoding="utf-8")
        # El tiempo del planificador es muy prudente; se usa una media fija de moto por secundarias.
        info[ruta["id"]] = (ruta, dist / 1000, dist / 1000 / VELOCIDAD_MEDIA_KMH, fichero)
        time.sleep(1)

    eventos = []
    for i, rid in enumerate(ORDEN_CALENDARIO):
        ruta, km, h, fichero = info[rid]
        eventos.append((PRIMER_DOMINGO + timedelta(weeks=i), ruta, km, h, fichero))
    (ROOT / "calendario-domingos.ics").write_text(ics(eventos), encoding="utf-8", newline="")

    # Resumen en JSON para el README
    resumen = [dict(fecha=d.isoformat(), id=r["id"], nombre=r["nombre"], dificultad=r["dificultad"],
                    km=round(km), horas_conduccion=round(h, 1), salida=r["hora"], gpx=f)
               for d, r, km, h, f in eventos]
    (ROOT / "rutas" / "resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2) + "\n",
                                                 encoding="utf-8")
    for e in resumen:
        print(e)


if __name__ == "__main__":
    main()
