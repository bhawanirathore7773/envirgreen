# ENVIRGREEN — Product & Technical Blueprint
### Part 4 of 5: Technical Architecture

> Part 4 of 5. Covers SEO, content/social strategy, database schema, Django app structure, API design, security, performance, deployment, testing, PWA, and AI scope.

---

## 1. SEO Strategy

- **URLs:** slug-based, stable, human-readable (`/campaigns/save-our-river/`, `/blog/how-to-develop-civic-sense/`).
- **Metadata:** per-object `meta_title`/`meta_description` fields on `Campaign`, `Issue`, `BlogPost`, `Event` (fallback to auto-generated from title/objective if left blank), rendered via a shared `{% seo_meta %}` template tag.
- **Structured data:** JSON-LD for `Organization` (sitewide), `Event` (event pages), `Article` (blog posts), `BreadcrumbList` (all detail pages). Do not add NGO-specific schema types that don't exist in schema.org's vocabulary — stick to what's real.
- **Sitemap/robots:** Django's `django.contrib.sitemaps` framework generating `sitemap.xml` from `Campaign`, `Issue`, `BlogPost`, `Event` querysets (published/public only); `robots.txt` disallowing `/dashboard/`, `/admin/`, `/volunteer/dashboard/`.
- **Open Graph/Twitter cards:** dynamic per campaign/issue/blog page, using the first gallery image as `og:image`.
- **Performance as SEO:** Core Web Vitals directly affect ranking — see Performance section below; this is not a separate workstream.

## 2. Content Strategy

Editorial calendar built around genuinely useful, non-keyword-stuffed topics: civic sense fundamentals, waste segregation how-tos, tree-care guides, local issue explainers, campaign/volunteer stories. Every blog post should answer a real search query a citizen in a target city would type ("how to report garbage dumping in [city]") rather than being written to a keyword density target. Story-format content (Before → Action → Result → Next Step, per file `04-content-and-samples.md`) doubles as both engagement content and long-tail SEO content, since these are naturally structured around real search intent ("river cleanup before after [city]").

## 3. Social Media Strategy

Each campaign auto-generates a kit (Instagram caption + story, Reel caption, X post, Facebook post, WhatsApp message, LinkedIn post, hashtag set, poster image, QR code) from a single `SocialKitGenerator` service, templated per platform with the campaign's title/goal/progress/hashtag interpolated in. Official platform embeds (not scraping) are used to surface latest posts on the homepage. No auto-posting on a user's behalf without explicit action — the kit produces copy-ready assets, not automated spam.

---

## 4. Database Architecture

Core model groups (grouped by Django app — full field detail for the heaviest-traffic models is in file `02-core-platform-systems.md`):

```
accounts:      User, UserProfile, Volunteer, Organization, Partner
campaigns:     Campaign, CampaignMember, MaterialPledge
events:        Event, EventRegistration
issues:        Issue, IssueUpdate, IssueEvidence, Category
authorities:   Authority, AuthorityContact
trees:         TreePlantation, TreeVerification
impact:        ImpactSnapshot, CleanupActivity
community:     Post, PostMedia, Comment, Reaction, SavedPost
moderation:    ContentReport, AuditLog
notifications: Notification
gamification:  Badge, UserBadge
donations:     Donation, DonationCampaignCategory
certificates:  Certificate
content:       BlogPost, Category (shared), MediaAsset
core:          Location, TeamMember, Task, TaskComment, SocialCampaign
```

Design notes:
- `Location` is a shared model (city, area/ward, lat/lng, approximate-display flag) referenced by `Issue`, `Campaign`, `TreePlantation`, `Event` — avoids duplicating geography logic per app.
- `Category` is shared between issues, blog, and campaigns via a `category_type` field rather than three separate tag tables.
- All verification-bearing models (`Issue`, `TreePlantation`, `CleanupActivity`) carry a `verification_status` and `verified_by` FK — this single pattern is what powers the anti-fake-impact system described in file `02-core-platform-systems.md`.
- `AuditLog` is a generic, append-only table (`actor`, `action`, `content_type`, `object_id`, `timestamp`, `metadata` JSONField) written to by signals across every app — never edited, only inserted.

