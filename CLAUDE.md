# OccuMap: working rules for Claude Code

## Who
Sebastian. Building this to close a deployment gap. The point is that I build it
and understand it. Not that it gets built.

## Session start, every time
1. Read NOTES.md and OCCUMAP_ROADMAP.md.
2. State the current phase, what's done, what's next. Three lines max.
3. Do not write any module code until I have described in my own words what
   the module does and why. If I haven't, ask me. Do not proceed on my say-so.

## How we build, Phase 1
Three steps per module, in order. Do not skip or merge them.

1. Drill. I describe what the module does and why in my own words. You probe three deep on every design decision: why this split, why this type, why a parameter and not a global, what breaks if we choose otherwise. If I can't defend a decision, we stay on it. No code until the drill is done.
2. Code. You write the module body. Confirmed signatures, behaviour matched to the notebook cell, nothing more.
3. Explain. You walk the body as pseudocode, block by block, and map each block to the decision from step 1 it implements. Then I restate the module's purpose and one trade-off without looking. If I can't, back to step 1.

Then: I run the verification. When it breaks, you explain the error and I say what to change before you change it. After commit, you review the diff as a colleague who didn't write it.

Config, normalise and loaders skipped step 1. Before Phase 1 closes, each gets the drill retroactively.

## Phase 1 rules
- Same behaviour as occumap.ipynb. No fixes, no improvements, no new features.
  One exception: cli.py, a terminal entry point the notebook never had.
- Extraction order: config, normalise, loaders, retrieval, classify, voting,
  pipeline, reconcile, cli. Dependencies only point backwards.
- Each module is verified against the notebook before the next starts.
- Known bugs are logged in NOTES.md, not fixed. They get fixed in Phase 2 with
  a test that captures them. NOTES.md is the only bug list; the roadmap
  points to it.
- Phase 6 follows Phase 1. Not Phase 2.

## Standards
- Pure functions separate from I/O separate from network calls.
- No hidden globals. Anything a function needs is a parameter or an import.
- Config in config.py, not inside logic.
- Docstrings on every public function. Type hints on signatures.
- No em dashes in anything you write.

## Session end, every time
1. Update NOTES.md: what was done, what's next, anything learned.
2. Commit with a message naming the phase and module. Push.
3. Do not leave half-written modules uncommitted.

## Do not
- Refactor beyond the current module.
- Add dependencies without asking.
- Explain a concept after writing the code. Concept first, then code.
- Write a module body before the drill is done. Once it is, Claude Code writes
  the body.

## Lessons
- Never claim a phase complete without the artifact. Three of nine modules is not Phase 1 done.
- Before saying nothing to change, check every noun in the requirements against the page. "Nothing" is a claim that needs the same evidence as "six things." Broken three times in one week. It is the default failure.
- Read the whole notebook before mapping cells to modules. Cell 7 had four jobs, not two.
- Config, normalise and loaders were pasted, not written. I can't defend them three deep yet. Retrieval onward follows the three-step protocol. The drill is the part that sticks.
- A clean "send it" is complete. Don't add one more edit on the way out.