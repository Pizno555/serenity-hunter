# Deep Research Workflow

Use this file when the user asks for current opportunities, ranked candidates, "which is worth researching now", or a full theme scan.

## Goal

Turn a broad investment theme into a ranked set of research priorities backed by current sources.

The final answer should read like a clear research conversation. The internal workflow can be rigorous; the external answer should stay plain and useful.

## Minimum completion standard

For a current theme scan, aim to complete these checks before the final answer:

- cover at least three value-chain layers;
- rank the scarce layers before ranking companies;
- inspect at least 35 sources when tools and runtime allow;
- build a starting candidate universe of at least 20 companies when the market is broad enough;
- build a candidate universe across visible winners, upstream suppliers, equipment, materials, testing, infrastructure, and adjacent beneficiaries;
- identify the strongest scarce layers;
- select the top 3-7 priorities;
- explain what each final candidate constrains or sits closest to;
- support each top candidate with concrete evidence;
- state what could make the judgment wrong;
- name at least one obvious or popular area that ranked lower and explain why;
- give the next checks the user should run.

If tools or time prevent that standard, state the limitation and give a focused partial answer with an exact verification path.

## Workflow

### 1. Scope the request

Infer the missing parts when reasonable:

- market: US, Hong Kong, A-share, Taiwan, Japan, Korea, Europe, global;
- theme: AI infrastructure, semiconductors, CPO, advanced packaging, robotics, power, cooling, materials, equipment, healthcare manufacturing, defense electronics;
- time window: for "now" use 3-12 months as the default research window;
- output: priority research candidates, reasoning, and next checks.

Ask a clarification only when the missing scope would materially change the answer.

### 2. Convert the theme into a system change

Write the practical chain:

`demand wave -> system pressure -> required technical change -> constrained layer`

Examples:

- AI clusters -> bandwidth and power pressure -> optical interconnect and switching upgrades -> lasers, DSP/ASICs, testing, packaging, substrates.
- AI servers -> power density and uptime pressure -> power conversion, transformers, switchgear, liquid cooling -> qualified equipment and components.
- Humanoid robotics -> actuator and sensing density -> precision reducers, motors, encoders, tactile sensing, batteries -> manufacturing yield and supplier qualification.

### 3. Build the value-chain map

#### Core Principle

Completeness first. This step is a physical-system enumeration task. It answers "what exists", not "what matters". Priority: full coverage > correct granularity > precise boundaries.

#### 8-Layer Framework (Checklist)

Fill each layer with industry-specific details:

1. **Downstream demand** — 最终客户和应用场景（谁在买、为什么买）
2. **System integrators** — 系统集成商/OEM（把零部件组装成最终产品的厂商）
3. **Modules / subsystems** — 模块/子系统（功能单元，如光模块、电源模块）
4. **Chips / devices** — 芯片/器件（核心功能芯片，如 GPU、DSP、激光器）
5. **Process and packaging** — 工艺/封装/测试（制造环节，如晶圆代工、先进封装、OSAT）
6. **Equipment and testing** — 设备/测试（生产用的机器，如光刻机、钻孔机、AOI）
7. **Materials and consumables** — 材料/耗材（生产消耗的原材料，如铜箔、玻纤布、树脂、特种气体）
8. **Physical infrastructure** — 物理基础设施（厂房、电力、水、物流等基础配套）

#### Granularity Rule

Layers whose economics differ must be split into independent sub-layers.

- Example 1: "materials and consumables" cannot stay as one bucket. Split it into copper foil, electronic glass fabric, resin, CCL, etc. when their supply-demand dynamics differ.
- Example 2: "equipment" may split into drilling, exposure, plating, lamination, inspection if each has different supplier concentration.

#### 7-Point Self-Check

Run these checks **before** entering Step 4. If any check fails, fix the gap and re-run until all pass.

| # | Check | Method | Failure Signal |
|---|---|---|---|
| 1 | Demand-side trace | Who are the end customers? Are all terminal demand segments listed? | Only one generic "downstream" or missing major end markets (e.g., AI servers, automotive, 5G). |
| 2 | Source-side trace | Does the map reach the deepest raw-material level? Every material should trace back to ore, petrochemical, or base-chemical origin. | "Copper foil" listed but no upstream "electrolytic copper"; "glass fabric" listed but no upstream "fiberglass yarn". |
| 3 | Equipment cross-check | Does every manufacturing / processing layer have a corresponding equipment layer? | "PCB fabrication" exists but no drilling / plating / AOI equipment; "CCL production" exists but no lamination / coating equipment. |
| 4 | Consumables cross-check | Does every manufacturing / processing layer have a corresponding chemicals / consumables layer? | "PCB fabrication" exists but no plating solution / etchant / solder mask ink; "CCL production" exists but no resin formulation / solvent. |
| 5 | Granularity check | Are any buckets too coarse? If two sub-layers have different supplier counts, qualification cycles, or expansion difficulty, they must be split. | "Upstream materials" as a single layer instead of separate copper foil / glass fabric / resin. |
| 6 | Known-item cross-check | Are all industry-recognized critical layers present on the map? | PCB chain missing CCL; semiconductor chain missing packaging; AI infrastructure missing optical modules; robotics chain missing reducers. |
| 7 | Completeness declaration | Output a formal declaration after all checks pass. | No declaration section — only a list of layers. |

