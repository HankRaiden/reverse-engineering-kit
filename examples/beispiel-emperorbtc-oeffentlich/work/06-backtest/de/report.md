# Backtest-Bericht

_Die Urteile folgen Kriterien, die vor dem Test festgelegt wurden. HOLD heißt: zu wenige Trades für eine Entscheidung._

spec: 05-hypotheses.toml · n_trials: 4 · rekit: 0.1.0 · created: 2026-11-16

| Hypothese | Urteil | Geprüfte Messgröße | 95-%-Konfidenzintervall (R) | Trades | Trefferquote | Profit-Faktor | Erwartungswert (R) | Max. Zwischenverlust (%) | p (Holm-korrigiert) |
|---|---|---|---|---|---|---|---|---|---|
| H1 | **REJECT** | Erwartungswert +0.059 | [-0.043, +0.156] | 2011 | 37 % | 1.09 | +0.059 | -60.8 | 0.512 |
| H2 | **REJECT** | Differenz zur Vergleichsregel +0.008 | [-0.131, +0.139] | 2011 | 37 % | 1.09 | +0.059 | -60.8 | 1.000 |
| H3 | **REJECT** | Erwartungswert -0.068 | [-0.140, +0.001] | 1924 | 33 % | 0.90 | -0.068 | -82.7 | 1.000 |
| H4 | **REJECT** | Differenz zur Vergleichsregel +0.031 | [-0.122, +0.182] | 1651 | 38 % | 1.14 | +0.089 | -50.6 | 1.000 |

## H1 — A breakout confirmed by volume has a positive expectancy per trade

- **Urteil:** REJECT
- **Begründung:** expectancy +0.059 R, 95% CI [-0.043, +0.156] (not shown), deflated-Sharpe probability 0.54 over 4 tried variants
- **Gesamtrendite (%):** +163.3
- **Sharpe (annualisiert):** 0.64
- **Deflated-Sharpe-Wahrscheinlichkeit:** 0.54
- **Konzentration:** Anteil der besten 3 Trades am Netto-Ergebnis (%): 5 · Netto-Ergebnis ohne die besten 3 Trades (R): +111.9

> Gesamtrendite und Zwischenverlust sind zum Schließzeitpunkt verbucht (exit-marked): Jeder Trade riskiert beim Einstieg 1.0 % des Kontos, über alle Symbole. Bis zu 5 Positionen waren gleichzeitig offen (bis zu 5.0 % des Kontos im Risiko). Das ist kein festgelegtes Portfolio.

> Die Konfidenzintervalle ziehen ganze Kalenderwochen neu, damit gleichzeitige Trades nicht als unabhängige Belege zählen.

## H2 — Requiring volume improves the breakout compared with the same breakout without volume

- **Urteil:** REJECT
- **Begründung:** difference +0.008 R, 95% CI [-0.131, +0.139] does not clear +0.00
- **Gesamtrendite (%):** +163.3
- **Sharpe (annualisiert):** 0.64
- **Deflated-Sharpe-Wahrscheinlichkeit:** –
- **Konzentration:** Anteil der besten 3 Trades am Netto-Ergebnis (%): 5 · Netto-Ergebnis ohne die besten 3 Trades (R): +111.9

> Gesamtrendite und Zwischenverlust sind zum Schließzeitpunkt verbucht (exit-marked): Jeder Trade riskiert beim Einstieg 1.0 % des Kontos, über alle Symbole. Bis zu 5 Positionen waren gleichzeitig offen (bis zu 5.0 % des Kontos im Risiko). Das ist kein festgelegtes Portfolio.

> Die Konfidenzintervalle ziehen ganze Kalenderwochen neu, damit gleichzeitige Trades nicht als unabhängige Belege zählen.

## H3 — A swing failure (sweep of the last swing point and close back inside) has a positive expectancy

- **Urteil:** REJECT
- **Begründung:** expectancy -0.068 R, 95% CI [-0.140, +0.001] (not shown), deflated-Sharpe probability 0.00 over 4 tried variants
- **Gesamtrendite (%):** -77.6
- **Sharpe (annualisiert):** -0.79
- **Deflated-Sharpe-Wahrscheinlichkeit:** 0.00
- **Konzentration:** Anteil der besten 3 Trades am Netto-Ergebnis (%): -5 · Netto-Ergebnis ohne die besten 3 Trades (R): -136.4

> Gesamtrendite und Zwischenverlust sind zum Schließzeitpunkt verbucht (exit-marked): Jeder Trade riskiert beim Einstieg 1.0 % des Kontos, über alle Symbole. Bis zu 5 Positionen waren gleichzeitig offen (bis zu 5.0 % des Kontos im Risiko). Das ist kein festgelegtes Portfolio.

> Die Konfidenzintervalle ziehen ganze Kalenderwochen neu, damit gleichzeitige Trades nicht als unabhängige Belege zählen.

## H4 — Trading the volume breakout only with the 200-EMA trend improves it

- **Urteil:** REJECT
- **Begründung:** difference +0.031 R, 95% CI [-0.122, +0.182] does not clear +0.00
- **Gesamtrendite (%):** +267.4
- **Sharpe (annualisiert):** 0.85
- **Deflated-Sharpe-Wahrscheinlichkeit:** –
- **Konzentration:** Anteil der besten 3 Trades am Netto-Ergebnis (%): 4 · Netto-Ergebnis ohne die besten 3 Trades (R): +141.6

> Gesamtrendite und Zwischenverlust sind zum Schließzeitpunkt verbucht (exit-marked): Jeder Trade riskiert beim Einstieg 1.0 % des Kontos, über alle Symbole. Bis zu 5 Positionen waren gleichzeitig offen (bis zu 5.0 % des Kontos im Risiko). Das ist kein festgelegtes Portfolio.

> Die Konfidenzintervalle ziehen ganze Kalenderwochen neu, damit gleichzeitige Trades nicht als unabhängige Belege zählen.
