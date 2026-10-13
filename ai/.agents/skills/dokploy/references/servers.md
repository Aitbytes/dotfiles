## Servers

```
GET /api/server.all
GET /api/server.one?serverId=xxx
GET /api/server.count
GET /api/server.withSSHKey
GET /api/server.buildServers
POST /api/server.create
POST /api/server.setup
GET /api/server.validate
POST /api/server.remove → {"serverId": "string"}
POST /api/server.update
GET /api/server.publicIp
GET /api/server.getServerTime
GET /api/server.getServerMetrics
POST /api/server.setupMonitoring → {"serverId": "string"}
GET /api/server.getDefaultCommand?serverId=xxx
GET /api/server.security
```
