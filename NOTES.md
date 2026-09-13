# OccuMap notes

## 31 Aug
- Key live, API reachable, Haiku responds.
- No terminal entry point. Pipeline lives in occumap.ipynb.
- src/ = synthetic data gen only, app/ = Streamlit review UI.
- Dropbox copy under NTUC Employment 2024/PulseProject is gone. GitHub is the source of truth.
- SSOC xlsx was never committed (*.xlsx gitignored). Restored with a negation rule.
- Notebook has 14 cells. Model is claude-sonnet-4-6, not Haiku. Retrieval returns top 15, not 5. BATCH_SIZE lives in cell 9, not config.

## Phase 1, done so far
- config.py, normalise.py, loaders.py extracted. Pasted, not typed. Re-read until defensible.
- pyproject.toml: hatchling, src layout, runtime and dev deps split. Editable install works.
- loaders verified: 297 titles, 1006 five-digit codes. Split distribution RNF 395, PME 390, T 216, NA 5 (the five are X-codes, legitimate).
- normalise verified on four cases: whitespace collapse, override before driver rule, short string, None.

## Known bugs, logged not fixed
- normalise: substring match. 'ns man' catches Operations Manager, Communications Manager, Admissions Manager, Relations Manager. 'nil' catches Manila, Vanilla. Fix in Phase 2 with word boundaries and a test on those titles.
- config: client constructed at import. Importing config needs a valid key. Fix: get_client().
- loaders: DATA_DIR resolves relative to the source file. Breaks in a container. Fix: env var with current path as fallback.
- loaders: openpyxl warnings not suppressed. Notebook cell 1 did this.
- loaders: no column validation after read_excel. If SingStat shifts header=4, columns misname silently.
- cell 7: except Exception: return None swallows everything. Ruff BLE001.
- cell 7: single_api_call(title, prompt) never uses title.
- cell 4: preprocess() called twice per row.

## Next
- retrieval.py. Typed by me. Candidate dataclass, retrieve() returns list, format_candidates() separate. Scoring unchanged from cell 6.