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
and self-reported. People write whatever they want. The result is tens 
of thousands of inconsistent, unstandardised entries that make 
workforce segmentation unreliable at scale.

Some examples of what you actually see:

| Raw Input | Challenge |
|---|---|
| `manager` | PME, or an inflated title? |
| `engineer` | Software engineer (PME) or plant operator (RNF)? |
| `self employed` | No occupational signal |
| `XXX driver` | RNF, but needs to be caught cleanly |
| `retired` | Not currently in the workforce |
| `-` / blank / `NA` | Unclassifiable noise |

Without a reliable classification, any downstream segmentation — 
targeted outreach, policy advocacy, benefit design — is built on 
shaky ground.

---

## The Solution

OccuMap uses Claude (via the Anthropic API) to reason against SSOC 
2024 Detailed Definitions and classify any occupation title — however 
messy — into one of four labels, with a confidence score and 
human-readable reasoning for every decision.

### Classification Schema

| Label | SSOC Major Groups | Description |
|---|---|---|
| **PME** | 1, 2 | Managers and Professionals |
| **T** | 3 | Technicians & Associate Professionals |
| **RNF** | 4–9 | Clerical, Services, Craft, Operators, Labourers |
| **NA** | X | Retired, self-employed, blank, unclassifiable |

### Edge Case Rules

- Any title containing `manager` → PME
- Any title containing `engineer` → PME (default)
- `XXX driver` → RNF
- `self-employed`, `retired`, blank → NA
- Ambiguous or low-confidence → flagged for human review

---

## Consistency Mechanisms

LLM inference can be variable. The same prompt does not always produce 
the same output. OccuMap implements five mechanisms to address this:

| # | Mechanism | What it does |
|---|---|---|
| 1 | **Temperature = 0** | Forces deterministic output for identical inputs |
| 2 | **Structured JSON output** | Constrains response format, prevents drift |
| 3 | **Confidence scoring + thresholding** | Auto-accepts high confidence results, flags low confidence for human review |
| 4 | **Majority voting** | Runs each title N times, takes the most common result |
| 5 | **Prompt versioning** | Locks the prompt so results are reproducible and auditable across batch runs |

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
├── src/
│   ├── parse_ssoc.py         # Parse SSOC xlsx into structured CSV
│   ├── classify.py           # Claude API classifier with all 5 
│   │                         # consistency mechanisms
│   └── pipeline.py           # Batch processing pipeline
├── app/
│   └── review_app.py         # Streamlit human-in-the-loop review UI
├── data/
│   ├── ssoc_definitions.csv  # Parsed SSOC 2024 knowledge base
│   └── synthetic_titles.csv  # Anonymised test occupation titles
├── dashboard/
│   └── occumap.twbx          # Tableau analytics dashboard
├── .env.example              # API key template (never commit .env)
├── requirements.txt
└── README.md
```

---

## Dashboard

Classification results feed a Tableau analytics dashboard with four views:

- **Workforce breakdown** — PME / T / RNF distribution across the 
  classified dataset
- **Confidence distribution** — model certainty across all 
  classifications
- **Review queue** — low-confidence cases flagged for human review, 
  with reasoning visible
- **Segment explorer** — filter and slice classifications by 
  demographic or input variable

---

## Getting Started

### Prerequisites

- Python 3.10+
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))
- SSOC 2024 Detailed Definitions xlsx 
  ([SingStat](https://www.singstat.gov.sg/standard-classifications/national-classifications/singapore-standard-occupational-classification-ssoc))

### Setup
```bash
git clone https://github.com/sebl-dai/occumap.git
cd occumap
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create your `.env` file:
```bash
cp .env.example .env
# Add your Anthropic API key to .env
```

### Run the classifier
```bash
python src/parse_ssoc.py        # Parse SSOC definitions
python src/classify.py          # Run classification on synthetic titles
streamlit run app/review_app.py # Launch human review UI
```

---

## Data Sources

SSOC 2024 published by the Singapore Department of Statistics:
https://www.singstat.gov.sg/standard-classifications/national-classifications/singapore-standard-occupational-classification-ssoc

---

## Status

🚧 In active development

---

## Author

[sebl-dai](https://github.com/sebl-dai)