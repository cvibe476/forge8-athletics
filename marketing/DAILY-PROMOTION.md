# Forge8 — Daily Promotion Playbook
Generated 12 Nov 2026. Everything here is grounded in facts read off the live site
and the Google Business Profile on that date. **Nothing here has been posted.**
You post it, or tell me to.

---

## 0. Read this first — the biggest exposure problem is a stuck merge

**The live site has no blog.** Verified on 12 Nov 2026:

| | Live site (`main`) | Branch (`seo/high-roi-fixes`) |
|---|---|---|
| Blog posts | **0** | **93** |
| Hyrox page | 404 | exists |
| `/links/` | 404 | exists |
| robots.txt | 404 | exists |
| URLs in sitemap | 10 | 105 |

`https://forge8athletics.com/pages/blog.html` loads and shows a heading — and
**zero posts**. The 93 posts, the Hyrox landing page, the robots.txt and the
expanded sitemap all sit on branch `seo/high-roi-fixes`, which is **11 commits
ahead of `origin/main` and 0 behind**. It is a clean fast-forward. It has been
open as PR #1 since 30 Oct 2026.

No amount of daily posting fixes this. You have 93 pages of content that Google
has never seen, and one merge turns them on.

**What is needed:** the `xfitforge8` account has no push access to
`cvibe476/forge8-athletics` (the repo that serves the live site). Either that
account is granted write access (then it's one merge), or whoever owns
`cvibe476` merges PR #1. **This is the single highest-value action available.**

Until it merges, do not promote blog URLs — they will 404. Every post below
points only at pages confirmed live today.

---

## 1. The review gap

| | Forge8 | CrossFit 1904 | Fitness4ward | The Strength Tank | Performance360 | CrossFit ATR |
|---|---|---|---|---|---|---|
| Google reviews | **10** | 57 | 83 | 84 | 137 | 286 |

Those four competitors came off the same Maps result page as Forge8 on 12 Nov
2026. Every one outranks Forge8 on review count by 6x to 29x.

**Why this is the whole game:** Google ranks local gyms largely on review volume
and recency. Forge8 has a **5.0 rating** and **2,215 profile views last month** —
people are already finding it. It has 10 reviews, and **zero new ones in the last
8 weeks**. The gym is not short on traffic. It is short on proof.

Two reviews a week takes Forge8 past 1904 inside four months. That is the single
highest-leverage thing on this page.

---

## 1. The review engine (do this first)

### The link
```
https://maps.google.com/?cid=6062255210617642062
```
Verified 12 Nov 2026 — resolves to the *Crossfit Forge8 Athletics* profile at
7550 Miramar Rd #630. Use this exact link. The old
`search.google.com/local/writereview?placeid=...` format returns **404** now;
it has been retired.

A QR code for it is at `images/review-qr.svg` on the site, and the scan target
was decoded back to that exact URL to confirm it works.

### The page
`pages/leave-a-review.html` → https://forge8athletics.com/pages/leave-a-review.html
Linked in the footer of every page and in the homepage footer.

### The ask (send by text, 1:1, the day after a good class)

> Hey [name] — glad you made it in today. Quick favor if you have 30 seconds:
> would you drop a line on Google about the gym? It genuinely helps people in
> Miramar find us. Here's the direct link, it opens the review box straight up:
> https://maps.google.com/?cid=6062255210617642062
> No pressure either way — see you [next class day].

**Send it one at a time, to people who actually train.** A batch blast gets
ignored and can look like review farming. Personal and specific works.

### Reply to every review within 48 hours
Replies are public and they are read by prospects more than the review. All 10
current reviews already have owner replies — keep that up. Fresh replies on old
reviews also signal an active business.

---

## 2. Google Business Profile posts — 8 weeks of copy

GBP posts show under your listing in Maps and Search. They expire after ~7 days,
so one a week is the minimum cadence. Post from
`business.google.com` → Posts. Add a photo every time; text-only posts
underperform badly.

Character limit is 1,500. All of these are well under.

---

### Week 1 — the 5 AM class reaches people before work does

**Post:**
> 5:00 AM is our quietest, fastest class. You're in, coached, and out before
> most of Miramar is on the road.
>
> Six classes every weekday: 5:00, 6:15, 12:00, 3:30, 4:45, 6:00. Saturday at
> 8:00 and 9:15. Every session is coach-led and scaled to you — first class or
> fifth year, same room.
>
> 7550 Miramar Road, Unit #630.
>
> **Button:** Sign up · free-trial page

---

### Week 2 — Hyrox training is inside your week, not added to it

**Post:**
> Training for a Hyrox doesn't have to mean a second gym membership and a
> separate running plan.
>
> Thursday classes at Forge8 blend CrossFit with Hyrox-specific work — sled,
> sandbag, wall balls, erg — so race prep happens inside your normal week. We're
> a CrossFit and Hyrox Affiliate.
>
> Eight stations, eight 1,000m runs. Come learn what the race actually asks of
> you before you sign up for one.
>
> **Button:** Learn more · membership page
> *(Do not link the Hyrox page yet — it 404s live. Use the membership page until PR #1 merges.)*

---

### Week 3 — three classes, seven days, no card

**Post:**
> New here? Take three coach-led classes in seven days, on us. No card, no
> contract, no sales call.
>
> Show up ten minutes early in athletic clothes and flat-soled shoes. We handle
> the rest, and the coach scales every workout to where you actually are.
>
> All levels. Every session.
>
> **Button:** Sign up · free-trial page

---

### Week 4 — 24-hour open gym is not a gimmick

**Post:**
> Your shift ends at 11 PM. Or starts at 4 AM. Either way, the gym is open.
>
> Unlimited members get 24-hour access to the full floor — every rack, every
> erg, the rig, all of it. The building is secured, well-lit and camera-monitored
> around the clock.
>
> Train before the 5 AM class, after the 6 PM, or at 2 AM when the gym is
> genuinely empty.
>
> **Button:** Learn more · membership page

---

### Week 5 — the coaches, by name

**Post:**
> Who's actually coaching you matters more than the equipment.
>
> Michael Martin — CF-L2, USAW, 20+ year Army veteran, BS Kinesiology.
> Angeline "Gigi" Redman — CF-L2, USAW-L1, movement quality and lifting
> fundamentals.
> Suellen Goncalves — CF-L1, ACE trainer, BS Psychology.
> Megan Toronto — CF-L1, pregnancy and postpartum athleticism, 2023 NAW
> semifinalist.
>
> Four coaches, four different backgrounds, one floor.
>
> **Button:** Learn more · coaches page

---

### Week 6 — drop in, no membership required

**Post:**
> In town for work or visiting from another box? Drop-ins are always welcome —
> $30 for a coach-led class, all levels.
>
> Just show up ten minutes before class. No forms to chase, no membership to
> sign. We'll get you set up and scaling.
>
> Weekdays 5:00 AM through 6:00 PM, Saturday 8:00 and 9:15.
>
> **Button:** Book · membership page

---

### Week 7 — what a first class actually looks like

**Post:**
> People put off walking in because they think they need to get fit first.
>
> A first class is this: you arrive ten minutes early, a coach walks you through
> the warm-up and the movements, and then you do the workout at a weight and
> pace that's right for you — alongside people doing the same one at theirs.
>
> Nobody is watching you struggle. Everybody started somewhere.
>
> **Button:** Sign up · free-trial page

---

### Week 8 — Saturday mornings in Miramar

**Post:**
> Saturday is 8:00 and 9:15. Two classes, then the rest of your weekend is
> yours.
>
> It's the busiest, loudest session of the week and the easiest one to bring a
> friend to. Free trial covers it.
>
> 7550 Miramar Road, Unit #630.
>
> **Button:** Sign up · free-trial page

---

### Evergreen rotation
After week 8, cycle back. Change the photo, change the opening line, keep the
facts the same. The facts are: 6 weekday classes, 2 Saturday, 24-hour open gym
for unlimited, $30 drop-in, $199/month, 3-class free trial, CrossFit + Hyrox
Affiliate, 4 coaches, Unit #630.

---

## 3. The #410 problem — still in the wild

The Google profile is correct at **Unit #630**. Several third-party listings are
not. These actively cost you: someone reads "#410", drives to the wrong suite,
and you never hear about it.

Confirmed wrong on 12 Nov 2026:
- **CrossFit.com** affiliate directory — shows Suite #410
- **Yelp** (mobile) — shows #410
- **WellnessLiving** — shows #410

Google Search snippets are also stale for pages that are *correct* at #630 —
that clears itself once Google recrawls, but the three above are edited by hand.

**Fix:** claim/edit each listing to 7550 Miramar Road, **Unit #630**, San Diego,
CA 92126. This is a data correction, not marketing — but it is worth more than a
month of posts, because it stops sending paying customers to the wrong door.

---

## 4. The duplicate profile

`business.google.com/locations` shows two entries:

| Store code | Name | Address | Status |
|---|---|---|---|
| 10277784865135682230 | Crossfit Forge8 Athletics | #630 | **Verified** |
| 00761723296043914585 | Forge8 Athletics | #410 | **Duplicate** |

The public Maps listing is clean — one result, correct address, so the duplicate
is already suppressed and is **not** currently costing you visibility. Leave it
alone. Do **not** delete or merge it without checking first: the review history
is attached to the verified record, and a bad merge can take reviews with it.
This is cleanup, not a fire.

---

## 5. The Ads budget — a real decision, not a task

Your Google Ads account is showing this message:

> **"Your ads stopped running on your busiest days. Fixing your limited budget
> can help."**

The campaign is `SanDiego_Crossfit_Nonbrand_Prospecting_nonbrand`. Recommended:
+10.8% budget, dynamic image extensions, sitelinks.

Translated: you are paying to be eligible for ads, and then getting switched off
on the days demand actually peaks. Either raise the budget or pause it — running
throttled is the worst of both. **This costs money, so it's your call, not mine.**

---

## 6. What I have not done, and why

I have not posted anything to your Google profile, Instagram or Facebook. Those
are public statements in your business's name and they go out under your brand —
you should see them before they're live. The copy above is ready; say the word on
any of it and I'll walk it through.

I also have not touched the #410 duplicate or the Ads budget, for the reasons
above.
