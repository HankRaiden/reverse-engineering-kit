# Was übertragbar ist und was nicht

## Übertragbar
Das Kit ist nicht an Krypto gebunden. Es funktioniert mit jedem öffentlichen Playbook, jeder Strategie und jedem
eigenen Prinzip, solange drei Dinge gelten:
1. **Die Regeln lassen sich als Wenn-Dann formulieren**, auch nur teilweise (Stufe 4 benennt den Rest).
2. **Es gibt historische Kursdaten** in der passenden Auflösung (Kerzen mit Eröffnung, Hoch, Tief, Schluss, Volumen).
3. **Der Broker oder die Börse bietet eine stabile API**, spätestens dann, wenn du nach dem Paper-Trading selbst
   weitergehst.

## Woran du eine stabile API erkennst
| Kriterium | Warum es zählt |
|-----------|----------------|
| Versionierte, dokumentierte Endpunkte | Damit sich nichts still ändert |
| Explizite Fehlercodes in jeder Antwort | „Kein Fehler“ ist nicht „Erfolg“ (Anti-Muster 1) |
| Stop-Loss direkt an der Börse setzbar und auslesbar | Schutz, der auch ohne dein Programm wirkt |
| Abrechnung je Trade abrufbar | Das Ergebnis kommt von der Börse, nicht aus eigener Rechnung |
| Test- oder Demo-Umgebung | Paper-Trading und Ausführungstests ohne Geld |
| Öffentliche Marktdaten ohne Konto | Backtests ohne Schlüssel |

## Andere Märkte
- **Aktien und ETFs:** Achte auf Dividenden, Splits, Handelszeiten und Lücken über Nacht.
  Lücken über den Stop sind dort häufiger.
- **Futures:** Achte auf Rollen der Kontrakte und Margin-Regeln.
- **Devisen:** Spreads ändern sich je nach Sitzung stark. Rechne konservativ mit Slippage.

Eigene Datenquellen bindest du per CSV ein (`ts, open, high, low, close, volume`) und nutzt `--csv-dir`.

## Nicht übertragbar
- Das Bauchgefühl eines diskretionären Traders. Was nicht beschrieben ist, kann nicht kodiert werden.
- Ergebnisse von einem Markt auf einen anderen. Jede Übertragung ist eine neue Hypothese.
