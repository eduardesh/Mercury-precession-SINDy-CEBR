import numpy as np, json
from sindy_mercurio import *
RUIDOS = [0, 0.1, 0.3, 1, 3, 10, 30, 100, 1000]
PASOS = [1, 2, 4, 8, 16]          # 0.5, 1, 2, 4, 8 días
OUT = []
for p in PASOS:
    for s in RUIDOS:
        Th, a = preparar(paso=p, ruido_m=s, desde_pos=True)
        res, i = pareto(Th, a); xi, act, err = res[i]
        OUT.append(dict(dias=H*p, ruido_m=s, rg=bool(act[9]), f=(float(xi[9]) if act[9] else None), falsos=[NOMBRES[j] for j in range(10, 13) if act[j]],
                        perdidos=[NOMBRES[j] for j in range(10) if not act[j]], err=float(err)))
        print(OUT[-1], flush=True)
        json.dump(OUT, open('salida_rompe.json', 'w'), indent=0, ensure_ascii=False)
