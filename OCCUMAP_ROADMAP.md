# OccuMap: Notebook to Production
### Build-and-learn roadmap, July 2026 onward
### Updated 14 September 2026
 
## Why this exists
 
One project taken to full depth. OccuMap goes from "Streamlit app on GitHub" to a tested, containerised, served, CI/CD'd classification system with a measured evaluation harness, and later a fine-tuned encoder compared against it. Every phase closes a gap named in an actual interview or JD. Every phase teaches the concepts underneath it, in context, before the code is written.
 
The end state is a single repo you can walk through layer by layer because you built every layer yourself. That is the interview fix. Not skeletons compressing studied knowledge, but fluency from execution.
 
## How this document works
 
Detail decays with distance. The current phase is fully detailed. Later phases are specified at the level of outcome, concepts, key decisions and exit criteria. At each phase closeout, the next one gets detailed, informed by what the last one taught. Categories are locked. Steps are earned.
 
## Rules of engagement
 
1. **Concept before code.** Every step gets its what and why before implementation. If code arrives without the concept, stop.
2. **Drill, code, explain.** From retrieval onward, each module runs three steps in order. Drill: Sebastian describes the module. The agent labels each decision as design or preference, questions design decisions until Sebastian has the why right, and records preferences without probing. Decisions Sebastian already defined are accepted unless Sebastian asks to go deeper. Code: the agent writes the body to the confirmed signatures, matched to the notebook. Explain: the agent walks the body as pseudocode mapped to the drill's decisions, then Sebastian restates the purpose and one trade-off without looking. Sebastian runs verification; the agent explains errors and changes code only after Sebastian says what to change. Config, normalise and loaders were pasted and are flagged as such; they get re-read until they can be defended three deep.
3. **No phase skipping.** Exit criteria pass before the next phase opens.
4. **Closeout ritual.** A phase ends with (a) exit criteria demonstrated, (b) README updated, (c) NOTES.md updated with what was learned, (d) this roadmap re-read and struck where the work disproved it.
5. **Session cadence.** Sessions happen when they happen. A skipped session shifts the plan; it does not break it. No weekday versus weekend rule.
6. **Honest framing.** Anything designed but not executed is labelled as such, everywhere, always. The repo's credibility is the whole point.
7. **Two instances.** Claude Code in VS Code builds alongside, governed by CLAUDE.md. A separate chat reviews what gets pushed and holds the plan across sessions.
## Execution order
 
Phases keep their numbers. The order they run in changed on 4 September:
 
**0, 1, 6, 2, 3, 4, 5, then 7 and 8 in 2027.**
 
Phase 6 moved to second because evaluation is the differentiator on every AI engineer JD reviewed this month, and because it is where five named knowledge gaps get built rather than studied. Phases 2 through 5 are the deployment gate and follow it.
 
## Phase 0: Readiness. Done 31 August.
 
Findings worth keeping:
 
- Repo lives at `~/Downloads/Repositories/occumap`. The Dropbox copy under `NTUC Employment 2024/PulseProject` no longer exists. GitHub is the source of truth.
- API key was a placeholder from 24 July to 31 August. Live now. Never entered git history (verified from a fresh clone).
- There was no terminal entry point. The pipeline lived entirely in `occumap.ipynb`. That is the baseline, and the reason Phase 1 is a refactor.
- `*.xlsx` was blanket-ignored, so the SSOC definitions file was never committed and the repo could not run from a fresh clone. Fixed with a negation rule.
- Docker Desktop: not yet installed. Do it before Phase 4 opens.
## Phase 1: Refactor (notebook to package). In progress.
 
**Outcome:** OccuMap becomes an installable Python package with a `src/` layout, runnable from the terminal, importable from anywhere. The notebook is archived, not deleted.
 
**The interview line this kills:** "your code lives in notebooks." Confirmed twice more in September: Airwallex and Mastercard both rejected at automated screen on the engineering half of the profile.
 
### Status, 14 September
 
| Module | State | Notes |
|---|---|---|
| `config.py` | Done, pasted | `client` constructed at import. Fix in Phase 2: `get_client()`. |
| `normalise.py` | Done, pasted | Pure. Carries the `ns man` substring bug (see Known bugs). |
| `loaders.py` | Done, pasted | 297 titles, 1006 five-digit codes. `DATA_DIR` resolves relative to source; breaks in a container. Warnings unsuppressed. No column validation. |
| `retrieval.py` | Done | Drill, code, explain 14 September. Body written by Claude Code. Matches cell 6 on all 297 synthetic titles. Design below. |
| `classify.py` | Empty | Cell 7 first half plus `major_group_context` from cell 6: prompt assembly, single API call, response parsing, parallel calls over `n_runs`, fallback result when every call fails. |
| `voting.py` | Empty | Cell 7 second half: `Counter`, winner, accept rule. Pure. |
| `pipeline.py` | Empty | Cell 4 apply, cell 9 batch loop, cell 10 results CSV write. |
| `reconcile.py` | Empty | Cell 13. Merge human review with auto-accepted. |
| `cli.py` | Empty | New. The one addition Phase 1 allows. `occumap classify "ASST MGR SALES"`. |
 
`pyproject.toml` exists with hatchling, src layout, runtime and dev dependency split. Editable install works. `CLAUDE.md` is in the repo.
 
### Retrieval design (the one real decision in Phase 1)
 
Cell 6's `get_ssoc_candidates` scores every SSOC row, takes the top 15, and returns a formatted prompt string. By the time it returns, the candidate list no longer exists as data. That is why recall at k is unmeasurable today.
 
Split it:
 
