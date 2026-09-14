# OccuMap: Notebook to Production
### Build-and-learn roadmap, July 2026 onward
### Updated 14 September 2026
 
## Why this exists
 
One project taken to full depth. OccuMap goes from "Streamlit app on GitHub" to a tested, containerised, served, CI/CD'd classification system with a measured evaluation harness, and later a fine-tuned encoder compared against it. Every phase closes a gap named in an actual interview or JD. Every phase teaches the concepts underneath it, in context, before the code is written.
 
The end state is a single repo you can walk through layer by layer, because you know what each layer does, why it is shaped that way, and what you decided along the way. That is the interview fix. Not skeletons compressing studied knowledge, but fluency from having made every decision.
 
## How this document works
 
Detail decays with distance. The current phase is fully detailed. Later phases are specified at the level of outcome, concepts, key decisions and exit criteria. At each phase closeout, the next one gets detailed, informed by what the last one taught. Categories are locked. Steps are earned.
 
## Phase rules
 
How each session and each module is built: CLAUDE.md. These rules govern phases.

1. **No phase skipping.** Exit criteria pass before the next phase opens.
2. **Closeout ritual.** A phase ends with (a) exit criteria demonstrated, (b) README updated, (c) NOTES.md updated with what was learned, (d) this roadmap re-read: struck where the work disproved it, re-detailed where it taught something, and the next phase confirmed as still deserving its place.
3. **Session cadence.** Sessions happen when they happen. A skipped session shifts the plan; it does not break it. No weekday versus weekend rule.
## Execution order
 
Phases keep their numbers. The order they run in changed on 14 September:
 
**1, 3, 4, 5, 6, 2, then 7 and 8 in 2027.**
 
Phases 3, 4 and 5 run first because FastAPI, Docker and CI/CD are the words that fail automated screens. Evaluation (6) and testing (2) follow.
 
## Phase 0: Readiness. Done 31 August.
 
Findings: NOTES.md, 31 Aug.
## Phase 1: Refactor (notebook to package). In progress.
 
**Outcome:** OccuMap becomes an installable Python package with a `src/` layout, runnable from the terminal, importable from anywhere. The notebook is archived, not deleted.
 
**The interview line this kills:** "your code lives in notebooks." Confirmed twice more in September: Airwallex and Mastercard both rejected at automated screen on the engineering half of the profile.
 
### Module plan
 
Extraction order is the table order. Status and verification: NOTES.md.
 
| Module | From the notebook |
|---|---|
| `config.py` | Cells 1 and 2: constants and client. `BATCH_SIZE` from cell 9, `TOP_N_CANDIDATES` from cell 6. |
| `normalise.py` | Cell 4: `preprocess` and its keyword lists. |
| `loaders.py` | Cell 3 titles CSV, cell 5 SSOC load. |
| `retrieval.py` | Cell 6 `get_ssoc_candidates`, split into `retrieve` and `format_candidates`. Design and its why: NOTES.md, 14 Sep. |
| `classify.py` | Cell 7 first half plus `major_group_context` from cell 6: prompt assembly, single API call, response parsing, parallel calls over `n_runs`, fallback result when every call fails. |
| `voting.py` | Cell 7 second half: `Counter`, winner, accept rule. Pure. |
| `pipeline.py` | Cell 4 apply, cell 9 batch loop, cell 10 results CSV write. |
| `reconcile.py` | Cell 13. Merge human review with auto-accepted. |
| `cli.py` | New, no notebook equivalent. `occumap classify "ASST MGR SALES"`. |
 
### Steps
 
Each module runs the build protocol in CLAUDE.md. Progress: NOTES.md.
 
1. Retrieval.
2. Classify and voting.
3. Pipeline and reconcile.
4. CLI.
5. Parity check: run the package over `synthetic_titles.csv`, diff against `synthetic_results.csv`. Same output or find why.
6. Archive the notebook into `notebooks/legacy/`.
7. Closeout ritual.
**Exit criteria:** `pip install -e .` succeeds; the CLI classifies a title end to end; outputs match the notebook baseline; no secrets in code; closeout done.
 
**Estimated remaining effort:** two sessions.
 
## Phase 6: Evaluate. Runs after Phase 5.
 
**Outcome:** the eval harness scoped in April, executed. A 60-title gold set, self-labelled against SSOC definitions with methodology documented, an eval script, and numbers with intervals in the README.
 
**Kills:** the H2O question ("how do you verify retrieval returns usable candidates at k"), the MAS-shaped weakness (evaluation rigour under questioning), and the Chanel round-two questions on measurement. Converts "validation framework: designed" into executed at portfolio scale.
 
