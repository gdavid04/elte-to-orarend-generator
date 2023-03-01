import matplotlib.pyplot as plt
import pandas as pd
import re

oraListaRaw = pd.read_csv('orak.csv')
oraLista = pd.DataFrame(oraListaRaw, columns = [ 'Kurzus', 'Idopont', 'Helyszin' ])

fig, ax = plt.subplots()
ax.axis([-0.5, 4.5, 24, 0])
ax.set_xticks(range(5))
ax.set_xticklabels([ 'Hétfő','Kedd', 'Szerda', 'Csütörtök', 'Péntek' ])
ax.set_yticks(range(24))
ax.set_yticklabels([ f'{ora}:00' for ora in range(24) ])
ax.hlines(range(24), -0.5, 4.5, colors = 'lightgray', zorder = -1)
ax.vlines([ n + 0.5 for n in range(5) ], 24, 0, colors = 'lightgray', zorder = -1)
for ora in oraLista.itertuples():
	m = re.match('(\\S+) ([0-9]+)\\:([0-9]+)\\-([0-9]+)\\:([0-9]+)', ora[2])
	nap = { 'Hétfo': 0, 'Kedd': 1, 'Szerda': 2, 'Csütörtök': 3, 'Péntek': 4 }[m.group(1)]
	oraKezd = int(m.group(2)) + int(m.group(3)) / 60
	oraHossz = int(m.group(4)) + int(m.group(5)) / 60 - oraKezd
	bar = ax.bar(nap, oraHossz, 1, oraKezd, edgecolor = 'black', color = 'lightblue' if ora[1].endswith('\nElőadás') else 'lightyellow')
	ax.bar_label(bar, [ora[1] + '\n' + ora[3].removesuffix(" (Interaktív tábla)")], label_type = 'center')

fig.show()
plt.waitforbuttonpress()
