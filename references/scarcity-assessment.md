# Scarcity Assessment

Use this file for Step 4 of the deep research workflow. It defines how to identify and rank scarce layers in the value chain.

## Core Principle

Replace subjective adjectives with interval labels. Replace weighted averages with trigger rules. Replace blind confidence with falsification tests.

## Step 4.1: Fact + Interval Extraction

For **every layer** from Step 3, fill in all 9 indicators. **Fact** section is mandatory — interval labels must be derived from facts, not intuition.

Layer: [name]

Supplier count
Fact: Global suppliers [list names], total [N]
Interval: [ Monopoly (1-2) / Oligopoly (3-5) / Dispersed (>5) ]

Qualification period
Fact: Typical process [description], takes [X] months
Interval: [ <6 mo / 6-18 mo / >18 mo ]

Expansion difficulty
Fact: New capacity requires [time] + [capex], bottleneck [description]
Interval: [ <1 yr / 1-2 yrs / >2 yrs ]

Critical know-how
Fact: Core process [description], controlled by [who]
Interval: [ Standardized / Proprietary but replicable / Global ≤3 teams ]

Material purity / precision
Fact: Specification [description], theoretical/engineering limit [description]
Interval: [ Industrial grade / Electronic grade / Near physical limit ]

Specialized equipment dependency
Fact: Key equipment [name], global suppliers [list], total [N]
Interval: [ >5 suppliers / 3-5 suppliers / Only 1-2 suppliers ]

Customer switching cost
Fact: Switching requires [time] + [process]
Interval: [ <3 mo / 3-12 mo / >12 mo ]

Current lead times
Fact: Current lead time [X] mo, historical normal [Y] mo
Interval: [ <3 mo / 3-6 mo / >6 mo ]

Capacity reservations
Fact: [Company A/B/C] have locked capacity until [date], approx [X]% locked
Interval: [ None / Partial / >80% locked ]

### Interval-to-Score Mapping (for internal tracking only — do NOT average)

| Indicator | High (3) | Medium (2) | Low (1) |
|---|---|---|---|
| Supplier count | Monopoly (1-2) | Oligopoly (3-5) | Dispersed (>5) |
| Qualification | >18 mo | 6-18 mo | <6 mo |
| Expansion | >2 yrs | 1-2 yrs | <1 yr |
| Know-how | Global ≤3 teams | Proprietary | Standardized |
| Purity/Precision | Near physical limit | Electronic grade | Industrial grade |
| Equipment | Only 1-2 suppliers | 3-5 suppliers | >5 suppliers |
| Switching cost | >12 mo | 3-12 mo | <3 mo |
| Lead times | >6 mo | 3-6 mo | <3 mo |
| Capacity lock | >80% locked | Partial | None |

## Step 4.2: Scarcity Level Assignment — Trigger Rules

**Do NOT compute weighted averages or sums.** Use the following trigger rules exclusively.

Note: Scarcity Level 1/2 here refers to chokepoint severity, not evidence strength. See `references/evidence-ladder.md` for evidence Tier definitions.

### Level 1 (Primary Chokepoint) — triggered by ANY of:

| Rule | Condition |
|---|---|
| L-1 | Supplier count = Monopoly (1-2) |
| L-2 | Supplier count = Oligopoly (3-5) AND Qualification = >18 mo |
| L-3 | Purity/Precision = Near physical limit AND Know-how = Global ≤3 teams |
| L-4 | Equipment = Only 1-2 suppliers AND Expansion = >2 yrs |
| L-5 | ≥4 out of 9 indicators = High (any combination) |
| L-6 | Expansion = >2 yrs AND Capacity lock = >80% locked |

### Level 2 (Secondary Chokepoint) — triggered by ANY of:

| Rule | Condition |
|---|---|
| L-7 | Supplier count = Oligopoly (3-5) AND Expansion = >2 yrs |
| L-8 | Qualification = >18 mo AND Switching cost = >12 mo |
| L-9 | 2-3 out of 9 indicators = High (any combination) |
| L-10 | Equipment = Only 1-2 suppliers (but Expansion < 2 yrs) |

