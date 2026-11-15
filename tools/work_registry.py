#!/usr/bin/env python3
"""work_registry.py — a single-file work registry for a multi-agent system.

The registry is the source of truth for what work exists, who owns it,
and what state it is in. State lives in one JSON file; writes are atomic
(write to a temp file, then rename) so a crash mid-write cannot corrupt it.

Usage:
    work_registry.py --file REGISTRY.json add "title" [--lane LANE]
    work_registry.py --file REGISTRY.json list [--status STATUS]
    work_registry.py --file REGISTRY.json claim ID --owner NAME
    work_registry.py --file REGISTRY.json block ID --note "what is needed"
    work_registry.py --file REGISTRY.json close ID --evidence "artifact"
    work_registry.py --file REGISTRY.json next   # open, un-owned, un-blocked

Exit codes: 0 ok, 1 no such item / invalid transition, 2 usage error.
"""
import argparse
import json
import os
import sys
import tempfile

STATUSES = ("open", "claimed", "blocked", "done")


def load(path):
    if not os.path.exists(path):
        return {"items": []}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(path, data):
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    os.replace(tmp, path)


def find(data, item_id):
    for item in data["items"]:
        if item["id"] == item_id:
            return item
    return None


def cmd_add(data, args):
    new_id = max((i["id"] for i in data["items"]), default=0) + 1
    data["items"].append({
        "id": new_id, "title": args.title, "lane": args.lane,
        "status": "open", "owner": None, "evidence": None, "note": None,
    })
    print(f"added #{new_id}: {args.title}")
    return 0


def cmd_list(data, args):
    for item in data["items"]:
        if args.status and item["status"] != args.status:
            continue
        owner = item["owner"] or "-"
        print(f"#{item['id']} [{item['status']}] ({item['lane']}) "
              f"{item['title']} — owner: {owner}")
    return 0


def cmd_next(data, _args):
    for item in data["items"]:
        if item["status"] == "open" and not item["owner"]:
            print(f"#{item['id']} ({item['lane']}) {item['title']}")
            return 0
    print("nothing dispatchable")
    return 0


def _transition(data, args, status, fields):
    item = find(data, args.id)
    if item is None:
        print(f"no item #{args.id}", file=sys.stderr)
        return 1
    if item["status"] == "done":
        print(f"item #{args.id} is already done", file=sys.stderr)
        return 1
    item["status"] = status
    item.update(fields)
    print(f"#{args.id} -> {status}")
    return 0


def cmd_claim(data, args):
    return _transition(data, args, "claimed", {"owner": args.owner})


def cmd_block(data, args):
    return _transition(data, args, "blocked", {"note": args.note})


def cmd_close(data, args):
    if not args.evidence:
        print("closing requires --evidence (the artifact that proves it)",
              file=sys.stderr)
        return 1
    return _transition(data, args, "done", {"evidence": args.evidence})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", required=True, help="registry JSON file")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add"); p.add_argument("title")
    p.add_argument("--lane", default="general"); p.set_defaults(fn=cmd_add)

    p = sub.add_parser("list"); p.add_argument("--status", choices=STATUSES)
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("claim"); p.add_argument("id", type=int)
    p.add_argument("--owner", required=True); p.set_defaults(fn=cmd_claim)

    p = sub.add_parser("block"); p.add_argument("id", type=int)
    p.add_argument("--note", required=True); p.set_defaults(fn=cmd_block)

    p = sub.add_parser("close"); p.add_argument("id", type=int)
    p.add_argument("--evidence", required=True); p.set_defaults(fn=cmd_close)

    p = sub.add_parser("next"); p.set_defaults(fn=cmd_next)

    args = ap.parse_args(argv)
    data = load(args.file)
    rc = args.fn(data, args)
    if rc == 0 and args.cmd in ("add", "claim", "block", "close"):
        save(args.file, data)
    return rc


if __name__ == "__main__":
    sys.exit(main())
