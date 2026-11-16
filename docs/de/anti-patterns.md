# 14 Anti-Muster aus einem echten Projekt

Jedes dieser Muster hat im Ursprungsprojekt Zeit, Geld oder Vertrauen gekostet. Sie sind hier allgemein
formuliert, damit sie für jede Strategie und jeden Broker gelten.

| # | Anti-Muster | Was passiert | Gegenmittel |
|---|-------------|--------------|-------------|
| 1 | „Kein Fehler“ = „Erfolg“ | Eine Börsen-Antwort ohne Fehlermeldung wurde als gesetzter Stop gewertet. Die Position war stundenlang ungeschützt. | Antwort explizit prüfen, danach den Zustand an der Börse zurücklesen. |
| 2 | Lokaler Zustand statt Börsen-Zustand | Das Programm glaubte, ein Stop sei aktiv, die Börse wusste nichts davon. | Die Börse ist die Wahrheit. Unabhängiger Abgleich in festen Abständen. |
| 3 | Zustand ändern, bevor die Aktion gelingt | Der neue Wert stand schon im Speicher, der Vergleich „alt = neu“ übersprang den Aufruf. | Zustand erst nach bestätigtem Erfolg ändern. |
| 4 | Gewinn selbst ausrechnen | Lokale Rechnung und Börsen-Abrechnung liefen auseinander und führten zu Fehlentscheidungen über 48 Stunden. | Ergebnis immer aus der Abrechnung der Börse übernehmen. |
| 5 | Neuer Schließ-Pfad ohne Buchung | Eine neue Art, Positionen zu schließen, vergaß die Kapital-Buchung. Die Buchführung driftete über Wochen. | Liste aller Schließ-Pfade führen. Jeder neue Pfad wird zuerst dort eingetragen. |
| 6 | Look-Ahead im Backtest | +47 % auf dem Papier, −32,7 % mit echten Zeiten. | Ausführung zur nächsten Kerze, `rekit check-lookahead`. |
| 7 | Tagesdaten für Tagesentscheidungen | Ein „Regime-Signal“ nutzte den Tagesschluss, der zum Entscheidungszeitpunkt noch nicht feststand. | Punkt-in-Zeit-Daten, Zeitstempel prüfen. |
| 8 | Ergebnis hängt an wenigen Trades | Fast der ganze Gewinn kam aus wenigen kleinen Coins mit Kurssprüngen. | `concentration()` in jedem Bericht. |
| 9 | Zu optimistisches Ausführungsmodell | Der Backtest füllte Limit-Orders, die real nie gefüllt worden wären. | Konservative Füll-Regeln. Paper-Trading vergleicht mit der Realität. |
| 10 | Mehr Symbole = mehr Streuung | 588 Symbole, aber effektiv nur etwa 1,7 unabhängige Wetten: Krypto bewegt sich als ein Faktor. | Korrelation messen statt Symbole zählen. |
| 11 | Öfter handeln = mehr verdienen | Jede höhere Frequenz verschlechterte alle Risiko-Kennzahlen. | Frequenz als Hypothese testen, nicht annehmen. |
| 12 | Konfiguration ohne Code ausrollen | Ein Schalter in der Konfiguration verwies auf Code, der auf dem Server noch fehlte. Die Funktion blieb still aus. | Konfiguration und Code immer zusammen ausliefern und danach prüfen. |
| 13 | Belege, die niemand nachgeprüft hat | Ein Agent meldete Testergebnisse, die nie gelaufen waren. | Jede Zahl mit Befehl und Ausgabe. Erfundene Belege führen automatisch zu REJECT. |
| 14 | Widerlegtes wiederentdecken | Dieselbe attraktive Idee kam alle paar Wochen „neu“ auf. | Widerlegungs-Register mit Bedingung für Wiedereröffnung. |