### Low Scarcity

Triggers NONE of the above. Mark as `[NON-CHOKEPOINT]`. Keep ≥1 company per layer in Step 5 for reference only. Do not deep-dive.

## Step 4.3: Cognitive Crowdedness Check (optional)

For Level 1 and Level 2 layers, check market consensus when tools and time allow. Skip if time-constrained — this is a bonus check, not a gate.

| Scarcity Level | Market Heat | Label | Action |
|---|---|---|---|
| Level 1 / Level 2 | Low | `[ALPHA]` | Highest priority |
| Level 1 / Level 2 | High | `[PRICED IN]` | Watch for valuation overrun |
| Low | High | `[BUBBLE]` | Mark as pseudo-chokepoint |
| Low | Low | Ignore | Do not include |

## Step 4.4: Falsification Stress Test (Red Team)

For **every Level 1 layer**, force-answer:

> "Under what specific conditions would this layer STOP being scarce?"

Provide **≥2 objectively observable falsification triggers**:

Layer: [name]
Falsification 1: [specific event] → If [X] happens, scarcity decreases.
Falsification 2: [specific event] → If [Y] reaches [threshold], scarcity disappears.

If unable to provide ≥2 realistic triggers → downgrade to Level 2.

**Example (HVLP copper foil, Mitsui monopoly):**

- Falsification 1: Mitsui announces HVLP capacity expansion ≥50% with 2-year deployment.
- Falsification 2: Tongguan Copper or Deyu Technology passes CCL manufacturer certification for HVLP Gen5 with volume shipment.
- Falsification 3: PCB industry shifts to glass-core substrate, bypassing copper foil roughness constraints.

## Step 4.5: Scarcity Type Annotation

Append a type label to each Level 1 / Level 2 layer:

| Type | Description |
|---|---|
| **Physical** | Locked by physics — long-term hold. Triggered by L-3, L-4, or ≥2 Physical indicators = High. |
| **Commercial** | Locked by certification/scale — durable but not physical. Triggered by L-2, L-8, or ≥2 Commercial indicators = High. |
| **Cyclical** | Supply-demand mismatch — cycle-sensitive. Triggered by L-6 or ≥2 Supply/Demand indicators = High. |
| **Transmissive** | Scarcity inherited from upstream. Layer itself is Medium but downstream-critical. |

Indicator categories: Physical/Engineering = Know-how, Purity, Equipment. Commercial/Time = Qualification, Expansion, Switching cost. Supply/Demand = Supplier count, Lead times, Capacity lock.

## Step 4.6: Final Output Structure

```
[Step 4 Output: Chokepoint Layer List]

=== Value Chain Chokepoint Summary ===

I. Level 1 Chokepoints (Primary Bottlenecks)

[Layer name]
Trigger: [L-X]
Key facts: [suppliers / data excerpt]
Scarcity type: [Physical / Commercial / Cyclical / Transmissive]
Crowdedness: [ALPHA / PRICED IN / BUBBLE — optional]
Falsification: (1) ... (2) ...

II. Level 2 Chokepoints (Secondary Bottlenecks)

III. Pseudo-Chokepoints / Bubble Risks (High heat, low scarcity)

IV. Appendix — Full 9-Indicator Fact Sheets (per layer)
```

Plain-language example:

```text
I would rank the layers first: equipment platforms, process-specific equipment, compute chips, advanced packaging materials, then broad component suppliers.
Equipment platforms and process-specific tools sit closer to fab expansion and technology migration. Broad component suppliers usually need stronger order and margin evidence to rank higher.
```

Chinese:

```text
先排稀缺层级：HVLP铜箔（全球仅3家，认证>18月）> 高端CCL > 普通PCB板材。铜箔和CCL更接近真实扩产瓶颈。
```
