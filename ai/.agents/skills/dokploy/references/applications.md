## Applications

### Create application
```
POST /api/application.create
Body: {
  "name": "string",           // required
  "environmentId": "string",  // required
  "appName": "string",        // optional, auto-generated if omitted
  "description": "string|null",
  "serverId": "string|null"   // for remote servers
}
```

### Get application details
```
GET /api/application.one?applicationId=xxx
```
Returns full details including source type, repository config, env vars, build type, status, domains, etc.

### Update application
```
POST /api/application.update
Body: {
  "applicationId": "string",  // required - identifies the app to update
  
  // Basic
  "name": "string",
  "appName": "string",
  "description": "string|null",
  "enabled": "boolean|null",
  "command": "string|null",
  "args": ["string"]|null,
  
  // Source & build
  "sourceType": "github"|"docker"|"git"|"gitlab"|"bitbucket"|"gitea"|"drop",
  "buildType": "dockerfile"|"heroku_buildpacks"|"paketo_buildpacks"|"nixpacks"|"static"|"railpack",
  "repository": "string|null",
  "owner": "string|null",
  "branch": "string|null",
  "buildPath": "string|null",
  "dockerfile": "string|null",
  "dockerContextPath": "string|null",
  "dockerBuildStage": "string|null",
  "dockerImage": "string|null",
  "registryId": "string|null",
  "triggerType": "push"|"tag",
  "autoDeploy": "boolean|null",
  "cleanCache": "boolean|null",
  "enableSubmodules": "boolean",
  
  // Git providers (use the specific one based on sourceType)
  "githubId": "string|null",
  "gitlabId": "string|null",
  "bitbucketId": "string|null",
  "giteaId": "string|null",
  "gitlabProjectId": "number|null",
  "gitlabRepository": "string|null",
  "gitlabOwner": "string|null",
  "gitlabBranch": "string|null",
  "gitlabBuildPath": "string|null",
  "gitlabPathNamespace": "string|null",
  "bitbucketRepository": "string|null",
  "bitbucketOwner": "string|null",
  "bitbucketBranch": "string|null",
  "bitbucketBuildPath": "string|null",
  "bitbucketRepositorySlug": "string|null",
  "giteaRepository": "string|null",
  "giteaOwner": "string|null",
  "giteaBranch": "string|null",
  "giteaBuildPath": "string|null",
  "customGitUrl": "string|null",
  "customGitBranch": "string|null",
  "customGitBuildPath": "string|null",
  "customGitSSHKeyId": "string|null",
  
  // Docker registry auth
  "username": "string|null",
  "password": "string|null",
  "registryUrl": "string|null",
  
  // Build-specific
  "publishDirectory": "string|null",
  "isStaticSpa": "boolean|null",
  "herokuVersion": "string|null",
  "railpackVersion": "string|null",
  "dropBuildPath": "string|null",
  
  // Resources
  "memoryReservation": "string|null",
  "memoryLimit": "string|null",
  "cpuReservation": "string|null",
  "cpuLimit": "string|null",
  "replicas": "number",
  
  // Docker Swarm advanced (all optional/nullable)
  "healthCheckSwarm": object|null,
  "restartPolicySwarm": object|null,
  "placementSwarm": object|null,
  "updateConfigSwarm": object|null,
  "rollbackConfigSwarm": object|null,
  "modeSwarm": object|null,
  "labelsSwarm": object|null,
  "networkSwarm": array|null,
  "stopGracePeriodSwarm": number|null,
  "endpointSpecSwarm": object|null,
  "ulimitsSwarm": array|null,
  
  // Other
  "buildServerId": "string|null",
  "buildRegistryId": "string|null",
  "environmentId": "string",
  "refreshToken": "string|null",
  "title": "string|null",
  "subtitle": "string|null",
  "applicationStatus": "idle"|"running"|"done"|"error",
  "createEnvFile": "boolean",
  "rollbackActive": "boolean",
  "registryId": "string|null",
  "rollbackRegistryId": "string|null",
  "createdAt": "string"
}
```
When changing source type, set the old provider fields to null and populate the new ones.

### Set environment variables
```
POST /api/application.saveEnvironment
Body: {
  "applicationId": "string",
  "env": "KEY=value\nKEY2=value2",   // newline-separated env vars
  "buildArgs": "string|null",
  "buildSecrets": "string|null",
  "createEnvFile": true
}
```
This REPLACES the entire env - include all existing vars you want to keep.

### Set git source (GitHub)
```
POST /api/application.saveGithubProvider
Body: {
  "applicationId": "string",
  "repository": "string|null",
  "owner": "string|null",
  "branch": "string|null",
  "buildPath": "string|null",
  "githubId": "string|null"
}
```
Similar endpoints: `saveGitlabProvider`, `saveBitbucketProvider`, `saveGiteaProvider`, `saveGitProvider`, `saveDockerProvider`.

### Set build type
```
POST /api/application.saveBuildType
Body: {
  "applicationId": "string",
  "buildType": "dockerfile"|"heroku_buildpacks"|"paketo_buildpacks"|"nixpacks"|"static"|"railpack",
  "dockerfile": "string|null",
  "dockerContextPath": "string|null",
  "dockerBuildStage": "string|null",   // REQUIRED when buildType is "dockerfile" — pass null if not needed
  "publishDirectory": "string|null",
  "herokuVersion": "string|null",
  "railpackVersion": "string|null",
  "isStaticSpa": "boolean|null"
}
```

### Lifecycle operations
```
POST /api/application.deploy     → {"applicationId": "string", "title": "string", "description": "string"}
POST /api/application.redeploy   → {"applicationId": "string"}
POST /api/application.start      → {"applicationId": "string"}
POST /api/application.stop       → {"applicationId": "string"}
POST /api/application.reload     → {"applicationId": "string"}
POST /api/application.delete     → {"applicationId": "string"}
POST /api/application.markRunning → {"applicationId": "string"}
POST /api/application.move       → {"applicationId": "string", "targetEnvironmentId": "string"}
POST /api/application.cancelDeployment → {"applicationId": "string"}
POST /api/application.refreshToken → {"applicationId": "string"}
POST /api/application.killBuild  → {"applicationId": "string"}
POST /api/application.cleanQueues → {"applicationId": "string"}
POST /api/application.clearDeployments → {"applicationId": "string"}
```

### Read logs
```
GET /api/application.readLogs?applicationId=xxx&tail=100&since=all
```
Parameters: `applicationId` (required), `tail` (default 100, max 10000), `since` (default "all", format: "all" or "Nd" "Nh" "Nm" "Ns"), `search` (optional filter string).

**Note:** Logs are only available after a deployment has been attempted. Returns `{"message":"Not found"}` if no logs exist yet.

### Disconnect git provider
```
POST /api/application.disconnectGitProvider
Body: {"applicationId": "string"}
```

### Search applications
```
GET /api/application.search?query=xxx
```

### Read application monitoring / Traefik
```
GET /api/application.readAppMonitoring?appName=xxx
GET /api/application.readTraefikConfig?applicationId=xxx
POST /api/application.updateTraefikConfig
Body: {"applicationId": "string", "traefikConfig": "string"}
```

### Preview deployments (application-specific)
```
GET /api/previewDeployment.all?applicationId=xxx
GET /api/previewDeployment.one?previewDeploymentId=xxx
POST /api/previewDeployment.delete → {"previewDeploymentId": "string"}
POST /api/previewDeployment.redeploy → {"previewDeploymentId": "string"}
```
