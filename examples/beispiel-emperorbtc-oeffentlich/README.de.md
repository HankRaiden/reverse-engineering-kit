# Durchgerechnetes Beispiel: EmperorBTCs öffentliche Prinzipien im Reverse Engineering

[English](README.md) · [Haftungsausschluss](../../DISCLAIMER.md)

> Unabhängiges Beispiel, **nicht mit EmperorBTC verbunden**. Die Prinzipien sind in eigenen Worten zusammengefasst,
> mit Links zu seinen öffentlichen Threads. **Ich übernehme keine Verantwortung für jegliche Ergebnisse, die in
> Verbindung mit diesem Projekt gegebenenfalls erzielt werden können.** Keine Finanzberatung.

Alle acht Stufen, einmal durchgespielt, damit du siehst, was jede liefert. Die Dateien liegen in [`work/`](work/)
(auf Englisch; die Berichte gibt es auch auf Deutsch).

| Stufe | Datei | Ergebnis |
|-------|-------|----------|
| 1 Quelle | [01-source.md](work/01-source.md) | öffentliche X-Threads, Telegram-Index, Tutorial-Tabelle |
| 2 Prinzipien | [02-principles/](work/02-principles/) | 7 Karten: Volumen, Swing-Failure, 200-EMA, festes Risiko, Open Interest, Divergenz, Überleben |
| 3 Regeln | [03-rules.md](work/03-rules.md) | 3 Regeln + 1 Vergleichsregel, 8 eigene Annahmen markiert |
| 4 Kodierbarkeit | [04-codability.md](work/04-codability.md) | 3 von 7 Prinzipien nicht getestet, mit Begründung |
| 5 Vorabregistrierung | [05-hypotheses.md](work/05-hypotheses.md) | 4 Hypothesen, je mind. 270 Trades, gesperrt |
| 6 Backtest | [06-backtest/de/report.md](work/06-backtest/de/report.md) | 5 Perpetuals, 4h, 2022-01 bis 2026-10 |
| 7 Widerlegung | [07-refutation.md](work/07-refutation.md) | sechs Pflichtfragen beantwortet |
| 8 Paper-Plan | [08-paper-plan.md](work/08-paper-plan.md) | kein Paper-Start empfohlen |

## Das Ergebnis, ehrlich
| Hypothese | Urteil | Kernzahl |
|-----------|--------|----------|
| H1 Ausbruch mit Volumen > 0 R | **REJECT** | +0,059 R je Trade, 95-%-KI [−0,010; +0,121], trotz +163 % Gesamtrendite |
| H2 Volumen verbessert Ausbrüche | **REJECT** | Differenz +0,008 R, KI [−0,088; +0,097] |
| H3 Swing-Failure > 0 R | **REJECT** | −0,068 R, KI [−0,129; −0,006]: negativ |
| H4 200-EMA-Filter verbessert H1 | **REJECT** | Differenz +0,031 R, KI [−0,070; +0,126] |

**Was das bedeutet:** Unsere kodierten Versionen dieser Prinzipien zeigten auf fünf großen Coins keine belastbare
Kante. Das heißt **nicht**, dass der Trader falsch liegt. Gerade der diskretionäre Kontext, den er lehrt, fehlt in
den Regeln (Stufe 4). Diese Lücke ist die eigentliche Erkenntnis. Sie passt zu dem, was das Live-Projekt hinter
diesem Kit gefunden hat: Der messbare Ertrag kam aus wenigen Episoden kleiner Coins, nicht aus den großen.

Nachrechnen: `./fetch.sh` (nur öffentliche Daten).
