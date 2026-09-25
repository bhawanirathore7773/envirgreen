# ENVIRGREEN — Product & Technical Blueprint
### Part 3 of 5: Core Platform Systems

> Part 3 of 5. Each system below follows **WHY → HOW → USER BENEFIT → DJANGO IMPLEMENTATION**, as requested. See `03-technical-architecture.md` for the full database schema and API layer these systems share.

---

## 1. Environmental Issue Reporting System

**WHY:** this is the platform's trust engine — if reports vanish into a black hole, nothing else on the site matters.

**HOW:** citizen submits category, description, photos/video, location (map pin + optional GPS), severity, recurrence flag → issue enters status pipeline:
`Reported → Verified → Authority Identified → Reported to Authority → Follow-up Required → Action Taken → Community Verification → Resolved` (with a parallel `No Action → Escalated` branch for non-responsive cases).

**USER BENEFIT:** the reporter can watch their report move, not just submit it and forget it — this alone is a bigger trust driver than any messaging copy.

**DJANGO:**
```python
class Issue(models.Model):
    STATUS_CHOICES = [
        ("reported", "Reported"), ("verified", "Verified"),
        ("authority_identified", "Authority Identified"),
        ("reported_to_authority", "Reported to Authority"),
        ("followup_required", "Follow-up Required"),
        ("action_taken", "Action Taken"),
        ("community_verified", "Community Verification"),
        ("resolved", "Resolved"), ("escalated", "Escalated"),
        ("no_action", "No Action"),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    location = models.ForeignKey("Location", on_delete=models.PROTECT)
    severity = models.CharField(max_length=20, choices=[("low","Low"),("medium","Medium"),("high","High")])
    is_recurring = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="reported")
    responsible_authority_category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class IssueUpdate(models.Model):
    issue = models.ForeignKey(Issue, related_name="timeline", on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=Issue.STATUS_CHOICES)
    note = models.TextField(blank=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```
A `post_save` signal on `IssueUpdate` writes to `AuditLog` and fires a notification to `issue.reporter`. Status transitions are enforced in a service function (`issues/services.py::transition_issue`), never directly in the admin, so invalid jumps (e.g., `reported → resolved`) are blocked at the code layer, not just by convention.

---

## 2. Campaign System

**WHY:** campaigns are the unit that converts individual reports/intentions into coordinated group action — this is where "I noticed a problem" becomes "we fixed it."

**HOW:** campaign has type (River Cleanup, Tree Plantation, etc.), objective, location, dates, organizer, a numeric goal (e.g., "10 cleanup drives"), and a progress counter. Supports four ways in: Volunteer, Financial, Material, Skills (see Section 3 below).

**USER BENEFIT:** a clear, bounded commitment ("join this one Sunday drive") is far less intimidating than an open-ended "help the environment" ask.

**DJANGO:**
```python
class Campaign(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    campaign_type = models.CharField(max_length=50, choices=CAMPAIGN_TYPE_CHOICES)
    objective = models.TextField()
    location = models.ForeignKey("Location", on_delete=models.PROTECT)
    start_date, end_date = models.DateField(), models.DateField(null=True, blank=True)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    goal_count = models.PositiveIntegerField(default=1)   # e.g. "10 drives"
    progress_count = models.PositiveIntegerField(default=0)
    related_issue = models.ForeignKey(Issue, null=True, blank=True, on_delete=models.SET_NULL)

class CampaignMember(models.Model):
    campaign = models.ForeignKey(Campaign, related_name="members", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    support_type = models.CharField(max_length=20, choices=[("volunteer","Volunteer"),("financial","Financial"),("material","Material"),("skills","Skills")])
    detail = models.CharField(max_length=255, blank=True)   # e.g. "Can provide: gloves, water"
```
`progress_count` increments via a service call when an admin marks a linked `CleanupActivity`/`Event` complete — never a free-text field a user can edit.

---

## 3. Campaign Support Types

Four support channels, each its own lightweight sub-form on the campaign page (tabbed UI, see file `01-sitemap-ux-design.md`):
- **Volunteer:** "I want to participate" → adds `CampaignMember(support_type="volunteer")`, optionally links to a specific `Event`.
- **Financial:** routes to `/donate/<campaign-slug>/`.
- **Material:** checkbox list (gloves, bags, plants, water, tools, transport, printing, equipment) → creates a `MaterialPledge` record the campaign manager sees in their ops dashboard.
- **Skills:** checkbox list (photography, video, design, social, tech, legal, event management, documentation) → tagged on the user's profile as a skill offer, surfaced to the Campaign Manager role.

---

## 4. Volunteer Management System

