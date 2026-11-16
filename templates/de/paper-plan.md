# Stufe 8 · Paper-Trading-Plan

> Wer: CIO + CTO · Ergebnis: `work/08-paper-plan.md` · **Tor: CHAIRMAN-GO für den Start**
> Paper-Trading heißt: echte Kurse, fiktive Trades, kein Geld, keine Orders.

## Was getestet wird
- Hypothese: H<N> (Urteil im Backtest: ACCEPT · REJECT · HOLD)
- Wenn das Urteil nicht ACCEPT ist: **Warum trotzdem Paper-Trading?** (z. B. nur zum Lernen, mit klarer Kennzeichnung)

## Ablauf
- Befehl: `rekit paper work/05-hypotheses.toml --hypothesis H<N> --symbol <SYMBOL>`
- Journal: `work/paper-H<N>-<symbol>.jsonl`
- Dauer: mindestens N Trades oder M Wochen, je nachdem, was später eintritt

## Vorab festgelegte Abbruch- und Erfolgskriterien
| Kriterium | Grenze | Aktion |
|-----------|--------|--------|
| Erwartungswert nach N Trades | unter Backtest-KI | Abbruch, zurück zu Stufe 5 |
| Max. Zwischenverlust | z. B. −15 % | Pause, Ursachenanalyse |
| Abweichung Paper vs. Backtest je Trade | > X R | Ausführungsmodell prüfen |

## Wöchentlicher Rhythmus
Wochen-Review mit `templates/de/weekly-review.md`; jede Schließung mit `templates/de/post-mortem.md`.

## Chairman
`CHAIRMAN-GO: Paper-Start H<N> ist genehmigt.`
