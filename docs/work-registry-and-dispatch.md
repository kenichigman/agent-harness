# Work registry and dispatch discipline

## The registry

One JSON file lists every unit of work the system knows about. Each entry carries:

- `id` — a small integer, stable for the life of the item.
- `title` — one line, verb-first.
- `lane` — the area the work belongs to (docs, research, maintenance, …). Lanes prevent collisions: two workers in the same lane coordinate; workers in different lanes mostly do not need to.
- `status` — `open`, `claimed`, `blocked`, `done`.
- `owner` — who holds it, once claimed.
- `evidence` — on completion, the artifact that proves the outcome (a file path, a test result, a log line). An item closed without evidence is not closed.
- `note` — the blocker, when blocked: the one specific thing needed, and from whom.

The registry is deliberately boring technology: a file, atomic writes, no database. Its value is that it is the *single* list — if work is not on it, the system is not doing it, and if it is on it, someone can always answer "what is happening with X" by reading one file.

## Dispatch discipline

The coordinator's seat is dispatch and grading, not execution. Three rules keep that division honest:

1. **Briefs are self-contained.** A dispatch names the goal, the inputs (exact paths or values), the fences, the deliverable, and the evidence required. A worker that has to ask "which file did you mean?" was under-briefed.
2. **One worker, one bounded job.** Workers do not originate side work. If a worker finds adjacent work, it reports it; the coordinator registers and dispatches it (or not).
3. **Fold-in is a grading act.** When a result returns, the coordinator verifies it against its evidence before marking the registry. Only then does the succession check run: what did this unblock?

## The stillness rule

A coordinating agent only acts on turns — when it is not running, nothing moves. So the end of every turn runs an origination sweep: scan the registry for items that are open, un-owned, and un-blocked, and dispatch what is dispatchable. A sweep that dispatches nothing while approachable work sits in the registry is a failed sweep, and the receipt (dispatched / blocked-with-reason / nothing-found-with-evidence) is recorded either way. This converts "the coordinator forgot" from a silent failure into a visible one.
