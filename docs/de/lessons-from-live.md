# Lehren aus dem Live-Betrieb

Dieses Kit stammt aus einem echten Projekt. Ein Krypto-Bot, gebaut aus öffentlich zugänglichem Trading-Wissen,
wurde von zwei KI-Agenten geführt und von einem Menschen kontrolliert. Er handelte vom **18. Februar bis 29. Juli 2026**
auf Bybit mit bewusst kleinem **Eigenkapital**.

> **Der Bot selbst ist nicht Teil dieses Kits und wird nicht veröffentlicht.** Hier stehen nur die Lehren, nur in
> Prozent und ohne Parameter. Keine dieser Zahlen ist eine Prognose oder Empfehlung.

## Was gemessen wurde
| Befund | Zahl | Fenster |
|--------|------|---------|
| Lernphase: Profit-Faktor der ersten rund 170 Trades | 1,00 (exakt break-even) | Feb–Mär 2026 |
| Zeitgewichtete Rendite nach dem letzten großen Regel-Update | +34,6 % | 01.04.–16.06.2026 |
| Bitcoin im selben Fenster | −3,3 % | 01.04.–16.06.2026 |
| Geldgewichtete Konto-Rendite (Bybit-Dashboard) | +7,8 % | 18.02.–03.07.2026 |
| Größter Zwischenverlust (zeitgewichtet) | −12,4 % | bis 16.06.2026 |

**Warum zwei so verschiedene Renditen?** Der Gewinn entstand überwiegend im April auf kleiner Kapitalbasis. Danach
kam mehr Kapital hinzu, und die Strategie lief etwa auf null. Zeitgewichtet misst die Strategie, geldgewichtet
misst das Konto. Beides ist wahr. Wer nur eine Zahl zeigt, verschweigt die andere.

## Die wichtigste Lehre: Konzentration
| Zeitraum | Zeitgewichtet | Ohne kleine Coins mit Kurssprüngen |
|----------|---------------|-------------------------------------|
| April–Mai | +35,7 % | +3,7 % |
| Juni–Juli | −3,0 % | −8,5 % |

Der Ertrag kam fast nur aus wenigen Episoden kleiner Coins mit starken Kurssprüngen. Bei großen, liquiden Coins lief
dieselbe Logik flach bis negativ. Deshalb gibt es `concentration()` in jedem Bericht dieses Kits.

## Was widerlegt wurde
| Idee | Ergebnis |
|------|----------|
| Längere Haltedauer bringt +47 % | Widerlegt: Mit echten Zeiten waren es −32,7 % (Look-Ahead). |
| Doppelter Hebel verdoppelt den Gewinn | Widerlegt: Risiko-Limits greifen zuerst, und es kam eine Liquidation dazu. |
| Härteres Nachziehen des Stops schützt Gewinne | Widerlegt: Jede Alternative war schlechter. |
| Abgebrochene Limit-Orders filtern Verlierer | Widerlegt: Das Konfidenzintervall umfasst null. |
| Illiquide Coins meiden | Widerlegt: Die illiquidesten Coins waren die größten Gewinner (siehe Konzentration). |
| Mehr Coins bringen mehr Streuung | Widerlegt: Effektiv blieben es etwa 1,7 unabhängige Wetten. |
| Marktbreite als Regime-Ampel | Widerlegt: Der Effekt war ein Look-Ahead-Artefakt. |
| Öfter handeln bringt mehr | Widerlegt: Jede höhere Frequenz verschlechterte alle Risiko-Kennzahlen. |
| Bessere Einstiegs-Filter finden | Widerlegt: Über 7.874 Signale außerhalb der Stichprobe verbesserte kein Filter das Ergebnis messbar. |

**Muster:** Was die Tests überlebte, nahm fast immer etwas weg, etwa Verlust-Zeitfenster, Meme-Coins oder nicht
zugeordnete Symbole. Etwas hinzuzufügen half praktisch nie.

## Die Pause
Am 29. Juli wurde der Bot pausiert. Eine Simulation mit dem unveränderten Code über die folgenden 56 Tage ergab
im Median +2,4 % (mittlere 90 % der Pfade: −4,9 % bis +19,3 %). Bitcoin stieg im selben Zeitraum um +34,1 %.
Der Bot hätte vom Anstieg also nur einen kleinen Teil mitgenommen.
