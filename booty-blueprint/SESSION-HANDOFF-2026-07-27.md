# Session Handoff — 2026-07-27

**Session:** Booty Blueprint copy revision (Heather's review) → Max widget spec → privacy policy gap
**Model:** Opus 5 (Claude Code, remote environment)
**Repo state at handoff:** working tree clean, both branches pushed

This exists because the remote container is ephemeral. Everything below is committed
so nothing is lost when it's reclaimed.

---

## What shipped

**PR #4 — `claude/privacy-contact-email` → `main`. MEANT TO MERGE. Still open (draft).**
One line: the published privacy policy listed `runheather808@gmail.com` — Heather's
personal address — as the studio's public privacy contact. Replaced with
`transform.hawaii@gmail.com`, confirmed as the studio account (it owns MASTER MARKETING,
04 MARKETING & BRAND, and the program PDFs in Drive). Depends on nothing else. **Still
live on the site until this merges.**

**PR #3 — `claude/booty-blueprint-landing-page-jgobal`. NOT for merge** (archive/review
surface, same as PRs #1 and #2). Four documents:

| File | What it is |
|---|---|
| `COPY-REVISION-SPEC-2026-07-26.md` | Final copy for all five of Heather's fixes |
| `MAX-WIDGET-SPEC-2026-07-26.md` | Max chat widget on the Blueprint page + the visitor-capture answer |
| `privacy-policy-DRAFT-2026-07-26.html` | Proposed replacement for `index.html` |
| `privacy-policy-REVIEW-NOTES.md` | What changed, what still needs deciding |

---

## Decisions locked this session

| Item | Decision |
|---|---|
| Heather #1 — "Permanent" | → **"Built to Last."** Plus a sweep for `forever` / `guaranteed` / `for life` and a results-vary qualifier near proof photos |
| Heather #2 — schedule | Page names the **Mon/Thu/Fri 8:00 AM anchor**; individual schedule set at the consultation. No alternate times on the page |
| Heather #3 — "flab to fit" | Both cut. Reframed to destination, not the reader's current body |
| Heather #4 — scarcity | **Six clients per coach.** Rolling enrollment unchanged operationally |
| Heather #5 — opener | Competitor formats cut; leads with what the program is |
| Privacy — contact email | `transform.hawaii@gmail.com` |
| Privacy — California traffic | None meaningful → no CCPA section; general rights paragraph stands |

**Why Fix 4 leads with the ratio, not a spot count:** "six clients per coach" is the
substantiation behind *every rep coached* — the exact claim Heather said the old schedule
bullet was undercutting in Fix 2. It also survives a staffing change, where a bare count
would silently go false.

---

## ⚠ Finding — the privacy gap is already live, not pending

Listing the Wix custom embeds on `transformationshawaii.com` (site
`e0b940f2-111c-4634-b92b-23fffc3bd13e`) turned up **a third-party AI chat widget already
running**: `botdisplay.com/chat-widget.js`, assistant "Front Desk," account
`1UJMK6josrIUTtKSSUjn`, **enabled**.

So visitor chat conversations are already being collected through a vendor the published
policy doesn't disclose. This was treated as a future risk to get ahead of; part of it is
live today. **`botdisplay.com` must join GoHighLevel, Meta, and Wix on the processor list**,
and publishing the updated policy is more urgent than "before the Max widget ships."

Also found on that site:
- A **disabled** LeadConnector/GHL chat widget embed (`67ca0cb71348fda2f37cd7fa`) — prior attempt
- A booking CTA embedding a `link.login2.app` iframe, plus `sessionStorage` use
- **No Google Analytics and no Meta pixel in custom embeds.** Does *not* prove absence — Wix's
  native Marketing Integrations panel and GHL's own tracking settings are both invisible from
  here. The pixel most likely lives on the GHL side, since that's where the ad landing paths
  are. ⚠ If it isn't firing anywhere, that's an ads-measurement problem, not just a policy one
- Every embed is categorized `ESSENTIAL`, the Wix consent category that bypasses cookie
  gating. An AI chat widget capturing visitor conversations is a hard sell as "essential" —
  recategorize when someone's in there

---

## Open — blocking

**1. Data retention wording.** The one thing holding the privacy draft. Options given:
purpose-based (recommended, ~70%), 7 years after last activity (~20%), 2 years (~10%).
Note: an earlier answer of "six weeks or 12 weeks" was program length, not data retention —
alumni reactivation means contact data plainly lives years past 12 weeks, so a 6/12-week
promise would be broken the first time a reactivation fires.

**2. Meta app review URL.** Confirm whether it points at this exact privacy page, and that
broadening the policy's scope doesn't disturb a review that currently passes.

**3. Payments.** Are Klarna/Affirm applications ever *started online*? If in-person only,
no payments section needed.

**4. Coach-naming doctrine call (Garrett).** The copy spec names Joanne in Fixes 2 and 4,
against the standing "never pedestal a coach" rule. Named because she's the coach of record
and the page already runs her consented photos. "Your coach" alternative is in the spec.

---

## Open — needs machine access this session didn't have

**Apply the five copy fixes** to `TPTS-MCP/Outputs/booty-blueprint-page.html` and deploy via
the GHL builder (recipe in the 7/25 codex entry). ⚠ The spec's find-strings are Heather's
quoted phrases, **not confirmed substrings of the file** — confirm against the file rather
than running a blind find-and-replace.

> **Fastest unblock:** paste the page HTML into a session and get back the fully-edited file,
> ready for the GHL code editor. Needs no access changes at all.

**Sync the Sales Max KB and Operators Codex.** Both still record "start anytime — no cohort,
no start date." Once the page says otherwise, Max contradicts the live page to exactly the
leads the page exists to convert. Also add the 6:1 cap to the KB as a sales fact in its own
right — it answers "how is this different from a gym" in four words.

**Heather's sign-off** on the revised page before it returns to ad rotation.

**Network policy.** `transformations.studio` and `facebook.com` are both blocked by this
environment's egress policy (proxy 403 on CONNECT). That blocked post-deploy verification and
the analysis of a Facebook reel sent for creative review. Changing it is an environment
setting — see code.claude.com/docs/en/claude-code-on-the-web.

---

## Post-deploy verification

- [ ] Fetch the live URL; grep for `Permanent`, `flab`, `no cohort`, `burnout circuit`,
      `squat challenge` — all should return **zero** hits
- [ ] No pricing anywhere on the page (standing policy — the consult closes)
- [ ] CTA still books the In-Person Goal Setting Orientation (`bjNAPqsv1EVNNVuJJszM` via
      `CV_BOOK_CONSULT_LINK`)
- [ ] Mobile hero renders (portrait composite `22e4ceb8`/`fa06ae92`)
- [ ] Update `TPTS-MCP/Outputs/booty-blueprint-page.html` so source of truth doesn't drift
