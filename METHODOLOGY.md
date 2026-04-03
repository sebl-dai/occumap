# OccuMap — Methodology

This document describes the classification approach, consistency 
mechanisms, validation framework, and known limitations of the 
OccuMap occupation classifier.

---

## Problem Statement

Occupation title fields in membership and CRM systems are free-text 
and self-reported. The result is tens of thousands of inconsistent, 
unstandardised entries that make workforce segmentation unreliable 
at scale.

Without a reliable classification, any downstream analysis — targeted 
outreach, policy advocacy, benefit design, workforce planning — is 
built on shaky ground.

---

## Classification Schema

OccuMap maps occupation titles to Singapore's Standard Occupational 
Classification 2024 (SSOC 2024), published by the Singapore Department 
of Statistics.

### Output Labels

| Label | SSOC Major Groups | Description |
|---|---|---|
| **PME** | 1, 2 | Professionals, Managers, Executives |
| **T** | 3 | Technicians and Associate Professionals |
| **RNF** | 4–9 | Rank and File (Clerical, Services, Craft, Operators, Labourers) |
| **NA** | X | Not applicable — retired, resigned, unemployed, unclassifiable |

### Edge Case Rules

The following rules are applied deterministically before the LLM is 
consulted:

- Any title containing `manager` → PME (Group 1)
- Any title containing `engineer` → PME (Group 2) by default
- Any title containing `technician` → T (Group 3) by default
- Taxi / Grab / Uber / private hire / bus drivers → RNF (Group 8)
- `retired`, `resigned`, `retrenched`, `unemployed` → NA
- `homemaker`, `housewife`, `NSF` → NA
- Blank, `-`, numeric codes, single-character entries → NA
- Freelance / self-employed titles → classify by the underlying 
  occupation, not the employment status

---

## Pipeline Architecture
```
Raw CRM title
      ↓
Stage 1: Pre-processor (rule-based, no LLM)
      ↓
Stage 2: LLM classifier (Claude API)
      ↓
Stage 3: Confidence thresholding + majority voting
      ↓
AUTO_ACCEPTED or NEEDS_REVIEW
      ↓
Stage 4: Human review queue (Streamlit)
      ↓
final_labels.csv
```

---

## Consistency Mechanisms

LLM inference can be variable. The same prompt does not always 
produce the same output. OccuMap implements six mechanisms to 
address this:

### 1. Temperature = 0
Forces deterministic output. At temperature 0, the model always 
selects the highest probability token, meaning identical inputs 
always produce identical outputs.

### 2. Structured JSON Output
The model is constrained to return a specific JSON schema on every 
call. This prevents format drift — the model cannot return a 
free-text explanation instead of a structured classification.
```json
{
  "classification": "PME",
  "major_group": "2",
  "major_group_title": "Professionals",
  "ssoc_code": "25121",
  "ssoc_occupation_title": "Software Developer",
  "confidence": 0.95,
  "reasoning": "Single concise sentence"
}
```

### 3. Confidence Scoring + Thresholding
Every classification includes a self-reported confidence score 
(0.0–1.0). Records below the threshold (default: 0.75) are 
automatically flagged for human review regardless of the label.

### 4. Majority Voting
Each title is classified N times (default: 3) in parallel. The 
most common result across runs is taken as the winning label. 
If runs disagree, confidence drops and the record is flagged 
for review.

### 5. Prompt Versioning
Every output row is tagged with the prompt version that produced 
it (e.g. `v1.3`). This enables targeted reprocessing — if the 
prompt is improved, only records from older versions need to be 
rerun.

### 6. Dynamic SSOC Candidate Injection
Before each LLM call, OccuMap performs a keyword search against 
the full SSOC 2024 Detailed Definitions table to identify the 
top 15 most relevant occupation codes for the input title. These 
candidates are injected into the prompt, grounding the model in 
real SSOC codes rather than relying on general knowledge.

This mechanism directly prevents SSOC code hallucination — the 
model selects from a pre-validated candidate list rather than 
generating codes from memory.

---

## Validation Framework

Every classified record receives a `validation_status`:

| Status | Meaning |
|---|---|
| **LLM_ONLY** | No rule-based opinion existed. LLM classified independently. |
| **AGREE** | Rule-based system and LLM reached the same label independently. |
| **DISAGREE** | Rule-based system and LLM diverged. Sent to human review. |
| **NEEDS_REVIEW** | LLM confidence below threshold or votes not unanimous. Sent to human review. |

AGREE records represent the highest-confidence classifications — 
two independent systems reached the same conclusion without 
consulting each other.

DISAGREE records are investigated to determine whether the rule 
or the LLM is correct. In practice, LLM reasoning tends to be 
more accurate for ambiguous titles than keyword-based rules.

---

## Human-in-the-Loop

Records with `NEEDS_REVIEW` or `DISAGREE` status are surfaced in 
a Streamlit review queue. A human reviewer sees:

- The original dirty title
- The LLM's classification, SSOC code, and confidence
- The LLM's reasoning in plain English
- The rule-based label where applicable

The reviewer makes one of two decisions:

- **Accept** — confirm the LLM label as correct
- **Override** — assign a different label with a written reason

Human decisions are recorded with reviewer initials and timestamp 
in `reviewed_labels.csv`, which is then merged with the LLM output 
to produce `final_labels.csv` — the definitive classification table.

---

## Output Schema

| Column | Description |
|---|---|
| `original_title` | Raw input title, unchanged |
| `rule_based_label` | Pre-processor verdict (PME/T/RNF/NA/NONE) |
| `llm_label` | LLM classification |
| `llm_major_group` | SSOC major group number |
| `llm_ssoc_code` | 5-digit SSOC 2024 code |
| `llm_ssoc_occupation_title` | Official SSOC occupation title |
| `llm_confidence` | Model confidence (0.0–1.0) |
| `llm_votes` | Number of runs agreeing on winning label |
| `llm_reasoning` | One-sentence explanation |
| `validation_status` | AGREE / DISAGREE / LLM_ONLY / NEEDS_REVIEW |
| `prompt_version` | Prompt version that produced this result |
| `final_label` | Definitive label after human review merge |
| `label_source` | LLM or HUMAN |

---

## Known Limitations

**Confidence calibration** — The confidence score is self-reported 
by the model, not mathematically derived. A score of 0.95 does not 
guarantee 95% accuracy. Confidence should be treated as a relative 
signal, not an absolute measure.

**SSOC code accuracy** — While dynamic candidate injection 
significantly reduces hallucination, the model may occasionally 
select a plausible but incorrect 5-digit code. SSOC codes should 
be validated against the official SingStat table for production use.

**Ambiguous titles** — Single-word or highly generic titles 
(e.g. `OFFICER`, `MANAGER`, `SUPERVISOR`) cannot be reliably 
classified without additional context. These are correctly flagged 
as NEEDS_REVIEW and require human judgment.

**Rule-based pre-processor limitations** — The keyword-based 
pre-processor has known edge cases where substring matching 
produces incorrect fast-path labels (e.g. `OPERATIONS MANAGER` 
being caught by the `not` substring). The LLM handles these 
correctly — the pre-processor label is a reference only and 
does not override the LLM classification.

---

## Data

All occupation titles used in this project are synthetic or 
anonymised. No real member data is used or stored in this 
repository.

SSOC 2024 Detailed Definitions sourced from:
https://www.singstat.gov.sg/standard-classifications/national-classifications/singapore-standard-occupational-classification-ssoc