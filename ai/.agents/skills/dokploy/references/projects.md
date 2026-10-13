## Projects

### Create project
```
POST /api/project.create
Body: {"name": "string", "description": "string|null", "env": "string"}
```
**Response is nested:** `{"project": {"projectId":"...", ...}, "environment": {"environmentId":"...", ...}}`
Extract IDs with: `jq -r '.project.projectId'` and `jq -r '.environment.environmentId'`

The created environment is the default "production" environment.

### Get project
```
GET /api/project.one?projectId=xxx
```

### Update project
```
POST /api/project.update
Body: {"projectId": "string", "name": "string", "description": "string|null"}
```

### Delete project
```
POST /api/project.remove
Body: {"projectId": "string"}
```

### Duplicate project
```
POST /api/project.duplicate
Body: {"projectId": "string", "name": "string", "sourceEnvironmentId": "string"}
```
`sourceEnvironmentId` is **required** — use the environment you want to duplicate from (typically the default production env).

### Search projects
```
GET /api/project.search?query=xxx
```
**Returns `{"message":"Not found","code":"NOT_FOUND"}` when no results** — treat as empty list, not an error.
