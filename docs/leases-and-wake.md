# Leases and wake management

## Why leases

A multi-agent fleet shares scarce things: one powerful workstation, one GPU, one single-writer ledger, one browser profile that only one session may drive. Without coordination, two well-meaning workers collide — both render to the same output path, both write the same file, both assume the machine is theirs.

A lease is the simplest sufficient mechanism: a named, time-boxed, single-holder claim stored in a file.

- **Acquire before use.** The holder records its name and an expiry. Acquisition fails if a live lease exists.
- **Expiry is the crash recovery.** A worker that dies holding a lease does not deadlock the fleet: the lease lapses on its own. Holders doing long work renew explicitly, which doubles as a heartbeat.
- **Release is explicit and checked.** Only the holder can release early, so one worker cannot drop another's claim by mistake.
- **Leases are visible.** `tools/lease.py status` shows every live claim, its holder, and its remaining time — the fleet's contention is one command away from any participant.

## Wake management

Execution hosts sleep. Waking one is a fleet action with its own discipline:

- **Wake under lease.** A worker wakes a host only while holding that host's lease, for named work. Casual wake-ups fragment the owner's machine time.
- **Owner intent outranks the schedule.** A dark machine late at night is the owner's decision until proven otherwise. The harness probes first (is the machine expected to be up? is work actually queued for it?) and never auto-wakes on a single failed probe. A standing permission to wake-and-use does not override a deliberate sleep.
- **Distinguish sleep states.** Wake mechanisms that reliably raise a machine from sleep may not raise it from full shutdown. The harness treats "wake from sleep" and "wake from off" as separate capabilities, each proven separately, and never plans around the unproven one.
- **A failed wake is a broken chain, not a skipped step.** If a wake attempt fails, that is an incident to own and fix — the queue depending on that host is blocked, and the registry says so — never a quiet note-and-move-on.
- **Long work holds the machine awake honestly.** Detached jobs that outlive a host's idle window run under a held lease that also keeps the host awake; a job silently killed by its host's sleep timer is a lease bug, not bad luck.