---

## 5. Django Application Structure

```
envirgreen/
├── core/            # Location, shared choices, base templates/tags
├── accounts/        # auth, profiles, roles/permissions
├── campaigns/
├── events/
├── volunteers/
├── issues/
├── authorities/
├── trees/
├── community/       # posts, comments, reactions, feed ranking
├── impact/          # snapshots, dashboard views
├── donations/
├── certificates/
├── notifications/
├── moderation/
├── gamification/
├── content/         # blog, civic-sense learning center
├── partners/
├── analytics/
└── api/             # DRF serializers/viewsets, versioned (api/v1/)
```
Each app owns its models, forms, signals, and a `services.py` for business logic that shouldn't live in views (status transitions, score recalculation, feed ranking). Cross-app logic (e.g., "award badge when tree survives") lives in the *awarding* app (`gamification`) listening to signals from the *source* app (`trees`) — keeps `trees` ignorant of gamification, so it can be tested and reused independently.

---

## 6. API Architecture (Django REST Framework)

```
/api/v1/auth/                  (token/session auth, DRF SimpleJWT or session)
/api/v1/users/<id>/
/api/v1/campaigns/             GET, POST (auth)
/api/v1/campaigns/<slug>/
/api/v1/events/
/api/v1/issues/                GET, POST
/api/v1/issues/<slug>/updates/ (timeline)
/api/v1/posts/                 feed endpoint, paginated, cursor-based
/api/v1/comments/
/api/v1/trees/
/api/v1/volunteers/
/api/v1/donations/
/api/v1/impact/snapshot/       public, heavily cached
/api/v1/notifications/
```
Even in an MVP built with Django templates + HTMX, routing all data access through DRF viewsets from day one means the React/Next.js frontend option (Option B in the brief) can be introduced later without a backend rewrite — HTMX partials and a future SPA both consume the same API surface. Use cursor pagination on `posts` and `issues` (offset pagination degrades badly past a few thousand rows); throttle write endpoints (`IssueRateThrottle`, `PostRateThrottle`) to blunt spam at the API layer, not just in application logic.

---

## 7. Security Architecture

- CSRF protection on all state-changing views (Django default; explicit `@csrf_protect` on any API view using session auth).
- `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`, `SECURE_SSL_REDIRECT` in production settings.
- Role-based permissions via Django Groups + custom `has_perm` checks, not hand-rolled `if user.role ==` checks scattered through views — centralize in `accounts/permissions.py`.
- File upload validation: enforce MIME type + magic-byte checking (not just extension), max size limits per upload type, image re-encoding on ingest (strips EXIF GPS data from uploaded photos automatically — important for reporter privacy).
- API throttling via DRF's `ScopedRateThrottle`.
- Input validation and output escaping via Django's template auto-escaping and DRF serializer validation — never build raw SQL from user input; use the ORM or parameterized queries exclusively.
- `AuditLog` (see schema above) on every status change, moderation action, and admin edit to sensitive fields.
- Secrets and credentials via environment variables (`django-environ`), never committed; separate `settings/local.py`, `settings/staging.py`, `settings/production.py`.

## 8. Performance Optimization

- `select_related`/`prefetch_related` on every list view touching FK/M2M-heavy models (campaign list with organizer + location; feed with author + media + reactions).
- Database indexes on `status`, `slug`, `created_at`, and FK columns used in filtering (`Issue.status`, `Post.created_at`).
- Redis for: page-fragment caching (impact dashboard, homepage counters), session storage, and Celery broker.
- Celery for async work: email sending, receipt/certificate PDF generation, nightly impact-snapshot computation, image thumbnail generation.
- Media on object storage (S3/Cloudflare R2/Cloudinary) behind a CDN — never served from the app server; responsive `srcset` images generated at upload time (e.g., via `django-imagekit` or a Celery task using Pillow), WebP/AVIF where supported.
- Pagination everywhere; infinite scroll only on the community feed, not on SEO-critical list pages (campaigns, issues) which should remain paginated with real page URLs for crawlability.

## 9. Deployment Architecture

