# BUILD PACKAGE — Sunday Story + Coach Briefing Cards w/ Pod Routing (Titus Sauce Roadmap #4)
**Date:** 2026-07-11 · **Author:** Fable 5 (final-day session) · **Status:** DEPLOY-READY DESIGN — execute after Roadmap #3
**Roadmap authority:** `[C] Titus-Sauce-Roadmap.md` — plays #6 + #7 + the Coach-Pod org model, approved as build-order item 4.

## PHASE 0 — `assigned_coach` REALITY CHECK (do first; ~1 hr)
The roadmap says the CF already exists — **the Operations Notebook never mentions it and nothing writes it today** (pod mapping lives implicitly in class rosters). 1) Create the GHL CF if absent (dropdown: garrett/mari/joanne/shayla). 2) Populate all actives: script a first pass from WF10's schedule CFs + class-block coach mapping; Garrett eyeballs once. 3) Onboarding sets it at activation; unassigned = Garrett's pod; nightly Brain rule flags any `titus-client` with it empty.

## PART A — COACH BRIEFING CARDS (build first: coach-facing, no member-send risk)
4 lines per client: state (trend + radar color, plain words) · celebrate (one specific thing to say out loud) · watch · ask (one question that shows we remember). `WF-Briefing-Cards`, cron `0 4,15 * * 1,2,4,5` HST (mirrors WF11's proven 4a/4p; classes M/T/Th/F):
1. Pull roster blocks from the same source WF10/WF11 read, grouped by class block.
2. Per client: `fetch_bundle` RPC (Fetch Context `jKcly7AFhv6dFEcj`, has ghl-fallback so non-Memory-V2 clients work) + latest radar row + last weigh-in + open commitments.
3. ONE Anthropic call per COACH (batch their block; cached static block ≥1024 tok, sonnet-5, thinking disabled); cards ~220ch each so 2–3 fit one SMS; more → numbered burst.
4. Send to coach's line via `/conversations/messages` from 4753 w/ `[CARDS 6AM]`-style label. Coach contacts: Garrett `GaPdKEftwuZTL9g6Z0x5`, Joanne `6KguiJARmPeVGGqaDPhG`; Mari + Shayla IDs = harvest from WF11's send nodes (laptop).
5. **Routing rule:** cards follow the CLASS ROSTER (whoever coaches the session); `assigned_coach` governs escalations + weekly pod digest. Radar RED always adds Garrett, coach CC'd.
6. Guardian `pxCzWL7wlfmR7fQf`; Sentinel expected-runs (M/T/Th/F cadence); note/log nodes onError-continue; 7am-hour doctrine fine (coach-facing).
**Garrett boss view:** extend Coaching Brain (`H3zxWj1CnZ9zMvq5`) with a per-pod rollup section — do NOT add another morning SMS (volume was the disease).
**Phase-2 (not launch):** coach reply commands (`C3 done`, `note <client> …`) namespace-guarded like HOLD.

## PART B — SUNDAY STORY (client-facing; build second, behind gate rails)
Weekly personal narrative from their ACTUAL week. `WF-Sunday-Story`, cron `0 15 * * 0` HST (Sun 3p):
1. Roster: `titus-client` actives minus paused/suppression — reuse the pre-send-gate exclusion set verbatim.
2. Bundle: `hot_context` week summary, weigh_ins delta (trend-first, perimenopause-aware), attendance vs plan, commitments, radar trajectory, scheduled_touches.
3. Compose per client (cached static block): 1–2 SMS max, model ≤235ch/segment; ≥2 concrete facts from THEIR week; zero generic praise; slipping → rescue-play tone, never guilt; data-empty → gentle "I noticed quiet" variant + coach FYI.
4. **Send lanes = engine lanes:** gateless → live on 8086 (explicit fromNumber); drafts-first → phone review page `/webhook/sunday-story-review?t=<token>` (clone alumni-evergreen prefetch-safe page; every review SMS carries the tappable link). Y-all / Y<id> / edit / skip.
5. Idempotency: `[SUNDAY-STORY]` note per client per week; sent story appends to Memory V2 turns so next week can reference it.
6. Guardian + Sentinel (weekly → register long-cadence to dodge the ~3d exec-retention false alarm).
**Cost:** ~40 clients × ~2.5K in/300 out weekly ≈ negligible w/ caching. No new approval needed.

## GARRETT DECISIONS
1. Approve 3 sample stories (ZZTEST + Heather + one drafts-first) before any live send. **Recommend first 2 Sundays 100% drafts-first for everyone.** 2. Card delivery hour: 4a (rec) vs 8:30p night-before. 3. Confirm routing rule (cards follow class, escalations follow pod).

## TEST BATTERY (12)
Phase-0 audit + Brain flag · 3-client block → one SMS · zero-data client → plain no-invention card · radar RED → Garrett+coach · weekend → no cards, Sentinel quiet · gateless story → 1–2 SMS, ≥2 facts, fromNumber 8086 · drafts-first → review page Y/skip + same-week rerun no-dupe · paused excluded · slipping → rescue tone · story retrievable next week · forced error → Guardian fires, batch continues (per-client isolation; the 404-note lesson) · coach reply w/ Phase-2 off → no crash.

## DEFINITION OF DONE
`build_wf_briefing_cards.py` + `build_wf_sunday_story.py` in Outputs (re-runnable, node --check, cred-harvest pattern from build_wf_morning_digest.py) · both ACTIVE + Guardian-wired · Sentinel registered · Brain pod-rollup live · battery green w/ receipts · CODEX + notebook · Garrett's 3 decisions recorded.
**Sequencing:** Phase 0 + Part A in one session; Part B the following session after sample approval — the review-page clone deserves its own verification pass.
