# ENVIRGREEN — Product & Technical Blueprint
### Part 2 of 5: Sitemap, User Journeys, UX Architecture, UI Design System & Wireframes

> Part 2 of 5. See `00-strategy-and-roadmap.md` for strategy, `02-core-platform-systems.md` for feature systems, `03-technical-architecture.md` for engineering, `04-content-and-samples.md` for sample copy.

---

## 1. Complete Sitemap

```
/                              Home
/about/                        About Envirgreen
/about/mission/                Our Mission
/about/team/                   Our Team
/about/work/                   Our Work
/campaigns/                    Campaign list
/campaigns/<slug>/             Campaign detail
/issues/                       Public issue map/list
/issues/<slug>/                Issue detail (status timeline)
/issues/report/                Report an issue (form)
/community/                    Community feed
/community/<username>/         User profile
/events/                       Event list
/events/<slug>/                Event detail
/volunteer/                    Volunteer landing + registration
/volunteer/dashboard/          Volunteer dashboard (auth)
/donate/                       Donation landing
/donate/<campaign-slug>/       Campaign-specific donation
/impact/                       Public impact dashboard
/impact/transparency/          Transparency & methodology page
/trees/                        Tree plantation hub + map
/trees/plant/                  Log a tree planting
/stories/                      Story/case-study hub
/gallery/                      Media gallery
/videos/                       Envirgreen TV
/blog/                         Blog / knowledge center
/blog/<slug>/                  Blog post
/civic-sense/                  Civic Sense Learning Center
/civic-sense/challenges/       Civic Challenges
/partner/                      Partnership / CSR intake
/certificates/verify/<code>/   Certificate verification
/contact/                      Contact
/faq/                          FAQ
/take-action/                  "What can I do?" wizard (modal/page)
/privacy/  /terms/  /guidelines/   Legal & community guidelines

Auth: /login/ /signup/ /logout/ /accounts/password-reset/
Internal (role-gated): /admin/ (Django admin) + /dashboard/ (custom ops dashboard for team roles)
```

URL rules: lowercase, hyphenated, slug-based, no query-string-dependent canonical content (see SEO section in file 3).

---

## 2. Core User Journeys

**Journey 1 — Volunteer signup**
Visitor lands on `/volunteer/` → sees current campaigns needing people → fills registration (skills, availability, city) → confirmation email → appears in Volunteer Manager's queue → gets matched to nearest active campaign → dashboard shows "your next activity."

**Journey 2 — Report an issue**
Visitor taps **Report an Issue** → category + photo + location (map pin or GPS) + severity → submits → sees "Pending Verification" status immediately → receives status-change notifications as it moves through the pipeline → can share the issue page to pressure-test community support.

**Journey 3 — Campaign → event → certificate**
User finds a campaign → joins → gets added to the linked event → checks in at the event (admin/organizer marks attendance) → post-event, "Action Taken" evidence uploaded → user's profile updates automatically → certificate auto-generated with QR verification.

**Journey 4 — Donate**
User opens a campaign → sees "Where your contribution goes" breakdown → selects amount + category → pays via gateway → receipt emailed → appears in personal donation history (never on a public leaderboard by amount).

**Journey 5 — Post → moderation → feed**
User creates a post (e.g., Achievement: "Planted 20 trees") → attached photo run through moderation queue → approved → appears in community feed ranked by the non-outrage algorithm (see file `02-core-platform-systems.md`) → others react with meaningful appreciation icons, not generic likes.

**Journey 6 — Plant a tree → verified impact**
User logs a tree planting with photo + species + location → status starts at "Planted" → admin or partner org verifies → periodic "Growing" check-ins (optional photo) → "Survived" status after a defined window → counts toward Action Score only once verified.

---

## 3. UX Architecture Principles

The entire IA is built around the loop from the master brief:
**SEE → REPORT → VERIFY → MOBILIZE → ACT → DOCUMENT → VERIFY RESULT → SHARE → INSPIRE → REPEAT**

Practical consequences for navigation:
- The primary nav always has **one unmissable action-oriented button** ("Take Action") — never buried in a hamburger menu.
- Every content page (issue, campaign, tree) ends with a **"what can I do about this right now"** block, not just a "read more."
- Status/timeline components are reused everywhere (issue pipeline, tree lifecycle, campaign progress) so users learn the pattern once.
- Public pages (impact, campaigns, issues) are indexable and fast; authenticated dashboards are separated behind `/dashboard/` and `/volunteer/dashboard/` so SEO crawl budget isn't wasted on private views.

---

## 4. UI Design System

### Color tokens
```
--envirgreen-deep:     #0B6B3A   /* primary brand, headers, primary buttons */
--envirgreen-fresh:    #35A853   /* active states, progress, links */
--envirgreen-leaf:     #66BB6A   /* secondary accents, tags, badges */
--envirgreen-earth:    #795548   /* civic/waste-category accents, "Earth" pillar */
--envirgreen-dark:     #10231A   /* body text on light backgrounds */
--envirgreen-bg:       #F7FAF7   /* page background */
--envirgreen-white:    #FFFFFF   /* cards, surfaces */
```
Rule of thumb: green is the *identity*, not the *wallpaper*. Cards default to white/neutral background; green is reserved for CTAs, progress fills, active nav states, and icons — roughly 10–15% of any given screen's surface area.

### Typography
- **Headings:** Manrope or Plus Jakarta Sans, bold, tight letter-spacing.
- **Body:** Inter, 16px base, 1.6 line-height for readability on long-form content (stories, blog).
- **Scale:** 12 / 14 / 16 / 20 / 28 / 40 / 56px, using a 1.25–1.333 modular ratio.

