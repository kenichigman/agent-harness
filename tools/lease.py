#!/usr/bin/env python3
"""lease.py — time-boxed, single-holder leases on shared resources.

A lease is a named claim in a JSON file: resource -> {holder, expires}.
Expiry is the crash recovery — a dead holder's lease lapses on its own.
Only the holder may release or renew a lease early.

Usage:
    lease.py --file LEASES.json acquire RESOURCE --holder NAME [--ttl 900]
    lease.py --file LEASES.json renew   RESOURCE --holder NAME [--ttl 900]
    lease.py --file LEASES.json release RESOURCE --holder NAME
    lease.py --file LEASES.json status

Exit codes: 0 ok, 1 refused (held by someone else / not held), 2 usage.
"""
import argparse
import json
import os
import sys
import tempfile
import time


def load(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(path, data):
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    os.replace(tmp, path)


def live(entry, now):
    return entry is not None and entry["expires"] > now


def cmd_acquire(data, args, now):
    entry = data.get(args.resource)
    if live(entry, now) and entry["holder"] != args.holder:
        print(f"refused: {args.resource} is held by {entry['holder']} "
              f"for {int(entry['expires'] - now)}s more", file=sys.stderr)
        return 1
    data[args.resource] = {"holder": args.holder, "expires": now + args.ttl}
    print(f"acquired {args.resource} by {args.holder} for {args.ttl}s")
    return 0


def cmd_renew(data, args, now):
    entry = data.get(args.resource)
    if not live(entry, now) or entry["holder"] != args.holder:
        print(f"refused: no live lease on {args.resource} held by "
              f"{args.holder}", file=sys.stderr)
        return 1
    entry["expires"] = now + args.ttl
    print(f"renewed {args.resource} for {args.ttl}s")
    return 0


def cmd_release(data, args, now):
    entry = data.get(args.resource)
    if entry is None:
        print(f"no lease on {args.resource}", file=sys.stderr)
        return 1
    if live(entry, now) and entry["holder"] != args.holder:
        print(f"refused: {args.resource} is held by {entry['holder']}",
              file=sys.stderr)
        return 1
    del data[args.resource]
    print(f"released {args.resource}")
    return 0


def cmd_status(data, _args, now):
    if not data:
        print("no leases recorded")
        return 0
    for name in sorted(data):
        entry = data[name]
        state = (f"held by {entry['holder']}, "
                 f"{int(entry['expires'] - now)}s left") if live(entry, now) \
            else "expired"
        print(f"{name}: {state}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", required=True, help="lease JSON file")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("acquire", "renew", "release"):
        p = sub.add_parser(name)
        p.add_argument("resource")
        p.add_argument("--holder", required=True)
        if name != "release":
            p.add_argument("--ttl", type=int, default=900)
    sub.add_parser("status")

    args = ap.parse_args(argv)
    now = time.time()
    data = load(args.file)
    fn = {"acquire": cmd_acquire, "renew": cmd_renew,
          "release": cmd_release, "status": cmd_status}[args.cmd]
    rc = fn(data, args, now)
    if rc == 0 and args.cmd != "status":
        save(args.file, data)
    return rc


if __name__ == "__main__":
    sys.exit(main())
