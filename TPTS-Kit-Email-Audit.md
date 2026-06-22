# TPTS Kit (ConvertKit) Email Setup Audit

**Prepared for:** Garrett Hall — Transformations Personal Training Studio (TPTS), Hilo, HI
**Date:** 2026-06-22
**Auditor scope:** Kit (ConvertKit) configuration & deliverability posture, for building an email marketing/automation system.

> **Sources & confidence:** Findings are cross-verified from (1) the TPTS Operations Notebook in Google Drive (entry dated **6/18/2026**, "KIT ESP + …") and (2) Kit's own account emails in Garrett's Gmail (`help@kit.com` / `help@convertkit.com`). Items that require the live Kit dashboard and could **not** be confirmed in this session (no Kit account/API access available here) are flagged **"Unable to verify — requires direct Kit account access."**

---

## TL;DR

Kit is **brand-new** — the account was created and paid for on **June 18, 2026** (Creator plan). It is essentially an **empty, freshly-provisioned account**: a handful of subscribers, **no segments/tags, no automations, no broadcasts sent**, and **the sending domain has not been authenticated in Kit**. Kit and GHL currently operate as **two completely separate systems**. Before any real send, two compliance/deliverability gaps must be closed: the **mailing address is still the Seattle placeholder** and the **timezone is still Eastern**, and the **sending domain is not yet DKIM/SPF-authenticated inside Kit**.

A key clarification up front: TPTS runs **two domains**, and they do different jobs.
- **transformationshawaii.com** — the public Wix marketing website.
- **transformations.studio** — the email/CRM sending domain. Transactional/lifecycle email runs through **GoHighLevel (GHL) + Mailgun** on the subdomain **`mail.transformations.studio`** (this is the domain that is SPF/DKIM/DMARC-authenticated — but for *GHL/Mailgun*, **not** for Kit).

---

## 1. Sending Domain Authentication

| Question | Finding |
|---|---|
| Is the TPTS sending domain authenticated in Kit (SPF + DKIM)? | **No — strong evidence it is NOT.** The 6/18 setup notebook entry records the Kit account being created, paid (Creator), and connected via OAuth, but lists the only open setup items as the mailing address and timezone — **no domain-authentication step was performed in Kit.** Kit is therefore almost certainly still sending from **Kit's shared/default sending domain**, not an authenticated TPTS domain. *(In-app confirmation: Unable to verify — requires direct Kit account access → Settings → Email → "Sending domain.")* |
| Or is Kit on a shared/default Kit subdomain? | **Yes — that is the current state.** A new Creator account sends from Kit's shared infrastructure until you explicitly add and verify a custom sending domain. |
| Current DMARC policy status? | The authenticated TPTS email domain `mail.transformations.studio` is at **`p=none`** (documented 5/28/2026), with a **planned ramp to `p=quarantine`** (workflow/tag `tpts-dmarc-ramp-quarantine`, targeted ~6/16). **Important:** this DMARC record governs **GHL/Mailgun sends**, not Kit. **Unable to verify the live, current DNS record in this session** (public DNS-over-HTTPS resolvers blocked the lookup). |

**What this means / action for Garrett:**
- In Kit → **Settings → Email → Sending domain**, add and verify a TPTS domain (e.g. a dedicated subdomain like `kit.transformations.studio` or `email.transformations.studio`) so Kit signs with **your** DKIM, not Kit's shared key. Use a *separate* subdomain from `mail.transformations.studio` so Kit's reputation and GHL/Mailgun's reputation don't contaminate each other.
- Because the org is moving `transformations.studio` toward **DMARC `p=quarantine`**, an **unauthenticated Kit send using a `@transformations.studio` From address will fail DMARC alignment and risk landing in spam/quarantine.** Authenticate in Kit *before* the policy tightens, or send from the authenticated subdomain only.
- **Manual check:** Kit Settings → Email → confirm "Sending domain" shows a verified TPTS domain with green DKIM/SPF/Return-Path status (not "kit.com" / shared).

---

## 2. List Status

| Question | Finding |
|---|---|
| Total subscribers in Kit? | **Very small — single digits.** The account is only days old (created 6/18). Kit's weekly digest email ("Your week with Kit," 12–19 June) reports **+3 subscribes, 0 unsubscribes, net +3** for the account named **"Transformations Personal Training Studio."** No prior list was imported per the notebook. **Exact live total: Unable to verify — requires direct Kit account access** (Dashboard → Subscribers). |
| Existing segments or tags? | **None found.** No tags/segments are referenced in the setup notes, and Kit's onboarding emails are still prompting Garrett to "create your first form/landing page/broadcast" — indicating an unconfigured account. *(Manual confirm: Kit → Subscribers → Tags / Segments.)* |
| List growth rate / source? | **Negligible so far (~3 in the first week).** No forms or landing pages are live in Kit yet, so there is **no active acquisition source feeding Kit.** TPTS's real lead flow currently lands in **GHL** (website chat via Assistable/Max, booking calendars, Meta ads), not Kit. |

**Action for Garrett:** Decide what populates Kit. Today, leads and members live in **GHL**; Kit has almost no one in it. You'll need either a one-time export/import from GHL or an ongoing sync (see §4) to make Kit useful for marketing.

---

