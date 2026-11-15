# Watchers and liveness

Long-running work fails silently by default: a process hangs, a host sleeps, a network drops, and every dashboard still shows the last good state. Watchers exist to make silence itself a signal.

## Two-signal liveness

A job is alive only when **two independent signals** agree:

1. **The process exists** — the recorded PID is alive and is the process that was started (not a recycled PID or a name-alike).
2. **The output is fresh** — the job's output or heartbeat file has been modified within its expected interval.

Either signal alone lies. A live process can be wedged and producing nothing. A fresh-looking file can be residue from a previous run. `tools/liveness.py` implements exactly this check and exits non-zero with the failing signal named.

## Rules for watchers

- **A check that can pass while the thing is dead is decoration.** Test every liveness check adversarially: kill the job, stale the output, and confirm the check fails. The classic failure is a process search that matches the checker's own command line and reports the job alive forever.
- **Watch the watchers.** Every supervisor emits its own heartbeat, and a periodic health check verifies the heartbeats are fresh. A dead watcher looks exactly like a healthy operation — that is the failure mode the second layer exists for.
- **Distinguish death from completion.** A job that finished naturally and a job that died mid-run can look identical to a naive check (process gone, output stopped). State files record the intended terminal state so the watcher can tell "done" from "gone".
- **Recovery is bounded.** On confirmed death, a watcher may restart the job — with a crash-loop guard: after a small number of restarts in a window, it stops restarting and escalates. Restarting a broken job forever is a second outage wearing a fix's clothes.
- **Correlate before reporting.** One cause (a full disk, a dead network link) often produces many victims. The watcher layer reports the cause, not a pile of unrelated job failures.
- **Escalation has a clock.** A self-heal that cannot heal — a restart that does not restore the listener, a wake that does not raise the host — escalates to the coordinator the same hour, not at the next scheduled review. Silence from a supervisor is itself a failure.
