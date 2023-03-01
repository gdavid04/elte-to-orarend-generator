import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from datetime import date
import requests

# TODO grafikus felület
ev = date.today().year
if date.today().month <= 6:
	felev = f'{ev-1}-{ev}-2'
else:
	felev = f'{ev}-{ev+1}-1'
print(f'Félév: {felev}')
kurzusokRaw = pd.read_excel('export.xlsx')
kurzusok = pd.DataFrame(kurzusokRaw, columns = [
	'Tárgy neve', 'Kurzus típusa',
	'Tárgy kódja', 'Kurzus kódja'
])
keresek = defaultdict(list)
kurzusNevek = dict()
for kurzus in kurzusok.itertuples():
	keresek[kurzus[3]].append(kurzus[4])
	kurzusNevek[kurzus[3] + ' ' + str(kurzus[4])] = f'{kurzus[1]}\n{kurzus[2]}'
oraLista = pd.DataFrame()
for targykod, kurzuskodok in tqdm(keresek.items(), desc = 'Tanrend lekérdezése…'):
	keres = requests.post(url = 'https://tanrend.elte.hu/oktatoitanrend.php', data = {
		'mit': targykod,
		'felev': felev,
		'darab': '1000',
		'submit': 'keres_kod_azon'
	})
	orakRaw = pd.read_html(keres.text, attrs = { 'id': 'resulttable' }, header = 0, flavor = 'bs4')
	orak = pd.DataFrame(orakRaw[0], columns = [ 'Kurzuskod', 'Csop.', 'Idopont', 'Helyszin' ])
	talalt = orak[orak['Csop.'].isin(kurzuskodok)]
	for kurzuskod in kurzuskodok:
		if not talalt['Csop.'].eq(kurzuskod).any():
			nev = kurzusNevek[targykod + " " + str(kurzuskod)].replace('\n', ' ')
			print(f'Nem található óra: {nev}')
	oraLista = pd.concat([oraLista, talalt], ignore_index = True)
oraLista.insert(0, 'Kurzus', (oraLista.pop('Kurzuskod') + ' ' + oraLista.pop('Csop.').astype('string')).map(kurzusNevek))

oraLista.to_csv('orak.csv', index = False)
