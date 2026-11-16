# Stage 4 · Codability matrix

> Who: CTO · Output: `work/04-codability.md` · Gate: none

| Rule | Codable? | What is lost when coding it? | Data needed | Data available? | Look-ahead risk | Decision |
|------|----------|------------------------------|-------------|-----------------|-----------------|----------|
| R1 | yes / partly / no | | OHLCV | yes | e.g. swing points only known after confirmation | test / do not test |

## Honesty note
- What a discretionary trader "sees" but does not describe cannot be reproduced by code. A negative test result therefore refutes the **rule**, not automatically the **trader**.
- Rules marked "no" are not silently dropped; they are listed here with the reason.
