# ENVIRGREEN — Product & Technical Blueprint
### Part 1 of 5: Product Analysis, Strategy, Feature Roadmap & Sustainability

> **Document set:** This is part 1 of 5. See `01-sitemap-ux-design.md`, `02-core-platform-systems.md`, `03-technical-architecture.md`, and `04-content-and-samples.md` for the rest of the blueprint.

---

## 1. Deep Product Analysis

**What Envirgreen actually is:** most "environmental NGO" sites are brochures — mission statement, donate button, photo gallery. Envirgreen's real product is a **closed feedback loop**: *see a problem → report it → someone verifies it → people mobilize → the problem visibly changes → that change is documented and shared*. The website is the container for that loop, not the point of it.

**The core risk:** civic-action platforms die from one of two failure modes —
1. **Credibility collapse** — inflated numbers, unverified "impact," or a report that quietly goes nowhere. Once one user catches a fake statistic, they stop trusting all of them.
2. **Engagement without action** — it becomes a place people scroll (like/comment) instead of a place people *do things*.

Every structural decision below (verification tiers, "Community Observation" vs "Verified" labeling, an appreciation system instead of vanity likes, a feed that ranks actions over outrage) exists to defend against these two failure modes specifically.

**What makes this different from a typical Django NGO site:** the reporting → status-tracking → resolution pipeline (Section 2 of file `02-core-platform-systems.md`) is a real workflow engine, not a contact form. That's the hardest part to build and the part most competitors skip — which is exactly why it's the platform's moat.

---

## 2. Product Strategy

### Positioning
**Primary tagline:** **"See it. Report it. Fix it — together."**
This is chosen over the more generic options in the brief because it names the loop itself, not just the sentiment. It works as a headline, a nav label for the core CTA, and a hashtag stem (`#ReportItFixIt`).

**Secondary campaign lines** (rotate by context, never all at once):
- Homepage hero subhead: *"Clean. Green. Responsible. Together."*
- Issue-reporting flows: *"Don't Just Complain. Take Action."*
- Tree/plantation flows: *"Plant Today. Protect Tomorrow."*
- Volunteer recruitment: *"Your City. Your Responsibility."*

### Who to win first
Trying to serve all five personas (citizens, volunteers, core team, institutions, authorities) equally on day one dilutes the build. Sequence:
1. **Citizens** (report + share) — lowest-friction entry, generates the content that makes the platform feel alive.
2. **Volunteers** (join + act) — converts reports into visible resolutions; without this group, reports pile up unresolved and kill trust.
3. **Core team / admin tooling** — needed as soon as #1 and #2 produce real volume.
4. **Institutions/CSR and authorities** — layer on once there's a track record (real before/after cases) to show them. Selling a partnership with zero completed campaigns is a hard sell; selling one with 10 documented cleanups isn't.

### The three pillars (homepage framing)
- **Clean** — surroundings and responsible waste behavior.
- **Green** — plant, protect, and grow trees.
- **Responsible** — civic sense and neighborhood ownership.

---

## 3. Signature Differentiating Features

These are the features that make Envirgreen feel unlike a template NGO site. Each is described with why it matters and what stops it from becoming vanity/fake metrics.

| Feature | Why it matters | Anti-gaming guardrail |
|---|---|---|
| **Issue Status Pipeline** (Reported → Verified → Authority Notified → Follow-up → Action Taken → Community Verified → Resolved) | Makes "we reported it" mean something instead of disappearing into a void | Status changes require admin/moderator action, logged in an `AuditLog` |
| **Envirgreen Action Score** | Single number summarizing *verified* participation, without turning people into a leaderboard-chasing bot | Score only counts actions with `verification_status=verified`; recalculated via signal, never user-editable |
| **Envirgreen Impact Card** | Shareable, personal, gives people a reason to post *their* action instead of a selfie | Auto-generated from DB fields — no free-text impact numbers a user can type in |
| **Envirgreen Community Action Index** (per city/area — explicitly *not* branded as an official environmental index) | Gives institutions/press a citable, comparable number without Envirgreen falsely claiming scientific authority | Methodology and "based on platform activity, not certified environmental data" disclaimer always shown beside the number |
| **Before/After Slider** | Visible transformation is the single most persuasive asset a civic campaign has | Both images tied to the same `CleanupActivity` record with timestamps; can't be swapped post-verification |
| **"I Did Something" quick-log** | Lowers the barrier from "I want to help" to "I just did" — captures spontaneous action, not just organized events | Goes to moderation queue before counting toward profile/score |
| **Responsible Authority Escalation Kit** | Turns frustration into a structured, non-harassing civic action | Auto-generated message is *always* factual/respectful; no mass-tagging or auto-DM tooling |

