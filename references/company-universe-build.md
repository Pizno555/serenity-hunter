# Company Universe Build

Use this file for Step 5 of the deep research workflow. It defines how to systematically build the candidate company universe instead of listing popular tickers from memory.

## Core Principle

Systematic discovery, not memory. Execute layer by layer. Do not skip any layer. For broad market scans, aim for at least 20 candidates across all layers.

**Breadth requirement:** Each sub-sector in the final report must have 4-6 companies, not just the top 1-2 names. Include candidates across three maturity stages:

| Stage | Meaning | Scorecard mapping |
|---|---|---|
| **10-100** | Validated leader — proven product, real revenue, verified market share | S/A (≥70) |
| **1-10** | Breaking through — product in certification or early production, inflection visible | B (55-69) |
| **0-1** | Early lead — claims or R&D stage, high elasticity, unproven but worth tracking | C (<55) |

The final ranking table (Step 7) narrows to top 5-8. But the sub-sector analysis table (Step 8) keeps all 4-6 per sector so users can self-select based on stage, evidence, and risk tolerance.

## Step 5.1: Six Discovery Methods

For each layer, attempt all 6 methods:

| # | Method | How to execute | Example (PCB: copper foil layer) |
|---|---|---|---|
| 1 | Keyword search | Search "[layer] 上市公司" and "[layer] listed company" in the target market's language | "铜箔 上市公司", "copper foil listed company" |
| 2 | Industry classification codes | Look up the relevant sector classification (e.g., 申万/中信 for A-shares, GICS for US/global) and extract constituent stocks for the target layer | 申万: 电子-元件-PCB → check copper foil sub-sector |
| 3 | Supply-chain reverse lookup | Identify downstream buyers in this layer, then find their disclosed suppliers from filings, prospectuses, or tender documents | CCL manufacturers (生益, 南亚) → who supplies their copper foil? |
| 4 | Patent / technology search | Search patents in this layer's technical domain and extract patent holders | "电解铜箔 专利 权利人" |
| 5 | Trade show exhibitor lists | Find exhibitor rosters from major industry exhibitions | CPCA Show, TPCA Show, SEMICON exhibitor lists |
| 6 | Industry association membership | Check relevant trade association member directories | CPCA member directory, China Electronic Materials Association |

**Rule for 0 results:** If a method returns zero results, mark it explicitly:
[Method X] returned 0 results. Reason: [tool limitation / no listed companies in this sub-sector / etc.]

## Step 5.2: Hard Gates

Do not proceed to Step 6 unless all gates pass:

| Gate | Condition | Failure remediation |
|---|---|---|
| **Gate 1: Method coverage** | Each layer must have ≥3 methods returning at least 1 verified company | Return to Step 5.1, use alternative search terms or data sources |
| **Gate 2: Scarce-layer quota** | Each Level 1 chokepoint layer (from Step 4) must have 4-6 companies across at least two maturity stages (10-100, 1-10, or 0-1). If Level 1 layers < 4 total, use Level 2 layers to reach 4. If a layer is a verified global duopoly/monopoly (e.g., ASML for EUV), state "Monopoly Exemption" and list the 1-2 players. | Return to Step 5.1, expand search to 0-1/1-10 stage candidates, private companies, or global listings |
| **Gate 3: Non-scarce-layer quota** | Each other layer must have ≥1 company | Return to Step 5.1 |
| **Gate 4: Cross-verification** | Compare the full candidate list against at least one industry classification code system. Any company in the classification but not in the list must be either added or explicitly excluded with a reason. | Add missing companies, or write exclusion reason |

**Retry Limit:** Maximum 2 retries per layer. If a gate still fails, output the layer as `[INCOMPLETE — REQUIRES HUMAN AUDIT]` and move on.

## Step 5.3: Company Classification

Tag each company with one of these labels:

| Label | Meaning |
|---|---|
| **Controls** | Monopoly/oligopoly in this layer — customers cannot bypass |
| **Core supply** | Major supplier with meaningful market share and pricing power |
| **Benefits** | Revenue correlates with the theme, but supply-chain position is loose |
| **Weak control** | Participates but easily replaceable, or weak pricing power |
| **Story** | Claims to have business but lacks specific evidence |

Also tag each company with a **maturity stage**:

| Stage | Criteria |
|---|---|
| **10-100** | Product in volume production, real revenue from this layer, verified market share |
| **1-10** | Product in certification or early production, revenue inflection visible but not yet at scale |
| **0-1** | R&D stage, small batch sampling, or claims without volume revenue — high elasticity, high uncertainty |

## Step 5.4: Pre-Step 6 Self-Check

All must pass before entering Step 6 (Gather and grade evidence):

- [ ] Every layer has ≥1 company.
- [ ] Each Level 1 chokepoint layer has 4-6 companies (or invoked Monopoly Exemption).
- [ ] Each Level 1 layer has candidates from at least 2 maturity stages (not all 10-100).
- [ ] Each layer has ≥3 discovery methods returning results.
- [ ] Cross-verification against at least one classification code system is complete.
- [ ] Every excluded company has an explicit exclusion reason.
