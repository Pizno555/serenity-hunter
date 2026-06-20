# Route Confusion Test Cases

For promotion gating. These cases test the boundary between
"should trigger" and "should not trigger" — the near-neighbor zone
where routing errors are most likely.

## Purpose

Route confusion tests verify that the skill does not over-trigger
(activating on investment-adjacent but non-research prompts) or
under-trigger (failing to activate on research prompts that lack
explicit keywords).

## Near-neighbor: should NOT trigger (investment-adjacent but no research workflow)

| # | Prompt | Why it's near-neighbor | Why it should NOT trigger |
|---|---|---|---|
| RC1 | 今天大盘怎么样？ | Mentions market | No theme, no chain, no research depth needed |
| RC2 | 帮我看一下我的持仓盈亏。 | Investment context | Portfolio review, not supply-chain research |
| RC3 | 这个基金费率太高了，帮我换个低费率的。 | Investment product | Product comparison, not chain analysis |
| RC4 | 帮我算一下定投收益率。 | Investment calculation | Financial calculation, no research workflow |

## Near-neighbor: MAY trigger (acceptable either way, but must behave correctly if triggered)

| # | Prompt | Why it's near-neighbor | If triggered, expected behavior |
|---|---|---|---|
| RC5 | AI 芯片现在还能买吗？ | Single ticker, no chain | Brief research-framed answer, not full scan |
| RC6 | 英伟达财报怎么看？ | Single company, no explicit research request | Evidence-framed analysis, not buy/sell call |
| RC7 | 新能源板块最近跌了，什么情况？ | Sector + price action | If triggered: identify if there's a chain-level explanation. If not: brief macro framing. |
| RC8 | 帮我看看这个公司靠不靠谱。 | Vague single-company request | Ask for clarification on what "靠谱" means, or default to single-company challenge mode |

## Near-neighbor: should trigger but might miss (under-trigger risk)

| # | Prompt | Why it might miss | Why it SHOULD trigger |
|---|---|---|---|
| RC9 | 帮我理一下 HBM 产业链上下游。 | No explicit "深度调研" keyword | "产业链" + theme = theme scan request |
| RC10 | 先进封装现在哪些环节卡脖子？ | "卡脖子" not in keyword list | "卡脖子" = "卡点" = chokepoint, should trigger |
| RC11 | 液冷这个方向值不值得跟踪？ | "值不值得" not exact match for "值得研究" | "值不值得" = research priority question |

## Evaluation criteria

- **RC1-RC4**: must NOT trigger (or if triggered, give a brief non-research answer)
- **RC5-RC8**: may trigger, but must give appropriate brief response, not full workflow
- **RC9-RC11**: should trigger — test whether new keywords ("卡脖子", "上下游", "值不值得") are caught

## Pass condition

- RC1-RC4: 0 false triggers
- RC5-RC8: if triggered, response is brief and appropriate (not full scan)
- RC9-RC11: all trigger correctly

## Status

- [x] Routing test run (2026-06-20): PASS
- [x] RC1-RC4: 4/4 pass (no false triggers)
- [x] RC9-RC11: 3/3 pass (new keywords "卡脖子", "上下游", "值不值得" all matched)
- [x] RC5-RC8: 4 cases, may trigger (acceptable either way)
- [x] RC9-RC11 keyword updates applied to trigger_eval.py
