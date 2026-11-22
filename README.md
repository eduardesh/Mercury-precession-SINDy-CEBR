# Redescubriendo a Einstein

**¿Puede un algoritmo redescubrir la relatividad general a partir de datos?**

El perihelio de Mercurio avanza 43 segundos de arco por siglo más de lo que predice la mecánica newtoniana; la relatividad general explicó la diferencia en 1915. Este proyecto aplica la identificación dispersa de dinámica no lineal (**SINDy**) a 200 años de efemérides de Mercurio, sin información previa sobre la física involucrada, y presenta los resultados en un sitio interactivo.

**Sitio:** https://eduardesh.github.io/Mercury-precession-SINDy-CEBR/

Los cálculos se ejecutan en el navegador, sin instalación ni registro.

## Experimentos

| | Experimento | Contenido |
|---|---|---|
| 1 | [Oscilador armónico amortiguado](https://eduardesh.github.io/Mercury-precession-SINDy-CEBR/resorte.html) | Identificación de un sistema lineal y papel del umbral en STLSQ |
| 2 | [Ley de gravitación](https://eduardesh.github.io/Mercury-precession-SINDy-CEBR/newton.html) | Selección entre fuerzas centrales r⁻¹, r⁻², r⁻³ |
| 3 | [El perihelio de Mercurio](https://eduardesh.github.io/Mercury-precession-SINDy-CEBR/mercurio.html) | Avance de 575″ por siglo medido en datos de JPL |
| 4 | [El término relativista](https://eduardesh.github.io/Mercury-precession-SINDy-CEBR/einstein.html) | Biblioteca de 13 términos; SINDy selecciona la corrección posnewtoniana con f = 0.99998 |
| 5 | [Sensibilidad al ruido y a la cadencia](https://eduardesh.github.io/Mercury-precession-SINDy-CEBR/rompe.html) | Límites impuestos por la diferenciación numérica |

[Fundamentos teóricos](https://eduardesh.github.io/Mercury-precession-SINDy-CEBR/teoria.html): ecuación de Binet, corrección de Schwarzschild, formulación de SINDy y criterios de validación.

## Origen

Basado en la tesis de licenciatura en Ingeniería Física de **Cristopher Eduardo Barrón Ramos** (Facultad de Ciencias Físico Matemáticas, Universidad Autónoma de Coahuila): *Redescubrimiento de la precesión relativista del perihelio de Mercurio con Machine Learning: identificación dispersa de dinámica no lineal (SINDy)*.

Datos: [JPL Horizons](https://ssd.jpl.nasa.gov/horizons/) (efemérides DE441), 1900–2100, cada 12 horas.

## Contenido del repositorio

- `docs/`: el sitio web (HTML, CSS y JavaScript; incluye una copia local de KaTeX para las ecuaciones). GitHub Pages lo publica desde aquí.
- `codigo/`: scripts de Python que descargan los datos y reproducen los resultados de la tesis. Ver `codigo/LEEME.md`.

## Usar y citar

Código bajo licencia MIT; textos bajo CC BY 4.0; KaTeX bajo su propia licencia MIT (`docs/katex/LICENSE`). Para citar el trabajo, véase `CITATION.cff`.
