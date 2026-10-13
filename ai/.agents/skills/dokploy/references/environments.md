## Environments

### Create environment
```
POST /api/environment.create
Body: {"name": "string", "description": "string", "projectId": "string"}
```

### List environments for a project
```
GET /api/environment.byProjectId?projectId=xxx
```

### Get/Update/Delete/Duplicate environment
```
GET /api/environment.one?environmentId=xxx
POST /api/environment.update
POST /api/environment.remove
POST /api/environment.duplicate
```
