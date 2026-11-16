# Projektgeschichte: von der ersten Zeile bis zur Pause, radikal ehrlich

Dieses Kit ist das Nebenprodukt eines echten Projekts. Hier steht, wie es lief, mit allem, was gelang, und allem,
was schiefging. Alle Ergebnisse beziehen sich nur auf **Trades mit Eigenkapital auf Bybit** und sind nur in Prozent
angegeben. Der Bot selbst wird nicht veröffentlicht ([warum](../../SAFETY.md)).

## Zeitleiste
| Datum (2026) | Ereignis | Was es bedeutete |
|--------------|----------|------------------|
| 11. Feb | Tag null: Handels-Engine, Walk-Forward-Tester, erste Tests | Gebaut in KI-Agenten-Sessions, nicht von Hand |
| 18.–19. Feb | Live mit bewusst kleinem Eigenkapital, erster geschlossener Trade | Keine Demo-Phase vorab. Ein Fehler, den das Kit heute mit Paper-Trading vermeidet. |
| Feb–Mär | Lernphase: rund 170 Trades, Profit-Faktor **1,00** | Der Bot verdiente nichts, überlebte aber. Jeder Fehler wurde zur Regel. |
| Feb–Apr | **14 dokumentierte Vorfälle**, darunter eine Position 5 Stunden ohne Stop-Loss, Stops, die eine Fremdbibliothek still verfallen ließ (15 Tage unentdeckt), eine Buchführung mit 12,3 % Abweichung zur Börse | Daraus entstanden die 7 Architektur-Prinzipien und die [14 Anti-Muster](anti-patterns.md) |
| 16. Mär | Vorab definiertes Kriterium erreicht: 30 von 30 Trades mit stabilem Stop-Loss | Erstes formales Tor bestanden |
| Mär–Apr | 32 datengetriebene Änderungen, einzeln begründet und getestet | Die meisten, die überlebten, *nahmen etwas weg* (Zeitfenster, Meme-Coins) |
| April | Stärkster Monat: zeitgewichtet rund **+39 %** | Fast ganz aus wenigen kleinen Coins mit Kurssprüngen. Das wurde früh als Risiko benannt. |
| Mai | Kapital wird erhöht. Danach läuft die Strategie etwa auf **null**. | Geldgewichtete und zeitgewichtete Rendite laufen ab hier weit auseinander |
| Mai–Jul | Parallel ein **vollautonomer Versuch** auf einem zweiten Eigenkapital-Konto: Die Agenten durften Strategien ohne Chairman-Freigabe live schalten. | Ab 5. Juni praktisch stillgelegt, null neue belastbare Kanten, laufende Kosten über dem Ertrag. Eingestellt. Der Mensch an den Toren war nicht Bürokratie, sondern der Teil, der funktionierte. |
| 16. Jun | Unabhängige Nachrechnung: **+34,6 %** zeitgewichtet seit 1. April gegenüber Bitcoin **−3,3 %** | Echte Eigenleistung im Messfenster, aber kurz und konzentriert |
| Jun–Jul | „Quantensprung-Untersuchung“: Fünf Analysen widerlegten sieben scheinbare Verbesserungen | Es gab keinen weiteren Hebel im Regelwerk |
| 8. Jul | Chairman reduziert das Kapital bewusst (Risiko runter) | Entscheidung des Menschen, nicht der Agenten |
| 29. Jul | Chairman pausiert den Bot, ohne offene Position | Ende der Live-Phase mit Eigenkapital |
| 28. Aug | Server abgeschaltet, vollständiges Archiv gesichert | |
| 23. Sep | Simulation „Was hätte der Bot ohne Pause verdient?“ für 56 Tage: Median **+2,4 %**, Bitcoin **+34,1 %** | Die Pause hat wenig gekostet. Gegen einfaches Halten von Bitcoin hätte der Bot klar verloren. |
| Nov | Dieses Kit: die Methode wird geteilt, der Bot nicht | |

## Bilanz
| Erfolge | Misserfolge |
|---------|-------------|
| Live-Track-Record mit echtem Geld statt Backtest-Poesie | Lernphase exakt break-even (Profit-Faktor 1,00) |
| +34,6 % zeitgewichtet (1. Apr–16. Jun) bei Bitcoin −3,3 %, dreifach unabhängig nachgerechnet | Der Gewinn hing an wenigen kleinen Coins. Ohne sie: April–Mai +3,7 %, Juni–Juli −8,5 % |
| In einer forensischen Prüfung über 62 Tage war keine von 228 Positionen je ohne Stop-Loss eröffnet worden | Davor gab es mehrere Vorfälle mit ungeschützten Positionen |
| Neun verlockende Ideen sauber widerlegt, bevor sie Geld kosteten | Eine Idee sah im naiven Backtest nach +47 % aus und war real −32,7 % |
| Gewaltenteilung CIO / CTO / Chairman hat Fehler zuverlässig abgefangen | Der vollautonome Versuch ohne Mensch an den Toren scheiterte |
| Über 150 formale Aufträge und über 100 Bewertungen, jede Freigabe protokolliert | Ein Agent meldete einmal Testergebnisse, die nie gelaufen waren. Seitdem führen erfundene Belege automatisch zu REJECT. |
| | Geldgewichtet lag die Konto-Rendite bis 3. Juli nur bei +7,8 % |

| Chancen | Risiken |
|---------|---------|
| Öffentliches Wissen lässt sich systematisch zerlegen und prüfen, mit jedem Broker mit stabiler API | Ein diskretionärer Trader lässt sich nie vollständig kodieren |
| KI-Agenten machen Forschung schnell und billig | KI-Agenten formulieren überzeugend, auch wenn sie sich irren. Ohne Tore und Belege ist das gefährlich. |
| Vorabregistrierung und Widerlegungs-Register sparen teure Wiederholungen | Kurze Track-Records (Monate) sagen wenig über Jahre |
| Die Methode ist auf andere Märkte übertragbar | Hebel und kleine Coins können in Stunden mehr kosten als Monate bringen |

## Was wir heute anders machen würden
1. Zuerst Paper-Trading, dann erst Live. Genau deshalb endet das Kit dort.
2. Den Konzentrations-Check von Tag eins an in jeden Bericht nehmen.
3. Den Menschen an den Toren nie wegoptimieren.
