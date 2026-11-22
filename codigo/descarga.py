"""Descarga de JPL Horizons: vectores baricéntricos ICRF (500@0), 1900-2100, paso 12 h."""
import urllib.parse, subprocess, numpy as np, sys, os
CUERPOS = {'sol':'10','mercurio':'199','venus':'299','tierra':'3','marte':'4','jupiter':'5','saturno':'6','urano':'7','neptuno':'8'}
TRAMOS = [('1900-01-01','1950-01-01'),('1950-01-01','2000-01-01'),('2000-01-01','2050-01-01'),('2050-01-01','2100-01-01 12:00')]
def baja(cod, a, b):
    q = dict(format='text', COMMAND=f"'{cod}'", EPHEM_TYPE="'VECTORS'", CENTER="'500@0'", START_TIME=f"'{a}'", STOP_TIME=f"'{b}'",
             STEP_SIZE="'12 h'", REF_PLANE="'FRAME'", REF_SYSTEM="'ICRF'", OUT_UNITS="'AU-D'", VEC_TABLE="'2'", CSV_FORMAT="'YES'", VEC_LABELS="'NO'", TIME_TYPE="'TDB'")
    t = subprocess.run(['curl', '-s', '-m', '600', 'https://ssd.jpl.nasa.gov/api/horizons.api?' + urllib.parse.urlencode(q)], capture_output=True, text=True, check=True).stdout
    s = t[t.index('$$SOE')+5:t.index('$$EOE')].strip().splitlines()
    return np.array([[float(x) for i, x in enumerate(l.split(',')) if i in (0, 2, 3, 4, 5, 6, 7)] for l in s])
for nom, cod in CUERPOS.items():
    f = f'raw/{nom}.npy'
    if os.path.exists(f): continue
    D = []
    for i, (a, b) in enumerate(TRAMOS):
        d = baja(cod, a, b)
        if D and abs(d[0, 0] - D[-1][-1, 0]) < 1e-6: d = d[1:]
        D.append(d)
    D = np.vstack(D); os.makedirs('raw', exist_ok=True); np.save(f, D); print(nom, D.shape, D[0, 0], D[-1, 0], flush=True)
