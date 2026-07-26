# Booty Blueprint Landing Page — Copy Revision Spec

**Date:** 2026-07-26
**Trigger:** Heather Rosario's pre-ship review of `transformations.studio/booty-blueprint`
**Status:** Ready to apply — 2 placeholders need real numbers before it ships (see Open Items)

---

## Read this first — how this spec was written

The page is **live** at `transformations.studio/booty-blueprint` (GHL funnel
`x6thDKvo8W4jJMiTRLeb`, step `dcbe9d44-9295-4ca5-9de4-f368f5aeadd8`, page
`bZ3LvHOe6A5OC0EM6EmP`). The source of truth is
`TPTS-MCP/Outputs/booty-blueprint-page.html` on the TPTS-MCP machine.

**This spec was written without reading that file.** The HTML is not in Drive, and
the live URL is blocked by this session's egress policy (proxy returned 403 on
CONNECT to `transformations.studio:443`). So the spec is built from Heather's
verbatim quoted strings plus the program facts of record in the Operations
Notebook (7/25 entry) and the Sales Max Knowledge Base (v8).

Consequence: **the find-strings below are Heather's quotes, not confirmed
substrings of the file.** Whoever applies this should open the HTML, confirm each
string, and treat the replacement copy as the deliverable rather than doing a
blind sed. If a passage doesn't match what's below, the *intent* column tells you
what the fix has to accomplish.

---

## Fix 1 — "Permanent" is a claim risk

**Heather:** *Muscle is use-dependent — stop training, it goes. That's an absolute
outcome claim on a paid fitness offer, which is exactly the category that draws
complaints.*

**Decision:** swap to **Built to Last**.

| Find | Replace |
|---|---|
| `Permanent` (headline use) | `Built to Last` |
| `Permanent gains.` | `Gains that hold.` |

Headline pattern, if it currently reads as a noun phrase:

> **Glutes Built to Last**

**Also sweep for and remove** any other absolute-outcome language in the same
family — these carry identical risk and Heather only caught the two loudest:
`forever`, `for life`, `guaranteed`, `never lose it`, `permanent results`,
`keep it for good`.

**Add** a plain qualifier wherever results or proof photos appear:

> Results depend on consistency and where you're starting from.

**Rationale to keep on file:** "Built to Last" describes *how the program is
constructed*, not an outcome the studio guarantees. That distinction is the whole
defense.

---

## Fix 2 — The schedule bullet contradicts itself

**Heather:** *"Mon/Thu/Fri 8:00 AM anchor class" or any slot 5–11 AM or afternoons
= not a class, it's open gym with a coach nearby. It also quietly undercuts "every
rep coached" — you can't guarantee coaching eyes across a 6-hour window without
staffing it.*

**Decision:** anchor class with **limited, named** alternate slots.

**Delete** all open-window language — anything of the form "sessions slot anywhere
5–11 AM," "or afternoons," "whenever works for you."

**Replacement copy:**

> **Three coached sessions a week.**
> The Blueprint class runs **Mon / Thu / Fri at 8:00 AM** with Joanne.
> Can't make 8:00? A limited number of alternate coached slots are available —
> **[PLACEHOLDER A: real alternate times]** — confirmed with your coach at your
> Goal Setting session.

**Why this shape:** it keeps the anchor (which is what makes it read as a program
rather than a gym membership), it keeps "every rep coached" true, and it stays
honest about the flexibility that actually exists — without implying a coach is
standing on the floor for six straight hours.

**Guardrail:** whatever goes in Placeholder A has to be slots Joanne is genuinely
on the floor for. If the honest answer is "it varies," the alternate sentence
comes out entirely and the page sells the 8:00 AM class only.

---

## Fix 3 — "Flab to fit," twice

**Heather:** *You're calling your buyer flabby in her own sales copy. Women buying
a glute program don't respond to that.*

**Decision:** cut both instances. Do not describe the reader's current body
anywhere on the page.

**Replacement direction — say what she's moving toward, not what you think she is:**

| Context | Replacement |
|---|---|
| Section heading | `Where you'll be in 12 weeks` |
| Transformation line | `From guessing to a plan you can actually follow.` |
| Proof / results framing | `Stronger through the hips. Steadier on your feet. Progress you can measure.` |

This also pulls the page back in line with standing brand doctrine in the Sales
Max KB: **lead with function, not looks.** "Flab to fit" is a looks frame *and* an
insult frame — it fails twice.

---

## Fix 4 — "Start anytime, no cohorts" kills urgency

**Heather:** *Combined with #2, the offer reads come whenever, start whenever — low
commitment, which fights a $1,299–$2,499 price. Keep rolling enrollment
operationally, but sell it as limited spots per training block.*

