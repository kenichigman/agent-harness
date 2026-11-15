# Skill: Dispatch Discipline

For a coordinating agent that delegates work to worker agents.

## The seat

The coordinator does three jobs: architecture, orchestration, system maintenance. Everything else is dispatched. Doing a worker's job inline — because it looks small, because it is faster this once — is the failure mode this skill exists to prevent: it consumes the coordinator's context, breaks the grading division (the doer grading their own work), and does not scale.

## A dispatchable brief contains

1. **Goal** — one or two sentences, outcome-shaped.
2. **Inputs** — exact paths, values, or links. No "the file from earlier".
3. **Fences** — what the worker must not touch, send, publish, or decide.
4. **Deliverable** — the artifact the worker returns, and where it goes.
5. **Evidence required** — what proves the outcome (test output, file listing, log excerpt).
6. **Stop conditions** — what makes the worker halt and report instead of improvising.

## Rules

- Register the work before dispatching it; the registry entry is the dispatch's home.
- One worker, one bounded job. Adjacent discoveries are reported, not chased.
- Fold-in is grading: verify the returned evidence against the artifact before closing the registry entry.
- End every fold-in with the succession check: what did this unblock, and is it dispatched?
- When no work is running, sweep the registry for approachable, un-owned, un-blocked items and dispatch them. Record the sweep's receipt either way.
- Report upward like a foreman, not a fire alarm: headway first (what moved), decisions made, then incidents — each with its disposition.
