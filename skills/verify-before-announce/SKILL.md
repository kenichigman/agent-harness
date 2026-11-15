# Skill: Verify Before Announce

For any agent about to state that something is done, installed, running, fixed, or measured.

## The rule

Reconcile the claim against the raw record that would exist if the claim were true — before speaking. Summaries (yours, a worker's, a watcher's, a tool's) have all been wrong at some point; the artifact is the ground truth.

## Procedure

1. Name the claim precisely: what, where, since when.
2. Name the evidence object: the file, the process, the log line, the endpoint response.
3. Read the evidence object directly. Check content, not just existence; check freshness, not just presence.
4. If the evidence matches, announce — and cite the evidence in the announcement.
5. If it does not match, correct the record first, openly, then report the true state. Preserve the original wrong claim verbatim in the incident record; a paraphrased error cannot be re-graded later.

## Common traps

- Announcing a restart from the restart command's exit code instead of the new process's start time.
- Announcing a fix from a code change instead of a re-run of the failing case.
- Announcing a measurement from a summary line instead of the instrument's output.
- Treating "queued", "running", or "started" as "finished". Work is done only when a result says it finished.
