# Reviews — Full Reference

Load this when you need: weekly review workflow, horizon reviews, or horizon notes.

## Weekly Reviews

The GTD weekly review process — review the past week and plan the next.

### Endpoints

```bash
# List past reviews
GET /api/reviews
# Optional: ?page=1&limit=10

# Start a new review (or get existing in-progress one)
POST /api/reviews
-d '{"notes": "Starting weekly review"}'
# If one is already in progress, returns the existing one

# Get current in-progress review
GET /api/reviews/current

# Get a specific review
GET /api/reviews/{id}

# Update review (e.g., check off sections)
PATCH /api/reviews/{id}
-d '{"checklist": {"getClear": true, "getCurrent": false, "getCreative": false},
     "notes": "Getting clear phase done"}'

# Mark review complete
POST /api/reviews/{id}/complete

# Delete review
DELETE /api/reviews/{id}
```

### Review Checklist

The checklist object tracks the three GTD review phases:
- `getClear` — Collect and process all loose papers and materials
- `getCurrent` — Review action lists, calendar, projects, waiting-for
- `getCreative` — Someday/maybe, new ideas

## Horizon Reviews

Structured reviews for each horizon level (similar to weekly reviews but focused on higher-level thinking).

```bash
GET /api/horizon-reviews
GET /api/horizon-reviews/current
GET /api/horizon-reviews/{id}
POST /api/horizon-reviews
PATCH /api/horizon-reviews/{id}
POST /api/horizon-reviews/{id}/complete
```

## Horizon Notes

Free-form notes for each horizon level. Use these to capture thoughts about purpose, vision, and long-term goals.

```bash
# List notes
GET /api/horizon-notes

# Create note
POST /api/horizon-notes
-d '{"level": "HORIZON_3", "title": "1-2 Year Goals", "content": "My goals for the next 1-2 years..."}'
```
