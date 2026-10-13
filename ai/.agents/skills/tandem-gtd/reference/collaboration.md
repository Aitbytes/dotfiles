# Collaboration — Full Reference

Load this when you need: teams, discussion threads, or structured decision-making.

## Teams

Collaboration teams for shared projects.

### Endpoints

```bash
# List teams
GET /api/teams

# Create team
POST /api/teams
-d '{"name": "Engineering", "description": "Engineering team projects", "icon": "🚀"}'

# Get/update/delete
GET /api/teams/{id}
PATCH /api/teams/{id} -d '{"name": "Engineering Team"}'
DELETE /api/teams/{id}'
```

### Team Members

```bash
# Add member by email or userId
POST /api/teams/{id}/members
-d '{"email": "colleague@example.com", "role": "MEMBER"}'
# or: {"userId": "<user-id>", "role": "ADMIN"}

# Update member role
PATCH /api/teams/{id}/members/{userId} -d '{"role": "ADMIN"}'

# Remove member
DELETE /api/teams/{id}/members/{userId}
```

**Roles:** `MEMBER`, `ADMIN`

---

## Threads

Discussion threads on tasks or projects within teams.

### Endpoints

```bash
# Create thread (requires taskId OR projectId)
POST /api/threads
-d '{"title": "What approach for the API?",
     "purpose": "QUESTION",
     "projectId": "<project-id>",
     "content": "Should we use REST or GraphQL?"}'

# Get thread with messages
GET /api/threads/{id}

# Resolve thread
PATCH /api/threads/{id} -d '{"resolve": true}'

# Delete thread
DELETE /api/threads/{id}'
```

**Purpose values:** `QUESTION`, `BLOCKER`, `UPDATE`, `FYI`

### Messages

```bash
# Add message to thread
POST /api/threads/{id}/messages
-d '{"content": "I think REST is simpler for our use case."}'

# Edit message
PATCH /api/threads/{id}/messages/{mid} -d '{"content": "Updated reply"}'

# Delete message
DELETE /api/threads/{id}/messages/{mid}
```

### Mentions & Thread Lists

```bash
# Threads mentioning current user
GET /api/threads/mentions

# Threads on a specific project/task
GET /api/projects/{id}/threads
GET /api/tasks/{id}/threads
```

---

## Decisions

Structured decision-making with approval or poll types.

### Poll Decision

```bash
POST /api/decisions
-d '{"question": "Which CMS should we use?",
     "decisionType": "POLL",
     "projectId": "<project-id>",
     "respondentUserIds": ["<user-id>"],
     "options": [
       {"label": "WordPress", "description": "Mature ecosystem"},
       {"label": "Strapi", "description": "Headless CMS"}
     ],
     "deadline": "2026-06-20T00:00:00.000Z"}'
```

### Approval Decision

```bash
POST /api/decisions
-d '{"question": "Approve Q3 budget?",
     "decisionType": "APPROVAL",
     "projectId": "<project-id>",
     "respondentUserIds": ["<user-id>"]}'
```

### Voting & Resolution

```bash
# Get decision details
GET /api/decisions/{id}

# Resolve decision
PATCH /api/decisions/{id}
-d '{"resolution": "Going with Strapi", "chosenOptionId": "<option-id>"}'

# Withdraw
PATCH /api/decisions/{id} -d '{"withdraw": true}'

# Vote on approval: APPROVE, REJECT, COMMENT, DEFER
POST /api/decisions/{id}/respond
-d '{"vote": "APPROVE", "comment": "Looks good"}'

# Vote on poll
POST /api/decisions/{id}/vote-option
-d '{"optionId": "<option-id>"}'
```

### Listing Decisions

```bash
# Pending decisions for current user
GET /api/decisions/pending

# Decisions on project/team
GET /api/projects/{id}/decisions
GET /api/teams/{id}/decisions
```
