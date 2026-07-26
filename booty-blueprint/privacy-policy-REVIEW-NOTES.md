# Privacy Policy Draft — Review Notes

**Draft:** `privacy-policy-DRAFT-2026-07-26.html`
**Replaces:** `/index.html` (the live policy) once approved
**Status:** Needs a human read before publishing. Not legal advice.

---

## What changed and why

| Change | Reason |
|---|---|
| Scope broadened from the Ads API app to the website, chat, and ads | The old policy described only the Meta Ads API app. A chat widget and visitor tracking collect data it never disclosed |
| **"We do not sell, rent, or share personal data with third parties" → "We do not sell or rent," plus a named-processor list** | This was the sharpest problem. The original sentence goes false the moment a widget writes to GoHighLevel. The fix separates *selling* (still true, still stated plainly) from *processing on our behalf* (true, now disclosed) |
| Added: information you provide, collected automatically, cookies/pixels, SMS, retention, children's privacy, third-party links | Categories the widget and page tracking create |
| Added phone number and ZIP to Contact | Contact completeness |
| **Kept the Meta Ads API section verbatim**, as "Advertising Data" | It likely supports a Meta app review. Dropping it could break something that currently passes |

## Deliberate choices worth a second opinion

**Chat disclosed as automated.** The draft says the chat "is assisted by an automated system" and that staff may review conversations. Disclosing an AI agent is the defensible position and costs nothing.

**"Please do not send health or medical information through the chat."** Consistent with the standing no-medical-claims rule, and it keeps sensitive health data out of the CRM, which is a category nobody wants to be storing.

**Adults-only stated explicitly.** Matches the KB's adults-only policy and closes the under-18 question cleanly.

**SMS section written to the standard carrier pattern** — frequency varies, rates may apply, STOP and HELP. Carriers and messaging platforms generally expect these elements to appear in a linked policy.

## Open items — confirm before publishing

1. **Analytics.** The draft refers to analytics providers generically. If Google Analytics is running, name it. If nothing but the Meta pixel is in use, that sentence can be tightened.
2. **Email address.** The policy points at `runheather808@gmail.com`. Confirm that is the right destination for deletion and access requests, or swap to a studio address.
3. **Retention periods.** Written as purpose-based rather than a fixed number of days, which is defensible and honest. If a specific period is preferred, it needs to be one that is actually enforced.
4. **State privacy laws.** The draft includes a general additional-rights paragraph. Ads reach beyond Hawaii and the KB acknowledges off-island leads, so if there is meaningful California traffic, a CCPA-specific section may be warranted. Worth a lawyer's read on this point specifically.
5. **Payments.** Not covered, because checkout happens in person after the consult. If Klarna or Affirm applications are ever initiated online, a payment section becomes necessary.
6. **The privacy URL.** Confirm whether the Meta app review points at this exact page, and that broadening its scope does not disturb that review.

## Publishing

The draft is deliberately **not** written over `index.html`. This branch is a review surface for the Booty Blueprint campaign work and is not intended to merge; a change to a published legal document should land through its own clean PR.

When approved:

```
git checkout -b claude/privacy-policy-update origin/main
cp booty-blueprint/privacy-policy-DRAFT-2026-07-26.html index.html
# remove the DRAFT comment block at the top of the file
```

Then open a PR against `main` on its own. **Publish the policy before the Max widget goes live**, not after.
