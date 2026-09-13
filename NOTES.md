# OccuMap notes

## 31 Aug
- Key live, API reachable, Haiku responds.
- No terminal entry point. Pipeline lives in occumap.ipynb.
- src/ = synthetic data gen only, app/ = Streamlit review UI.
- Dropbox copy under NTUC Employment 2024/PulseProject is gone. GitHub is the source of truth.
- SSOC xlsx was never committed (*.xlsx gitignored). Restored with a negation rule.
- Notebook has 14 cells. Model is claude-sonnet-4-6, not Haiku. Retrieval returns top 15, not 5. BATCH_SIZE lives in cell 9, not config.

## 14 Sep
- Reconciled CLAUDE.md, roadmap and NOTES. Decisions:
  - Double preprocess() is logged, fixed in Phase 2. Not fixed in pipeline.
  - NOTES.md is the only bug list. Roadmap points here.
  - cli.py is the one new feature Phase 1 allows.
  - Phase 6 measures the unfixed pipeline on purpose, as the baseline.
  - Lexical scorer is frozen after Phase 1. TF-IDF and dense retrievers are separate modules in Phase 6.
- Cell numbers in all docs are 0-indexed (cell 0 is the title markdown).
- Extraction order corrected to what happened: config, normalise, loaders.

## Phase 1, done so far
- config.py, normalise.py, loaders.py extracted. Pasted, not typed. Re-read until defensible.
- pyproject.toml: hatchling, src layout, runtime and dev deps split. Editable install works.
- config checked: MODEL, PROMPT_VERSION, CONFIDENCE_THRESHOLD, MAJORITY_VOTE_RUNS match cell 2. BATCH_SIZE matches cell 9. TOP_N_CANDIDATES matches cell 6 default top_n=15.
- loaders verified: 297 titles, 1006 five-digit codes. Split distribution RNF 395, PME 390, T 216, NA 5 (the five are X-codes, legitimate).
- normalise verified on four cases: whitespace collapse, override before driver rule, short string, None.

## Known bugs, logged not fixed
All fixed in Phase 2 with a test that captures them, unless stated otherwise.
- normalise: substring match. 'ns man' catches Operations Manager, Communications Manager, Admissions Manager, Relations Manager. 'nil' catches Manila, Vanilla. Fix with word boundaries and a test on all six titles.
- config: client constructed at import. Importing config needs a valid key. Fix: get_client().
- loaders: DATA_DIR resolves relative to the source file. Breaks in a container. Fix: env var with current path as fallback.
- loaders: openpyxl warnings not suppressed. Notebook cell 1 did this.
- loaders: no column validation after read_excel. If SingStat shifts header=4, columns misname silently.
- cell 4: preprocess() called twice per row.
- cell 6: scoring runs .apply(score, axis=1) across ~1000 rows per title. Not fixed in the lexical scorer, which stays frozen as the Phase 6 baseline. The Phase 6 TF-IDF retriever is the replacement.
- cell 7: except Exception: return None swallows everything. Ruff BLE001.
- cell 7: single_api_call(title, prompt) never uses title.
- cell 9: except Exception as e: print(...) in the batch loop swallows row failures. Same class as cell 7.

## Open questions
- Fast path never skips the LLM. Cell 9 process_row calls classify_title on every row, including rows preprocess already labelled. The rule label only feeds AGREE/DISAGREE. Cell 0 says the rules fast-path obvious cases before the LLM. Bug or intended validation design? Decide before Phase 6, since it shapes the fast-path stratum.

## Next
- retrieval.py. Typed by me. Candidate dataclass, retrieve() returns list, format_candidates() separate. Scoring unchanged from cell 6: five terms, not three.
- Verification must include the three cases where cell 6 returns "": empty title, only stopwords, no row scoring above 0. format_candidates([]) has to return "" too, not the header line.
