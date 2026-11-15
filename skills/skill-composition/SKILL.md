# Skill: Skill Composition

For packaging an agent system's judgment into reusable playbooks ("skills") and combining them on a job.

## What a skill is

A skill is a short, bounded playbook: when it applies, the procedure, the rules, and the stop conditions — written so a worker with no shared context can execute it. Skills are the unit of reuse in the harness: a lesson learned once, written down once, applied by every later worker.

## Composition

Skills join multiplicatively, not additively. A job dispatched as a composition inherits **every** factor's discipline and fences:

- *parallel-sharding × smallest-change* — split the job into independent chunks across workers; inside each chunk, make the smallest change that fully solves that piece. Parallelism never licenses bloat inside a worker.
- *dispatch × verify-before-announce* — delegate the work, then grade the returned evidence against the artifact before accepting it.
- *liveness-watch × lease* — supervise the job, and hold the shared resource it runs on for exactly the job's lifetime.

## Rules

- **Grading never composes away.** No composition may delegate the verdict itself; evidence-gathering can shard, judgment cannot.
- **Fences are inherited, not negotiated.** If any factor in a composition forbids an action, the composition forbids it.
- **A composition that proves out graduates.** When the same combination works repeatedly, name it, write it down as its own skill, and dispatch it by name thereafter.
- **Keep skills small.** One skill, one job. A skill that needs a table of contents is two skills.
- **Invoke, don't posture.** A discipline that is claimed but never actually loaded into a worker's brief is decoration. Dispatches name their skills explicitly.
