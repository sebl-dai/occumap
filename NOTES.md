# OccuMap notes

What happened and what's known. Rules: CLAUDE.md. Plan: OCCUMAP_ROADMAP.md.

## Module status

| Module | State | Verification |
|---|---|---|
| `config.py` | Done, pasted. Drill owed. | MODEL, PROMPT_VERSION, CONFIDENCE_THRESHOLD, MAJORITY_VOTE_RUNS match cell 2. BATCH_SIZE matches cell 9. TOP_N_CANDIDATES matches cell 6 default top_n=15. |
| `normalise.py` | Done, pasted. Drill owed. Parity break open. | Four cases, labels only: whitespace collapse, override before driver rule, short string, None. None title mismatches the notebook. |
| `loaders.py` | Done, pasted. Drill owed. | 297 titles, 1006 five-digit codes. Split RNF 395, PME 390, T 216, NA 5 (the five are X-codes, legitimate). load_ssoc() frame equals notebook ssoc_5digit. |
| `retrieval.py` | Done 14 Sep. Drill, code, explain. | format_candidates(retrieve(t, load_ssoc(), 15)) equals notebook get_ssoc_candidates(t) on six named cases (SOFTWARE ENGINEER, ASST MGR SALES, ART TEACHER, empty, SENIOR ASSISTANT, ZZQX) and all 297 synthetic titles, raw and cleaned. |
| `classify.py` | Not started | |
| `voting.py` | Not started | |
| `pipeline.py` | Not started | |
| `reconcile.py` | Not started | |
| `cli.py` | Not started | |

Packaging: pyproject.toml with hatchling, src layout, runtime and dev deps split. Editable install works.

## Next
- External review of the retrieval commits and this workflow, in a separate Claude chat.
- Then classify.py: drill first.

## Phase 1 parity breaks, fix before pipeline
- normalise: introduced in extraction, not a notebook bug. Cell 4 checks `pd.isna`; normalise.py checks `is None`. NaN and pd.NA return `('nan', None)` instead of `(nan, 'NA')`, so they reach the LLM. None and blank strings return `''` instead of the original input. The synthetic run can't catch it (0 blank titles); needs a targeted check.

## Known bugs, logged not fixed
Fix plan: roadmap Phase 2, unless an entry says otherwise.
- normalise: substring match. 'ns man' catches Operations Manager, Communications Manager, Admissions Manager, Relations Manager. 'nil' catches Manila, Vanilla. Fix with word boundaries and a test on all six titles.
- config: client constructed at import. Importing config needs a valid key. Fix: get_client(). Decided 14 Sep: fix pulled into Phase 3 as part of API design; its test follows in Phase 2.
- loaders: DATA_DIR resolves relative to the source file. Breaks in a container. Fix: env var with current path as fallback. Decided 14 Sep: fix pulled into Phase 4 as required, since the container runs before Phase 2; its test follows in Phase 2.
- loaders: openpyxl warnings not suppressed. Notebook cell 1 did this.
- loaders: no column validation after read_excel. If SingStat shifts header=4, columns misname silently.
- cell 4: preprocess() called twice per row.
- cell 6: NaN title passes the `not title` guard (NaN is truthy), becomes the word "nan", and substring-matches "finance", "maintenance". 0 of 297 synthetic titles are blank, so current results are unaffected. Only reachable through pandas: a blank cell in a CSV read by pipeline. A CLI or API call passes a string, and an empty string is caught by the guard. Source is cell 4: preprocess returns a missing title unchanged as NaN. Fix, decided 14 Sep: preprocess returns "" for a missing title, so retrieve, the prompt and every later retriever get a real empty string. Empty titles skip the LLM entirely, no 3 API calls to get back NA.
- cell 6: scoring runs .apply(score, axis=1) across ~1000 rows per title. Not fixed in the lexical scorer, which stays frozen (roadmap Phase 6). retrieve also copies the full 1006-row frame per title so the score column never lands on the caller's frame; scoring into a separate Series would drop the copy with identical results.
- cell 7: except Exception: return None swallows everything. Ruff BLE001.
- cell 7: single_api_call(title, prompt) never uses title.
- cell 9: except Exception as e: print(...) in the batch loop swallows row failures. Same class as cell 7.

