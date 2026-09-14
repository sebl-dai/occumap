# OccuMap: working rules for Claude Code

## Who
Sebastian. Building this to close a deployment gap. The point is that I know
what's what, know the whys, and can explain what I did. Not that it gets built,
and not that I typed it.

## Where things live
- CLAUDE.md: how you behave. Protocol, standards, lessons.
- NOTES.md: what happened and what's known. Module status, session log, bugs,
  parity breaks, open questions, dated decisions.
- OCCUMAP_ROADMAP.md: what's planned and why. Phase order, module plan,
  concepts, exit criteria, timeline.
- Each fact lives in exactly one of these. Anywhere else gets a one-line pointer.

## Session start, every time
1. Read NOTES.md and OCCUMAP_ROADMAP.md.
2. State the current phase, what's done, what's next. Three lines max.
3. Do not write any module code until I have described in my own words what
   the module does and why. If I haven't, ask me. Do not proceed on my say-so.

## How we build, Phase 1
Three steps per module, in order. Do not skip or merge them.

1. Drill. I describe what the module does and why in my own words. You list the decisions in the module and label each one. I can relabel any of them.
   - Design: choosing otherwise breaks something later (measurement, testing, imports, parity with the notebook). You ask me why: why this split, why this type, why a parameter and not a global, what breaks if we choose otherwise. If my answer is wrong or incomplete, keep questioning until I get it right.
   - Preference: either choice works. You state the trade-off in one line and record my pick. No probing.
   - If I already defined a decision and its why, accept it. If I want to go deeper, I ask.
   No code until every design decision has its why.
2. Code. You write the module body. Confirmed signatures, behaviour matched to the notebook cell, nothing more.
3. Explain. You walk the body as pseudocode, block by block, and map each block to the decision from step 1 it implements. Then I restate the module's purpose and one trade-off without looking. If I can't, back to step 1.

Then: I run the verification. When it breaks, you explain the error and I say what to change before you change it. After commit, the diff is reviewed in a separate Claude chat, outside Claude Code. That chat also holds the plan across sessions.

Config, normalise and loaders skipped step 1. Before Phase 1 closes, each gets the drill retroactively.

## Phase 1 rules
- Same behaviour as occumap.ipynb. No fixes, no improvements, no new features.
  One exception: cli.py, a terminal entry point the notebook never had.
- Build modules in the roadmap's extraction order. Dependencies only point
  backwards.
- Each module is verified against the notebook before the next starts.
- Known bugs are logged in NOTES.md, not fixed. NOTES.md is the only bug list.

## Standards
- Pure functions separate from I/O separate from network calls.
- No hidden globals. Anything a function needs is a parameter or an import.
- Config in config.py, not inside logic.
- Docstrings on every public function. Type hints on signatures.
- No em dashes in anything you write.
- Anything designed but not executed is labelled as such, everywhere, always.
  The repo's credibility is the whole point.
- Notebook cells are numbered from 0. Cell 0 is the title markdown.

## Session end, every time
1. Update NOTES.md: what was done, what's next.
2. A lesson that changes how we work goes under Lessons below, not in NOTES.md.
3. Commit with a message naming the phase and module. Push.
4. Do not leave half-written modules uncommitted.

## Do not
- Refactor beyond the current module.
- Add dependencies without asking.
- Introduce a concept for the first time after writing the code. Concepts land
  in the drill; step 3 only maps the code back to them.
- Write a module body before the drill is done. Once it is, Claude Code writes
  the body.

## Lessons
- Never claim a phase complete without the artifact. Three of nine modules is not Phase 1 done.
- Before saying nothing to change, check every noun in the requirements against the page. "Nothing" is a claim that needs the same evidence as "six things." Broken three times in one week. It is the default failure.
- Read the whole notebook before mapping cells to modules. Cell 7 had four jobs, not two.
- Config, normalise and loaders were pasted, not written, and I couldn't defend them three deep. The drill is the part that sticks.
- "I don't think testing it is necessary" is a claim about design, not a preference. If a choice decides what can be tested later, it is design.
- A clean "send it" is complete. Don't add one more edit on the way out.