**Decision:** cap the coached floor.

**Delete:** `Start anytime, no cohorts` and any "no start date" / "no cohort"
phrasing.

**Replacement copy:**

> Joanne keeps **[PLACEHOLDER B: N]** women on the Blueprint floor at a time.
> Spots open as clients finish their block.

CTA microcopy:

> Ask about current openings at your Goal Setting session.

**Why this exact shape:** it is the one framing that creates real urgency *and*
stays literally true under rolling enrollment. Operations don't change — Garrett
still fits people in whenever there's room. The page just stops advertising that
there's always room.

**Guardrail — this one matters:** the number in Placeholder B has to be real and
actually enforced. A cap the studio doesn't honor is a false-scarcity claim, which
is the same category of exposure as Fix 1 and would undo the point of this whole
pass. If there is no number Garrett will hold to, fall back to:
*"We take a limited number of new Blueprint clients each training block."*

---

## Fix 5 — The opening line names the competition's formats

**Heather:** *"Not a burnout circuit, not a squat challenge" plants their images in
your highest-attention sentence. Lead with what it is.*

**Delete** the negation opener entirely.

**Replacement opener (primary):**

> A 3-day-a-week glute and posterior-chain program, coached rep by rep, in Hilo.

**Supporting line underneath:**

> Built around the largest muscle group in your body — the one that drives your
> hips, protects your low back, and keeps you steady as you get older.

**General rule to apply beyond this one sentence:** the page should not name,
describe, or gesture at competitor formats anywhere. Every sentence spent on what
this isn't is a sentence not spent on what it is.

---

## Open items — needed before this ships

| # | Item | Owner | Blocks |
|---|---|---|---|
| A | The real alternate coached slot times (or a decision to drop alternates) | Garrett / Joanne | Fix 2 |
| B | The real cap on Joanne's Blueprint floor | Garrett | Fix 4 |

---

## Downstream sync — do not skip

Fixes 2 and 4 change facts that are **written into the Sales Max knowledge base**,
which is what Max tells leads. If the page changes and the KB doesn't, Max will
contradict the live page to the exact leads the page is meant to convert.

**`max_knowledge_base.txt` (v8) — two edits required:**

1. `PROGRAM TRACKS` → `GLUTE TRANSFORMATION` and the `THE BOOTY BLUEPRINT PAGE`
   section currently describe the page. Neither mentions cohorts, so no change
   needed there — **but** verify no "start anytime" language crept in.
2. The Operations Notebook and Operators Codex both record the program as
   **"start anytime — no cohort, no start date."** That is now wrong as a *sales*
   line even though it stays true operationally. Both need a note that the public
   framing is a capped floor with spots opening as clients finish.

**`OPERATORS-CODEX.md`** — same correction, 7/25 entry.

**Also worth flagging:** the codex carries a standing doctrine — *never pedestal a
coach; market the system, because two former TPTS coaches left and became
competitors.* This spec names Joanne in Fixes 2 and 4 because she is the actual
coach of record and the page already uses her consented photos. That's a
deliberate exception to a real rule, and it's Garrett's call to confirm. The
system-first alternative for both lines is "your coach" instead of "Joanne."

---

## Deploy path

The page is a **Code element inside the GHL page builder**, not a file the site
serves. Editing it means the builder recipe documented in the 7/25 codex entry:

1. Close the **Ask AI panel first**.
2. Canvas **Insert Element** (not "Blank Section").
3. Quick Add search box **retains prior text** — `triple_click` before typing.
4. Element cards are **drag-and-drop** — a plain click adds nothing.
5. Placed Code element → **Open Code Editor** → Ctrl+A → Ctrl+V.
6. **Modal Save** is the only commit, then the top-bar **floppy**. Success tell is
   the "Last saved <time>" chip replacing "Autosave off."
7. **Verify by fetching the public URL and grepping markers.** The builder canvas
   renders custom code as a grey bar and proves nothing.

Update `TPTS-MCP/Outputs/booty-blueprint-page.html` in the same pass so the source
of truth doesn't drift from what's live.

---

## Post-deploy verification

- [ ] Fetch `transformations.studio/booty-blueprint`, grep for `Permanent`,
      `flab`, `no cohort`, `burnout circuit`, `squat challenge` — all should return zero hits
- [ ] Confirm no pricing appears anywhere on the page (standing policy — the
      consult closes)
- [ ] Confirm the CTA still books the In-Person Goal Setting Orientation
      (`bjNAPqsv1EVNNVuJJszM` via `CV_BOOK_CONSULT_LINK`)
- [ ] Mobile hero renders (portrait composite `22e4ceb8`/`fa06ae92`)
- [ ] Send the revised page to Heather for sign-off before it goes back into ad rotation
