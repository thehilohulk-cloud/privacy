# Kit Email Copy — Final Drafts for All Three Sequences (+2 triggered singles)
**Date:** 2026-07-11 · **Author:** Fable 5 (final-day session) · **Status:** COPY COMPLETE — awaiting Garrett approval batch; NOTHING staged in Kit (Zapier's Kit write-API is platform-restricted from this session; sequence content is UI-paste anyway).
**Authority:** `email-as-revenue-plan-2026-07-07.md` (Garrett-staged) + `alumni-evergreen-SPEC.md` §3 (Kit layer G7). This supersedes "skeletons" — it is finalize-ready copy.

## HARD GATES BEFORE ANY ACTIVATION (all Garrett/UI)
1. Kit from-address off gmail → verified `transformations.studio` identity. 2. TZ Eastern → Hawaii. 3. Mailing address Seattle placeholder → 474 Laukapu St, Hilo, HI 96720 (CAN-SPAM). 4. Import GHL segments to Kit tags `tpts-members`/`tpts-alumni`/`tpts-leads` (suppress `bad email` + hard bounces); members NEVER get alumni/lead sales copy. 5. `/pre-send-gate` before first live send.

## LINK PLACEHOLDERS (fill from vault — verify HTTP 200 pre-send)
`{{SCAN_LINK}}` = free 12-point scan booking link (UTM `utm_source=kit&utm_medium=email&utm_content=<id>`) · `{{OG_LINK}}` = THE canonical OG $399.99/4wk rollover link (never rebuild) · `{{V08_LINK}}`/`{{V10_LINK}}` = optional video rows post-shoot · Kit liquid `{{ subscriber.first_name | default: "there" }}` · Canva header = PNG export, never Canva HTML.

---

# SEQUENCE 1 — ALUMNI QUARTERLY `2824013` (the priority: 542 people)
Entry: `tpts-alumni`. **SMS-collision exclusion: skip/exit anyone with [ALUMNI-EVERGREEN] SMS touch < 30d (Kit tag `alumni-sms-touched` synced from GHL `alumni-outreach-<yyyymm>`).** Auto-exit on purchase. E1 → E2 at +7d to NON-OPENERS only; openers who don't book get nothing more until next quarter.

## Email 1 — story + scan (NO price)
**Subject:** The scan you never picked up · **Preview:** Your numbers are still in our system. 30 minutes, no charge, no catch.
> Aloha {{ subscriber.first_name | default: "there" }},
> Garrett here, from Transformations.
> Every week somebody walks back through our door after a year — sometimes three — and the first thing they say is some version of "sorry." A parent got sick. Work got heavy. Kids needed them. That's not falling off. That's handling your life.
> Here's what I tell every one of them, and what I want you to hear too: **your body remembers the work.** Muscle you built here comes back faster the second time — that's not a pep talk, it's physiology. And your numbers are still in our system. You wouldn't be starting over. You'd be picking up.
> So here's my open invitation, no strings on it:
> **Come do a free 12-point body scan.** Thirty minutes. You stand on the scale for sixty seconds, we look at where you actually are — muscle, body fat, the real picture — and you leave with your numbers whether we ever train together again or not. Wear slippers if you want.
> No lecture. No "where you been." First one to tease you answers to me.
> **[Book your free scan → {{SCAN_LINK}}]**
> Good to see your name again.
> — Garrett · Transformations · Hilo, Hawai'i

*(OPTIONAL once shot: "I made a short video about exactly this — {{V10_LINK}}")*

## Email 2 — the 4-week reset (+7d, non-openers only; the ONLY priced email)
**Subject:** The 4-week reset, if you're ready · **Preview:** One block. Your old numbers as the starting line. Same coach.
> Aloha {{ subscriber.first_name | default: "there" }},
> I'll keep this one short and straight.
> If you've been thinking about coming back but "someday" keeps moving, here's the smallest real step that exists: **one 4-week block. $399.99.** Same coaching, the scans, and Titus — our coach in your phone who keeps your macros and answers at 9pm — included. Payment plans through Klarna work at checkout if that spreads it better.
> Four weeks is long enough to feel like yourself again and short enough to say yes to. Alumni almost always surprise themselves in the first block — the strength comes back before the scale moves, and the scan proves it.
> **[Start your 4-week reset → {{OG_LINK}}]**
> Or, if you'd rather look before you leap: the free scan invitation from my last email stands. {{SCAN_LINK}}
> Either way — the door never closed.
> — Garrett · Transformations · Hilo, Hawai'i

---

# SEQUENCE 2 — MEMBER MONTHLY `2824014` (retention; value only, NEVER sales — the 6.01 failure mode)
Shape (reusable): one idea → one action → one open door. Month 1 below (Garrett's staged Draft #1, polished):
**Subject:** The 10-minute rule that beats a perfect workout you skip · **Preview:** Consistency math, one plate swap, and this week's studio note.
> Aloha {{ subscriber.first_name | default: "there" }},
> Quick one this month.
> The members who get the scan results they want aren't the ones with perfect workouts — they're the ones who show up when it's inconvenient. A 10-minute session you actually do beats a 60-minute one you skip. That's not a motivational quote; it's just the math of adaptation.
> **This month's one thing:** swap one refined-carb side (white rice, bread) for a fist of protein or veg at your biggest meal. One swap, every day. That's it. (Not sure what fits your numbers? Text Titus — (808) 515-8086 — he keeps your macros so you don't have to.)
> **Studio note:** [ROTATING SLOT — Garrett fills monthly: schedule changes / a member win with permission / education corner / supplement note. One item only.]
> Reply to this email if you want me to look at where your last body scan landed — happy to walk you through the numbers before your next one.
> — Garrett · Transformations · Hilo, Hawai'i

*(Month 2+ topics: protein at breakfast · the sleep-and-scale story · walking after dinner · plateau-is-data reframe [perimenopause-aware]. Never two ideas in one email.)*

---

# SEQUENCE 3 — LEAD NURTURE 7-DAY `2824015` (wraps the consult; complements the SMS drip; auto-exit on consult completed or `paid – active member`)

## Email 1 (Day 0, on booking) — what actually happens
**Subject:** What actually happens at your consult (nothing to prepare) · **Preview:** 30 minutes. 12 numbers. A straight answer. Slippers are fine.
> Aloha {{ subscriber.first_name | default: "there" }},
> You're booked — good. Now let me kill the mystery, because not knowing what to expect is the number-one reason people no-show, and you're not going to be one of them.
> Here's the whole thing, start to finish:
> **You walk in, I meet you at the door.** I'm Garrett — it's my studio. No sales guy, no tour-and-pitch. Just us at a table, talking story.
> **First, the FitIndex scan.** You stand on a scale for about sixty seconds, shoes and socks off — so wear whatever's easy. It gives us twelve numbers: muscle, body fat, water, the real picture. Not to judge you. It's a starting line, and it's yours to keep whether we ever work together or not.
> **Then we talk.** What you've tried, what your weeks look like, what you actually want. I'll tell you honestly what I'd do — and honestly if I'm not the right fit.
> No workout. Don't dress up. Nothing to study. Nobody here does pressure — the aunties would hear about it.
> See you soon — I'll be the one holding the door.
> — Garrett · Transformations · Hilo, Hawai'i

*(OPTIONAL once shot: 90-second video version — {{V08_LINK}})*

## Email 2 (Day 2 / T-2) — make your scan accurate
**Subject:** One minute of prep makes your scan numbers real · **Preview:** When to weigh, what to skip, and why the scale lies without this.
> Aloha {{ subscriber.first_name | default: "there" }},
> Your scan takes sixty seconds — but a little prep makes the numbers worth keeping. Body-composition scales read water as much as anything, so:
> • **Come consistent:** if you can, don't eat a big meal or train hard in the 2 hours before. • **Hydrate normally** that day — don't chug, don't fast the water. • **Bare feet** on the scale (that's how it reads), so easy footwear. • If it's morning, great. If not — no stress. We mark the time and compare like-to-like next time. **The trend is the truth, not any single reading.**
> That last line, by the way, is half of what we do here: most people quit plans that were working because they watched one number on one day. Twelve numbers over time don't lie.
> Your consult's on the calendar — nothing else to do.
> — Garrett · Transformations · Hilo, Hawai'i

## Email 3 (Day 5 / T-1) — proof, not promises
**Subject:** She'd "tried everything" too · **Preview:** What twenty years of scans actually show.
> Aloha {{ subscriber.first_name | default: "there" }},
> Almost every consult starts the same way: "Garrett, I've tried everything. Nothing works after 40."
> And they're half right. The stuff that worked at 28 — starving all week, pounding cardio, hoping — really does stop working. The method has to change with your body.
> What I've watched work for twenty years, for hundreds of women here in Hilo: lifting two or three times a week, eating enough protein (usually MORE food than you think), and measuring the right things. Not just the scale — muscle, body fat, twelve numbers. [SLOT: one named member story w/ written permission — Candice pattern. Until then:] The women training here started exactly where you are; some started with a walk and one dumbbell. That's not the beginner version of the program — that IS the program, scaled to day one.
> You haven't tried everything. You've tried one thing — eat less, move more — about eleven different ways. The consult is where you see the other thing.
> If your consult's still on the calendar: see you there. If life moved it, one tap fixes that: {{SCAN_LINK}}
> — Garrett · Transformations · Hilo, Hawai'i

---

# TRIGGERED SINGLES
## Rollover — trigger: program end within 14d (pairs w/ WF-Convert)
**Subject:** Your next block — let's lock it before your spot does
> Aloha {{ subscriber.first_name | default: "there" }},
> Your current block wraps in about two weeks. The scan tells the story better than I can — you've built something. The only way to keep momentum cheap is to not lose it.
> Same schedule, same coach, no restart: **[Lock your next block → {{OG_LINK}}]** (Klarna at checkout if that helps.)
> Rather talk it through first? Reply here or grab me after any session. Deciding on the spot is not a thing we do.
> — Garrett

## Birthday — trigger: birthday CF
**Subject:** Happy birthday from the studio 🎂
> Aloha {{ subscriber.first_name | default: "there" }},
> Happy birthday from all of us at Transformations. No pitch today — just this: **a free 12-point body scan, on us, any time this month.** Thirty minutes, your numbers, yours to keep. {{SCAN_LINK}}
> Go eat the cake. (Titus says it fits.)
> — Garrett

---

# NEXT STEPS
1. Garrett approval batch (tone, OPTIONAL video rows, member-story slot, ramp plan). 2. Laptop/UI: gates 1–3 → tag imports → paste into sequences `2824013/14/15` → wire exclusion tags + auto-exits → `/pre-send-gate`. 3. **First live send = Alumni Email 1 only, ~50-person tranche** (fresh-domain deliverability ramp); full 542 after one clean tranche. Replies land in Triage's alumni lane.
