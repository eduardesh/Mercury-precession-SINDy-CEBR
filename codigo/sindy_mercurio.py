"""SINDy clásico sobre Mercurio (como el cap. 4 de la tesis) y tablas para el sitio."""
import numpy as np, json, sys
C = 173.1446326846693                       # AU/día
GM = dict(sol=2.9591220828411956e-4, mercurio=4.9125001948893182e-11, venus=7.2434523326441187e-10, tierra=8.9970116036316091e-10,
          marte=9.5495488297258119e-11, jupiter=2.8253458252257917e-07, saturno=8.4597059933762903e-08, urano=1.2920265649682399e-08,
          neptuno=1.5243573478851939e-08)    # DE440
PLAN = ['venus', 'tierra', 'marte', 'jupiter', 'saturno', 'urano', 'neptuno']
R_SOL = 696000/149597870.7
ra, de = np.radians(286.13), np.radians(63.87)
POLO = np.array([np.cos(de)*np.cos(ra), np.cos(de)*np.sin(ra), np.sin(de)])
H = 0.5                                      # días
D = {k: np.load(f'raw/{k}.npy') for k in ['sol', 'mercurio'] + PLAN}
T = D['sol'][:, 0]

import math
def W(orden, m):
    k = orden//2; s = np.arange(-k, k+1); A = np.vander(s, increasing=True).T; b = np.zeros(len(s)); b[m] = math.factorial(m); return np.linalg.solve(A, b)
def deriv(x, h, m, orden=10):
    w = W(orden, m); k = orden//2; n = len(x)
    out = np.zeros((n-2*k,) + x.shape[1:])
    for j, wj in enumerate(w): out += wj*x[j:n-2*k+j]
    return out/h**m

NOMBRES = ['Sol'] + [{'tierra': 'Tierra-Luna', 'jupiter': 'Júpiter'}.get(p, p.capitalize()) for p in PLAN] + ['J2 del Sol', 'Relatividad', 'Falso: 1/r³', 'Falso: masa extendida', 'Falso: arrastre']
REAL = 10
def biblioteca(r, v, rp):
    """r, v heliocéntricos de Mercurio; rp: dict de posiciones heliocéntricas de planetas."""
    rn = np.linalg.norm(r, axis=1)[:, None]
    cols = [-r/rn**3]
    for p in PLAN:
        d = rp[p] - r; dn = np.linalg.norm(d, axis=1)[:, None]; pn = np.linalg.norm(rp[p], axis=1)[:, None]
        cols.append(d/dn**3 - rp[p]/pn**3)
    z = (r @ POLO)[:, None]
    cols.append(-1.5*GM['sol']*R_SOL**2/rn**5*((1 - 5*z**2/rn**2)*r + 2*z*POLO))
    mu = GM['sol'] + GM['mercurio']; v2 = np.sum(v*v, 1)[:, None]; rv = np.sum(r*v, 1)[:, None]
    cols.append(mu/(C**2*rn**3)*((4*mu/rn - v2)*r + 4*rv*v))
    cols += [r/rn**4, r, -v]
    return np.stack(cols, axis=-1)            # (n, 3, 13)
ESCALA = np.array([1.0] + [1.0]*7 + [1.0, 1.0, 1.0, 1.0, 1.0])
VERDAD = np.array([GM['sol'] + GM['mercurio']] + [GM[p] for p in PLAN] + [np.nan, 1.0, 0, 0, 0])

def preparar(paso=1, ruido_m=0.0, semilla=0, desde_pos=False):
    idx = slice(None, None, paso); h = H*paso
    rs = {k: D[k][idx, 1:4] for k in D}; vs = {k: D[k][idx, 4:7] for k in D}
    rng = np.random.default_rng(semilla)
    rM = rs['mercurio'] - rs['sol']
    if ruido_m > 0 or desde_pos:
        rM = rM + rng.normal(0, ruido_m/149597870700, rM.shape)
        v = deriv(rM, h, 1); a = deriv(rM, h, 2); r = rM[5:-5]; sl = slice(5, -5)
    else:
        vM = vs['mercurio'] - vs['sol']; a = deriv(vM, h, 1); r = rM[5:-5]; v = vM[5:-5]; sl = slice(5, -5)
    rp = {p: (rs[p] - rs['sol'])[sl] for p in PLAN}
    return biblioteca(r, v, rp), a

def stlsq(Th, y, lam, activos):
    n = Th.shape[-1]; A = Th.reshape(-1, n); b = y.reshape(-1)
    s = np.sqrt(np.mean(A**2, 0)); s[s == 0] = 1; An = A/s
    act = np.array(activos, bool)
    for _ in range(25):
        xi = np.zeros(n)
        if act.any(): xi[act] = np.linalg.lstsq(An[:, act], b, rcond=None)[0]
        nuevo = act & (np.abs(xi) >= lam*np.abs(xi).max())
        if (nuevo == act).all(): break
        act = nuevo
    err = np.sqrt(np.mean((An @ xi - b)**2))/np.sqrt(np.mean(b**2))
    return xi/s, act, err

LAMS = np.logspace(0, -14, 57)
def pareto(Th, y, activos=None, tol=0.05):
    if activos is None: activos = [True]*Th.shape[-1]
    res = [stlsq(Th, y, l, activos) for l in LAMS]
    e = np.array([r[2] for r in res]); emin = e.min()
    i = next(j for j in range(len(LAMS)) if e[j] <= (1 + tol)*emin)   # el umbral más grande a menos de 5 % del error mínimo
    return res, i

def resumen(xi, act, err):
    out = []
    for j in range(len(NOMBRES)):
        if act[j]:
            rel = xi[j]/VERDAD[j] if VERDAD[j] and np.isfinite(VERDAD[j]) and VERDAD[j] != 0 else None
            out.append(dict(termino=NOMBRES[j], coef=float(xi[j]), rel=(float(rel) if rel is not None else None), real=j < REAL))
    return dict(terminos=out, error=float(err))

if __name__ == '__main__':
    OUT = {}
    Th, a = preparar()
    res, i = pareto(Th, a)
    xi, act, err = res[i]
    print('lambda', LAMS[i], 'activos', [NOMBRES[j] for j in range(13) if act[j]], 'err', err)
    print('f =', xi[9], ' mu rel', xi[0]/VERDAD[0] - 1, ' J2', xi[8])
    for j in range(1, 8): print(NOMBRES[j], xi[j]/VERDAD[j] - 1)
    OUT['base'] = dict(lam=float(LAMS[i]), **resumen(xi, act, err))
    OUT['pareto'] = [dict(lam=float(l), err=float(r[2]), n=int(r[1].sum()), rg=bool(r[1][9]), falsos=int(r[1][10:].sum())) for l, r in zip(LAMS, res)]
    # interruptores: quitar planetas / J2 / RG de la biblioteca
    OUT['interruptores'] = {}
    for pl in (1, 0):
        for j2 in (1, 0):
            for rg in (1, 0):
                activos = [True] + [bool(pl)]*7 + [bool(j2), bool(rg), True, True, True]
                r2, i2 = pareto(Th, a, activos)
                OUT['interruptores'][f'{pl}{j2}{rg}'] = dict(lam=float(LAMS[i2]), **resumen(*r2[i2]))
                print(pl, j2, rg, [t['termino'] for t in OUT['interruptores'][f'{pl}{j2}{rg}']['terminos']], OUT['interruptores'][f'{pl}{j2}{rg}']['error'])
    json.dump(OUT, open('salida_base.json', 'w'), indent=1, ensure_ascii=False)