**WHY:** without a real pipeline from "signed up" to "did something," volunteer registration is just an email list.

**HOW:** registration captures skills, availability, interests, and city → Volunteer Manager matches to open campaign/event slots → volunteer dashboard tracks upcoming commitments, history, tasks, certificates, badges.

**USER BENEFIT:** a volunteer always has a clear "what's next for me" instead of registering once and hearing nothing.

**DJANGO:** `Volunteer` model extends `UserProfile` (OneToOne) with `skills` (M2M to a `Skill` tag model), `availability` (JSONField or a simple choice set — weekday/weekend/evening), `preferred_activities` (M2M to `Category`). `EventRegistration` links `Volunteer` to `Event` with an `attended` boolean set by the organizer post-event — this boolean, not the registration itself, is what counts toward Action Score.

---

## 5. Donation / Support System

**WHY:** donors need to see exactly where money goes, or the platform reads as just another anonymous charity box.

**HOW:** every donation is tagged to a campaign and a spend category (Plantation, Cleanup Equipment, Awareness, Volunteer Activities, Community Programs, Technology, Operations). Receipt auto-generated and emailed. Personal donation history is private; only aggregate, category-level totals are shown publicly on the Transparency page.

**USER BENEFIT:** confidence that ₹500 given to "Save Our River" cleanup gear actually shows up as gear spend later, not a black box.

**DJANGO:**
```python
class Donation(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT)
    category = models.CharField(max_length=50, choices=SPEND_CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gateway_txn_id = models.CharField(max_length=100, unique=True)
    receipt_pdf = models.FileField(upload_to="receipts/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```
Payment gateway integration (Razorpay is the standard choice for an India-first NGO) is isolated behind a `payments/` service module so the gateway can be swapped without touching `Donation` model logic. Receipt generation runs async via Celery.

---

## 6. Tree Plantation System

**WHY:** a photo of a sapling proves nothing about long-term impact — survival tracking is what separates a real plantation program from a photo-op.

**HOW:** `TreePlantation` record logs species, count, location, photo, planting org → lifecycle status `Planted → Verified → Growing → Survived`, with optional periodic check-in photos.

**USER BENEFIT:** "35 trees planted" on a profile means something specific and checkable, not a self-reported number.

**DJANGO:**
```python
class TreePlantation(models.Model):
    STATUS = [("planted","Planted"),("verified","Verified"),("growing","Growing"),("survived","Survived")]
    planter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    species = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=1)
    location = models.ForeignKey("Location", on_delete=models.PROTECT)
    coordinates = gis_models.PointField(null=True, blank=True)   # if using GeoDjango
    status = models.CharField(max_length=20, choices=STATUS, default="planted")
    organisation = models.ForeignKey("Organization", null=True, blank=True, on_delete=models.SET_NULL)

class TreeVerification(models.Model):
    tree = models.ForeignKey(TreePlantation, related_name="checkins", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=TreePlantation.STATUS)
    photo = models.ImageField(upload_to="tree_checkins/")
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```
Only `status="survived"` counts toward the public survival-rate stat on the Impact Dashboard — a number most tree-planting NGOs never publish, and one that builds unusual credibility when it's honest.

---

## 7. Impact Measurement System

**WHY:** the Impact Dashboard is the platform's single most important credibility surface — every other feature feeds it.

**HOW:** aggregate metrics (trees planted/surviving, waste collected, drives run, volunteers, issues reported/resolved, institutions reached) computed from real model counts, filterable by month/quarter/year/lifetime and by city.

**USER BENEFIT:** anyone — press, a potential CSR partner, a skeptical citizen — can check the platform's claims themselves instead of taking Envirgreen's word for it.

**DJANGO:** an `ImpactMetric` model is *not* used to store hand-entered numbers. Instead, a nightly Celery task (`impact/tasks.py::recompute_impact_snapshot`) queries the real tables (`TreePlantation.objects.filter(status="survived").count()`, etc.) and writes a dated `ImpactSnapshot` row — this gives fast dashboard reads without expensive live aggregation on every page view, while keeping the source of truth honest.

---

## 8. Authority Engagement Workflow

**WHY:** citizens are frustrated but rarely equipped to escalate an issue effectively — and unmanaged frustration turns into harassment, which the brief correctly wants to avoid entirely.

**HOW:** `Document → Report → Notify → Follow-up → Escalate → Community awareness → Envirgreen action`. When an issue is verified, the system suggests a **responsible authority category** (e.g., "Municipal Solid Waste Dept.") based on the issue category — never a guess presented as fact — and generates a **respectful, factual draft message** the user can copy, plus a social-share kit. No auto-messaging, no mass-tagging, no contact-scraping.

