#!/usr/bin/env python3
"""liveness.py — two-signal liveness check for a long-running job.

A job is alive only when BOTH signals agree:
  1. the PID recorded in the pid file belongs to a live process;
  2. the job's output/heartbeat file is younger than --max-age seconds.

Either signal alone lies: a live process can be wedged, and a fresh file
can be residue from a previous run.

Usage:
    liveness.py --pid-file JOB.pid --output-file JOB.log [--max-age 300]

Exit codes: 0 alive, 1 dead (failing signal printed), 2 usage error.
"""
import argparse
import os
import sys
import time


def pid_alive(pid):
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # exists, owned by someone else
    return True


def check(pid_file, output_file, max_age, now=None):
    """Return (alive, reason). Pure enough to unit-test."""
    now = time.time() if now is None else now
    try:
        with open(pid_file, encoding="utf-8") as fh:
            pid = int(fh.read().strip())
    except (OSError, ValueError):
        return False, f"signal 1 FAIL: pid file {pid_file} unreadable"
    if not pid_alive(pid):
        return False, f"signal 1 FAIL: pid {pid} is not alive"
    try:
        age = now - os.path.getmtime(output_file)
    except OSError:
        return False, f"signal 2 FAIL: output file {output_file} missing"
    if age > max_age:
        return False, (f"signal 2 FAIL: output is {int(age)}s old "
                       f"(max {max_age}s)")
    return True, f"alive: pid {pid} running, output {int(age)}s old"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pid-file", required=True)
    ap.add_argument("--output-file", required=True)
    ap.add_argument("--max-age", type=int, default=300)
    args = ap.parse_args(argv)
    alive, reason = check(args.pid_file, args.output_file, args.max_age)
    print(("OK  " if alive else "DEAD") + " " + reason)
    return 0 if alive else 1


if __name__ == "__main__":
    sys.exit(main())
