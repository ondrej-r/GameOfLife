# Game of Life

Cílem projektu je vytvoření Conwayovy Hry života (Conway's Game of Life). Jedná se o simulaci změny stavu buněk na dvourozměrném poli podle předem daných pravidel. Uživatel na začátku zadá počáteční konfiguraci hracího pole a poté hra probíhá automaticky bez dalšího vstupu. Simulace funguje na základě čtyř jednoduchých pravidel, která určují zrození, přežití nebo zánik jednotlivých buněk:

1. Každá živá buňka s méně než dvěma živými sousedy zemře.
2. Každá živá buňka se dvěma nebo třemi živými sousedy zůstává žít.
3. Každá živá buňka s více než třemi živými sousedy zemře.
4. Každá mrtvá buňka s právě třemi živými sousedy oživne.

Projekt obsahuje textovou verzi hry spustitelnou v terminálu a grafickou verzi hry vytvořenou s pomocí knihovny PyGame.

## Instalace a Použití

### Instrukce k instalaci:

Ujistěte se, že máte nainstalovaný Python na vašem počítači. Pokud ho nemáte, nainstalujte Python z [oficiální stránky](https://www.python.org/downloads/).

Dalším krokem je vytvoření a aktivace virtuálního prostředí. Pokud nemáte virtuální prostředí nainstalované, použijte:
```
pip install virtualenv
```
Vytvořte nové virtuální prostředí.
Ve Windows:
```
python -m venv .venv
```
nebo
Na MacOS/Linux:
```
python3 -m venv .venv
```
Aktivujte virtuální prostředí. Na Windows:
```
.venv\Scripts\activate
```
Na MacOS/Linux:
```
source .venv/bin/activate
```
Naklonujte repository pomocí Gitu:
```
git clone https://github.com/ondrej-r/GameOfLife.git
```
Nainstalujte požadované dependencies pomocí pip:

    pip install -r requirements.txt

### Pokyny k použití:

Pro spuštění textové verze hry v terminálu:
```
python src/main.py
```
Pro spuštění grafické verze s využitím PyGame:
```
python src/main.py -g
```

Podrobnější dokumentace je k nalezení [zde](https://github.com/ondrej-r/GameOfLife/wiki).
