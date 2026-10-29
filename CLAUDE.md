# top-gas · Instrucciones para Claude

Rutas en moto por Mallorca (GPX para Wikiloc). El catálogo se genera con `python3 scripts/generar_rutas.py`.

## Flujo de trabajo (decidido por el propietario del repositorio)

Cada cambio se deja terminado de principio a fin, sin pedir confirmación:

1. Hacer el cambio y regenerar las rutas si hace falta.
2. Comprobar: los GPX son XML válido y el generador no avisa de tramos en autovía ni de tramos repetidos (si avisa, rediseñar la ruta).
3. Commit y push a la rama de trabajo.
4. **Crear el pull request contra `main` y hacer el merge automáticamente.**
5. Esperar a que la automatización `Publicar GPX` (GitHub Actions) suba los GPX a la release `gpx`, y comprobar que los enlaces de descarga responden.
6. Actualizar la página web del catálogo. Los botones de descarga apuntan a `https://github.com/rortizlotum-ops/top-gas/releases/download/gpx/<fichero>.gpx`, que baja el archivo `.gpx` directamente (no una página web), como necesita Wikiloc.

## Convenciones de las rutas

- Salida y llegada: Gasolinera BP del polígono de Marratxí.
- Nunca por autovía ni autopista (Ma-1, Ma-13, Ma-19, Ma-20…).
- Los pueblos son puntos de paso: se cruzan o bordean por lo más directo, sin entrar al centro y volver a salir por el mismo sitio, salvo que se pida expresamente parar en uno. Solo las paradas (faros, santuarios, miradores, calas…) se visitan.
- La vuelta va por un camino distinto a la ida. Solo se aceptan coincidencias a menos de 8 km de la gasolinera y las idas y vueltas a una parada en fondo de saco. El generador avisa de cualquier otro tramo repetido.
- Numeración propia en cada dificultad, desde el 1: fáciles (verde) 1, 2, 3…; medias (amarillo) 1, 2, 3…; difíciles (rojo) 1, 2, 3…. «La 3 roja» = Difícil 3. La asigna el generador automáticamente.
- Series con nombre propio: "Vuelta a Mallorca…", "Ruta Faros N", "Ruta Puigs N".
- Salida habitual a las 8:30 o 9:00 y vuelta a partir de las 15:00.
- Tiempo de conducción calculado a 45 km/h de media.

## Antes de cada salida: comprobar la ruta

Cuando el propietario diga qué ruta van a hacer y qué día (p. ej. «la 3 roja el domingo 8»):

1. Ejecutar `python3 scripts/comprobar_ruta.py "roja 3" 2026-11-08`. Cruza el track del GPX con:
   - las incidencias de carreteras del Consell de Mallorca, en directo (servicio público
     `https://ide.conselldemallorca.net/server/rest/services/public/ws_inccar/MapServer`, el mismo que usa
     https://cim.conselldemallorca.net/apps/incidencies/);
   - las festes locals oficiales (`datos/festes_locals_2026.json`, del calendario laboral de la CAIB);
   - los mercados semanales y las ferias (`datos/mercados_y_ferias.json`, orientativo).
2. Buscar además en internet las fiestas, ferias, mercadillos medievales, carreras o pruebas deportivas
   de ese fin de semana en los pueblos por los que pasa la ruta (agenda de mallorca.com, webs de los
   ayuntamientos, thecalendarmallorca.com), porque suelen cortar la travesía principal del pueblo.
3. Responder con un resumen claro: cortes (⛔), avisos (⚠️) e información (ℹ️), indicando en qué punto
   de la ruta está cada uno. Se puede sugerir un desvío o una ruta alternativa, pero **la decisión es
   del propietario**.
4. **No modificar ni regenerar las rutas por las incidencias** (ni siquiera por cortes largos): las rutas
   se mantienen tal cual; la comprobación solo informa.

Mantenimiento de datos: cuando se publique el calendario laboral de 2027 en
https://www.caib.es/sites/calendarilaboral/, añadir `datos/festes_locals_2027.json` y actualizar las ferias.
