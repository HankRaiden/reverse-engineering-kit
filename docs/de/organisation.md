# Die Organisation: zwei Agenten, ein Prüfer, ein Mensch

Die wichtigste Idee des Kits ist keine Formel, sondern eine **Gewaltenteilung**. Kein Agent darf allein
entscheiden, was als bewiesen gilt.

## Rollen
| Rolle | Wer | Darf | Darf nicht |
|-------|-----|------|-----------|
| **Chairman** | du | an den Toren GO / HOLD / NO-GO geben, jede Entscheidung per Veto stoppen | sich zur Technik überreden lassen, ohne die Belege zu sehen |
| **CIO** | KI-Agent | Quelle erfassen, Prinzipien und Regeln formulieren, Aufträge schreiben, Lieferungen bewerten (0–100) | selbst rechnen oder Code schreiben, Tore überspringen |
| **CTO** | KI-Agent | Regeln kodieren, `rekit` ausführen, mit Belegen liefern | eigene Statistik schreiben, gesperrte Dateien ändern, Orders senden |
| **Challenger** | KI-Agent | jedes Ergebnis angreifen (6 Pflichtfragen), Widerlegungen ins Register schreiben | beschönigen |

## Zwei Klassen von Arbeit
- **ANALYSE:** Lesen, Zusammenfassen, Backtests, Berichte. Die Agenten arbeiten selbständig.
- **ENTSCHEIDUNG:** Prinzipien-Auswahl, Vorabregistrierung, Paper-Start. Diese Arbeit startet nur mit dem
  wörtlichen Satz `CHAIRMAN-GO: …`. Jede Entscheidung landet in `work/approval-log.jsonl`.

## Der Kreislauf
```
CIO formuliert Auftrag ──► [Tor, falls ENTSCHEIDUNG: Chairman GO / HOLD / NO-GO]
        ▲                                │ GO
        │ HOLD / NO-GO: zurück           ▼
CIO bewertet ◄── Challenger greift an ◄── CTO baut, testet, liefert mit Belegen
```

## Vier Angaben in jeder Agenten-Antwort
1. **Verdict:** ACCEPT · ACCEPT_WITH_AUFLAGEN · HOLD · REJECT
2. **Klasse:** ANALYSE oder ENTSCHEIDUNG
3. **Nächstes Tor:** was vor dem nächsten Schritt erfüllt sein muss
4. **Wer ist dran:** CIO, CTO oder Chairman

So weißt du als Chairman in jeder Nachricht in fünf Sekunden, ob du gebraucht wirst.

## Warum so viel Form?
Weil KI-Agenten sehr überzeugend formulieren, auch wenn sie sich irren. Im Projekt, aus dem dieses Kit stammt,
liefen über 150 formale Aufträge und über 100 Bewertungen durch genau diese Schleife. Die teuersten Fehler
entstanden dort, wo sie umgangen wurde.

## Beispiel
Einen vollständigen Auftrag mit Bewertung findest du in
`examples/beispiel-emperorbtc-oeffentlich/work/`.