Gunicorn (WSGI) or Uvicorn+Daphne (if ASGI/websockets needed for live notifications later) behind Nginx, PostgreSQL (managed, e.g., RDS or a managed Postgres provider), Redis (managed), Celery worker + beat as separate processes/containers, object storage + CDN, HTTPS via Let's Encrypt or platform-managed certs, structured logging (JSON logs) shipped to a log aggregator, automated daily DB backups with tested restore procedure, CI/CD pipeline (GitHub Actions: lint → test → build → deploy) with staging environment mirroring production before promotion.

## 10. Testing Strategy

Unit tests per app (models, services, signals) using `pytest-django`; API tests via DRF's `APIClient` covering auth, permissions, and the 6 critical user journeys listed below; factory-based test data (`factory_boy`) rather than fixtures for maintainability; a small end-to-end suite (Playwright) covering the highest-value flows only (issue report submission, campaign join, donation, tree logging) rather than trying to E2E-test everything.

**Critical journeys to cover explicitly:** volunteer signup → confirmation; issue report → photo upload → status tracking; campaign join → event → certificate; campaign → donate → receipt; post → moderation → feed → appreciation; tree log → verification → profile impact.

## 11. Mobile / PWA Strategy

Django serves a `manifest.json` + service worker (via `django-pwa` or a hand-rolled minimal SW) enabling "Add to Home Screen," offline caching of static shell + last-viewed campaign/issue pages, and a background-sync-capable issue-report draft (so a photo taken with no signal queues for submission once reconnected). This is deliberately scoped as *installable web app*, not full offline-first — a true offline data layer is Phase 5+ complexity not worth taking on before the core platform has traction.

## 12. AI Features (scoped conservatively)

All AI features keep a human in the loop for anything that affects public trust or a person's record:
- **Issue photo classification** — suggests a category (e.g., "Garbage dumping"); admin/moderator confirms before it's shown publicly. Never auto-publishes a category.
- **Campaign/social copy drafting** — internal team tool to draft descriptions/captions for editing, not for autonomous publishing.
- **Civic education Q&A** — a scoped assistant answering "how do I dispose of X," grounded in the platform's own Civic Sense content, not open-ended.
- **Authority/location assistant** — suggests a responsible-authority *category* from publicly known jurisdiction boundaries; always labeled as a suggestion, never presented as a confirmed contact.
- **Admin-side**: report summarization, duplicate-report detection, translation assist — all reviewed before acting on them.

No AI feature auto-verifies impact, auto-resolves an issue, or auto-scores a user — those stay strictly rule-based and human-gated, per the anti-fake-impact requirements in file `02-core-platform-systems.md`.

## 13. Future Mobile App Strategy

Because the API layer (`/api/v1/`) is built from day one regardless of whether the MVP frontend is server-rendered, a native app (React Native or Flutter) or the PWA-to-native wrap can consume the same endpoints without backend changes — the sequencing risk to avoid is building views that only work as server-rendered HTML with no API equivalent.

---

## 14. Final Recommended Technology Stack

| Layer | Choice | Why |
|---|---|---|
| Backend | Python, Django, Django REST Framework | Matches existing skillset; DRF gives a clean API from day one |
| Database | PostgreSQL (+ PostGIS if map features need real geo queries) | Relational integrity for the verification/status workflows; GIS support for the tree/issue map |
| Cache/Queue | Redis + Celery | Async email/PDF/image work, dashboard caching |
| Frontend (MVP) | Django templates + HTMX + Alpine.js | Fastest path to a working, fast MVP without a separate frontend build |
| Frontend (Phase 3+, if community features outgrow HTMX) | Next.js against the existing DRF API | No backend rewrite needed — API-first design pays off here |
| Media | Cloudflare R2 or AWS S3 + CDN | Never serve uploads from the app server |
| Deployment | Gunicorn + Nginx, containerized (Docker), CI/CD via GitHub Actions | Reproducible deploys, easy staging/production parity |
| Payments | Razorpay (or equivalent India-first gateway) | Standard for INR donations with receipt/webhook support |

---

*Continue to `04-content-and-samples.md` for exact homepage copy, CTA copy, and full sample content for a campaign, issue report, volunteer page, social posts, dashboard, profile, and the river-cleaning campaign example.*
