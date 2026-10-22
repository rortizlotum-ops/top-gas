# top-gas · Instrucciones para Claude

Rutas en moto por Mallorca (GPX para Wikiloc). El catálogo se genera con `python3 scripts/generar_rutas.py`.

## Flujo de trabajo (decidido por el propietario del repositorio)

Cada cambio se deja terminado de principio a fin, sin pedir confirmación:

1. Hacer el cambio y regenerar las rutas si hace falta.
2. Comprobar: los GPX son XML válido y el generador no avisa de tramos en autovía.
3. Commit y push a la rama de trabajo.
4. **Crear el pull request contra `main` y hacer el merge automáticamente.**
5. Actualizar la página web del catálogo para que los enlaces de los GPX apunten a `main`, y comprobar que los enlaces de descarga responden.

## Convenciones de las rutas

- Salida y llegada: Gasolinera BP del polígono de Marratxí.
- Nunca por autovía ni autopista (Ma-1, Ma-13, Ma-19, Ma-20…).
- Numeradas automáticamente por dificultad (fáciles, medias, difíciles).
- Series con nombre propio: "Vuelta a Mallorca…", "Ruta Faros N", "Ruta Puigs N".
- Salida habitual a las 8:30 o 9:00 y vuelta a partir de las 15:00.
- Tiempo de conducción calculado a 45 km/h de media.
