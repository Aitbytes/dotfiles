# Wiki — Full Reference

Load this when you need: knowledge base articles, version history, backlinks, or article management.

## Endpoints

```bash
# List/search wiki articles
GET /api/wiki
# Optional: ?search=query&tag=tag-name&teamId=<id>&scope=all&includePersonal=true&limit=20&before=<cursor>

# Create article
POST /api/wiki
-d '{"title": "Onboarding Guide", "slug": "onboarding", "content": "# Welcome\n\n...", "tags": ["onboarding", "hr"], "teamId": null}'

# Get article by slug
GET /api/wiki/{slug}

# Update article (version for concurrency)
PATCH /api/wiki/{slug}
-d '{"content": "Updated content", "message": "Added new section", "version": 1}'

# Delete article
DELETE /api/wiki/{slug}
```

## Backlinks

```bash
# See which articles link to this one
GET /api/wiki/{slug}/backlinks
```

## Version History

```bash
# View revision history
GET /api/wiki/{slug}/history
```

## Move / Rename

```bash
# Change slug (rename/move article)
POST /api/wiki/move
-d '{"slug": "old-slug", "newSlug": "new-slug"}'
```

## Search Parameters

| Param | Description |
|-------|-------------|
| `search` | Full-text search query |
| `tag` | Filter by tag |
| `teamId` | Filter by team |
| `scope` | `all` or team-specific |
| `includePersonal` | Include personal (non-team) articles |
| `limit` | Results per page (default varies) |
| `before` | Cursor for pagination |
