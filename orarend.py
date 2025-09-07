import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from datetime import date
import requests

# TODO grafikus felület
kurzusokRaw = pd.read_excel('export.xlsx')
kurzusok = pd.DataFrame(kurzusokRaw, columns = [
	'Tárgy neve', 'Kurzus típusa',
	'Tárgy kódja', 'Kurzus kódja'
])
keresek = defaultdict(list)
kurzusNevek = dict()
kurzusTipusok = dict()
for kurzus in kurzusok.itertuples():
	keresek[kurzus[3]].append(kurzus[4])
	kurzusNevek[kurzus[3] + ' ' + str(kurzus[4])] = kurzus[1]
	kurzusTipusok[kurzus[3] + ' ' + str(kurzus[4])] = kurzus[2]
oraLista = []
for targykod, kurzuskodok in tqdm(keresek.items(), desc = 'Tanrend lekérdezése…'):
	keres = requests.get(url = 'https://gabordavid.web.elte.hu/to/query', params = {
		'subject_code': targykod
	})
	if keres.json()['status'] != 'ok':
		print(f'Hiba: {targykod}')
		continue
	orak = keres.json()['data']
	for kurzuskod in kurzuskodok:
		talalt = False
		for ora in orak:
			if ora['Csop.'] == str(kurzuskod):
				oraLista.append(ora)
				talalt = True
		if not talalt:
			oraLista.append({
				'Kurzusnev': kurzusNevek[targykod + ' ' + str(kurzuskod)],
				'Kurzuskod': targykod,
				'Csop.': kurzuskod,
				'Oratipus': kurzusTipusok[targykod + ' ' + str(kurzuskod)].lower()
			})
			print(f'Nem található óra: {targykod} {kurzuskod}')

pd.DataFrame(oraLista).to_csv('orak.csv', index = False)