- `retrieve(title, ssoc, k) -> list[Candidate]`. Pure. Scores and ranks. Returns structured results including the score.
- `format_candidates(candidates) -> str`. Pure. Builds the prompt block.
- `Candidate` is a frozen dataclass: `ssoc_code`, `title`, `split`, `score` (float).
- `ssoc` is a parameter, not a global. `k` is a parameter with no default, so retrieval.py never imports config; the caller passes `TOP_N_CANDIDATES`.
- Scoring logic unchanged. Same five terms: phrase match (10), example phrase (8), word overlap (2 per word), example word (2 per word), definition word (1 per word). Same `score > 0` filter and `nlargest`. Same `.apply` across all rows. Slow, but Phase 1 is shape, not speed.
### Known bugs, logged not fixed
 
Kept in NOTES.md, the single list. Not repeated here so the two cannot drift.
### Remaining steps
 
1. Retrieval: done 14 September. Verified against cell 6 on six named cases and all 297 synthetic titles.
2. Classify and voting: drill, code, explain, verified.
3. Pipeline and reconcile: drill, code, explain. The double `preprocess()` call is kept as is; it is fixed in Phase 2.
4. CLI.
5. Parity check: run the package over `synthetic_titles.csv`, diff against `synthetic_results.csv`. Same output or find why.
6. Archive the notebook into `notebooks/legacy/`.
7. Closeout ritual.
**Exit criteria:** `pip install -e .` succeeds; the CLI classifies a title end to end; outputs match the notebook baseline; no secrets in code; closeout done.
 
**Estimated remaining effort:** two sessions.
 
## Phase 6: Evaluate. Runs second.
 
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
 
**Key decision:** stratification scheme for the 60 titles. Depends on the open question in NOTES.md: the rule-based fast path does not skip the LLM today.

**Baseline, decided 14 September:** Phase 6 measures the pipeline with its known bugs unfixed, on purpose. Those numbers are the before; Phase 2 fixes are measured against them. The Phase 1 lexical scorer is frozen as the retrieval baseline. TF-IDF and dense retrievers go in separate modules and are compared against it, not swapped in.
 
**Exit criteria:** gold set labelled and frozen; eval script runs against the pipeline; results table with intervals in the README; recall at k curve; error analysis names the failure patterns; closeout ritual.
 
**Estimated effort:** two sessions.
 
## Phase 2: Test
 
**Outcome:** a pytest suite covering core logic, Claude API mocked, running free, fast and offline.
 
**Kills:** the silent-breakage problem, and "how do you know it works" at the code level.
 
**Concepts:** unit versus integration; arrange-act-assert; fixtures; mocking external services; coverage as signal; how untestable code reveals design flaws from Phase 1; TDD as a gate (write the failing test, prove it fails, then implement).
 
**Fixes that land here, each with a test that captures the bug first:** word-boundary keyword matching; `get_client()` instead of client-at-import; `DATA_DIR` from an env var with the current path as fallback; suppressed openpyxl warnings; a column assertion after load; typed exceptions instead of blind `except` (cells 7 and 9); one `preprocess()` call per row instead of two; resolve the unused `title` parameter in the API call.
 
**Tooling:** Ruff for lint. A pre-commit hook that runs pytest and ruff and blocks on failure. This is the first control, as opposed to policy, in the repo.
 
**Exit criteria:** `pytest` green; API fully mocked; normalise, voting and retrieval each have meaningful cases including the four "-ions Manager" titles plus Manila and Vanilla; hook installed; closeout ritual.
 
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
 
**Concepts:** image versus container; layers and caching; Dockerfile anatomy; `.dockerignore`; secrets via environment at runtime; port mapping; slim base images; non-root user.
 
**Exit criteria:** fresh `docker build` succeeds; container serves the API from the host; image contains no secrets; closeout ritual.
 
**Estimated effort:** one session.
 
## Phase 5: Automate and deploy
 
**Outcome:** GitHub Actions runs tests and builds the image on every push; the container deploys; a public URL exists.
 
**Change, 5 September:** deploy target is Azure Container Apps, not Cloud Run. Azure is what Singapore enterprises run and it is named in Shell's and Chanel's JDs. Cloud Run remains a fallback if Azure's free tier proves awkward.
 
**Kills:** the CI/CD gap.
 
**Concepts:** what CI does; workflow, job, step, runner; secrets in CI; container registries; what the platform abstracts and what it does not.
 
**Key decision:** a public endpoint spending the Claude API key needs a plan. Rate limiting, a demo mode with cached responses, or exposing only the rule-based fast path. Decided deliberately and documented.
 
**Exit criteria:** push triggers test-and-build; deploy succeeds; public URL responds; key exposure decision implemented; closeout ritual.
 
**Estimated effort:** one to two sessions.
 
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
| 6 Evaluate | 3 to 11 Oct |
| 2 Test | 17 to 18 Oct |
| 3 Serve | 24 to 25 Oct |
| 4 Containerise | 31 Oct to 1 Nov |
| 5 Automate and deploy | 7 to 8 Nov |
| Buffer | Rest of November |
| LangGraph wrap | Optional, December |
| 7 Train | 2027 |
| 8 Compare | 2027 |
 
Mid-November: a deployed, tested, measured public system. Applications sent in September cycle back in October and November; panels in November see the repo finished.
 
Skipped sessions shift the plan; they do not break it.
 
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
 
Rolling-wave: categories locked, steps earned, later phases detailed only on arrival.
 
Reviewed at every phase closeout. Strike what the work has disproven, re-detail what it has taught, confirm the next phase still deserves its place.