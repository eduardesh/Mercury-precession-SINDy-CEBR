# Código

Estos scripts descargan los datos de JPL Horizons y generan `docs/datos_mercurio.json`, el archivo que usan los experimentos 3, 4 y 5 del sitio. Reproducen el capítulo 4 de la tesis.

```bash
pip install -r requirements.txt
python descarga.py       # Sol, Mercurio y planetas, 1900–2100 cada 12 h (unos minutos; ~75 MB en raw/)
python sindy_mercurio.py # SINDy clásico con la regla del codo + interruptores de la biblioteca
python rompe.py          # malla de ruido × cadencia (unos 20 minutos)
python perihelio.py      # avance del perihelio medido en los datos
python datos_sitio.py    # junta todo en ../docs/datos_mercurio.json
```

Resultado esperado de `sindy_mercurio.py`: exactamente Sol, 7 planetas, J2 del Sol y relatividad, sin señuelos, con f = 0.999982.

Los experimentos 1 y 2 (resorte y Newton) no necesitan este código: simulan y ejecutan SINDy dentro de la propia página (JavaScript en `docs/resorte.html` y `docs/newton.html`).
