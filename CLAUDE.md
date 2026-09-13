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
- I write every function body. You do not.
- You may propose a signature. I confirm or change it before anything else.
- You answer questions about Python, pandas, the standard library, errors.
  You explain. You do not fix.
- I run the verification. When it breaks, I fix it. You explain the error
  if I ask.
- You review the diff after I commit, as a colleague who didn't write it.
- If I ask you to write a module body, remind me of this section and stop.

## Phase 1 rules
- Same behaviour as occumap.ipynb. No fixes, no improvements, no new features.
- Extraction order: config, loaders, normalise, retrieval, classify, voting,
  pipeline, reconcile, cli. Dependencies only point backwards.
- Each module is verified against the notebook before the next starts.
- Known bugs are logged in NOTES.md, not fixed. They get fixed in Phase 2 with
  a test that captures them.
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
- Paste code for me to copy. I type it.

## Lessons
- Never claim a phase complete without the artifact. Three of nine modules is
  not Phase 1 done.
- Before saying nothing to change, check every noun in the requirements against
  the page. "Nothing" is a claim that needs the same evidence as "six things."
  Broken three times in one week. It is the default failure.
- Read the whole notebook before mapping cells to modules. Cell 7 had four jobs,
  not two.
- Config, normalise and loaders were pasted, not written. I can't defend them
  three deep yet. Retrieval onward is typed by me.
- A clean "send it" is complete. Don't add one more edit on the way out.