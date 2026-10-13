# Vokabeltrainer

Drei Vokabeltrainer mit Karteikasten und Hörmodus, jeweils als eigene App:

| App | Adresse | Inhalt |
|---|---|---|
| Englisch | https://wolfgangmockel-del.github.io/vokabeltrainer-/ | Grundwortschatz 2000 (1796 Einträge) |
| Kroatisch | https://wolfgangmockel-del.github.io/vokabeltrainer-/kroatisch/ | 1200 Vokabeln und 300 Redewendungen (A2) |
| Spanisch | https://wolfgangmockel-del.github.io/vokabeltrainer-/spanisch/ | 1200 Vokabeln und 300 Redewendungen (A2) |

Auf Android in Chrome öffnen und im Menü „App installieren“ bzw. „Zum Startbildschirm hinzufügen“ wählen.
Jede App hat ihren eigenen Lernstand, pro Person, auf dem jeweiligen Handy.

Für Kroatisch und Spanisch braucht das Handy die passende Stimme der Google Sprachausgabe
(Einstellungen → System → Sprache & Eingabe → Sprachausgabe → Sprachdaten installieren).

## Ändern

Die Vokabeln stehen in `vokabeln.csv`, `vokabeln-hr.csv` und `vokabeln-es.csv`, der App-Code in `src/`.
Nach einer Änderung `python3 tools/build.py` ausführen; das erzeugt die drei Apps neu.
