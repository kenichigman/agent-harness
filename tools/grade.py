#!/usr/bin/env python3
"""grade.py — derive a verdict from checked findings, by rule.

Analysis is cheap; commitment is the scarce resource. A reviewer can
find every error in a document and still sign the wrong verdict, so the
verdict here is not an impression — it is a fixed function of the
findings:

    any critical finding        -> FAIL
    else any major finding      -> PASS-WITH-NOTES is not allowed;
                                   the verdict is FAIL-WITH-FIXES
    else any minor finding      -> PASS-WITH-NOTES
    else                        -> PASS

Input: a JSON file {"findings": [{"severity": "critical|major|minor",
"summary": "..."}, ...]} — or a bare JSON list of findings.
Output: the verdict line, then the findings grouped by severity.

Usage:
    grade.py FINDINGS.json
Exit codes: 0 PASS / PASS-WITH-NOTES, 1 FAIL / FAIL-WITH-FIXES, 2 usage.
"""
import json
import sys

SEVERITIES = ("critical", "major", "minor")
RULES = [
    ("critical", "FAIL"),
    ("major", "FAIL-WITH-FIXES"),
    ("minor", "PASS-WITH-NOTES"),
]


def verdict_for(findings):
    present = {f["severity"] for f in findings}
    for severity, verdict in RULES:
        if severity in present:
            return verdict
    return "PASS"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__.splitlines()[0], file=sys.stderr)
        print("usage: grade.py FINDINGS.json", file=sys.stderr)
        return 2
    with open(argv[0], encoding="utf-8") as fh:
        data = json.load(fh)
    findings = data["findings"] if isinstance(data, dict) else data
    for f in findings:
        if f.get("severity") not in SEVERITIES:
            print(f"bad severity in finding: {f!r}", file=sys.stderr)
            return 2
    verdict = verdict_for(findings)
    print(f"VERDICT: {verdict} ({len(findings)} finding(s))")
    for severity in SEVERITIES:
        for f in findings:
            if f["severity"] == severity:
                print(f"  [{severity}] {f.get('summary', '')}")
    return 0 if verdict.startswith("PASS") else 1


if __name__ == "__main__":
    sys.exit(main())
