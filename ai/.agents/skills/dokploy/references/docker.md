## Docker / Container Operations

```
GET /api/docker.getContainers?serverId=xxx          // list all containers
GET /api/docker.getContainersByAppNameMatch?appName=xxx&appType=stack|docker-compose&serverId=xxx
GET /api/docker.getContainersByAppLabel?appName=xxx&type=standalone|swarm&serverId=xxx
GET /api/docker.getServiceContainersByAppName?appName=xxx&serverId=xxx
GET /api/docker.getStackContainersByAppName?appName=xxx&serverId=xxx
GET /api/docker.getConfig?containerId=xxx&serverId=xxx
POST /api/docker.restartContainer → {"containerId": "string"}
```
