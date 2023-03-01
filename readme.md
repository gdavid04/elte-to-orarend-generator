# ELTE TO lekérdező és Órarend Generátor
Az eszköz célja, hogy a TO-s adatbázis automatikus lekérdezésével gyorsan generáljon egy órarendet.

Használat
---------
- Telepítsd a Python 3-at és a `dependencies`-ben szereplő csomagokat pl. `pip`-el
- Exportáld a Neptunból a felvett kurzusok listáját xlsx-be és helyezd a letöltött `export.xlsx` fájlt a projekt mappájába
- Futtasd le az `orarend.py`-t, ami legenerál egy `orak.csv` fájlt, ami tartalmazza az eszköz által megtalált órákat és figyelmeztet, ha egy kurzushoz nem talált semmit)
- A hiányzó órákat kézzel add hozzá az `orak.csv`-hez
- Futtasd le a `tablazat.py`-t, ami legenerálja az órarendet, amit aztán a mentés gombbal tudsz elmenteni (méretezd át az ablakot, ha összefolyik a szöveg)

Figyelmeztetés
--------------
A program által generált kimenet csak tájékoztató jellegű.