**Concepts, each built by hand before the library version:**
 
1. Precision, recall, F1 from a confusion matrix. Macro versus micro and when each misleads.
2. Stratified sampling: choosing the strata (fast-path versus LLM, confidence band, split label) and seeing what it costs.
3. Wilson intervals, computed by hand next to the normal approximation, watching them diverge at n=60.
4. Recall at k: for each gold title, is the true code in the top k. Swept across k in {5, 10, 15, 25}. This answers whether 15 was a guess.
5. TF-IDF: build sklearn's `TfidfVectorizer` as a separate retriever next to the frozen lexical scorer, measure recall at k for both, see which terms IDF downweights.
6. Hybrid retrieval: add a dense retriever (sentence-transformers, FAISS index), fuse with reciprocal rank fusion, measure lexical versus dense versus hybrid. This is what Cortex Search does underneath.
7. Lift measurement: split the gold set, treat one half as control, compute lift and its interval. Synthetic, but the arithmetic is an A/B test.
**Tooling:** MLflow for experiment tracking, since prompt version against recall at k is exactly what it is for and it is named in Shell's and Chanel's JDs.
 
**Key decision:** stratification scheme for the 60 titles. Depends on the fast-path open question in NOTES.md.

**Baseline, decided 14 September:** Phase 6 measures the pipeline with its known bugs unfixed, on purpose. Those numbers are the before; Phase 2 fixes are measured against them. The Phase 1 lexical scorer is frozen as the retrieval baseline. TF-IDF and dense retrievers go in separate modules and are compared against it, not swapped in.
 
**Exit criteria:** gold set labelled and frozen; eval script runs against the pipeline; results table with intervals in the README; recall at k curve; error analysis names the failure patterns; closeout ritual.
 
**Estimated effort:** two sessions.
 
## Phase 2: Test
 
**Outcome:** a pytest suite covering core logic, Claude API mocked, running free, fast and offline.
 
**Kills:** the silent-breakage problem, and "how do you know it works" at the code level.
 
**Concepts:** unit versus integration; arrange-act-assert; fixtures; mocking external services; coverage as signal; how untestable code reveals design flaws from Phase 1; TDD as a gate (write the failing test, prove it fails, then implement).
 
**Fixes that land here:** every entry under Known bugs in NOTES.md, each with a test that captures the bug first. Not listed here so the two cannot drift.
 
**Tooling:** Ruff for lint. A pre-commit hook that runs pytest and ruff and blocks on failure. This is the first control, as opposed to policy, in the repo.
 
**Exit criteria:** `pytest` green; API fully mocked; normalise, voting and retrieval each have meaningful cases; every fix above has its test; hook installed; closeout ritual.
 
**Estimated effort:** one to two sessions.
 
## Phase 3: Serve
 
**Outcome:** OccuMap behind FastAPI. `POST /classify` takes a title, returns code, label, confidence. `GET /health`. Auto docs at `/docs`.
 
**Kills:** "serve as API: never built." Named as required in Shell, Mastercard, the agency posting, and BNY.
 
**Concepts:** what an HTTP API is; REST conventions; pydantic schemas as validated contracts; service layer versus logic layer; sync versus async at a working level; OpenAPI docs for free.
 
**Addition, 4 September:** instrument the service with Langfuse. Trace, cost, latency and confidence per call. This is the entry point to the AgentOps layer named in McKinsey, Mastercard and Temasek JDs, and it converts "I designed confidence-tiered routing to manage cost" into a dashboard.
 
**Key decision:** what the response schema exposes.
 
**Exit criteria:** `uvicorn` serves locally; both endpoints behave; invalid input returns clean 422s; docs render; Langfuse traces visible; closeout ritual.
 
**Estimated effort:** one to two sessions.
 
## Phase 4: Containerise
 
**Outcome:** one `Dockerfile`; `docker build` then `docker run` yields the working API on any machine.
 
**Kills:** Docker, the top-priority named gap across every JD tally.

**Before it opens:** install Docker Desktop.

**Required fix:** `DATA_DIR` from an environment variable, with the current path as fallback (known bug in NOTES.md). Its test lands in Phase 2.
 
**Concepts:** image versus container; layers and caching; Dockerfile anatomy; `.dockerignore`; secrets via environment at runtime; port mapping; slim base images; non-root user.
 
**Exit criteria:** fresh `docker build` succeeds; `DATA_DIR` fix in place; container serves the API from the host; image contains no secrets; closeout ritual.
 
