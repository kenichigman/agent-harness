# Skill: Liveness Watch

For setting up supervision over a long-running job, service, or scheduled worker.

## Setup

1. The job records its PID in a pid file and touches an output or heartbeat file on a known interval.
2. The watcher checks both signals (see `tools/liveness.py`): process alive, output younger than the agreed maximum age.
3. The watcher itself appends a heartbeat line to its own log on every pass, so a second-level check can verify the watcher is alive.

## Operating rules

- Test the check adversarially at setup: kill the job and confirm the watcher fires; freeze the output and confirm it fires; only then trust it.
- Never let a liveness check match its own process (search patterns that include the checker's command line are the classic self-deception).
- On confirmed death: restart at most a small fixed number of times within a window, then stop and escalate. Log every restart with its reason.
- A restart is not a recovery until the two signals pass again. Verify, then report.
- If the watcher cannot restore the job, escalate within the hour with: what died, the evidence, what was tried, and the one thing needed next.
- Distinguish "finished" from "died": the job writes its terminal state to a state file; the watcher reads it before alarming.
