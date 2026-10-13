## Quick Discovery

### List all projects and services
```
GET /api/project.all
```
Returns all projects with nested environments containing their services (applications, databases, composes). **This is the primary discovery endpoint.** Always start here to find IDs.

### Get server/destination info
```
GET /api/server.all
GET /api/destination.all
```

### Search endpoints
```
GET /api/project.search?query=xxx
GET /api/application.search?query=xxx
GET /api/compose.search?query=xxx
GET /api/{type}.search?query=xxx   (mysql, postgres, redis, mongo, mariadb)
```
**All search endpoints return `{"message":"Not found","code":"NOT_FOUND"}` when no results match** — not an empty array `[]`. Treat the `NOT_FOUND` response as an empty result set, not an error.