## Open questions
- Fast path never skips the LLM. Cell 9 process_row calls classify_title on every row, including rows preprocess already labelled. The rule label only feeds AGREE/DISAGREE. Cell 0 says the rules fast-path obvious cases before the LLM. Bug or intended validation design? Decided 14 Sep: settled in the Phase 3 drill as an API contract question (what /classify does for a title the rules already labelled). The answer also shapes the Phase 6 fast-path stratum. Decided 14 Sep for empty titles only: they skip the LLM from Phase 2. Other fast-path rows still open.

## Decisions

### 14 Sep: retrieval design
- Candidate(ssoc_code: str, title: str, split: str, score: float), frozen. retrieve(title: str | None, ssoc: pd.DataFrame, k: int) -> list[Candidate]. format_candidates(candidates: list[Candidate]) -> str.
- Scoring unchanged from cell 6: phrase match (10), example phrase (8), word overlap (2 per word), example word (2 per word), definition word (1 per word). Same `score > 0` filter and `nlargest`.
- Design, drilled until the why was right: retrieve and format split. Cell 6 returned a prompt string, so the candidate list no longer existed as data and recall at k was unmeasurable. Now candidates stay data, and other retrievers plug into the same formatter. Lexical kept exactly as cell 6; the semantic comparison is planned in roadmap Phase 6.
- Design, defined by me: frozen dataclass; ssoc as a parameter; k with no default, so retrieval.py never imports config and needs no API key; empty results as [] and "" (matches notebook).
- Design, relabelled after external review: scoring lifted to module-level _score_row(row, title_clean, content_words). A closure inside retrieve cannot be called from a test; Phase 2 needs to score one handcrafted row without running retrieve. Shape change only, results unchanged.
- Preferences, recorded: score as float, stopwords in retrieval.py, title typed str | None.

## Session log

### 31 Aug
- Key live, API reachable, Haiku responds. The key was a placeholder from 24 July to 31 August and never entered git history (checked from a fresh clone).
- Repo lives at ~/Downloads/Repositories/occumap. Dropbox copy under NTUC Employment 2024/PulseProject is gone. GitHub is the source of truth.
- No terminal entry point. Pipeline lives in occumap.ipynb.
- src/ = synthetic data gen only, app/ = Streamlit review UI.
- SSOC xlsx was never committed (*.xlsx gitignored). Restored with a negation rule.
- Notebook has 14 cells. Model is claude-sonnet-4-6, not Haiku. Retrieval returns top 15, not 5. BATCH_SIZE lives in cell 9, not config.

### 14 Sep
- Reconciled CLAUDE.md, roadmap and NOTES. Rules that came out of it are in CLAUDE.md; the Phase 6 baseline decision is in roadmap Phase 6.
- Build protocol changed to drill, code, explain. The drill later split into design and preference, and diff review moved to a separate Claude chat. Current protocol: CLAUDE.md.
- retrieval.py built. Claude wrote and ran the verification at my request, an exception to "I run the verification". External review relabelled the scorer closure as design; lifted to _score_row, results unchanged.
- Found the normalise parity break. Logged above.
- Restructured the three docs so each fact lives in one file.
- Goal reworded: knowing the whys and explaining the work matters, not typing it. Execution order changed and Phase 9 placeholder added. The three breaks that caused were resolved: smoke test in Phase 5 CI, DATA_DIR fix in Phase 4, Known issues and version on the deploy. Details: CLAUDE.md "Who" and the roadmap.
- Phase 5 smoke test changed to retrieval only, no API call and no secret. get_client pulled into Phase 3. Fast-path question moved to the Phase 3 drill.
