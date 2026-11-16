# Quickstart: the first stage in 10 minutes

You do not need Python. You need a source you trust and [Claude Code](https://claude.com/claude-code)
(or another agent tool that reads `AGENTS.md`).

## 1. Set up (once)
```bash
git clone https://github.com/HankRaiden/reverse-engineering-kit.git
cd reverse-engineering-kit
uv sync --extra data      # installs the core (uv: https://docs.astral.sh/uv/)
uv run pytest -q          # all green? then the core is fine
claude                    # start Claude Code in the folder
```

## 2. Your role
You are the **chairman**. You write no code and calculate nothing. You decide at three gates:

| Gate | After stage | Your question |
|------|-------------|---------------|
| 1 | 2 Principles | Are these really the core ideas of my source? |
| 2 | 5 Hypotheses | Do I commit to exactly these tests? The file gets locked afterwards. |
| 3 | 8 Paper plan | Do I start paper trading under these stop rules? |

## 3. The first command
Tell the agent in your own language what you want to test, or call the stage directly:
```
/source  I want to test the public swing-trading principles of <source>. Links: …
```
The CIO creates `work/01-source.md`. Then, in order:

```
/source → /principles → [gate 1] → /rules → /codability → /preregister → [gate 2, rekit lock]
       → /backtest → /refute → /paper-plan → [gate 3] → rekit paper
```
`/chairman` shows you at any time which gate is open and whose turn it is.

## 4. What you get at the end
- A rule set two people would read the same way (`work/03-rules.md`)
- An honest list of what cannot be coded (`work/04-codability.md`)
- Per hypothesis a verdict **ACCEPT / REJECT / HOLD** with confidence interval, correction for many trials and a
  concentration check (`work/06-backtest/report.md`)
- A refutation register, so you do not learn the same expensive lesson twice
- A paper-trading plan with stop rules fixed in advance

## 5. What you do not get
No live trading. The kit cannot send orders, and an automated test makes sure it never learns to.
See [SAFETY.md](../../SAFETY.md) and [After paper trading](after-paper-trading.md).

A fully worked example lives in `examples/beispiel-emperorbtc-oeffentlich/`.
