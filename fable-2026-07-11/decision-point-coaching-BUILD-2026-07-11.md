# BUILD PACKAGE — Decision-Point Coaching (Titus Sauce Roadmap #3)
**Date:** 2026-07-11 · **Author:** Fable 5 (final-day session) · **Status:** DEPLOY-READY DESIGN — execute from the laptop TPTS-MCP session
**Roadmap authority:** `[C] Titus-Sauce-Roadmap.md` — Garrett-approved build order; #1 Deliverables + #2 Radar LIVE, this is #3.
**Frame:** the word-of-mouth feature. A client stands in a restaurant, texts Titus a menu photo, and gets a specific order for THEIR macros in under two minutes. Nobody else's coach does this. That story gets retold.

---

## 1. CLIENT EXPERIENCE (what we're shipping)

| Trigger (inbound to 8086) | Titus's move |
|---|---|
| **Menu photo** | Reads the menu, picks 1 best order + 1 backup for their remaining macros today (uses the running macro tally), names the swap ("rice not fries, double protein"). |
| **Grocery cart photo / list** | Approves/flags items against their plan; suggests 2–3 additions that fill this week's gaps. |
| **Plate photo** | QUALITATIVE ONLY (see §3): structure check vs B:P+C+V / L:P+C+V / D:P+F+V, portion language ("palm of protein"), and a next-meal adjustment. Never invented gram/calorie numbers. |
| **"I'm craving ___" text (the 9pm moment)** | Craving protocol: name it, normalize it, 10-minute delay + protein-first counter-offer, fit-it-in math if they still want it ("that fits — log it, lighter carbs at breakfast"). Never guilt (Radar rescue-play tone). |
| **"Traveling Thu–Sun" text** | Travel survival plan deliverable: airport/hotel/restaurant defaults, minimum-effective workout, weigh-in expectations on return (water weight education). |

All reactive (inbound-triggered) — quiet-hours rules don't block replies to a client who just texted. Proactive follow-ups stay inside existing proactive-touch rails.

## 2. ARCHITECTURE — one new sub-workflow + prompt work; engine barely changes

**Today:** inbound MMS → journal writes `[sent an image]` (7/9 empty-body fix), FitIndex screenshots ride a dedicated extraction path (`fitindex-extraction-spec.md`). The engine LLM never *sees* image content.