**Estimated effort:** one session.
 
## Phase 5: Automate and deploy
 
**Outcome:** GitHub Actions runs ruff and a one-title smoke test, and builds the image, on every push; the container deploys; a public URL exists. The smoke test stands in until Phase 2's pytest suite replaces it.
 
**Change, 5 September:** deploy target is Azure Container Apps, not Cloud Run. Azure is what Singapore enterprises run and it is named in Shell's and Chanel's JDs. Cloud Run remains a fallback if Azure's free tier proves awkward.
 
**Kills:** the CI/CD gap.
 
**Concepts:** what CI does; workflow, job, step, runner; secrets in CI; container registries; what the platform abstracts and what it does not.
 
**Key decision:** a public endpoint spending the Claude API key needs a plan. Rate limiting, a demo mode with cached responses, or exposing only the rule-based fast path. Decided deliberately and documented.
 
**Exit criteria:** push triggers ruff, the one-title smoke test and the image build; deploy succeeds; public URL responds; `/health` returns the package version; key exposure decision implemented; deployed README has a Known issues section pointing at NOTES.md; closeout ritual.
 
**Estimated effort:** one to two sessions.
 
## Phase 9: Frontend

React with TypeScript, calls the Phase 3 API, replaces the Streamlit review app. Detailed at Phase 5 closeout.

## Optional after Phase 6: LangGraph wrap
 
One session. Wrap the escalation agent in LangGraph. Not because it is better engineering than the raw API version, but because LangChain or LangGraph is named in four of ten JDs reviewed this month and the keyword filter is literal. Only after the raw version exists and works.
 
## Phase 7: Train. 2027.
 
**Outcome:** a small encoder (DeBERTa-v3-small or ModernBERT) fine-tuned on the SSOC task in PyTorch. Training curves watched, overfitting caused and fixed, a checkpoint evaluated against the frozen gold set.
 
**Kills:** "have you trained anything" and PyTorch. This is also what makes vLLM and air-gapped delivery possible, since both need weights you own.
 
**Compute:** MPS first, Colab fallback. The SuperX B200 trial was skipped on 10 September. Not needed at this model size.
 
**Concepts and key decisions unchanged from the original plan.** Detailed at Phase 6 closeout.
 
**Estimated effort:** three to four sessions.
 
## Phase 8: Compare. 2027.
 
**Outcome:** "Fine-tuned encoder versus LLM RAG for occupation classification: accuracy, cost, latency, failure modes." Both systems yours, so the comparison is honest.
 
**Kills:** the judgment question.
 
Unchanged from the original plan. Detailed at Phase 7 closeout.
 
## Timeline
 
| Phase | Window |
|---|---|
| 0 Readiness | Done 31 Aug |
| 1 Refactor | Through 28 Sep |
| 3 Serve | 3 to 4 Oct |
| 4 Containerise | 10 to 11 Oct |
| 5 Automate and deploy | 17 to 18 Oct |
| 6 Evaluate | 24 Oct to 1 Nov |
| 2 Test | 7 to 8 Nov |
| Buffer | Rest of November |
| LangGraph wrap | Optional, December |
| 7 Train | 2027 |
| 8 Compare | 2027 |
 
Mid-November: a deployed, tested, measured public system. Applications sent in September cycle back in October and November; panels in November see the repo finished.
 
## Hardware and housekeeping
 
- M1 Pro 16GB/512GB is sufficient for every phase through 6. Phase 7 fits via MPS at DeBERTa-v3-small scale; Colab is the free fallback.
- `docker system prune` after image experiments. One Python environment per project.
- No hardware purchases on this path.
## What the end product is for
 
**A live demo in interviews.** A public URL and a docs page mean "walk me through something you built" is answered with a running system. Classify a title live, then descend the layers: API, container, tests, eval results, traces.
 
**A working tool for real data.** Anyone holding free-text occupation titles can `docker run` the image or call the endpoint and get SSOC 2024 codes with confidence scores.
 
**Public writing that markets you.** The Phase 6 eval and the Phase 8 comparison, published, are outbound positioning.
 
**Your own boilerplate.** The packaging, tests, Dockerfile, CI workflow and eval harness copy forward into every project after this one, including the NTUC pilots.
 
**Evidence with a timestamp.** A shipped, public, documented system outweighs any claim about capability.
 
## What this document is
 
The plan and the sequence. The curriculum is the effort itself. The standard the effort answers to: nothing gets copy-pasted whose why you have not lived. If code ships but the concept did not land, the step is not done.