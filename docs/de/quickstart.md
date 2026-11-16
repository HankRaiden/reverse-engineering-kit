# Schnellstart: in 10 Minuten zur ersten Stufe

Du brauchst kein Python. Du brauchst eine Quelle, der du vertraust, und [Claude Code](https://claude.com/claude-code)
(oder ein anderes Agenten-Werkzeug, das `AGENTS.md` liest).

## 1. Einrichten (einmalig)
```bash
git clone https://github.com/HankRaiden/reverse-engineering-kit.git
cd reverse-engineering-kit
uv sync --extra data      # installiert den Rechenkern (uv: https://docs.astral.sh/uv/)
uv run pytest -q          # alles grün? Dann ist der Kern in Ordnung.
claude                    # Claude Code im Ordner starten
```

## 2. Deine Rolle
Du bist **Chairman**. Du schreibst keinen Code und rechnest nichts. Du entscheidest an drei Toren:

| Tor | Nach Stufe | Deine Frage |
|-----|-----------|-------------|
| 1 | 2 Prinzipien | Sind das wirklich die Kernideen meiner Quelle? |
| 2 | 5 Hypothesen | Will ich mich auf genau diese Tests festlegen? Danach wird gesperrt. |
| 3 | 8 Paper-Plan | Starte ich das Paper-Trading unter diesen Abbruchregeln? |

## 3. Der erste Befehl
Sag dem Agenten auf Deutsch, was du prüfen willst, oder rufe die Stufe direkt auf:
```
/source  Ich möchte die öffentlichen Swing-Trading-Prinzipien von <Quelle> prüfen. Links: …
```
Der CIO legt `work/01-source.md` an. Dann folgen der Reihe nach:

```
/source → /principles → [Tor 1] → /rules → /codability → /preregister → [Tor 2, rekit lock]
       → /backtest → /refute → /paper-plan → [Tor 3] → rekit paper
```
Mit `/chairman` siehst du jederzeit, welches Tor offen ist und wer dran ist.

## 4. Was du am Ende bekommst
- Ein Regelwerk, das zwei Menschen gleich lesen würden (`work/03-rules.md`)
- Eine ehrliche Liste, was sich nicht in Code fassen lässt (`work/04-codability.md`)
- Je Hypothese ein Urteil **ACCEPT / REJECT / HOLD** mit Konfidenzintervall, Korrektur für viele Versuche und
  Konzentrations-Check (`work/06-backtest/report.md`)
- Ein Widerlegungs-Register, damit du dieselbe Idee nicht zweimal teuer lernst
- Einen Paper-Trading-Plan mit vorab festgelegten Abbruchregeln

## 5. Was du nicht bekommst
Kein Live-Trading. Das Kit kann keine Orders senden, und ein automatischer Test verhindert, dass es das je lernt.
Siehe [SAFETY.md](../../SAFETY.md) und [Nach dem Paper-Trading](after-paper-trading.md).

Ein komplett durchgespieltes Beispiel liegt in `examples/beispiel-emperorbtc-oeffentlich/`.
