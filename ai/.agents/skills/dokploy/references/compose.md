## Compose (Docker Compose / Stack)

### Create compose
```
POST /api/compose.create
Body: {
  "name": "string",                    // required
  "environmentId": "string",           // required  
  "appName": "string",
  "description": "string|null",
  "composeType": "docker-compose"|"stack",
  "composeFile": "string",             // the docker-compose.yml content
  "serverId": "string|null"
}
```

### Get compose
```
GET /api/compose.one?composeId=xxx
```

### Update compose
```
POST /api/compose.update
Body: {
  "composeId": "string",              // required
  "name": "string",
  "appName": "string", 
  "description": "string|null",
  "env": "string|null",               // environment variables
  "composeFile": "string",
  "sourceType": "git"|"github"|"gitlab"|"bitbucket"|"gitea"|"raw",
  "composeType": "docker-compose"|"stack",
  "composePath": "string",
  "suffix": "string",
  "randomize": "boolean",
  "isolatedDeployment": "boolean",
  "isolatedDeploymentsVolume": "boolean",
  "command": "string",
  "autoDeploy": "boolean|null",
  "triggerType": "push"|"tag"|null,
  // ... same git provider fields as application.update
}
```

### Environment variables
```
POST /api/compose.saveEnvironment
Body: {"composeId": "string", "env": "string|null"}
```

### Lifecycle
```
POST /api/compose.deploy    → {"composeId": "string", "title": "string", "description": "string"}
POST /api/compose.redeploy  → {"composeId": "string"}
POST /api/compose.start     → {"composeId": "string"}
POST /api/compose.stop      → {"composeId": "string"}
POST /api/compose.delete    → {"composeId": "string"}
POST /api/compose.move      → {"composeId": "string", "targetEnvironmentId": "string"}
POST /api/compose.cancelDeployment → {"composeId": "string"}
POST /api/compose.refreshToken → {"composeId": "string"}
POST /api/compose.cleanQueues → {"composeId": "string"}
POST /api/compose.clearDeployments → {"composeId": "string"}
POST /api/compose.killBuild → {"composeId": "string"}
POST /api/compose.disconnectGitProvider → {"composeId": "string"}
```

### Compose introspection
```
GET /api/compose.loadServices?composeId=xxx                  // list services in compose (needs deployed compose)
GET /api/compose.loadMountsByService?composeId=xxx&serviceName=xxx  // mounts for a service
GET /api/compose.getConvertedCompose?composeId=xxx           // get rendered compose file (returns string, may return literal "null" if not yet deployed)
GET /api/compose.getDefaultCommand?composeId=xxx
POST /api/compose.fetchSourceType → {"composeId": "string"}
POST /api/compose.randomizeCompose → {"composeId": "string"}
POST /api/compose.isolatedDeployment → {"composeId": "string"}
```

### Templates
```
GET /api/compose.templates
GET /api/compose.getTags
POST /api/compose.deployTemplate
Body: {"environmentId": "string", "id": "string", "serverId": "string", "baseUrl": "string"}
**`serverId` is required — pass `""` (empty string) if you don't have a remote server, NOT `null`.**
POST /api/compose.processTemplate
Body: {"base64": "string", "composeId": "string"}
POST /api/compose.import
Body: {"base64": "string", "composeId": "string"}
```

### Search
```
GET /api/compose.search?query=xxx
```
**Returns `{"message":"Not found"}` when no results** — treat as empty list.
