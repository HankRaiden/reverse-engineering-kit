# Safety · Sicherheit

## What this kit can never do · Was dieses Kit nie kann
- **Send orders.** There is no order function, no private exchange endpoint and no field for API keys or secrets.
  · **Orders senden.** Es gibt keine Order-Funktion, keinen privaten Börsen-Endpunkt und kein Feld für Schlüssel.
- **Hold your money or your keys.** Market data comes from public endpoints or your own CSV files.
  · **Dein Geld oder deine Schlüssel halten.** Marktdaten kommen aus öffentlichen Endpunkten oder eigenen CSV-Dateien.

## How this is enforced · Wie das durchgesetzt wird
`tests/test_safety.py` fails the build if any file contains order or private-API calls (order placement,
private endpoints, key fields) or if the exchange library is used anywhere except the read-only data loader.
The test runs on every push (GitHub Actions). Pull requests that weaken it will not be merged.

`tests/test_safety.py` lässt den Build scheitern, sobald eine Datei Order- oder Private-API-Aufrufe enthält oder die
Börsen-Bibliothek außerhalb des lesenden Daten-Moduls benutzt wird. Der Test läuft bei jedem Push.

## Why · Warum
The bot this kit grew out of is **not** published, on purpose: inexperienced traders could copy it, lose money and
hold the author responsible. The kit gives you the method, not a money machine.

Der Bot, aus dem dieses Kit entstand, wird bewusst **nicht** veröffentlicht. Unerfahrene Trader könnten ihn
nachbauen, Geld verlieren und den Autor dafür verantwortlich machen. Das Kit gibt dir die Methode, keine Geldmaschine.

See also · Siehe auch: [DISCLAIMER.md](DISCLAIMER.md)
