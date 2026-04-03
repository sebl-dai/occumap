# OccuMap

Personal recreation of an LLM-based occupation classifier.

Built using Python and the Claude API (Anthropic) to demonstrate 
end-to-end classification logic that maps messy, real-world occupation 
titles to Singapore's Standard Occupational Classification (SSOC 2024) 
— outputting PME / Technician / RNF workforce labels alongside mapped 
SSOC codes, confidence scores, and a human-in-the-loop review workflow.

All occupation titles used in this project are synthetic or anonymised.
No real member data is used or stored.

---

## The Problem

Occupation title fields in membership and CRM systems are free-text 
and self-reported. The result is tens of thousands of inconsistent, 
unstandardised entries that make workforce segmentation unreliable 
at scale.

Some examples of what you actually see in a real CRM:

| Raw Input | Challenge |
|---|---|
| `MANAGER` | PME, or an inflated title? |
| `ENGINEER` | Software engineer (PME) or plant operator (RNF)? |
| `SELF EMPLOYED` | No occupational signal |
| `GRAB DRIVER` | RNF — but needs to be caught cleanly |
| `RETIRED` | Not currently in the workforce |
| `SNR MKTG MGR` | Abbreviated — needs normalisation |
| `-` / blank / `NA` | Unclassifiable noise |

Without a reliable classification, any downstream segmentation 
is built on shaky ground.

---

## The Solution

OccuMap uses Claude (via the Anthropic API) to reason against SSOC 
2024 Detailed Definitions and classify any occupation title — however 
messy — into one of four labels, with a confidence score and 
human-readable reasoning for every decision.

### Classification Schema

| Label | SSOC Major Groups | Description |
|---|---|---|
| **PME** | 1, 2 | Professionals, Managers, Executives |
| **T** | 3 | Technicians & Associate Professionals |
| **RNF** | 4–9 | Clerical, Services, Craft, Operators, Labourers |
| **NA** | X | Retired, self-employed, blank, unclassifiable |

---

## Consistency Mechanisms

LLM inference can be variable. OccuMap implements six mechanisms 
to address this:

| # | Mechanism | What it does |
|---|---|---|
| 1 | **Temperature = 0** | Deterministic output for identical inputs |
| 2 | **Structured JSON output** | Constrains response format, prevents drift |
| 3 | **Confidence scoring + thresholding** | Auto-accepts high confidence, flags low confidence for human review |
| 4 | **Majority voting** | Runs each title N times, takes the most common result |
| 5 | **Prompt versioning** | Every output tagged with prompt version for auditability |
| 6 | **Dynamic SSOC candidate injection** | Injects real SSOC codes into the prompt, preventing hallucination |

See [METHODOLOGY.md](METHODOLOGY.md) for full details.

---

## Stack

| Layer | Tool |
|---|---|
| Classification engine | Python + Claude API (Anthropic) |
| SSOC knowledge base | SSOC 2024 Detailed Definitions (SingStat) |
| Human review UI | Streamlit |
| Analytics dashboard | Tableau |

---

## Project Structure
```
occumap/
├── app/
│   └── review_app.py         # Streamlit human-in-the-loop review UI
├── data/
│   ├── synthetic_titles.csv  # Anonymised test occupation titles (297)
│   └── synthetic_results.csv # Classification results
├── src/
│   └── generate_synthetic.py # Synthetic dataset generator
├── .env.example              # API key template
├── METHODOLOGY.md            # Full methodology documentation
├── requirements.txt
└── README.md
```

---

## Dashboard

Classification results feed a Tableau analytics dashboard  

- **Workforce breakdown** — PME / T / RNF distribution
- **Confidence distribution** — model certainty across all classifications
- **Review queue** — low-confidence cases flagged for human review

---

## Results (synthetic dataset, 297 titles)

| Label | Count | % |
|---|---|---|
| PME | 128 | 43% |
| RNF | 86 | 29% |
| T | 73 | 25% |
| NA | 10 | 3% |

- Average model confidence: **0.893**
- Auto-accepted: **268** (90%)
- Sent to human review: **29** (10%)
- Human reviewed: **19**

---

## Data

All occupation titles are synthetic or anonymised. No real member 
data is used or stored in this repository.

SSOC 2024 published by the Singapore Department of Statistics:
https://www.singstat.gov.sg/standard-classifications/national-classifications/singapore-standard-occupational-classification-ssoc

---

## Status

✅ Classification pipeline — complete  
✅ Human review queue (Streamlit) — complete  
✅ Tableau dashboard — complete  
✅ Notebook — complete