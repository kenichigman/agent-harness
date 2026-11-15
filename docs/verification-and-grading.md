# Verification and grading

The harness's most expensive lesson, learned repeatedly: **a report is a claim, not evidence.** Workers, watchers, and delivery channels have all, at some point, narrated an action that the disk said never happened — a restart that left no trace, a success whose artifact did not exist. The grading layer exists because of that.

## Verify against the artifact

Every completion claim names the artifact that would exist if the claim were true: the output file, the log record, the process start time, the test result. Before the claim is accepted or relayed:

1. Read the artifact itself, not a summary of it.
2. Check it says what the claim says (content, not just existence — a file can exist and be empty, stale, or from a previous run).
3. Only then record the outcome.

A success is announced only with its evidence object in hand. When verification fails, the correction is made openly and the original claim is preserved in the incident record — a summarized error cannot be re-graded or learned from; the verbatim record can.

## Verdicts are derived, not felt

Analysis is cheap; commitment is the scarce resource. A reviewer can find every planted error in a document and still sign the wrong verdict at the bottom. So wherever a verdict matters, it is **derived by rule from checked findings**, not produced as a model's overall impression:

- Findings are enumerated first, each with a severity.
- A fixed rule maps findings to a verdict (for example: any critical finding → fail; warnings only → pass-with-notes).
- Where a judgment genuinely cannot be reduced to a rule, it is escalated to a human or a senior seat — never mechanically faked.

`tools/grade.py` is the minimal implementation: findings in (JSON), verdict out, rule stated in the code.

## Grade the assembly, not just the model

When a check or an agent fails, the unit that failed is the *assembled context* — the prompt, the tools, the data it was actually given — not the nominal model. A configuration that refuses in a test harness may behave correctly in production assembly, and vice versa. Benchmark verdicts do not transfer across assemblies without a live re-run in the real one.

## Evidence-graded confidence

Every confidence statement the system makes carries its evidence or its label:

- **Proven** — demonstrated by an artifact or a live test.
- **Provisional** — believed, with partial evidence; the missing evidence is named.
- **Conditional** — true if a named condition holds.
- **Unproven** — asserted but not yet tested.

A single point of failure caps the grade of anything built on it, however strong the surrounding evidence is. Grades stay down until the artifacts exist; a confidence statement that outruns its evidence has stopped being a safety document and become marketing.
