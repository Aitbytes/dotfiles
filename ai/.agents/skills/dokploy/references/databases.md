## Databases

All database types (MySQL, PostgreSQL, Redis, MongoDB, MariaDB) follow the same pattern.

### Password constraints

Database passwords **must not** contain these characters: `$ ! ' " \ /` or spaces. Using them causes a validation error:
`"Password contains invalid characters. Please avoid: $ ! ' " \ /` and space characters for database compatibility"`

### Create database
```
POST /api/{type}.create
```
Required fields vary by type:

**MySQL / PostgreSQL:**
```json
{"name": "str", "environmentId": "str", "databaseName": "str", "databaseUser": "str", "databasePassword": "str", "appName": "str", "description": "str|null", "dockerImage": "image:tag", "serverId": "str|null"}
```
MySQL also accepts: `"databaseRootPassword": "string"`

**MongoDB:**
```json
{"name": "str", "environmentId": "str", "databaseUser": "str", "databasePassword": "str", "appName": "str", "description": "str|null", "dockerImage": "mongo:7", "serverId": "str|null", "replicaSets": "boolean|null"}
```

**Redis:**
```json
{"name": "str", "environmentId": "str", "databasePassword": "str", "appName": "str", "description": "str|null", "dockerImage": "redis:8", "serverId": "str|null"}
```

**MariaDB:**
```json
{"name": "str", "environmentId": "str", "databaseName": "str", "databaseUser": "str", "databasePassword": "str", "databaseRootPassword": "str", "appName": "str", "description": "str|null", "dockerImage": "mariadb:11", "serverId": "str|null"}
```

> **Default Docker images:** The default images shown in the UI (`mongo:15`, `mariadb:6`) may not exist on Docker Hub. If you omit `dockerImage`, double-check that the auto-populated tag actually exists. Known working defaults: MongoDB → `7`, MariaDB → `11`, PostgreSQL → `15`, MySQL → `8`, Redis → `8`.

### Get database
```
GET /api/{type}.one?{type}Id=xxx
```

### Update database
```
POST /api/{type}.update
Body: {"{type}Id": "string", ...same fields as create plus: "command":"string|null","args":["string"]|null,"env":"string|null","externalPort":"number|null","memoryReservation":"string|null","memoryLimit":"string|null","cpuReservation":"string|null","cpuLimit":"string|null","applicationStatus":"idle"|"running"|"done"|"error","replicas":"number", "environmentId":"string", "createdAt":"string"}
```

### Lifecycle
```
POST /api/{type}.deploy       → {"{type}Id": "string"}
POST /api/{type}.start        → {"{type}Id": "string"}
POST /api/{type}.stop         → {"{type}Id": "string"}
POST /api/{type}.reload       → {"{type}Id": "string", "appName": "string"}   // appName is REQUIRED for reload
POST /api/{type}.remove       → {"{type}Id": "string"}
POST /api/{type}.rebuild      → {"{type}Id": "string"}
POST /api/{type}.changeStatus → {"{type}Id": "string", "applicationStatus": "..."}
POST /api/{type}.move         → {"{type}Id": "string", "targetEnvironmentId": "string"}
POST /api/{type}.saveExternalPort → {"{type}Id": "string", "externalPort": "number"}
POST /api/{type}.saveEnvironment  → {"{type}Id": "string", "env": "string|null"}
```

### Search
```
GET /api/{type}.search?query=xxx
```
**Returns `{"message":"Not found"}` when no results** — treat as empty list.
