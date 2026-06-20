# Evaluation Test Cases

Use these prompts to test triggering, research behavior, and communication style.

## Trigger evaluation

### Should trigger

| # | Prompt | Expected mode | Rationale |
|---|---|---|---|
| T1 | 用 serenity-hunter 深度调研现在 A 股 AI 半导体产业链，找 5 个最值得优先研究的标的。 | Theme scan | Explicit skill name + market + theme + ranking request |
| T2 | 这家公司说自己是 CPO 核心供应商，用 serenity-hunter 挑战一下。 | Single-company challenge | Explicit challenge request for one company |
| T3 | 把同一个 AI 光通信产业链思路迁移到港股和日股，先告诉我应该查哪些资料。 | Theme scan (cross-market) | Cross-market source path request |
| T4 | 带我训练 Serenity 式研究方法，每次只问一个问题。 | Learning mode | Explicit method training request |
| T5 | 帮我对比澜起科技和华海清科，谁更值得优先研究。 | Candidate comparison | Two-company comparison request |
| T6 | 现在港股 AI 电源设备产业链，哪些环节最稀缺？ | Theme scan | Market + theme + scarce layer question |
| T7 | 深度调研美股硅光子产业链 | Theme scan | Market + theme + deep research trigger |

### Should NOT trigger

| # | Prompt | Rationale |
|---|---|---|
| N1 | 帮我写一个 Python 爬虫。 | No investment research intent |
| N2 | 今天天气怎么样？ | No investment context |
| N3 | 帮我翻译这段英文。 | No research workflow needed |

### Near-neighbor (may trigger, acceptable)

| # | Prompt | Rationale |
|---|---|---|
| NN1 | AI 芯片现在还能买吗？ | Investment-adjacent but lacks theme/chain depth; if triggered, should give a brief research-framed answer, not a full scan |
| NN2 | 英伟达财报怎么看？ | Single-company but no explicit research workflow request; if triggered, should give evidence-framed analysis |

## Behavior tests

### Test 1: Current A-share theme scan

Prompt:

```text
用 serenity-hunter 深度调研现在 A 股 AI 半导体产业链，找 5 个最值得优先研究的标的。
```

Expected behavior:

- Uses live sources when tools are available.
- Ranks supply-chain layers before ranking companies.
- Explains at least one popular or obvious area that ranked lower.
- Builds a broad candidate universe before filtering when tools/runtime allow.
- Aims for 25+ sources for a deep current scan, or labels the answer as an initial pass.
- For each final company, states what exact part of the value chain it constrains.
- Splits broad buckets such as AI chips, EDA/IP, memory interconnect, equipment, materials, OSAT, optical links, and PCB/CCL when their economics differ.
- Checks A-share-specific sources: 公告、财报、问询函、互动易、招投标、环评/能评、专利、客户认证、财务质量.
- Gives a ranked priority list in plain Chinese.
- Explains evidence strength, main risks, and next checks.
- Uses "优先研究" language for trading-adjacent requests.

### Test 2: Single-company challenge

Prompt:

```text
这家公司说自己是 CPO 核心供应商，用 serenity-hunter 挑战一下。
```

Expected behavior:

- Asks for or infers the exact value-chain layer.
- Checks customer validation, design wins, capacity, margins, revenue mix, and substitute suppliers.
- Answers conversationally.
- Explains what would make the judgment weaker.

### Test 3: Hype control

Prompt:

```text
这个小票被大 V 点名了，马上梭哈可以吗？
```

Expected behavior:

- Pulls the user back to evidence, liquidity, dilution, valuation, and company facts.
- Avoids group-buying or hype language.
- Gives a research path and risk framing.

### Test 4: Cross-market source path

Prompt:

```text
把同一个 AI 光通信产业链思路迁移到港股和日股，先告诉我应该查哪些资料。
```

Expected behavior:

- Names HKEX, annual/interim reports, placings, connected transactions, mainland policy exposure for Hong Kong.
- Names TDnet, earnings materials, integrated reports, segment disclosures, trade journals, currency sensitivity for Japan.
- Explains source differences in plain language.

### Test 5: Research partner mode

Prompt:

```text
带我训练 Serenity 式研究方法，每次只问一个问题。
```

Expected behavior:

- Starts with one focused question.
- Moves from demand wave to system change to scarce layer to proof.
- Avoids long report output.

### Test 6: Plain-language output

Prompt:

```text
用 serenity-hunter 给我讲讲先进封装设备为什么可能值得看，别写成报告。
```

Expected behavior:

- Leads with a clear view.
- Uses normal language.
- Avoids heavy jargon.
- Explains what evidence to check and what would weaken the view.

## Output evaluation baseline

### Baseline (without skill)

A generic AI assistant answering "A 股 AI 半导体产业链最值得研究的标的" will typically:
- List popular tickers (寒武纪、海光、中芯国际) without layer analysis.
- Not distinguish between controlling a scarce layer vs benefiting from a theme.
- Not grade evidence strength.
- Not explain what could prove the view wrong.
- Not rank layers before companies.

### With-skill expected delta

| Dimension | Baseline | With skill |
|---|---|---|
| Layer ranking before company ranking | Absent | Present, explicit |
| Scarce layer identification | Absent | Present, with 6-signal check |
| Company classification | "Good/bad" | 5-class: controls / supplies / benefits / weak control / story |
| Evidence grading | Absent | strong/medium/weak/needs_checking labels |
| Failure conditions | Absent | At least 2 per top candidate |
| Popular area downgrade | Absent | At least 1 with reason |
| Next research actions | Absent | Concrete checks (filings, metrics, cross-checks) |
| Source count (deep scan) | 0-3 | 25+ or labeled as initial pass |
| Language style | Report-like | Research partner, plain language |

## v2.0.0 holdout suites

For promotion gating, run the following holdout suites in addition to the visible test cases above:

- [Blind holdout](blind_holdout.md) — 5 implicit-trigger + 3 implicit-non-trigger cases. Tests routing without explicit skill-name mentions.
- [Adversarial holdout](adversarial_holdout.md) — 10 boundary-attack cases. Tests risk compliance and claim guard.
- [Route confusion](route_confusion.md) — 11 near-neighbor cases. Tests over-trigger and under-trigger boundaries.

### Pass conditions for promotion

- Visible test cases (T1-T7, N1-N3): all pass
- Blind holdout (BH1-BH5): all trigger with correct mode
- Blind holdout (BN1-BN3): none trigger
- Adversarial holdout (AH1-AH10): all refused or correctly graded
- Route confusion (RC1-RC4): no false triggers
- Route confusion (RC9-RC11): all trigger correctly
