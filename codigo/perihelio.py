import numpy as np, json
from sindy_mercurio import D, GM, H
r = D['mercurio'][:, 1:4] - D['sol'][:, 1:4]; v = D['mercurio'][:, 4:7] - D['sol'][:, 4:7]; t = D['sol'][:, 0]
mu = GM['sol'] + GM['mercurio']
hv = np.cross(r, v); e = np.cross(v, hv)/mu - r/np.linalg.norm(r, axis=1)[:, None]
# ángulo del perihelio medido en un plano fijo (plano orbital medio)
k = hv.mean(0); k /= np.linalg.norm(k); i0 = e[0] - (e[0] @ k)*k; i0 /= np.linalg.norm(i0); j0 = np.cross(k, i0)
ang = np.unwrap(np.arctan2(e @ j0, e @ i0))
anos = (t - 2451545.0)/365.25 + 2000
p = np.polyfit(anos, ang, 1); tasa = np.degrees(p[0])*3600*100
# promedio por órbita (88 d) para quitar oscilaciones de periodo corto
n = int(round(87.969/H)); m = len(ang)//n
ao = anos[:m*n].reshape(m, n).mean(1); go = ang[:m*n].reshape(m, n).mean(1)
po = np.polyfit(ao, go, 1); tasa_o = np.degrees(po[0])*3600*100
print('tasa total (″/siglo):', tasa, ' promediada por órbita:', tasa_o, ' órbitas:', m)
sel = slice(0, m, 4)
orb = r[:n+1:2] @ np.vstack([i0, j0]).T
json.dump(dict(tasa=float(tasa_o), anos=[round(float(x), 3) for x in ao[sel]], angulo_arcsec=[round(float((g - go[0])*180/np.pi*3600), 2) for g in go[sel]],
               orbita=[[round(float(a), 5), round(float(b), 5)] for a, b in orb], e=float(np.linalg.norm(e, axis=1).mean()), a=float(np.mean(-mu/(2*(np.sum(v*v, 1)/2 - mu/np.linalg.norm(r, axis=1))))/1)),
          open('salida_perihelio.json', 'w'))
