## Backups

### Create and manage backups
```
POST /api/backup.create
Body: {"schedule": "string", "enabled": "boolean|null", "prefix": "string", "destinationId": "string", "keepLatestCount": "number|null", "database": "string", "databaseType": "postgres"|"mariadb"|"mysql"|"mongo"|"web-server", "backupType": "database"|"compose", "postgresId": "string|null", "mysqlId": "string|null", "mariadbId": "string|null", "mongoId": "string|null", "composeId": "string|null", "serviceName": "string|null", "userId": "string|null", "metadata": "object|null"}

GET /api/backup.one?backupId=xxx
POST /api/backup.update
POST /api/backup.remove    → {"backupId": "string"}
GET /api/backup.listBackupFiles?destinationId=xxx&search=xxx&serverId=xxx
```
**`destinationId` is required** — a backup destination must exist first. Create one via `POST /api/destination.create` if you don't have one.

### Manual backups
```
POST /api/backup.manualBackupPostgres → {"postgresId": "string", "backupId": "string"}
POST /api/backup.manualBackupMySql    → {"mysqlId": "string", "backupId": "string"}
POST /api/backup.manualBackupMariadb  → {"mariadbId": "string", "backupId": "string"}
POST /api/backup.manualBackupMongo    → {"mongoId": "string", "backupId": "string"}
POST /api/backup.manualBackupCompose  → {"composeId": "string", "backupId": "string"}
POST /api/backup.manualBackupWebServer → {"backupId": "string"}
```
**Manual backups require an existing backup config** — create the backup via `POST /api/backup.create` first, then trigger a manual run using the returned `backupId`.

## Destinations (Backup Storage)

```
POST /api/destination.create  → {"name": "string", "provider": "..."}
POST /api/destination.testConnection
GET /api/destination.one?destinationId=xxx
GET /api/destination.all
POST /api/destination.remove  → {"destinationId": "string"}
POST /api/destination.update
```

## Volume Backups

```
GET /api/volumeBackups.list
GET /api/volumeBackups.one?volumeBackupId=xxx
POST /api/volumeBackups.create
POST /api/volumeBackups.update
POST /api/volumeBackups.delete → {"volumeBackupId": "string"}
POST /api/volumeBackups.runManually → {"volumeBackupId": "string"}
```
