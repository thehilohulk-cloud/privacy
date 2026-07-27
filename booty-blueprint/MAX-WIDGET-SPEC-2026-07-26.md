# Max Sales Widget on the Booty Blueprint Page — Spec

**Date:** 2026-07-26
**Page:** `transformations.studio/booty-blueprint` (GHL funnel `x6thDKvo8W4jJMiTRLeb`, page `bZ3LvHOe6A5OC0EM6EmP`)
**Status:** Spec — one hard blocker before any of it ships (see Blocker)

---

## Part 1 — The widget

### What it is

A GHL chat widget on the Blueprint page, backed by the same Max agent and the same
Sales Max Knowledge Base (v8) that runs the Facebook and Instagram DMs. Same
brain, new surface. Because the page is already a GHL funnel page, the widget is
native — no third-party script, no extra vendor.

### Placement and priority

**The booking CTA stays primary.** This is the standing rule in the KB and it
applies harder on the page than in DMs:

> NEVER INSTEAD OF A TIME. The win is still a booked Goal Setting session. A link
> is not a booking.

So: widget bubble bottom-right, collapsed on load. It does **not** auto-open, it
does **not** cover the booking calendar on mobile, and it is never the largest
call to action in the viewport. A visitor who arrived ready to book should be able
to book without ever touching it.

The widget exists to catch the visitor who reads the whole page and still doesn't
book — which today is a silent exit.

### Opening message

Proactive nudge after ~30 seconds or on exit intent, not on load:

> Questions about the Blueprint? I can check what's open this week.

That opener is deliberate: it offers the booking, not a conversation. It matches
the KB's "offer two specific times" instinct rather than inviting an open-ended
chat the visitor has to carry.

### Capture flow

Straight out of the KB, unchanged:

- Real first name plus a phone or email **inside the first two replies**
- Never quote a price — redirect to the free Goal Setting session
- Never promise a specific class time — the schedule is set at the consult
  (see Fix 2 in the copy revision spec)
- Off-island or asking about a teen: capture, deflect warmly, fire Notify Garrett
- The win is a booked Goal Setting Orientation via `CV_BOOK_CONSULT_LINK`

### Consent at the point of capture — required, not optional

If Max collects a phone number on this widget and the studio later **texts** that
number, the consent has to be captured at the moment the number is given. This is
the part that is easy to skip and expensive to skip.

The widget needs visible disclosure at the capture step, along these lines:

> By sharing your number you agree we may text you about your consultation.
> Message and data rates may apply. Reply STOP to opt out.

Store the consent with a timestamp on the GHL contact record. Without a stored
timestamped consent, every follow-up text is an unconsented message to a number
the studio obtained online.

---

## Part 2 — "Can we capture who visits the page?"

Yes — but "who visits" splits into three very different things, and they are not
equally advisable. Ranked by how much they'd actually earn.

### Tier 1 — People who engage. **Do this.**

Anyone who talks to Max, books, or fills a form becomes a GHL contact with a real
name and a real phone or email, given voluntarily. This is the entire point of the
widget and it is the only tier that produces a lead you can legitimately call.

Everything the studio actually wants from "capture who visits" lives here.

### Tier 2 — Known contacts you already have. **Do this too.**

When someone arrives from a GHL email or SMS link, GHL can attribute that visit to
the contact record it already belongs to. So you learn *"Anna opened the Blueprint
page twice this week and didn't book"* — which is a genuinely strong follow-up
trigger, and it is first-party data from someone already in the database who
already opted in.

This is the highest-value item in this whole document and it costs nothing but
configuration. Pair it with the existing nurture ladder: page view without a
booking inside 48 hours fires a follow-up.

Aggregate analytics (Meta pixel, GA) also sit here — useful for ad optimization,
not for identifying individuals.

### Tier 3 — De-anonymizing strangers. **Recommend against.**

There is a vendor category that resolves anonymous traffic to real names, emails,
and addresses by matching against identity graphs — sold as "visitor
identification." It is technically available and it is what people usually mean
when they ask this question.

The problem is not that it's hard. It's that **the output is unusable.** A phone
number obtained this way carries no consent, so texting or calling it is an
unconsented contact to a number the person never gave you. The regulatory exposure
sits in exactly the same family as the "Permanent" claim Heather just made us
remove — and this one is worse, because a claim risk draws a complaint while
unconsented outreach draws statutory damages per message.

There's a business reason too, and it's the one I'd lead with. Cold-contacting
someone who browsed a glute program and never raised their hand is a bad first
impression in a town this size. Transformations sells on referral and reputation
in Hilo. That is a poor thing to spend.

**What to do instead:** Tier 1 and Tier 2 capture everyone who has shown real
intent. For the rest, the correct lever is retargeting — reach the same anonymous
visitors through Meta's ad platform, where the consent and the identity stay on
Meta's side of the wall. Given C3 is over-concentrated at 29% pool penetration and
the tested creative bench is spent, a Blueprint-page retargeting audience is
probably a better use of this instinct anyway.

---

## Blocker — the privacy policy does not cover any of this

`index.html` in this repo is the published policy at the studio's privacy URL. It
describes exactly one thing: the **TPTS Ads API application** and its use of
Meta's Marketing API. Verified 2026-07-26 — it contains **no** mention of
cookies, website visitors, tracking, chat, SMS, or consent.

Adding a chat widget and visitor tracking to a public page collects categories of
personal data the posted policy does not disclose. That has to be fixed **before**
the widget goes live, not after.

**Required additions:**

| Section | What it must say |
|---|---|
| Information We Collect | Website visitor data — IP, device, pages viewed, referrer — and chat transcripts and contact details submitted through the widget |
| How We Use Information | Responding to inquiries, booking consultations, and marketing follow-up |
| Cookies & Tracking | Cookies and pixels used, including Meta's, and how to opt out |
| SMS / Text Messaging | Consent, message frequency, rates may apply, STOP to opt out |
| Data Sharing | Named processors — GoHighLevel, Meta. **Note:** the current policy says "we do not sell, rent, or share personal data with third parties," which is not accurate once data sits in GHL and Meta. Reword to distinguish *selling* from *processing on our behalf* |
| Your Rights | Keep, and add a deletion request path |

The "we do not share with third parties" line is the sharpest edge. It is a
specific factual claim on a live page, and a chat widget writing to GHL makes it
false the day it ships.

**This is a real change to a published legal document.** The table above is what
needs covering, not finished language — it should get a human review before it
goes up. This repo is the right place to draft it.

---

## Deploy path

Widget itself is GHL-native — configure in the location's Chat Widget settings and
enable on the Blueprint funnel page. No Code element edit required, so the
drag-and-drop builder recipe from the 7/25 codex entry is **not** needed here.

Sequence matters:

1. Update and publish the privacy policy **first**
2. Configure the widget, with the consent line at the capture step
3. Point the widget at the Sales Max KB v8 agent
4. Enable Tier 2 known-contact attribution
5. Enable on the Blueprint page only — do not roll it site-wide in the same pass

## Verification

- [ ] Privacy policy live and covering all six rows above, **before** step 2
- [ ] Widget collapsed on load; does not cover the booking calendar on mobile
- [ ] Booking CTA still the primary action in the first viewport
- [ ] Test conversation creates a GHL contact with name + phone/email
- [ ] Consent stored with a timestamp on the contact record
- [ ] Max does not quote a price and does not promise a class time
- [ ] Known-contact attribution fires on a click from a GHL email
- [ ] Confirm the widget did not push pricing onto a page whose whole design is that pricing lives in the consult
