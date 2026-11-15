# agent-harness

A small, dependency-free toolkit for running a multi-agent system: a coordinating "cloud agent head" dispatches bounded work to worker agents and local execution hosts, tracks it in a work registry, guards shared resources with leases, watches long-running jobs with two-signal liveness checks, and only accepts results that are graded against evidence.

## What it is

One line: the orchestration layer for a fleet of agents — registry, dispatch discipline, leases, watchers, and verification — written so a stranger can run every piece of it on their own machine in an afternoon.

This repository is a **derived toolkit edition** of a system that runs in production for its author. It contains the architecture, the reusable tools, and the operating playbooks (as generalized "skills"). It deliberately does **not** contain the personal layer the production system runs on top of: no memory files, no relationship or people records, no standing personal instructions, no operational logs, no credentials, and no machine- or network-specific configuration. That exclusion is a design boundary, not an omission — see "Boundary" below.

## How it works

The architecture has five parts (full detail in `docs/architecture.md`):

1. **Work registry** — a single JSON file is the source of truth for what work exists, who owns it, and what state it is in. Work that is not in the registry does not get dispatched.
2. **Dispatch discipline** — the coordinator dispatches and grades; it does not do the workers' jobs inline. Every dispatch is a self-contained brief: goal, inputs, fences (what not to touch), and the evidence a finished result must carry.
3. **Leases and wake management** — shared resources (a workstation, a GPU, a single-writer file) are held under time-boxed leases so two agents never collide, and sleeping machines are woken only under a lease and never against their owner's evident intent.
4. **Watchers and liveness** — a job is alive only when two independent signals agree: the process exists *and* its output is fresh. A watcher that can report "healthy" while the job is dead is worse than no watcher.
5. **Grading and verification** — worker reports are claims, not evidence. Results are graded against the artifact they name (the file, the log line, the test output) before they are accepted, and verdicts are derived from checked findings by rule, not by a model's mood.

Skills — short, composable playbooks — are how the coordinator's judgment is packaged for workers. Skills compose multiplicatively: a job can be dispatched as, for example, *parallel-sharding × smallest-change discipline × verify-before-announce*, and it inherits every factor's rules. See `docs/architecture.md` and `skills/`.

## Layout

```
docs/       architecture and the four subsystem write-ups
skills/     generalized playbooks (dispatch, verification, liveness, composition)
tools/      runnable Python tools (standard library only)
examples/   a sample registry and a runnable quickstart script
tests/      unit tests for the tools
```

## Usage

Requirements: Python 3.10 or newer. No third-party packages — everything in `tools/` is standard library only.

Quickstart (works in a scratch directory, touches nothing outside it):

```sh
sh examples/quickstart.sh
```

By hand:

```sh
# a work registry: add, claim, close, list
python3 tools/work_registry.py --file /tmp/registry.json add "write the summary" --lane docs
python3 tools/work_registry.py --file /tmp/registry.json claim 1 --owner worker-a
python3 tools/work_registry.py --file /tmp/registry.json close 1 --evidence "summary.md exists, 42 lines"
python3 tools/work_registry.py --file /tmp/registry.json list

# a lease on a shared resource
python3 tools/lease.py --file /tmp/leases.json acquire workstation --holder worker-a --ttl 600
python3 tools/lease.py --file /tmp/leases.json status
python3 tools/lease.py --file /tmp/leases.json release workstation --holder worker-a

# two-signal liveness for a long-running job
python3 tools/liveness.py --pid-file /tmp/job.pid --output-file /tmp/job.log --max-age 300

# derive a verdict from checked findings
python3 tools/grade.py examples/findings.example.json
```

Run the tests:

```sh
python3 -m unittest discover -s tests
```

Every tool takes its state file as an argument — there are no hardcoded paths, hosts, or accounts anywhere in this repository. Examples default to local, dry-run-shaped usage.

## Boundary

**In scope:** the orchestration architecture, the registry/lease/liveness/grading tools, and the generalized operating playbooks.

**Out of scope (by design):** the personal layer — memory, people and relationship records, personal standing instructions, daily operational logs, real work registries with live operational data, credentials of any kind, and any configuration naming a real machine, network, or account. The production system's content lanes (research, media, coursework, trading experiments) are separate projects and are not part of this toolkit.

## License

MIT — see `LICENSE`. Author: kenichigman <kenichigman@users.noreply.github.com>.
