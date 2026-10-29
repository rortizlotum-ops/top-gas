#!/usr/bin/env python3
"""Comprueba si una ruta tiene inconvenientes un día concreto.

Uso:
    python3 scripts/comprobar_ruta.py "roja 3" 2026-11-08
    python3 scripts/comprobar_ruta.py "amarilla 4" 2026-11-08
    python3 scripts/comprobar_ruta.py todas 2026-11-08      # resumen de todas las rutas

Cruza el recorrido del GPX con:
  1. Incidencias de carreteras del Consell de Mallorca, en directo
     (https://cim.conselldemallorca.net/apps/incidencies/, servicio ws_inccar).
  2. Festes locals oficiales 2026 (CAIB) de los pueblos por los que pasa: datos/festes_locals_2026.json.
  3. Mercados semanales y ferias de esos pueblos: datos/mercados_y_ferias.json.

Las fiestas y ferias son orientativas: antes de salir hay que confirmar en la web del ayuntamiento
o en las agendas (p. ej. mallorca.com/ca/agenda) si ese fin de semana hay algo que corte el pueblo.
"""
import json
import math
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATOS = ROOT / "datos"
INCIDENCIAS = "https://ide.conselldemallorca.net/server/rest/services/public/ws_inccar/MapServer"
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
COLORES = {"verde": "Fácil", "amarilla": "Media", "amarillo": "Media", "roja": "Difícil", "rojo": "Difícil",
           "facil": "Fácil", "media": "Media", "dificil": "Difícil"}
KX, KY = 111320 * math.cos(math.radians(39.6)), 110570
CERCA_INCIDENCIA_M = 150   # incidencia sobre la ruta
CERCA_PUEBLO_M = 700       # la ruta pasa por el pueblo (o lo bordea)
DIAS_FIESTA = 4            # margen alrededor de una festa local (las fiestas duran varios días)


def _sin_acentos(t):
    return unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()


def buscar_ruta(texto):
    resumen = json.load(open(ROOT / "rutas" / "resumen.json", encoding="utf-8"))
    t = _sin_acentos(texto)
    m = re.search(r"(\d+)", t)
    color = next((v for k, v in COLORES.items() if k in t), None)
    if not (m and color):
        sys.exit(f"No entiendo la ruta «{texto}». Ejemplos: «roja 3», «amarilla 4», «verde 1».")
    for r in resumen:
        if r["dificultad"] == color and r["num"] == int(m.group(1)):
            return r
    sys.exit(f"No existe la ruta {color} {m.group(1)}.")


def leer_track(fichero):
    texto = (ROOT / "rutas" / fichero).read_text(encoding="utf-8")
    return [(float(lon), float(lat)) for lat, lon in re.findall(r'<trkpt lat="([\d.]+)" lon="([\d.]+)"', texto)]


def _xy(lon, lat):
    return lon * KX, lat * KY


def _dist_punto_segmento(p, a, b):
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    if dx == dy == 0:
        return math.dist(p, a)
    u = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.dist(p, (ax + u * dx, ay + u * dy))


def distancia_a_track(track_xy, punto_xy):
    return min(_dist_punto_segmento(punto_xy, a, b) for a, b in zip(track_xy, track_xy[1:]))