**USER BENEFIT:** turns "I'm angry about this" into "here's a clear, professional ask," which is both more effective and safer for the user.

**DJANGO:** `Authority` and `AuthorityContact` models store *publicly available* official channels only (entered/verified by the Envirgreen team, not scraped). A `generate_escalation_message(issue)` service function fills a vetted template — this is intentionally not an open AI free-text generator, to guarantee tone stays respectful.

---

## 9. Moderation System

**WHY:** any platform with user-generated posts and photo uploads needs moderation before it needs almost anything else — this is not optional infrastructure.

**HOW:** `Report Post / Comment / User` → moderation queue with statuses `Pending → Approved / Rejected / Removed / Escalated`. Clear published Community Guidelines (no hate, harassment, threats, defamation, spam, false environmental claims, personal info exposure, illegal-activity encouragement).

**USER BENEFIT:** the feed stays trustworthy and safe enough that people are comfortable posting their real name and location.

**DJANGO:**
```python
class ContentReport(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # generic FK to Post/Comment/User
    object_id = models.PositiveIntegerField()
    reason = models.CharField(max_length=50, choices=REPORT_REASON_CHOICES)
    status = models.CharField(max_length=20, choices=[("pending","Pending"),("approved","Approved"),("rejected","Rejected"),("removed","Removed"),("escalated","Escalated")], default="pending")
```
A basic duplicate/spam heuristic (perceptual image hashing + text similarity via `difflib` or a small embedding check) flags likely duplicate issue reports for admin review before they hit the public feed — reduces moderator load without removing the human decision.

---

## 10. Gamification System

**WHY:** gamification should reward *verified* effort, not attention-seeking — the brief is explicit that fake reports or spam must never be rewarded.

**HOW:** badges (First Tree, Clean Start, Green Champion, Waste Warrior, Awareness Creator, Community Builder, Campaign Champion) awarded automatically on verified milestones. Levels (Community Member → Active Volunteer → Green Contributor → Environmental Champion → Envirgreen Leader) based on cumulative verified Action Score. Leaderboard ranks by verified actions/hours/participation — never by donation amount.

**USER BENEFIT:** recognition feels earned, which makes it motivating instead of gimmicky.

**DJANGO:** `Badge` + `UserBadge` (M2M through model with `awarded_at`), awarded via signal receivers listening on the relevant verification events (`TreeVerification` saved with `status="survived"`, `IssueUpdate` saved with `status="resolved"` where `actor` = reporter's own report, etc.) — badge logic lives in `gamification/rules.py`, decoupled from the models that trigger it.

---

## 11. Notification System

**WHY:** the status-pipeline and campaign features are only as engaging as the reminders that bring people back to check on them.

**HOW:** in-app + email (SMS/WhatsApp as a later integration). Trigger events: issue status change, campaign starting soon, cleanup goal reached, appreciation received, issue update posted.

**DJANGO:** a single `Notification` model (`recipient`, `verb`, `target` generic FK, `read_at`) written by a lightweight `notify.send()` helper called from the relevant signals; email delivery is queued via Celery so a spike in activity (e.g., a campaign hitting its goal) never blocks the request/response cycle.

---

## 12. Community / Social System

**WHY:** the feed is where individual actions become visible collective momentum — but engagement-optimized feeds famously reward outrage, which is the opposite of what a civic-action platform needs.

**HOW:** post types — Report, Achievement, Action, Awareness, Campaign, Appreciation. Reactions are meaningful, not a single like: 🌱 Green Action, 🧹 Clean Action, 🌳 Tree Champion, 💚 Community Support, 👏 Inspiration. Feed ranking explicitly prioritizes (1) verified actions, (2) active campaigns, (3) local issues, (4) educational content, (5) volunteer achievements, (6) community contributions — recency-weighted within each tier, not a raw engagement-count sort.

**USER BENEFIT:** the most-seen post is "look what we changed," not "look at me" — which is the platform's entire philosophical point.

**DJANGO:** `Post` (type, text, media M2M, location FK, campaign FK nullable, category FK), `Reaction` (user, post, reaction_type — unique_together to prevent duplicate reacting), `Comment`, `SavedPost`. Feed query is a weighted `annotate()` combining a `verified` boolean, a recency decay factor, and post-type weight — computed in a `feed/services.py::rank_feed()` function so the ranking logic is unit-testable in isolation from the view.

---

*Continue to `03-technical-architecture.md` for the full database schema, Django app structure, API design, SEO, security, performance, deployment, testing, and AI-feature scope.*
