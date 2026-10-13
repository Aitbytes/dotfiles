# AI Features — Full Reference

Load this when you need: AI-powered next action suggestions, inbox batch capture, project scaffolding, or AI chat.

## AI Context (Next Actions)

Get AI-powered suggestions for what to work on next, based on available context, energy, and time.

```bash
GET /api/ai/context
# Optional: ?contexts=@Computer,@Home&energyLevel=medium&availableTime=30
```

Returns recommended tasks given the constraints.

## AI Inbox Capture (Batch)

Batch-capture multiple thoughts into inbox in a single call.

```bash
POST /api/ai/inbox/capture
-d '{"items": ["Fix leaking faucet", "Buy groceries", "Review Q3 budget"]}'
```

Each string becomes an inbox item.

## AI Project Scaffolding

Get AI-suggested task breakdown for a project.

```bash
POST /api/ai/scaffold-project
-d '{"projectTitle": "Launch new product",
     "projectDescription": "A detailed description...",
     "tasks": [{"title": "Market research"}, {"title": "Prototype"}, {"title": "User testing"}]}'
```

Returns enriched task suggestions with estimates, sequencing, and context assignments.

## AI Chat

Streaming SSE chat for GTD coaching and workflow assistance.

```bash
POST /api/ai/chat
-d '{"messages": [{"role": "user", "content": "What should I focus on today?"}],
     "context": "I have 2 hours available and I'\''m at my computer."}'
```

Returns a server-sent event (SSE) stream with the AI response.