### Core components (build once, reuse everywhere)
- **Status Pipeline bar** — horizontal stepper (mobile: vertical), used for issues and tree lifecycle.
- **Progress ring/bar** — campaign goal progress ("4/10 drives completed").
- **Before/After slider** — draggable divider, two images, "Real Action. Visible Change." caption.
- **Impact stat card** — icon + number + label, used across dashboard, homepage counters, profile stats.
- **Appreciation bar** — row of reaction icons (🌱🧹🌳💚👏) with counts, replacing a single "like."
- **Verification badge** — small pill (Community Member / Verified Volunteer / Campaign Volunteer / Envirgreen Team / Partner Org), consistent colors per tier.

### Motion
Scroll-reveal on section entry, counter count-up on the impact dashboard, card elevation on hover, timeline step animation on issue pages. No parallax, no autoplay video with sound, respects `prefers-reduced-motion`.

---

## 5. Homepage Wireframe (section by section)

```
┌─────────────────────────────────────────────┐
│ NAV: Logo | Campaigns | Community | Impact   │
│      | Volunteer | [Take Action ▸ button]    │
├─────────────────────────────────────────────┤
│ HERO                                         │
│ Real photo/video: volunteers + clean street  │
│ H1: "Let's Make Our Surroundings             │
│      Clean, Green & Responsible."            │
│ Sub: Envirgreen brings people together...    │
│ [Join Envirgreen]  [Take Action]             │
│ (tertiary link: Report an Issue)             │
├─────────────────────────────────────────────┤
│ LIVE IMPACT COUNTER (DB-driven, count-up)    │
│ Trees Planted | Kg Waste Collected |         │
│ Cleanup Drives | Volunteers | Issues Resolved│
├─────────────────────────────────────────────┤
│ WHY ENVIRGREEN — 3 pillars                   │
│ Clean · Green · Responsible (icon + 1 line)  │
├─────────────────────────────────────────────┤
│ THREE CORE ACTIONS (big tappable cards)      │
│ REPORT · JOIN · CREATE IMPACT                │
├─────────────────────────────────────────────┤
│ ACTIVE CAMPAIGNS (horizontal scroll cards)   │
│ image / title / location / progress /        │
│ volunteers / days left / [Join Campaign]     │
├─────────────────────────────────────────────┤
│ BEFORE / AFTER SLIDER (feature transformation)│
├─────────────────────────────────────────────┤
│ COMMUNITY HIGHLIGHTS (3–4 recent verified     │
│ posts/achievements, not a full feed)         │
├─────────────────────────────────────────────┤
│ IMPACT MAP preview (static image → link to    │
│ full interactive map)                        │
├─────────────────────────────────────────────┤
│ STORIES (1 featured before/action/after story)│
├─────────────────────────────────────────────┤
│ PARTNER / CSR strip (logos, if any real ones) │
├─────────────────────────────────────────────┤
│ FOOTER (full sitemap + social + legal)       │
└─────────────────────────────────────────────┘
```

---

## 6. Section-by-Section Structure — Other Major Pages

**Campaign detail page:** hero image/video → objective + location + dates → progress bar toward goal → volunteer/financial/material/skills support tabs → updates timeline → photo/video gallery → before/after (if applicable) → related issues → social share kit → "Join Campaign" sticky CTA.

**Issue detail page:** title + category tag + severity → photo evidence gallery → location (approximate map pin) → status pipeline stepper → timeline log (dated entries) → supporter/volunteer counts → responsible-authority category (if identified) → related campaign link → share buttons → "Follow this issue" toggle.

**Volunteer dashboard:** upcoming events list → joined campaigns → contribution history table → tasks assigned (if internal team) → certificates earned → badges → personal Action Score + Impact Card generator.

**Impact Dashboard (public):** filter bar (city / time range: month, quarter, year, lifetime) → stat grid (trees, waste, drives, volunteers, issues reported/resolved) → charts (trend lines) → map preview → link to Transparency page.

**Community profile page:** avatar, name, city, bio, verification badge → stat row (trees planted, cleanups, issues reported, campaigns joined, badges) → Impact Card (shareable) → activity timeline → badges shelf.

**Community feed:** composer (post type selector: Report/Achievement/Action/Awareness/Campaign/Appreciation) → ranked feed cards → each card: avatar, badge, location, timestamp, text, media, tags, appreciation bar, comment/share/save/report actions.

---

## 7. Accessibility Requirements

- Semantic HTML landmarks (`<nav>`, `<main>`, `<header>`, `<footer>`) on every template.
- All interactive elements keyboard-reachable in logical tab order; visible focus rings (not just browser default suppressed).
- Alt text required at upload time for all issue/campaign/tree photos (field-level validation, not optional).
- Color contrast: body text ≥ 4.5:1 against `--envirgreen-bg`; verify `--envirgreen-fresh` on white meets 4.5:1 for small text (test — likely needs a slightly darker shade for text use vs. decorative use).
- Forms: explicit `<label>` for every field, inline error messages tied via `aria-describedby`.
- Respect `prefers-reduced-motion` — disable scroll-reveal/count-up animations.
- Maps and image galleries must have a non-visual equivalent (list view toggle for the tree/issue map).

---

## 8. Design Direction Summary

Apple-level restraint + social-platform familiarity + NGO credibility + environmental warmth. In practice: generous whitespace, rounded 12–16px card corners, soft single-layer shadows (avoid heavy drop-shadows), large real photography (never generic stock), and typography doing most of the "premium" work rather than decoration. Every green accent should be intentional — if a screen feels "too green," it's not tighter to the brand, it's harder to read.

---

*Continue to `02-core-platform-systems.md` for the issue, campaign, volunteer, donation, tree, impact, moderation, gamification and notification systems.*