#### Completeness Declaration Format

After all checks pass, output:

```
[Value-Chain Completeness Declaration]
Total layers covered: [N]
layer-01: [name] — [one-sentence definition]
layer-02: [name] — [one-sentence definition]
...
Layers not included:
[layer name] — reason: [xxx]
(write "none" if no gaps)
Self-check items passed: 1-7 all passed
```

### Step 4: Search for scarce layers

Read `references/scarcity-assessment.md` for the full scarcity assessment procedure: 9-indicator fact extraction, trigger rules (L-1 to L-10), falsification stress test, and scarcity type annotation.

Complete the layer ranking before building the company universe in Step 5.

### Step 5: Build the company universe

Read `references/company-universe-build.md` for the full company discovery procedure: 6 discovery methods, 4 hard gates, company classification, and pre-evidence self-check.

### 6. Gather current evidence

#### 6a. Gather and prioritize sources

Work through source tiers top-down (Tier 1 → Tier 7). See `references/evidence-ladder.md` for the 7-Tier source search priority.

For deep current scans, aim for 35+ sources before the final ranking. A good mix:

- 10+ annual/interim/quarterly reports, official announcements, earnings transcripts, investor presentations, official customer/order documents
- 10+ exchange filings, regulatory/project approvals, supplier/customer cross-checks
- 5+ patents, standards, technical papers, certification records
- 5+ trade publications, industry association data, company website, sell-side research
- 5+ reputable financial and industry media
- leads from social posts and price action, confirm with stronger sources

#### 6b. Cross-verify key data points

Key data points: revenue growth, gross margin, capacity, orders, certifications, pricing, capex, inventory, receivables.

For each key data point, cross-check across ≥2 independent sources from different Tier levels.

Consistency judgment:
- Consistent (sources agree) → keep original strength label
- Minor variance (sources differ slightly but direction is same) → note the variance
- Conflicting (sources disagree on direction or magnitude) → downgrade one level

Single-source rule: any key data point backed by only one source automatically downgrades to Medium (if from Tier 1-2) or Weak (if from Tier 3-7). See `references/evidence-ladder.md` for full rules.

### 7. Rank candidates

Rank by:

- demand pressure;
- tightness of the scarce layer;
- supplier concentration;
- expansion difficulty;
- evidence strength;
- valuation gap or market misunderstanding;
- near-term events that could change investor perception;
- financing, governance, liquidity, accounting, and geopolitical risk.

Use `scripts/serenity_scorecard.py` when a repeatable numeric score helps.

Keep two rankings distinct:

1. **Layer ranking**: which parts of the system deserve attention first.
2. **Company ranking**: which companies best represent those layers with evidence.

This keeps the answer from becoming a generic list of popular stocks.

For each final company, answer:

- What exactly does it constrain?
- Where does it sit in the chain?
- Why does it rank here?
- What evidence supports that rank?
- What would make the rank weaker?

### 8. Explain the answer

The answer should start with the conclusion:

- the layers worth prioritizing;
- the top names to research first;
- the reason those names rank higher;
- the strongest proof;
- the popular areas that ranked lower;
- the main ways the view can be wrong;
- the next checks.

Prefer normal prose. Add a compact table only for rankings or evidence comparison.

## A-share deep scan pattern

For A-share prompts, verify through:

- 年报、半年报、季报、临时公告；
- 交易所问询函、互动易、上证 e 互动；
- 招投标、中标公告、客户认证；
- 环评/能评、地方项目备案、产能建设记录；
- 专利、标准、行业协会资料；
- 应收、存货、合同负债、现金流、毛利率；
- 关联交易、资产注入、定增、可转债、股权质押。

The final answer should avoid sounding like a broker report. Use direct investment language:

`先看带宽和工艺约束，再看纯算力芯片...`

`先排产业链层级，再排公司。我会优先看这几层...`

`我会优先看这几层...`

`这个公司排前面，是因为它更靠近真实扩产约束...`

`这个热门方向我会先降级，因为...`

`这个判断最容易错在...`

`下一步先查...`
