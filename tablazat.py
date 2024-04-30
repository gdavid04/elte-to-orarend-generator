import matplotlib.pyplot as plt
import pandas as pd
import re
import math

oraLista = pd.read_csv('orak.csv', dtype = str)

fig, ax = plt.subplots()
ax.set_xticks(range(5))
ax.set_xticklabels([ 'Hétfő','Kedd', 'Szerda', 'Csütörtök', 'Péntek' ])
ax.set_yticks(range(24))
ax.set_yticklabels([ f'{ora}:00' for ora in range(24) ])
ax.hlines(range(24), -0.5, 4.5, colors = 'lightgray', zorder = -1)
ax.vlines([ n + 0.5 for n in range(5) ], 24, 0, colors = 'lightgray', zorder = -1)
minh, maxh = 24, 0
for _, ora in oraLista.iterrows():
	nev, csop = ora['Kurzusnev'], ora['Csop.']
	if not isinstance(ora['Idopont'], str):
		print(f'Hiányos: {nev} {csop}')
		continue
	m = re.match('(\\S+) ([0-9]+)\\:([0-9]+)\\-([0-9]+)\\:([0-9]+)', ora['Idopont'])
	if not m:
		print(f'Hiányos: {nev} {csop}')
		continue
	nap = { 'Hétfo': 0, 'Kedd': 1, 'Szerda': 2, 'Csütörtök': 3, 'Péntek': 4 }[m.group(1)]
	oraKezd = int(m.group(2)) + int(m.group(3)) / 60
	oraHossz = int(m.group(4)) + int(m.group(5)) / 60 - oraKezd
	bar = ax.bar(nap, oraHossz, 1, oraKezd, edgecolor = 'black', color = 'lightyellow' if ora['Oratipus'] == 'gyakorlat' else 'lightblue')
	ax.bar_label(bar, [nev + '\n' + ora['Helyszin'].removesuffix(" (Interaktív tábla)")], label_type = 'center')
	minh, maxh = min(minh, oraKezd), max(maxh, oraKezd + oraHossz)
ax.axis([-0.5, 4.5, math.ceil(maxh), math.floor(minh)])

fig.show()
plt.waitforbuttonpress()
