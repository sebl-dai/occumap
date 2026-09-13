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
- Build protocol changed in CLAUDE.md: drill, code, explain, per module, in order. Claude writes bodies after the drill passes. Config, normalise and loaders get the drill retroactively before Phase 1 closes.
- Drill refined: design decisions (choosing otherwise breaks something) get questioned until the why is right. Preferences get recorded, not probed. Decisions I already defined are accepted; I ask if I want deeper.
- Diff review happens in a separate Claude chat, outside Claude Code.
- Retrieval design locked. Candidate(ssoc_code: str, title: str, split: str, score: float), frozen. retrieve(title: str | None, ssoc: pd.DataFrame, k: int) -> list[Candidate]. format_candidates(candidates: list[Candidate]) -> str.
  - Design, drilled until the why was right: retrieve and format split, so candidates stay data (recall at k measurable, other retrievers plug into the same formatter). Lexical now, semantic in Phase 6 against this baseline.
  - Design, defined by me: frozen dataclass; ssoc as a parameter; k with no default, so retrieval.py never imports config and needs no API key; empty results as [] and "" (matches notebook).
  - Design, relabelled after external review: scoring lifted to module-level _score_row(row, title_clean, content_words). A closure inside retrieve cannot be called from a test; Phase 2 needs to score one handcrafted row without running retrieve. Shape change only, results unchanged.
  - Preferences, recorded: score as float, stopwords in retrieval.py, title typed str | None.
- Learned: "I don't think testing it is necessary" is a claim about design, not a preference. If a choice decides what can be tested later, it is design.
- Lexical vs semantic: build lexical exactly as cell 6. Semantic is Phase 6, measured against this baseline. New dependencies (sklearn, sentence-transformers, torch, FAISS, MLflow) get asked about when Phase 6 needs them.

## Phase 1, done so far
- config.py, normalise.py, loaders.py extracted. Pasted, skipped the drill. Each gets the drill retroactively before Phase 1 closes.
- pyproject.toml: hatchling, src layout, runtime and dev deps split. Editable install works.
- config checked: MODEL, PROMPT_VERSION, CONFIDENCE_THRESHOLD, MAJORITY_VOTE_RUNS match cell 2. BATCH_SIZE matches cell 9. TOP_N_CANDIDATES matches cell 6 default top_n=15.
- loaders verified: 297 titles, 1006 five-digit codes. Split distribution RNF 395, PME 390, T 216, NA 5 (the five are X-codes, legitimate).
- normalise verified on four cases: whitespace collapse, override before driver rule, short string, None.
- retrieval.py: drill, code, explain done 14 Sep. Verified: format_candidates(retrieve(t, load_ssoc(), 15)) == notebook get_ssoc_candidates(t) on six named cases (SOFTWARE ENGINEER, ASST MGR SALES, ART TEACHER, empty, SENIOR ASSISTANT, ZZQX) and on all 297 synthetic titles, raw and cleaned. load_ssoc() frame equals notebook ssoc_5digit. Claude wrote and ran the check at my request, an exception to "I run the verification".

## Known bugs, logged not fixed
All fixed in Phase 2 with a test that captures them, unless stated otherwise.
- normalise: substring match. 'ns man' catches Operations Manager, Communications Manager, Admissions Manager, Relations Manager. 'nil' catches Manila, Vanilla. Fix with word boundaries and a test on all six titles.
- config: client constructed at import. Importing config needs a valid key. Fix: get_client().
- loaders: DATA_DIR resolves relative to the source file. Breaks in a container. Fix: env var with current path as fallback.
- loaders: openpyxl warnings not suppressed. Notebook cell 1 did this.
- loaders: no column validation after read_excel. If SingStat shifts header=4, columns misname silently.
- cell 4: preprocess() called twice per row.
- cell 6: NaN title passes the `not title` guard (NaN is truthy), becomes the word "nan", and substring-matches "finance", "maintenance". 0 of 297 synthetic titles are blank, so current results are unaffected. Only reachable through pandas: a blank cell in a CSV read by pipeline. A CLI or API call passes a string, and an empty string is caught by the guard. Source is cell 4: preprocess returns a missing title unchanged as NaN. Phase 2 fix, decided 14 Sep: preprocess returns "" for a missing title, so retrieve, the prompt and every later retriever get a real empty string. Empty titles skip the LLM entirely, no 3 API calls to get back NA.
- cell 6: scoring runs .apply(score, axis=1) across ~1000 rows per title. Not fixed in the lexical scorer, which stays frozen as the Phase 6 baseline. The Phase 6 TF-IDF retriever is the replacement. retrieve also copies the full 1006-row frame per title so the score column never lands on the caller's frame; scoring into a separate Series would drop the copy with identical results.
- cell 7: except Exception: return None swallows everything. Ruff BLE001.
- cell 7: single_api_call(title, prompt) never uses title.
- cell 9: except Exception as e: print(...) in the batch loop swallows row failures. Same class as cell 7.

## Open questions
- Fast path never skips the LLM. Cell 9 process_row calls classify_title on every row, including rows preprocess already labelled. The rule label only feeds AGREE/DISAGREE. Cell 0 says the rules fast-path obvious cases before the LLM. Bug or intended validation design? Decide before Phase 6, since it shapes the fast-path stratum. Decided 14 Sep for empty titles only: they skip the LLM from Phase 2. Other fast-path rows still open.

## Next
- External review of the retrieval commits and this workflow, in a separate Claude chat.
- Then classify.py: drill first.
