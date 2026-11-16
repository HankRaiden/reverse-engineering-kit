# Stufe 4 · Kodierbarkeits-Matrix

> Wer: CTO · Ergebnis: `work/04-codability.md` · Tor: keins

| Regel | Kodierbar? | Was geht beim Kodieren verloren? | Daten nötig | Daten verfügbar? | Look-Ahead-Risiko | Entscheidung |
|-------|-----------|----------------------------------|-------------|------------------|-------------------|--------------|
| R1 | ja / teilweise / nein | | OHLCV | ja | z. B. Swing-Punkte erst nach Bestätigung bekannt | testen / nicht testen |

## Ehrlichkeits-Vermerk
- Was ein diskretionärer Trader „sieht“, aber nicht beschreibt, kann kein Code nachbilden. Ein negatives Testergebnis widerlegt also die **Regel**, nicht automatisch den **Trader**.
- Regeln mit „nein“ werden nicht still weggelassen, sondern hier mit Grund aufgeführt.
