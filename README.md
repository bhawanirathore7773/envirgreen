# Envirgreen — Django project scaffold

A working MVP build of the platform described in the accompanying blueprint
docs (`docs/00-strategy-and-roadmap.md` through `docs/04-content-and-samples.md`).
This is real, migrated, running code — not a mockup — covering the Phase 1
(MVP) feature set plus model scaffolding for Phase 2/3.

## What's actually implemented

- **Auth & profiles** — signup/login, role field, public profile pages with
  impact stats computed live from real records (never hand-editable).
- **Issue reporting** — full report → photo upload → audited status pipeline
  → public timeline (`issues` app + `issues/services.py`).
- **Campaigns** — list/detail, join as volunteer/material/skills support,
  progress bar toward a stated drive goal (`campaigns` app).
- **Events** — list/detail, registration, attendance tracking (`events` app).
- **Volunteers** — registration form, dashboard of joined campaigns/events
  (`volunteers` app).
- **Trees** — log a planting, lifecycle status, list view (map view is a
  list for now — swap in Leaflet/Google Maps JS against the same data).
- **Community feed** — post types, meaningful reactions (not a single
  "like"), a ranking function that favors verified action over raw
  engagement (`community/services.py::rank_feed`).
- **Donations** — records intent + spend category; **no live payment
  gateway is wired up** — see "What's stubbed" below.
- **Impact dashboard** — real, DB-computed numbers, city-filterable.
- **Moderation & audit** — `ContentReport` queue, append-only `AuditLog`
  written on every issue status change.
- **Gamification** — badge model + two example auto-award rules wired to
  real signals (first verified tree, first campaign join) — extend
  `gamification/rules.py` for the rest of the badge set in the blueprint.
- **REST API** — `/api/v1/campaigns/`, `/api/v1/issues/`,
  `/api/v1/impact/snapshot/` as a working example of the pattern; the other
  apps follow the same viewset/serializer shape.
- **SEO basics** — sitemap.xml, robots.txt, semantic templates.
- **Django admin** — every model registered and manageable.

## What's stubbed / your next steps

- **Payment gateway** — `donations/views.py` records a `pending` donation
  and stops short of a real charge. Wire up Razorpay (or your gateway of
  choice) and its webhook before accepting real money.
- **Celery / Redis** — not installed here. `impact/services.py` computes
  the dashboard live on each request; swap to a nightly Celery task
  writing `ImpactSnapshot` once you add Celery (see requirements.txt).
- **Object storage** — media currently saves to local `/media/`. Point
  `DEFAULT_FILE_STORAGE` at S3/Cloudflare R2 before deploying.
- **Map views** — `trees/map.html` and the issue list are plain lists.
  Drop in Leaflet + OpenStreetMap tiles (free, no API key) against the
  existing `Location` lat/lng fields.
- **Full badge set, social-kit generator, authority escalation kit,
  certificates, notifications delivery** — modeled in the blueprint docs
  but not built out here; the patterns already in this codebase
  (`services.py` per app, signal-driven side effects) are what to extend.
- **PostgreSQL** — this scaffold runs on SQLite for zero-setup local dev.
  Swap `DATABASES` in `envirgreen/settings.py` before deploying.

## Running it locally

```bash
python -m venv .venv && source .venv/bin/activate   # or your preferred env tool
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo_data      # optional: adds one campaign/issue/event so pages aren't empty

python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `/admin/` for the admin panel.

## Project layout

Each app owns its `models.py`, `admin.py`, `views.py`, `urls.py`, and where
relevant a `services.py` for business logic that shouldn't live in views
(e.g. `issues/services.py::transition_issue` is the *only* path that should
change an issue's status, so every change gets an `AuditLog` entry).

```
core/          shared Location + Category models, homepage, about, contact
accounts/      Profile (role, stats), signup/login/profile views
campaigns/     Campaign, CampaignMember
events/        Event, EventRegistration
issues/        Issue, IssueUpdate, status-transition service
volunteers/    Volunteer, Skill, registration + dashboard
trees/         TreePlantation, TreeVerification
community/     Post, Reaction, Comment, feed ranking service
donations/     Donation (gateway integration pending)
impact/        ImpactSnapshot, live aggregation service
notifications/ Notification model + inbox view
moderation/    ContentReport, AuditLog
gamification/  Badge, UserBadge, signal-driven award rules
content/       BlogPost
api/           DRF serializers + viewsets (v1)
templates/     all HTML, base.html holds the design system
static/css/    main.css — color tokens, typography, components
```

See the `docs/` folder (the 5-part blueprint) for the full product
rationale, database schema for the not-yet-built pieces, and sample
copy for every page.
