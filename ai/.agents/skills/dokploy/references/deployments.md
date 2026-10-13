## Deployments

```
GET /api/deployment.all?applicationId=xxx           // deployments for an application
GET /api/deployment.allByCompose?composeId=xxx       // deployments for a compose
GET /api/deployment.allByServer?serverId=xxx
GET /api/deployment.allCentralized
GET /api/deployment.queueList
GET /api/deployment.allByType?id=xxx&type=xxx      // type: "application"|"compose"|"previewDeployment"
POST /api/deployment.killProcess → {"deploymentId": "string"}
POST /api/deployment.removeDeployment → {"deploymentId": "string"}
```

Use `deployment.all` with the applicationId to monitor deployment progress.
