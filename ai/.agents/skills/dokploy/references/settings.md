## Settings

### Health & Info
```
GET /api/settings.health
GET /api/settings.getDokployVersion
GET /api/settings.getReleaseTag
GET /api/settings.isCloud
GET /api/settings.getIp
```

### Traefik Configuration
```
GET /api/settings.readTraefikConfig
POST /api/settings.updateTraefikConfig → {"traefikConfig": "string"}
GET /api/settings.readWebServerTraefikConfig
POST /api/settings.updateWebServerTraefikConfig → {"traefikConfig": "string"}
GET /api/settings.readMiddlewareTraefikConfig
POST /api/settings.updateMiddlewareTraefikConfig → {"traefikConfig": "string"}
POST /api/settings.reloadTraefik
GET /api/settings.haveTraefikDashboardPortEnabled
POST /api/settings.updateTraefikPorts → {"httpPort": "number", "httpsPort": "number"}
GET /api/settings.getTraefikPorts
GET /api/settings.readTraefikEnv
POST /api/settings.writeTraefikEnv → {"env": "string"}
```

### Server IP / Domain
```
POST /api/settings.updateServerIp → {"serverIp": "string"}
POST /api/settings.assignDomainServer → {"host": "string"}
```

### Maintenance / Redis
```
POST /api/settings.reloadServer
POST /api/settings.cleanRedis
POST /api/settings.reloadRedis
POST /api/settings.cleanAllDeploymentQueue
```

### Docker Cleanup
```
POST /api/settings.cleanUnusedImages
POST /api/settings.cleanUnusedVolumes
POST /api/settings.cleanStoppedContainers
POST /api/settings.cleanDockerBuilder
POST /api/settings.cleanDockerPrune
POST /api/settings.cleanAll
POST /api/settings.cleanMonitoring
```

### Docker Cleanup Schedule
```
POST /api/settings.updateDockerCleanup → {"cronExpression": "string"}
POST /api/settings.updateLogCleanup → {"cronExpression": "string", "maxAgeDays": "number"}
GET /api/settings.getLogCleanupStatus
```