---

## 4. Complete Feature List — MVP vs Phase 2 vs Phase 3

Mapped from the master brief's five build phases, but re-sequenced around **one pilot city first**, since a two-sided marketplace (reports + volunteers) needs local density to feel alive.

### MVP (Months 1–3) — "Prove the loop works in one city"
- Auth, user profiles (basic), roles: Community Member / Verified Volunteer / Envirgreen Team / Admin
- Homepage, About, Campaigns (list + detail), Events (list + detail), Volunteer registration, Contact, static Impact page
- **Issue reporting** end-to-end: submit → photo upload → status pipeline → public issue page with timeline
- **Campaign creation & join** (volunteer only, no financial support yet)
- Admin panel for moderating issues, campaigns, volunteers
- Core SEO (meta tags, sitemap.xml, robots.txt, semantic HTML)
- Mobile-first responsive UI, WCAG-AA basics

### Phase 2 (Months 4–7) — "Make participation visible and social"
- Community feed: posts (Report/Achievement/Action/Awareness/Campaign/Appreciation types), reactions, comments
- Tree plantation tracking + status (Planted → Verified → Growing → Survived)
- Donation system (single gateway, campaign-linked, receipts)
- Impact Dashboard (public, DB-driven, city-filterable)
- Notification system (in-app + email)
- Verification badge tiers
- Before/After slider component
- Certificates (PDF, QR-verifiable)

### Phase 3 (Months 8–12) — "Scale and defend trust"
- Tree Map + Impact Map (clustered, privacy-safe)
- Authority Engagement Kit (auto-generated respectful complaint text, shareable social kit, official channel lookup)
- Social Media Campaign Kit (auto-generated captions/hashtags/poster/QR per campaign)
- Gamification: badges, levels, Action Score, leaderboard (non-monetary metric)
- Moderation queue with spam/duplicate detection
- Civic Sense Learning Center + Civic Challenges
- Partnership/CSR intake system
- PWA (installable, offline-capable issue drafting)
- Multi-city support, Hindi localization (i18n scaffolding should exist from Phase 1, content added here)

**AI features and a second city launch are explicitly Phase 4+** — see file `03-technical-architecture.md` for the AI feature list, which is intentionally conservative (classification suggestions with mandatory human confirmation, not autonomous decisions).

---

## 5. Monetization & Sustainability (NGO-appropriate)

The brief is right to flag: donation-amount leaderboards and aggressive donation pressure damage trust. Sustainable, appropriate revenue paths:

1. **CSR partnerships** — companies fund a named campaign (e.g., "Plantation Drive sponsored by [Company]") with transparent spend reporting on the Transparency page. This is the highest-value channel because Indian CSR law (Companies Act Sec. 135) creates a standing budget line many mid-size firms must deploy.
2. **In-kind sponsorship** — cleanup kits (gloves, bags, tools) sponsored by local businesses, credited on the campaign page and social kit.
3. **Institutional partnership fees** — schools/colleges running structured awareness programs pay a modest program fee that funds materials + facilitator time; positioned as a program cost, not a donation.
4. **Event-based fundraising** — ticketed community events (fun runs, eco-fairs) with proceeds tied to a specific, named goal.
5. **Grants** — government/CSR/foundation grants tied to measurable outcomes the Impact Dashboard already tracks, which makes grant reporting nearly free (export the dashboard).
6. **Merchandise** — reusable bottles/bags sold at cost-plus-small-margin, positioned as "gear," not fundraising.

Avoid: paid verification badges, pay-to-rank leaderboards, donation amount as a public status symbol.

---

## 6. 12-Month Roadmap

| Quarter | Focus | Key Milestone |
|---|---|---|
| **Q1** | MVP build + single pilot city (e.g., Jaipur) | First 50 verified issue reports, first campaign completed with before/after documentation |
| **Q2** | Community layer + donations + tree tracking | 500 registered volunteers, first CSR partner signed, Impact Dashboard goes public |
| **Q3** | Trust & scale infrastructure — moderation, gamification, authority kit, maps | First authority-acknowledged resolution documented publicly, first Civic Challenge run |
| **Q4** | PWA, second-city readiness, i18n (Hindi), partnership program formalized | Multi-city architecture validated, 12-month impact report published (real numbers only) |

---

*Continue to `01-sitemap-ux-design.md` for sitemap, user journeys, UI system, and page-by-page wireframes.*
