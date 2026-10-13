---
name: dokploy
description: Manage Dokploy deployments via its REST API. Create/read/update/delete projects, applications (with repo assignment), databases (MySQL, PostgreSQL, Redis, MongoDB, MariaDB), compose stacks, environment variables, domains, backups, and more. Deploy, redeploy, stop, start, view logs, and monitor all from the CLI.
---

# Dokploy API Skill

Manage Dokploy deployments via its REST API. Dokploy is a self-hosted deployment platform that manages applications, databases, docker-compose stacks, backups, domains, and more.

**This file is an index.** Read the relevant sub-file(s) for your task before making API calls.

For detailed API documentation, read the relevant reference file(s) for your task:

| Task | Read |
|------|------|
| Authentication, URL conventions, resource hierarchy | [references/prerequisites.md](references/prerequisites.md) |
| Discover projects, environments, services (primary entry point) | [references/discovery.md](references/discovery.md) |
| Projects (create, get, update, delete, duplicate) | [references/projects.md](references/projects.md) |
| Environments (create, get, update, delete) | [references/environments.md](references/environments.md) |
| Applications (all operations: CRUD, deploy, env vars, git, build type, logs, move, etc.) | [references/applications.md](references/applications.md) |
| Docker Compose / Stack deployments | [references/compose.md](references/compose.md) |
| Databases (MySQL, PostgreSQL, Redis, MongoDB, MariaDB) | [references/databases.md](references/databases.md) |
| Docker container inspection | [references/docker.md](references/docker.md) |
| Deployments (list, monitor, kill) | [references/deployments.md](references/deployments.md) |
| Domains and TLS certificates | [references/domains.md](references/domains.md) |
| Backups (scheduled + manual) and destinations | [references/backups.md](references/backups.md) |
| Servers (list, create, setup, metrics) | [references/servers.md](references/servers.md) |
| Settings (health, Traefik, maintenance, cleanup) | [references/settings.md](references/settings.md) |
| SSH keys, Git providers, certificates, mounts, rollbacks, schedules, volume backups, notifications | [references/misc.md](references/misc.md) |
| Step-by-step workflows (new project + app, env vars, logs, database creation, compose deployment, moving services, backups) | [references/workflows.md](references/workflows.md) |
| Python helper client class | [references/python_helper.md](references/python_helper.md) |
| Tips and best practices | [references/tips.md](references/tips.md) |

**Always start with [references/discovery.md](references/discovery.md)** to find IDs of resources you need.