**Build: `WF-Vision-Router` (new n8n sub-workflow, Execute-Workflow pattern like Fetch Context `jKcly7AFhv6dFEcj`):**
1. **Input:** `{contact_id, message_id, attachment_urls[]}` from the engine's inbound path when attachments present.
2. **Fetch image** (GHL attachment URL → binary → base64; cap 5MB, downscale if bigger — Anthropic image limit).
3. **Classify + extract** — ONE Anthropic vision call (sonnet-5, thinking disabled, max_tokens 700, static spec block ≥1024 tok so `cache_control` is not inert). Output contract (strict JSON): `{ "type": "fitindex_weight | fitindex_measurements | menu | grocery | food_plate | progress_photo | other", "coaching_context": "dense factual description for the coach LLM — NO advice here", "legibility": "full | partial | none", "confidence": 0.0, "needs_human_review": false }`
4. **Route:** `fitindex_*` → hand off to the EXISTING extraction path unchanged (two-numbers trap rules live there; do not duplicate them). `menu|grocery|food_plate` → return `coaching_context` to the engine. `progress_photo|other` → return short neutral description ("[client sent a photo: …]").
5. **Engine patch (the only engine change):** where the history/turn builder currently substitutes `[image/attachment]`, when Vision-Router returned context, inject instead: `[IMAGE CONTEXT — vision] <coaching_context>` as part of the SAME user turn. The normal engine call composes the reply. **One brain, one reply path — no second sender, no dual-send risk.** Mirror the patch in the engine build script same-session (source-sync doctrine).
6. **Failure containment:** Vision-Router errors → engine proceeds with `[client sent a photo I couldn't read — ask them what it is]` (onError-continue; note-logging never kills a run). Guardian `pxCzWL7wlfmR7fQf` on the sub-workflow. Sub-workflow must be ACTIVATED (callers won't publish otherwise).

**Memory V2:** Append Turn stores the turn text INCLUDING the `[IMAGE CONTEXT]` block → embeddings make "that poke bowl last month" semantically recallable. No schema change needed.

## 3. DOCTRINE GUARDRAILS (non-negotiable, from existing specs)
- **No plate-photo macro estimation.** `fitindex-extraction-spec.md` doctrine: vision = OCR of legible text/screens, never gram guessing. Plate photos get STRUCTURE + PORTION-HAND language + trend framing. If a client asks "how many calories is this?" → "camera can't weigh food — here's the portions read: …" Menu items with printed macros/prices = legible text, fair game.
- **Never fabricate.** Illegible menu → say so, ask what section they're looking at. `legibility: none` → never bluff.
- **Prestige affiliate link NEVER to members** (Garrett rule): supplement questions at decision points answer normally, no link.
- **Running-macro-count section already in master prompt** — Decision-Point REUSES that tally; macro math inside approved targets ≠ macro proposal → NOT review-flagged (per Heather BMR fix). Actual plan-target changes still ride the plan-gate.
- **Sign-off discipline:** no "- Coach Titus" signature on replies (only cold opens).
- **Red flags:** ED-pattern language at craving moments → escalate to Garrett ALWAYS (existing medical/distress lane), reply stays gentle-neutral.

## 4. MASTER-PROMPT BLOCK — see Drive copy of this doc for the full paste-ready text (menu order-picking w/ running tally + kb/13 carb timing; grocery approve/flag/add; plate portion-language-only; 9pm craving protocol [normalize → counter-offer → fit-it-in → identity language, never guilt]; travel survival plan; SPEED RULE: one pass, one clarifying question if unreadable). Voice-brain addition: "You can't see photos on a call — tell them to text the photo to this number."

## 5. GATING / LATENCY POLICY — Garrett decision (recommendation first)
Decision moments die in minutes; a next-morning draft approval is a dead feature.
- **Option A (RECOMMENDED — launch):** Decision-point replies live only for `gateless: true` clients (Heather, Mari, crew). Drafts-first clients get the draft as today; don't announce to them yet. Zero new send authority.
- **Option B (phase 2, after 2 clean weeks):** new Triage `[DP]` lane — auto-send when image/craving/travel intent detected AND no plan-target change AND no red-flag scan hit (reuse the 12/12-gated category scan pattern) → send + `[AUTO-SENT][DP]` audit note + Garrett FYI.

## 6. TEST BATTERY (ZZTEST fixture `6a526a13193168187c1286c3` + Garrett's chart)
1 menu clear → 1 order + 1 backup w/ remaining macros · 2 menu blurry → one question, no bluff · 3 grocery → approve/flag/add · 4 plate → zero numeric macros · 5 plate + "how many calories?" → declines, coaches portions · 6 FitIndex screenshot → extraction path intact (two-numbers trap regression) · 7 image-only MMS → no Anthropic 400 (7/9 regression) · 8 9:15pm craving → protocol, no guilt · 9 ED-pattern → Garrett flagged, warm-neutral reply · 10 travel → 4-part plan · 11 drafts-first menu photo → normal draft (Option A) · 12 Vision-Router hard failure → engine still replies, Guardian fires, run completes.

## 7. ROLLOUT: canary Garrett+Heather → tuning crew → member announce after 2 clean weeks AND Membership Agreement v2 consent coverage check. Announce SMS copy staged in the Drive doc (2 variants ≤235ch), NOT sent.

## 8. DEFINITION OF DONE: `engine/build_wf_vision_router.py` + engine patch mirrored same-session · sub-workflow ACTIVE + Guardian-wired · master-prompt block in the CANONICAL file then both brains (do unification prereq FIRST) · 12/12 battery green w/ receipts · OPERATORS-CODEX + notebook · announce copy staged pending Garrett.
**Prereq flag (do first, 30 min):** chart compress-oldest → `client_story` (Heather ~11.4K/12K cap) — don't launch a photo-heavy feature into a nearly-full chart.
