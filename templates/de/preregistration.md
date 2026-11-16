# Stufe 5 · Hypothesen-Vorabregistrierung

> Wer: CIO · Ergebnis: `work/05-hypotheses.md` + `work/05-hypotheses.toml` · **Tor: CHAIRMAN-GO, danach `rekit lock`**

Nach dem Sperren ist die Datei eingefroren. Wer sie danach ändert, bekommt von `rekit backtest` eine Ablehnung.
Neue Ideen gehören in eine NEUE Datei, und sie zählen als zusätzliche Versuche.

## H<N> · <Aussage in einem Satz>
- **Regel(n):** R<N> aus `work/03-rules.md`
- **Erwartung:** z. B. „Erwartungswert > 0 R je Trade“
- **Messgröße:** `expectancy_r` oder `expectancy_diff_r` (gegen eine Vergleichsregel)
- **Verwerfungs-Kriterium:** Die untere Grenze des 95-%-Konfidenzintervalls liegt nicht über der Schwelle.
- **Mindest-Stichprobe:** N Trades (mit `rekit.stats.min_trades` begründet)
- **Daten:** Börse, Symbole, Zeitrahmen, Zeitraum
- **Parameter-Raster (falls vorhanden):** Jede Kombination zählt als eigener Versuch. Beurteilt wird nur außerhalb der Stichprobe (Walk-Forward).

## Zahl der Versuche
Summe aller Varianten in dieser Datei: __ (fließt in die Deflated-Sharpe-Korrektur ein)

## Chairman
`CHAIRMAN-GO: Vorabregistrierung <Datei> ist genehmigt.` → danach `rekit lock work/05-hypotheses.toml`
