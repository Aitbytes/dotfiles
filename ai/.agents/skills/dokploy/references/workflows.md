## Common Workflows

### 1. Create a new project with an application
```bash
# Create project (response is nested: {project: {...}, environment: {...}})
PROJ=$(curl -s -X POST "$DOKPLOY_URL/api/project.create" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Project","description":"Project description"}')
ENV_ID=$(echo "$PROJ" | jq -r '.environment.environmentId')
PROJ_ID=$(echo "$PROJ" | jq -r '.project.projectId')

# Create application in project's default environment
curl -s -X POST "$DOKPLOY_URL/api/application.create" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-app","environmentId":"'"$ENV_ID"'"}'

# Set GitHub repo
curl -s -X POST "$DOKPLOY_URL/api/application.saveGithubProvider" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"applicationId":"<app-id>","repository":"my-repo","owner":"my-org","branch":"main","buildPath":"/"}'

# Set env vars
curl -s -X POST "$DOKPLOY_URL/api/application.saveEnvironment" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"applicationId":"<app-id>","env":"PORT=3000\nNODE_ENV=production","buildArgs":null,"buildSecrets":null,"createEnvFile":true}'

# Add domain
curl -s -X POST "$DOKPLOY_URL/api/domain.create" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"host":"myapp.example.com","port":3000,"https":true,"applicationId":"<app-id>","certificateType":"letsencrypt"}'

# Deploy
curl -s -X POST "$DOKPLOY_URL/api/application.deploy" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"applicationId":"<app-id>"}'
```

### 2. Update env vars and redeploy
```bash
# Get current app to read env
APP=$(curl -s "$DOKPLOY_URL/api/application.one?applicationId=<app-id>" -H "x-api-key: $DOKPLOY_API_KEY")
# Modify env string, then:
curl -s -X POST "$DOKPLOY_URL/api/application.saveEnvironment" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"applicationId":"<app-id>","env":"NEW_VAR=value\n'"$EXISTING_ENV"'","buildArgs":null,"buildSecrets":null,"createEnvFile":true}'

curl -s -X POST "$DOKPLOY_URL/api/application.redeploy" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"applicationId":"<app-id>"}'
```

### 3. View logs
```bash
curl -s "$DOKPLOY_URL/api/application.readLogs?applicationId=<app-id>&tail=200&since=1h" \
  -H "x-api-key: $DOKPLOY_API_KEY"
```

### 4. Stop/start services
```bash
curl -s -X POST "$DOKPLOY_URL/api/application.stop" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"applicationId":"<app-id>"}'

curl -s -X POST "$DOKPLOY_URL/api/application.start" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"applicationId":"<app-id>"}'
```

### 5. Create a PostgreSQL database
```bash
curl -s -X POST "$DOKPLOY_URL/api/postgres.create" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"My DB","environmentId":"<env-id>","databaseName":"mydb","databaseUser":"admin","databasePassword":"securepass123"}'
# Password constraints: no $ ! ' " \ / or spaces

curl -s -X POST "$DOKPLOY_URL/api/postgres.deploy" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"postgresId":"<postgres-id>"}'
```

### 6. Create a docker-compose deployment
```bash
COMPOSE_FILE=$(cat docker-compose.yml)

curl -s -X POST "$DOKPLOY_URL/api/compose.create" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg cf "$COMPOSE_FILE" '{name:"My Stack",environmentId:"<env-id>",composeType:"docker-compose",composeFile:$cf}')"

curl -s -X POST "$DOKPLOY_URL/api/compose.deploy" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"composeId":"<compose-id>"}'
```

### 7. Move a service to a different environment
```bash
curl -s -X POST "$DOKPLOY_URL/api/application.move" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"applicationId":"<app-id>","targetEnvironmentId":"<new-env-id>"}'
```
**Note:** All `.move` endpoints use `targetEnvironmentId`, not `environmentId`. This applies to applications, databases, and compose.

### 8. Set up a backup
```bash
# First check available destinations (destinationId is REQUIRED)
curl -s "$DOKPLOY_URL/api/destination.all" -H "x-api-key: $DOKPLOY_API_KEY"

# Create backup
curl -s -X POST "$DOKPLOY_URL/api/backup.create" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"schedule":"0 2 * * *","enabled":true,"prefix":"daily","destinationId":"<dest-id>","keepLatestCount":7,"database":"mydb","databaseType":"postgres","postgresId":"<pg-id>"}'
```
