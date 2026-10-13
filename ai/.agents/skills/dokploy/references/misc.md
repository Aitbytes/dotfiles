## SSH Keys

```
GET /api/sshKey.all
GET /api/sshKey.one?sshKeyId=xxx
POST /api/sshKey.create
POST /api/sshKey.generate
POST /api/sshKey.update
POST /api/sshKey.remove → {"sshKeyId": "string"}
```

## Git Providers

```
GET /api/gitProvider.getAll
POST /api/gitProvider.remove → {"gitProviderId": "string"}

# GitHub
GET /api/github.one?githubId=xxx
GET /api/github.githubProviders
GET /api/github.getGithubRepositories?githubId=xxx
GET /api/github.getGithubBranches?githubId=xxx&owner=xxx&repo=xxx
POST /api/github.testConnection
POST /api/github.update

# GitLab
GET /api/gitlab.one?gitlabId=xxx
GET /api/gitlab.gitlabProviders
GET /api/gitlab.getGitlabRepositories?gitlabId=xxx
GET /api/gitlab.getGitlabBranches?gitlabId=xxx&projectId=xxx
POST /api/gitlab.testConnection
POST /api/gitlab.update

# Bitbucket, Gitea follow same pattern
```

## Mounts

```
POST /api/mounts.create
Body: {"type": "bind"|"volume"|"file", "hostPath": "string|null", "volumeName": "string|null", "content": "string|null", "mountPath": "string", "serviceType": "application"|"postgres"|"mysql"|"mariadb"|"mongo"|"redis"|"compose", "serviceId": "string", "applicationId": "string|null", "postgresId": "string|null", "mysqlId": "string|null", "mariadbId": "string|null", "mongoId": "string|null", "redisId": "string|null", "composeId": "string|null"}
```
**`serviceId` is required** — this is the ID of the service the mount belongs to (same as the specific `{type}Id` field like `postgresId`). Set both `serviceId` and the specific type ID field.

```
GET /api/mounts.one?mountId=xxx
POST /api/mounts.update
POST /api/mounts.remove → {"mountId": "string"}
GET /api/mounts.allNamedByApplicationId?applicationId=xxx
GET /api/mounts.listByServiceId?composeId=xxx&serviceName=xxx
```

## Rollbacks

```
POST /api/rollback.rollback → {"applicationId": "string", "rollbackId": "string"}
POST /api/rollback.delete   → {"rollbackId": "string"}
```

## Schedules (Cron Jobs)

```
GET /api/schedule.list?id=xxx&scheduleType=application|compose|server|dokploy-server
GET /api/schedule.one?scheduleId=xxx
POST /api/schedule.create
Body: {"name": "string", "cronExpression": "string", "command": "string", "scheduleType": "application"|"compose"|"server"|"dokploy-server", "applicationId": "string|null", "composeId": "string|null", "serverId": "string|null", "serviceName": "string|null", "enabled": "boolean", "script": "string|null", "shellType": "bash"|"sh", "timezone": "string|null", "userId": "string|null"}
POST /api/schedule.update
POST /api/schedule.delete → {"scheduleId": "string"}
POST /api/schedule.runManually → {"scheduleId": "string"}
```

## Notifications

```
GET /api/notification.all
GET /api/notification.one?notificationId=xxx
POST /api/notification.remove → {"notificationId": "string"}

# Per-provider create/test/update:
POST /api/notification.createSlack / .testSlackConnection / .updateSlack
POST /api/notification.createTelegram / .testTelegramConnection / .updateTelegram
POST /api/notification.createDiscord / .testDiscordConnection / .updateDiscord
POST /api/notification.createEmail / .testEmailConnection / .updateEmail
POST /api/notification.createResend / .testResendConnection / .updateResend
POST /api/notification.createGotify / .testGotifyConnection / .updateGotify
POST /api/notification.createNtfy / .testNtfyConnection / .updateNtfy
POST /api/notification.createCustom / .testCustomConnection / .updateCustom
POST /api/notification.createLark / .testLarkConnection / .updateLark
POST /api/notification.createTeams / .testTeamsConnection / .updateTeams
POST /api/notification.createPushover / .testPushoverConnection / .updatePushover
```

## User & API Keys

```
GET /api/user.getUserByToken?token=xxx   // token is REQUIRED as query param
GET /api/user.getMetricsToken
POST /api/user.generateToken    // generate new auth token
POST /api/user.createApiKey
Body: {"name": "string", "metadata": {"organizationId": "string"}, "prefix": "string", "expiresIn": "number", "rateLimitEnabled": "boolean", "rateLimitTimeWindow": "number", "rateLimitMax": "number", "remaining": "number", "refillAmount": "number", "refillInterval": "number"}
POST /api/user.deleteApiKey → {"apiKeyId": "string"}
```
