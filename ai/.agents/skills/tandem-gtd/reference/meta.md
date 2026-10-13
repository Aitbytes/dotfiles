# Meta & Admin — Full Reference

Load this when you need: dashboard stats, insights, activity history, search, notifications, import/export, settings, or waiting-for tracking.

---

## Waiting For

Track items delegated to others and awaiting response.

```bash
# List waiting-for items
GET /api/waiting-for
# Optional: ?resolved=true|false|all

# Create
POST /api/waiting-for
-d '{"description": "Q4 report from accounting", "person": "Jane Smith", "dueDate": "2026-06-20T00:00:00.000Z"}'

# Update (mark resolved or change fields)
PATCH /api/waiting-for/{id}
-d '{"isResolved": true}'

# Delete
DELETE /api/waiting-for/{id}
```

---

## Dashboard & Insights

```bash
# Dashboard stats (health, progress, velocity, blocked queue, milestones, burn-down)
GET /api/dashboard/stats

# Insights (productivity analytics, system health)
GET /api/insights
GET /api/insights/export
```

---

## History & Activity

```bash
# Activity feed
GET /api/history/feed
# Optional: ?days=7&limit=50&source=all|manual|ai|cascade

# Weekly summary
GET /api/history/weekly-summary
# Optional: ?weekOf=2026-06-09
```

---

## Search

```bash
# Full-text search across tasks, projects, wiki, inbox
GET /api/search?q=keyword
# Optional: &scope=all|tasks|projects|wiki|inbox&limit=20
```

---

## Notifications

```bash
# List notifications
GET /api/notifications
# Optional: ?unreadOnly=true&limit=50

# Mark single notification as read
PATCH /api/notifications/{id}

# Mark all as read
POST /api/notifications/mark-all-read

# Unread count
GET /api/notifications/unread-count
```

---

## Settings & API Tokens

```bash
# Get feature flags
GET /api/settings/features

# List API tokens (metadata only, never exposes secrets)
GET /api/settings/api-tokens
# Note: Creating/deleting tokens requires session auth, not Bearer
```

---

## Help Articles

```bash
# List help articles
GET /api/help
# Optional: ?category=Getting Started&tag=gtd-basics&search=review

# Get article by slug
GET /api/help/{slug}
```

---

## Import / Export

```bash
# Export all data
GET /api/export
# Optional: ?format=json|csv

# Import workflow
POST /api/import/upload        # Upload file for preview
GET /api/import/{jobId}        # Check status
POST /api/import/{jobId}/confirm   # Confirm and process
POST /api/import/{jobId}/cancel    # Cancel import
```
