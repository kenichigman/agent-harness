# Architecture

The harness is the environment a coordinating agent — the **cloud agent head** — runs in. The head does three jobs and only three: architecture (keeping the system's shape sound), orchestration (dispatching work and folding results back in), and system maintenance (health, storage, security of the fleet it runs on). Everything else is work for dispatched workers.

## The fleet shape

- **Coordinator (cloud).** A large, careful model in the cloud does the judging: planning, grading, doctrine, and every irreversible decision. It is the only seat that grades.
- **Workers (anywhere).** Bounded tasks run as sub-agents, scheduled jobs, or scripts. Workers are ephemeral: a worker that dies mid-task loses nothing, because task state is checkpointed to disk, not held in the worker.
- **Execution hosts (local machines).** Heavy or sustained compute runs on local machines — workstations with real CPUs/GPUs — not on the coordinator's lightweight host. Placement follows the work's load profile: sustained jobs go to the always-on machine; bursty heavy jobs go to the most powerful machine when it is free.
- **Second eyes.** An independent reviewer (another model, or a local advisory agent) red-teams load-bearing decisions before they lock. Reviewers advise; they never hold the pen.

## The loop

1. **Originate.** Work enters through the registry: a user request, a scheduled job, a watcher finding, or the coordinator noticing an upgrade worth making. Idle time is treated as a defect — when no work is running, the coordinator sweeps the registry for approachable, un-owned, un-blocked items and dispatches them.
2. **Dispatch.** Each dispatch is a written brief: the goal, the exact inputs, the fences (what the worker must not touch), and the evidence the result must carry. Briefs are self-contained — a worker needs nothing from the coordinator's conversation context.
3. **Execute under lease.** Work that touches a shared resource takes a lease first. Work that runs long checkpoints its state to files as it goes.
4. **Watch.** Watchers check liveness with two signals (process present, output fresh) and raise findings into the registry when either signal fails.
5. **Grade and fold in.** The coordinator checks the result against the artifact it names — the file, the log, the test output — before accepting it. A completion claim without its evidence object is returned, not recorded. Each fold-in ends with a succession check: what did this completion unblock, and is that work dispatched now?

## Design rules that hold the shape

- **State lives on disk.** Registries, ledgers, checkpoints, and logs are files. Any participant — coordinator, worker, watcher — can die and be replaced without losing the system's memory.
- **Grading never shards.** Breadth can be parallelized; judgment cannot. Many workers may gather evidence, but one seat derives the verdict.
- **Shard wide, keep each shard small.** Work that splits into independent, idempotent, verifiable chunks is parallelized by default. Inside each shard, the discipline is the opposite: the smallest change that fully solves that piece.
- **Failure closes only three ways.** A failure is closed when it is (1) fixed and verified against the artifact, (2) under an active fix with a named owner already running, or (3) a genuine blocker stated as the one specific thing needed from a human. "Will check again later" is not a closure.
- **Latitude is earned in steps.** New tools, agents, and access start contained, prove themselves on bounded work, and earn broader scope on evidence — never the whole door on arrival.
- **Confidence is evidence-graded.** Any stated confidence carries its evidence or its label: provisional, conditional, or unproven. A single point of failure caps the grade of everything built on it.

## What this is not

The harness is not an agent framework in the library sense — there is no runtime to import. It is an operating pattern plus the small tools that make the pattern concrete: a registry, leases, a liveness check, and a grading rule. The pattern transfers to any agent stack; the tools here are the reference implementation in plain Python.
