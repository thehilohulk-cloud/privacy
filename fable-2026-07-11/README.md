# Fable Final-Day Session Artifacts — 2026-07-11

Everything produced in the 7/11 Claude Code Remote session (this repo's task branch), committed here for durability. **Google Drive is the working source of truth** — these are copies at commit time. Not intended to merge to `main` (this repo serves the privacy-policy page); this branch is an archive + review surface, same pattern as PR #1.

## Contents

| File | What it is | Drive home |
|---|---|---|
| `decision-point-coaching-BUILD-2026-07-11.md` | Titus Sauce Roadmap #3 deploy-ready build package (WF-Vision-Router, master-prompt block, gating options, 12-test battery) | TPTS-MCP plans folder |
| `sunday-story-briefing-cards-BUILD-2026-07-11.md` | Roadmap #4 build package (Phase-0 `assigned_coach` audit, WF-Briefing-Cards, WF-Sunday-Story) | TPTS-MCP plans folder |
| `build_wf_morning_digest.py` | Zero-config n8n builder for the consolidated morning digest (digest-migration SPEC items 1+2). Validated: py_compile, node --check on embedded JS, emitted workflow JSON + wiring | TPTS-MCP plans folder |
| `wf-morning-digest-RUNBOOK.md` | Deploy runbook for the above (TODO(VERIFY-GHL) checks, Sentinel registration, 2-clean-runs rule) | TPTS-MCP plans folder |
| `youtube-warmfirst-shoot-kit-2026-07-11.md` | 10 objection-pair scripts + half-day shoot logistics + distribution wiring + Day-30 cold-unlock metrics | TPTS-MCP plans folder |
| `kit-email-copy-2026-07-11.md` | Finalize-ready copy for all 3 Kit sequences + rollover/birthday singles (link placeholders to fill from vault) | TPTS-MCP plans folder |
| `02-BACKLOG.md` | Full backlog refresh reconciled against notebook 7/4–7/11 (old version archived in Drive as `02-BACKLOG-archived-2026-07-11.md`) | Garrett-HQ backlog folder |

**Nutrition packets (L1–L4 PDFs + generator) are NOT in this repo** — binary files don't ride the API push path used from this session. They live in Drive → Library → *1. Challenge Levels* (`Transformations-Nutrition-Guide-L1regenerated/L2/L3/L4-DRAFT.pdf` + `[C] build_challenge_packet.py — FULL canonical source L1-L4`), and the four PDFs were also delivered in the 7/11 Cowork chat. Factors: L1 1.25 / L2 1.75 / L3 2.25 from sources; **L4 2.75 EXTRAPOLATED — verify vs Canva original**.

## Session log
Three dated notebook entries (prepend to TPTS-Operations-Notebook.md) live in the Drive notebook folder: `…FABLE-FINAL-BUILDS.md`, `…FABLE-FINAL-ROUND2.md`, `…FABLE-FINAL-ROUND3-kit-copy.md`. They carry the full findings, including: Stripe billing-watch results (Kristie not converted / Gail card-update landed / Charmaine active / Arati unconverted), the `assigned_coach` gap, the L4 sourcing gap, and the Kit write-API restriction from this session.

## Regenerating the packets
```
python3 build_challenge_packet.py            # emits l1–l4 HTML (script in Drive, see above)
chromium --headless --disable-gpu --no-sandbox --print-to-pdf=lN_packet.pdf --no-pdf-header-footer file://$PWD/lN_packet.html
```
Needs `pip install segno`. In the Cowork sandbox, Chromium lives at `/opt/pw-browsers/chromium`.
