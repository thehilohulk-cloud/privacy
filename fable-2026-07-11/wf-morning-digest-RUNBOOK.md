# RUNBOOK — WF-Morning-Digest deploy (digest-migration SPEC items 1+2, consolidated)
**Date:** 2026-07-11 · **Author:** Fable 5 (final-day session) · **Companion:** `build_wf_morning_digest.py` (same folder)
**What ships:** ONE n8n morning digest SMS (4:45a HST, front desk 4753, `[MORNING]` prefix) replacing laptop tasks `ops-log-rollup` (4:31a) + `tpts-overwatch-morning` (5:35a). This implements the SPEC's recommended consolidation — **Garrett still needs to bless that choice; if he wants two texts, run the builder twice with split section configs (trivial edit: name + cron + which source nodes).**

## Why the builder is safe to run as-is
- **Zero-config harvest:** it copies the GHL credential, `fromNumber` (4753), `locationId`, and the Anthropic credential from live fleet nodes (Triage V3 / Coaching Brain class workflows) instead of hardcoding. If harvest can't find something it STOPS with instructions — it never deploys half-wired.
- Fetch-or-create by name; deactivate→PUT→activate with re-GET verify; staticData carried through PUT (heartbeat preserved on re-runs); settings whitelisted to `executionOrder`+`errorWorkflow`; Guardian `pxCzWL7wlfmR7fQf` wired; every embedded JS block `node --check`ed pre-deploy; n8n API key read from a vault file (`N8N_API_KEY_FILE`), never inline.
- All source-pull nodes are `alwaysOutputData` + onError-continue: a dead source becomes a named gap in the SMS ("gaps: ghl-payments"), never a dead morning. LLM-compose failure falls back to a deterministic raw-numbers SMS. **A silent morning is the one failure mode this workflow is not allowed to have** — that's the exact 7/6–7/11 incident class this migration exists to kill.
- Heartbeat anchor: review window = since `staticData.lastSuccessISO` (cap 72h), per `reference_scheduled_tasks_app_open_constraint` doctrine — never a fixed "last 24h".

## Deploy steps (laptop TPTS-MCP session)
1. `set N8N_BASE_URL=...` + `set N8N_API_KEY_FILE=<vault path>` → `python build_wf_morning_digest.py --dry-run` (inspect JSON) → run without flag.
2. **Resolve the two `TODO(VERIFY-GHL)` nodes** against the local SKILL.md files (`ops-log-rollup`, `tpts-overwatch-morning`) — the exact GHL endpoints those tasks read. Builder assumes `/calendars/events` (appointments) + `/payments/transactions` (revenue). If the SKILL.md files show different sources (e.g. an ops-log contact's notes, opportunity pipeline reads, or the revenue scoreboard vs $30K-Aug/$50K-Oct/$85K-Q1'27 targets), port those reads as additional HTTP source nodes → add to `Aggregate` (pattern is uniform: every source is one `grab()` + one section). **The scoreboard targets should be added to the SYSTEM_PROMPT if ported.**
3. If the harvester warned about a missing n8n self-read credential: open the two fleet-health nodes in the UI and attach the same header-auth cred Sentinel `2yWJo3KocHsqSZGp` uses for `/api/v1/executions`.
4. Manual execute → confirm SMS lands on the 4753 thread, `[MORNING]` prefix, ≤320ch, quiet-morning form reads clean.
5. **Sentinel registration:** add `WF-Morning-Digest` to expected-runs (daily cadence). It is NOT long-cadence — normal miss detection applies.
6. **Two-clean-scheduled-runs rule:** leave the local Claude tasks running in parallel until n8n has fired clean on schedule twice (you'll get doubled digests for 2 mornings — acceptable). Then delete `ops-log-rollup` + `tpts-overwatch-morning` locally, and note that `TPTS-Claude-Daily-Restart` (4:30a) loses two of its dependents (keep it — other locals remain).
7. OPERATORS-CODEX + notebook entry; mirror any live patches back into the builder same-session (source-sync doctrine).

## Anthropic node notes
`claude-sonnet-5`, `thinking: {"type":"disabled"}`, `max_tokens: 400`, system block carries `cache_control` — **verify `cache_read_input_tokens > 0` on the second run**; if 0, the block is under the 1024-token floor → pad the system prompt (add the section spec verbatim), don't remove caching.

## Remaining SPEC items after this ships
- **overwatch-weekly (Mon 6:30a):** clone this builder — cron `30 6 * * 1`, window = 7d fixed (not heartbeat), add funnel/utilization/retention reads, max_tokens 600. Estimated 30 min once this one is proven.
- **doc-send-daily-check (9a):** same skeleton; sources = onboarding-docs workflow health + sent/signed watchlist.
- **BLOCKED (unchanged):** campaign3 (needs a Meta Graph token as an n8n cred first) · lincoln-watch (needs Gmail OAuth cred; likely dies naturally when the attorney replies).
- **Verify-then-retire `remote-silence-watch` checklist:** (1) list clients it watches (its SKILL.md) → (2) diff vs Titus Watchdog `me0i8pEBXa2v2XeJ` + Accountability `ofSY32qpFTee12qW` coverage (remote+bridge vs Titus-migrated-only) → (3) if Watchdog covers all remote/bridge clients, delete the local task; else extend Watchdog's roster rather than migrating the watcher.
