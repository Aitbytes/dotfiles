## Domains

```
POST /api/domain.create
Body: {"host": "string", "path": "string|null", "port": "number|null", "https": "boolean", "applicationId": "string|null", "composeId": "string|null", "serviceName": "string|null", "certificateType": "letsencrypt"|"none"|"custom", "customCertResolver": "string|null", "domainType": "compose"|"application"|"preview"|null, "previewDeploymentId": "string|null", "internalPath": "string|null", "stripPath": "boolean"}

GET /api/domain.one?domainId=xxx
GET /api/domain.byApplicationId?applicationId=xxx
GET /api/domain.byComposeId?composeId=xxx
POST /api/domain.update
POST /api/domain.delete        → {"domainId": "string"}
POST /api/domain.generateDomain
GET /api/domain.canGenerateTraefikMeDomains
POST /api/domain.validateDomain → {"host": "string"}
```

## Certificates

```
GET /api/certificates.all
GET /api/certificates.one?certificateId=xxx
POST /api/certificates.create
Body: {"name": "string", "certificateData": "string", "privateKey": "string", "autoRenew": "boolean|null", "organizationId": "string", "serverId": "string|null", "certificatePath": "string"}
POST /api/certificates.remove → {"certificateId": "string"}
```
