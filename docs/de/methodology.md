# Methodik: Warum die Zahlen dieses Kits belastbar sind

Die meisten Backtests im Netz sind nicht gelogen. Sie sind nur zu freundlich. Das Kit baut fünf Schutzwände
gegen die häufigsten Arten, sich selbst zu täuschen.

## 1. Vorabregistrierung statt nachträglichem Zurechtbiegen
Bevor eine Zahl berechnet wird, steht fest: Was wird getestet, woran wird es gemessen, ab wann gilt es als
widerlegt, und wie viele Trades braucht man dafür. Nach dem Chairman-GO friert `rekit lock` die Datei per
SHA-256 ein. `rekit backtest` verweigert jede geänderte Datei.
**Warum:** Wer nach dem Ergebnis die Regeln anpasst, misst am Ende nur, wie gut er anpassen kann.

## 2. Kein Blick in die Zukunft (Look-Ahead)
- Ein Signal wird auf dem **Schluss** einer Kerze berechnet und erst zur **Eröffnung der nächsten** ausgeführt.
- Swing-Hochs und -Tiefs sind erst bekannt, wenn die Bestätigungs-Kerzen geschlossen sind. `rekit` meldet sie
  entsprechend spät.
- `rekit check-lookahead` verändert zufällig alle Daten **nach** einem Zeitpunkt t. Ändert sich dadurch ein
  Signal **vor** t, schaut die Regel in die Zukunft, und der Test bricht ab.
**Warum:** In einem echten Projekt sah eine Idee im naiven Backtest nach +47 % aus. Mit echten Ausführungszeiten
waren es −32,7 %.

## 3. Ausführung realistisch statt optimistisch
Gebühren auf beiden Seiten, Slippage bei Market-Fills und Stops, Lücken über den Stop (Ausführung zur
Eröffnung, nicht zum Stop-Preis). Treffen Stop und Ziel dieselbe Kerze, gilt der Stop als zuerst getroffen.

## 4. Statistik, die mit Zufall rechnet
| Werkzeug | Frage, die es beantwortet |
|----------|---------------------------|
| Bootstrap-Konfidenzintervall (1.000×) | Wie sicher ist der Erwartungswert, wenn die Trades zufällig anders gefallen wären? |
| Deflated Sharpe (Bailey & López de Prado) | Wie wahrscheinlich ist das Ergebnis echt, wenn ich N Varianten probiert habe? |
| Holm-Korrektur | Halten mehrere Hypothesen gleichzeitig, oder hat eine nur zufällig „gewonnen“? |
| Stärke-Analyse (`min_trades`) | Wie viele Trades brauche ich überhaupt, um einen Effekt dieser Größe zu sehen? |
| Walk-Forward | Wenn ich Parameter auf der Vergangenheit wähle: Halten sie in der folgenden, ungesehenen Zeit? |

Das Urteil ist mechanisch:
- **HOLD:** weniger Trades als vorab festgelegt. Weder Ja noch Nein.
- **ACCEPT:** Die untere Grenze des 95-%-Intervalls liegt über der Schwelle, die Deflated-Sharpe-Wahrscheinlichkeit
  beträgt mindestens 0,95, und die Hypothese bleibt nach der Holm-Korrektur signifikant.
- **REJECT:** alles andere.

## 5. Konzentration: die unbequemste Frage
`concentration()` zeigt, wie viel des Ergebnisses aus den besten drei Trades oder dem besten Symbol stammt und was
ohne sie übrig bleibt. Ein Ergebnis, das an drei Trades hängt, ist kein Regelwerk, sondern Glück mit Buchführung.
Im Projekt, aus dem dieses Kit stammt, war genau das der wichtigste Befund (siehe [Lehren aus dem Live-Betrieb](lessons-from-live.md)).

## Was die Methodik nicht kann
Sie beweist keine Zukunft. Ein ACCEPT heißt: „In diesen Daten, mit diesen vorab festgelegten Regeln, ist der Effekt
unwahrscheinlich Zufall.“ Märkte ändern sich. Deshalb folgt auf ACCEPT Paper-Trading und nicht echtes Geld.