def _consulta(capa):
    q = urllib.parse.urlencode({"f": "json", "where": "1=1", "outFields": "*", "outSR": 4326,
                                "returnGeometry": "true", "resultRecordCount": 2000})
    req = urllib.request.Request(f"{INCIDENCIAS}/{capa}/query?{q}", headers={"User-Agent": "top-gas/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r).get("features", [])


def recorrido_sobre_tramos(track_xy, tramos, margen_m=30):
    """Metros de la ruta que van por encima de los tramos afectados (a menos de `margen_m`)."""
    segs = [(_xy(*a), _xy(*b)) for camino in tramos for a, b in zip(camino, camino[1:])]
    if not segs:
        return 0.0
    total, previo_cerca, previo = 0.0, False, None
    for p in track_xy:
        cerca = any(_dist_punto_segmento(p, a, b) < margen_m for a, b in segs)
        if cerca and previo_cerca:
            total += math.dist(previo, p)
        previo_cerca, previo = cerca, p
    return total


def incidencias_del_dia(dia):
    """Incidencias activas ese día (puntos con sus datos y, si hay, el tramo afectado)."""
    ini = datetime(dia.year, dia.month, dia.day).timestamp() * 1000
    fin = ini + 86400000
    tramos = {}
    for f in _consulta(2):
        tramos.setdefault(f["attributes"]["idinciden"], []).extend(f["geometry"].get("paths", []))
    res = []
    for f in _consulta(1):
        a = f["attributes"]
        if (a.get("inici") or 0) > fin or (a.get("fin") is not None and a["fin"] < ini):
            continue
        res.append((a, f["geometry"], tramos.get(a["idinciden"], [])))
    return res


def es_solo_de_noche(observaciones):
    """True si la incidencia solo aplica de noche (p. ej. «de 22:00 a 06:00 hores»)."""
    m = re.search(r"de (\d{1,2})[:.]\d{2} a (\d{1,2})[:.]\d{2}", observaciones or "")
    return bool(m) and int(m.group(1)) >= 20 and int(m.group(2)) <= 7


def _fecha_ms(ms):
    return datetime.fromtimestamp(ms / 1000).strftime("%d/%m/%Y") if ms else "sin fecha de fin"


def comprobar(ruta, dia, detalle=True):
    track = leer_track(ruta["gpx"])
    txy = [_xy(lon, lat) for lon, lat in track]
    avisos = []

    # 1. Incidencias del Consell
    try:
        incidencias = incidencias_del_dia(dia)
    except Exception as e:  # noqa: BLE001
        incidencias = []
        avisos.append(("?", f"No se ha podido consultar el servicio de incidencias del Consell ({e})."))
    fin_de_semana = dia.weekday() >= 5
    for a, geo, tramos in incidencias:
        puntos = [_xy(geo["x"], geo["y"])] + [_xy(x, y) for p in tramos for x, y in p]
        d = min(distancia_a_track(txy, q) for q in puntos)
        if d > CERCA_INCIDENCIA_M:
            continue
        # Con tramo dibujado: solo afecta si la ruta va por él (al menos 200 m), no si pasa al lado o lo cruza.
        por_el_tramo = not tramos or recorrido_sobre_tramos(txy, tramos) >= 200
        obs = (a.get("observacions") or "").strip()
        solo_laborables = "laborable" in obs.lower()
        solo_noche = es_solo_de_noche(obs)
        nivel = "!!" if a.get("gravetat") == "TANCADA" else "!"
        if (solo_laborables and fin_de_semana) or solo_noche or not por_el_tramo:
            nivel = "i"
        tramo = " → ".join(x for x in (a.get("desinici"), a.get("desfin")) if x) or f"pk {a.get('pkinici')}–{a.get('pkfin')}"
        texto = (f"{a.get('carretera')} ({tramo}): {a.get('gravetat')} – {a.get('afeccio')} por {a.get('causa', '').lower()}, "
                 f"hasta {_fecha_ms(a.get('fin'))}. {obs}")
        if not por_el_tramo:
            texto += " [Está junto a la ruta, pero la ruta no pasa por ese tramo: puede haber más tráfico por el desvío.]"
        elif solo_noche:
            texto += " [Es solo de noche: de día no afecta.]"
        elif nivel == "i":
            texto += " [Es solo en días laborables: en fin de semana no debería afectar.]"
        avisos.append((nivel, texto))

    # 2 y 3. Pueblos por los que pasa: fiestas, mercados y ferias
    loc = json.load(open(DATOS / "localidades.json", encoding="utf-8"))["localidades"]
    festes = json.load(open(DATOS / "festes_locals_2026.json", encoding="utf-8"))["festes"]
    mf = json.load(open(DATOS / "mercados_y_ferias.json", encoding="utf-8"))
    pueblos = {n for n, (la, lo) in loc.items() if distancia_a_track(txy, _xy(lo, la)) <= CERCA_PUEBLO_M}

    def pasa(nombre):
        return any(p in pueblos for p in re.split(r", | i (?=[A-ZÀ-Úa-zs])", nombre) + [nombre])

    for nombre, fiestas in festes.items():
        if not pasa(nombre):
            continue
        for f in fiestas:
            fd = date.fromisoformat(f["fecha"])
            if abs((fd - dia).days) <= DIAS_FIESTA:
                avisos.append(("!", f"{nombre}: festa local el {fd.strftime('%d/%m')} ({f['motivo'] or 'fiesta local'}). "
                                    "Puede haber calles cortadas esos días."))
    dia_semana = DIAS[dia.weekday()]
    for pueblo in mf["por_dia"].get(dia_semana, []):
        if pasa(pueblo):
            nota = mf.get("notas", {}).get(pueblo, "")
            if pueblo == "Sencelles" and dia_semana == "sábado" and dia.day > 7:
                continue
            avisos.append(("!", f"{pueblo}: mercado semanal del {dia_semana} (aprox. 8:00–14:00){' – ' + nota if nota else ''}. "
                                "Suele cortar calles del centro."))
    for f in mf["ferias"]["lista"]:
        if pasa(f["lugar"]) and date.fromisoformat(f["desde"]) <= dia <= date.fromisoformat(f["hasta"]):
            avisos.append(("!", f"{f['lugar']}: {f['nombre']} ({f['desde']}{' a ' + f['hasta'] if f['hasta'] != f['desde'] else ''})."))

    if detalle:
        print(f"\n{ruta['dificultad']} {ruta['num']} · {ruta['nombre']} — {dia_semana} {dia.strftime('%d/%m/%Y')}")
        unicos = sorted({p.lower(): p for p in pueblos}.values())
        print(f"Pasa por (o junto a): {', '.join(unicos) or '—'}")
        if not avisos:
            print("Sin incidencias, fiestas, mercados ni ferias conocidas en el recorrido.")
        iconos = {"!!": "⛔", "!": "⚠️ ", "i": "ℹ️ ", "?": "❓"}
        for nivel, texto in sorted(avisos, key=lambda x: ["!!", "!", "?", "i"].index(x[0])):
            print(f"  {iconos[nivel]} {texto}")
    return avisos


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    dia = date.fromisoformat(sys.argv[2])
    if sys.argv[1].lower() == "todas":
        resumen = json.load(open(ROOT / "rutas" / "resumen.json", encoding="utf-8"))
        for r in resumen:
            av = comprobar(r, dia, detalle=False)
            cortes = sum(1 for n, _ in av if n == "!!")
            otros = sum(1 for n, _ in av if n == "!")
            estado = "⛔ CORTE" if cortes else ("⚠️ " if otros else "✅")
            print(f"{estado:8} {r['dificultad']} {r['num']:>2} · {r['nombre'][:60]}  ({cortes} cortes, {otros} avisos)")
    else:
        comprobar(buscar_ruta(sys.argv[1]), dia)


if __name__ == "__main__":
    main()
