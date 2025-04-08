### Game of Life

Cílem projektu je vytvoření Conwayovy Hry života (Conway's Game of Life). Jedná se o simulaci změny stavu buněk na dvourozměrném poli podle předem daných pravidel. Uživatel na začátku zadá počáteční konfiguraci hracího pole a poté hra probíhá automaticky bez dalšího vstupu. Simulace funguje na základě čtyř jednoduchých pravidel, která určují zrození, přežití nebo zánik jednotlivých buněk:

1. Každá živá buňka s méně než dvěma živými sousedy zemře.
2. Každá živá buňka se dvěma nebo třemi živými sousedy zůstává žít.
3. Každá živá buňka s více než třemi živými sousedy zemře.
4. Každá mrtvá buňka s právě třemi živými sousedy oživne.

Projekt obsahuje textovou verzi hry spustitelnou v terminálu a grafickou verzi hry vytvořenou s pomocí knihovny PyGame.