## 3. Deliverability Health

| Question | Finding |
|---|---|
| Spam complaint rate in Kit? | **Unable to verify — requires direct Kit account access.** With ~3 subscribers and **no broadcasts sent**, there is effectively no complaint data yet. (Kit surfaces this under Dashboard / per-broadcast reports once you send.) |
| Has Kit flagged auth/deliverability issues? | **No issue flags observed**, but note the account has **not been domain-authenticated** (see §1) and Kit's automated emails are still onboarding prompts, not warnings. The two real "issues" are configuration gaps, not Kit alerts: **(a)** unauthenticated sending domain, **(b)** placeholder mailing address (CAN-SPAM requires a valid physical address in the footer) and wrong timezone. |
| Bounce rate metrics? | **Unable to verify — requires direct Kit account access.** No sends → no bounce data in Kit. |

**Context:** The deliverability work already done in the notebook (open-rate recovery from 18.63%→benchmark, Google Postmaster Tools, dedicated-domain warming) all applies to the **GHL/Mailgun** pipeline on `mail.transformations.studio` — **none of that reputation transfers to Kit.** Kit starts cold on its own shared IP and will need its own warm-up.

---

## 4. Integration Status

| Question | Finding |
|---|---|
| Is Kit connected to GHL? | **No native integration. They operate as separate systems.** GHL remains the single source of truth (members, billing/Stripe, tags, custom fields, AI agents, transactional + lifecycle email via Mailgun). Kit was adopted **only** as a dedicated marketing-email ESP. The only Kit "integration" today is a **Kit MCP connected to Claude Code via OAuth** (`app.kit.com/mcp`) for AI-assisted drafting — and that connection **can only create *draft* broadcasts**, not send. |
| Automations/workflows/scheduled sends already in Kit? | **None.** No sequences, visual automations, or scheduled broadcasts exist yet. (All existing TPTS automation lives in **n8n + GHL** — e.g. WF-A/WF-B alumni flows, WF-OG poller, Della scheduling — none of it touches Kit.) |

**Action for Garrett:** If Kit is to receive GHL contacts automatically, build a bridge. Options available in this stack: **Zapier** or **Make.com** (both connected) can sync GHL tags/contacts → Kit tags/sequences. Decide the system of record per contact to avoid double-emailing (GHL lifecycle vs. Kit marketing).

---

## 5. Sending Capabilities

| Question | Finding |
|---|---|
| What automation/workflow features does Kit support? | Kit (Creator plan) supports: **Broadcasts** (one-off newsletters), **Sequences** (drip/welcome series), **Visual Automations** (trigger → action workflows: tag added, form subscribed, link clicked, etc.), **Forms & Landing Pages**, **Tags & Segments**, and **Creator Network / Recommendations** for list growth. It does **not** do true e-commerce "abandoned cart" the way Shopify/GHL does — Kit Commerce covers selling digital products/paid newsletters, not gym membership carts. Cart/booking-abandon logic for TPTS belongs in **GHL**. |
| Dedicated IP available, or shared? | **Shared IP.** The account is on the **Creator** plan; a dedicated IP is **not offered at the Creator tier** (it's a higher-tier / high-volume option and only makes sense at much larger send volumes than TPTS has). For TPTS's list size, **shared IP is correct** — a dedicated IP with a tiny list would actually *hurt* deliverability. |

---

## 6. Prestige Labs / Commerce Hooks

| Question | Finding |
|---|---|
| Existing Kit links to Prestige Labs referral URLs / product-promo automations? | **None in Kit.** The TPTS Prestige Labs referral link — **`https://refer.prestigelabs.com/?af=z9ygock3`** — is the documented standard for supplement content, and there is a **"Prestige Labs Monthly" promo automation, but it runs as SMS via n8n/GHL, not Kit.** Prestige Labs also emails ready-made promo kits to Garrett (`campaigns@prestigelabs.com`). **No Prestige Labs link or product-promotion automation exists inside Kit yet** — this is greenfield. |

**Action for Garrett:** When building supplement/upsell broadcasts in Kit, standardize on the referral link above and consider a Kit sequence that mirrors the existing monthly Prestige cadence (currently SMS-only).

---

## Priority Fix List (before first real Kit send)

1. **Authenticate a TPTS sending subdomain in Kit** (DKIM/SPF/Return-Path) — use a subdomain *separate* from `mail.transformations.studio`. *(Blocks DMARC alignment risk as `transformations.studio` ramps to `p=quarantine`.)*
2. **Fix the mailing address** — currently the **Seattle placeholder**; set to **474 Laukapu St, Hilo, HI 96720** (CAN-SPAM requirement).
3. **Fix the timezone** — currently **Eastern**; set to **Hawaii (GMT-10)** so scheduled sends fire at the right local time.
4. **Decide the GHL→Kit contact bridge** (Zapier/Make) and which system owns which message type, to avoid double-emailing members.
5. **Warm up Kit's shared-IP reputation** with small, engaged sends before any large blast.

## Items requiring direct Kit dashboard access to confirm
- Exact total subscriber count, and any imported lists.
- Live spam-complaint and bounce rates (only meaningful after sends begin).
- Confirmation of sending-domain authentication status (Settings → Email).
- Any tags/segments not surfaced in the setup notes.
