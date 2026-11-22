import json, numpy as np
from sindy_mercurio import *
Th, a = preparar(); res, i = pareto(Th, a)
base = json.load(open('salida_base.json')); per = json.load(open('salida_perihelio.json')); rom = json.load(open('salida_rompe.json'))
path = [dict(lam=float(l), err=float(r[2]), act=[int(x) for x in r[1]], f=float(r[0][9]) if r[1][9] else None) for l, r in zip(LAMS, res)]
out = dict(nombres=NOMBRES, pareto=path, elegido=int(i), interruptores=base['interruptores'], perihelio=per,
           rompe=[{k: v for k, v in r.items() if k != 'err'} for r in rom])
json.dump(out, open('../docs/datos_mercurio.json', 'w'), separators=(',', ':'), ensure_ascii=False)
print(len(json.dumps(out)), 'bytes; elegido', i, LAMS[i])
