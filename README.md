# Bundeswettbewerb Mathematik 2025 - Runde 1

zusammen mit henry :3

[Link zum PDF mit Aufgaben (https://www.mathe-wettbewerbe.de/)](https://www.mathe-wettbewerbe.de/fileadmin/Mathe-Wettbewerbe/Bundeswettbewerb_Mathematik/Dokumente/Aufgaben_und_Loesungen_BWM/2025/BWM_2025_Aufgabenblatt_SCREEN.pdf)

[Link zum PDF mit unseren Lösungen](final.pdf) (Stand 03.03.2025, also so wie es eingereicht wurde) Wird nicht mehr neugeneriert, wenn Änderungen an `bwm.tex` gemacht werden, die neue Version muss jeder selbst kompilieren

## Potentielle Punktabzüge

(In Bezug auf die [abgegebene Version](final.pdf), ich versuche momentan diese Fehler nachzuholen)

✔️ = Problem (immerhin) nachbearbeitet, 〰️ = meh, ❌ = nicht

|Aufgabe|Probleme|
|-|-|
|A1|-|
|A2|<ul><li>❌ aus den beiden iterativen Mustern von 2^m und n!/(5m)! lässt sich nicht unbedingt folgern, dass die Reihe an LZ(n!) auch alle Ziffern unendlich oft hat</li></ul>|
|A3|<ul><li>〰️ unerklärt, warum MC und ME die Winkelhalbierenden ihrer Halbkreissektoren sind</li><li>✔️ keine Erklärung für sqrt(cos^2(a)) = cos(a)</li></ul>|
|A4|<ul><li>❌ "Hufeisen"strategie funktioniert nicht für n=3 oder m=3; Renate muss vorher aufhören, Erhard zu spiegeln</li></ul>|

## Struktur

- `./bwm`: `.tex`-Dateien und all die anderen auxfiles die im `.gitignore` stehen
- `./henry`: Lösungen, die Henry mir geschickt hat
- `./img`: Bilder für dieses README
- `./python`: Python scripts zum Überprüfen der Beweise unserer Lösungen

## Bilder

Ich hab dieses Projekt ausgenutzt um auch ein bisschen LaTeX zu lernen :)

Formeln: <br>![alt text](img/formel.png)

Tabellen: <br>![alt text](img/tabelle.png)

Wunderschöne geometrische Skizzen: <br>![alt text](img/geo.png)

Und noch mehr wunderschöne Diagramme: <br>![alt text](img/spiel.png)
