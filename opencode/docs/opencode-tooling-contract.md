# OpenCode Tooling Contract

Phase 2: Contract Design

## Purpose

This document defines the shared runtime contract for networked OpenCode custom tools.

It covers five things:

1. Shared result envelope
2. Error taxonomy
3. Proxy policy
4. Retry and backoff policy
5. Logging and diagnostic fields

This contract is intended to replace the current ad hoc behavior where wrappers return plain strings on failure and many Python implementations collapse transport failures into empty arrays.

## Goals

- Every custom tool returns one predictable JSON envelope.
- Agents can distinguish success, partial success, empty results, retryable failure, and hard failure without parsing prose.
- Network behavior is consistent across tools.
- Proxy usage is explicit and auditable.
- Retry behavior is deterministic and bounded.
- Diagnostics are rich enough for debugging but safe enough to return to agents.

## Non-Goals

- This phase does not choose the final reduced tool inventory.
- This phase does not define agent prompt changes.
- This phase does not require MCP servers to adopt the same envelope immediately.
- This phase does not expose secrets, raw proxy credentials, or full internal stack traces to agents.

## Contract Versioning

All custom tools should emit a versioned envelope.

- Contract version string: `tool-result/v1`
- Future breaking changes must increment the version.
- New additive fields may be introduced within `v1` if they are optional.

## Shared Result Envelope

Every custom tool must return a JSON object with this top-level shape.

```json
{
  "contract_version": "tool-result/v1",
  "ok": true,
  "status": "ok",
  "tool": "youtube",
  "action": "transcript",
  "provider": "youtube-transcript-api",
  "stage": "completed",
  "request_id": "01HTX3Q6T2K5W5Y6Y2B3N7D9QG",
  "duration_ms": 1842,
  "attempts": {
    "total": 2,
    "per_stage": {
      "discovery": 1,
      "transcript_fetch": 1
    }
  },
  "proxy": {
    "mode": "auto",
    "used": true,
    "source": "proxy-conf",
    "route": "redacted",
    "bypassed": false,
    "bypass_reason": null
  },
  "fallbacks": {
    "available": ["youtube-transcript", "youtube-transcript-api", "whisper"],
    "tried": ["youtube-transcript", "youtube-transcript-api"],
    "selected": "youtube-transcript-api"
  },
  "data": {},
  "error": null,
  "diagnostics": {}
}
```

### Required top-level fields

| Field              | Type                    | Meaning                                                                                                              |
| ------------------ | ----------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `contract_version` | string                  | Contract schema version. Always `tool-result/v1` for this phase.                                                     |
| `ok`               | boolean                 | True only when the tool completed successfully enough for the caller to use `data`.                                  |
| `status`           | enum                    | One of `ok`, `partial`, `empty`, `error`.                                                                            |
| `tool`             | string                  | Canonical tool name, not an alias.                                                                                   |
| `action`           | string                  | Logical operation performed by the tool, such as `search`, `lookup`, `fetch`, `transcript`, `resolve`.               |
| `provider`         | string or null          | Upstream provider or sub-provider used for the final result.                                                         |
| `stage`            | string                  | Final execution stage, such as `completed`, `discovery`, `fetch`, `parse`, `transcript_fetch`, `fallback`, `failed`. |
| `request_id`       | string                  | Unique per invocation. Stable across internal retries within the same call.                                          |
| `duration_ms`      | integer                 | End-to-end runtime in milliseconds.                                                                                  |
| `attempts`         | object                  | Retry and stage-attempt summary.                                                                                     |
| `proxy`            | object                  | Proxy routing summary with redacted values only.                                                                     |
| `fallbacks`        | object                  | Fallback availability and actual path taken.                                                                         |
| `data`             | object or array or null | Normalized success payload. Present for `ok`, `partial`, and `empty`.                                                |
| `error`            | object or null          | Structured failure object. Null only when there is no error condition.                                               |
| `diagnostics`      | object                  | Non-secret metadata useful for debugging, testing, and observability.                                                |

### Status semantics

| Status    | `ok`  | Meaning                                                                               |
| --------- | ----- | ------------------------------------------------------------------------------------- |
| `ok`      | true  | Successful execution with usable result data.                                         |
| `partial` | true  | Some useful result exists, but coverage is incomplete, degraded, or fallback-derived. |
| `empty`   | true  | Execution succeeded, but the source returned no matching data. This is not an error.  |
| `error`   | false | Execution failed or produced unusable output. `error` must be populated.              |

### Rules for `data`

- `data` must never contain free-form wrapper error text.
- `data` may be an empty array or object only when `status` is `empty` or the tool's normal successful shape is genuinely empty.
- `data` must remain domain-shaped. This contract standardizes the envelope, not every tool's payload schema.
- If partial results are usable, return them in `data` and set `status` to `partial` with a populated `error` explaining degradation.

### Rules for `error`

- `error` must be null when `status` is `ok` or `empty`.
- `error` may be present when `status` is `partial`.
- `error` must be present when `status` is `error`.
- `error.message` must be concise, factual, and machine-safe.
- `error.details` may include structured metadata, but never secrets, tokens, cookies, or proxy credentials.

## Error Taxonomy

Every failure or degradation must map to a stable `error.kind`.

### Error object shape

```json
{
  "kind": "rate_limited",
  "code": "YOUTUBE_429",
  "message": "Transcript endpoint returned HTTP 429",
  "retriable": true,
  "temporary": true,
  "stage": "transcript_fetch",
  "provider": "youtube-transcript-api",
  "http_status": 429,
  "retry_after_ms": 5000,
  "details": {
    "host": "www.youtube.com"
  }
}
```

### Error kinds

| Kind                 | Meaning                                                                                             | Retriable by default |
| -------------------- | --------------------------------------------------------------------------------------------------- | -------------------- |
| `invalid_input`      | Caller supplied invalid or incomplete arguments.                                                    | No                   |
| `config_error`       | Local configuration missing or invalid, such as absent API key or malformed config file.            | No                   |
| `dependency_error`   | Required local runtime dependency missing or failed to start.                                       | No                   |
| `proxy_config_error` | Proxy config exists but is malformed, unsupported, or unreadable.                                   | No                   |
| `proxy_auth_failed`  | Proxy rejected authentication or CONNECT.                                                           | Usually no           |
| `dns_failed`         | DNS resolution failed.                                                                              | Yes                  |
| `connect_failed`     | TCP/TLS connection could not be established.                                                        | Yes                  |
| `timeout`            | Upstream request or local subprocess exceeded budget.                                               | Yes                  |
| `rate_limited`       | Provider responded with 429 or equivalent quota/rate signal.                                        | Yes                  |
| `auth_required`      | Upstream requires authentication not supplied.                                                      | No                   |
| `forbidden`          | Upstream denied access with 403 or equivalent.                                                      | Usually no           |
| `not_found`          | Requested resource does not exist.                                                                  | No                   |
| `blocked`            | Bot protection, anti-automation, CAPTCHA, or challenge page detected.                               | Usually no           |
| `upstream_error`     | Upstream server returned 5xx or a non-specific provider failure.                                    | Yes                  |
| `protocol_error`     | Invalid HTTP response, malformed JSON, schema mismatch, or transport protocol violation.            | Sometimes            |
| `parse_error`        | Source fetched successfully but content could not be parsed into the expected structure.            | Sometimes            |
| `empty_result`       | Execution succeeded but no matching records were found. Use only with `status: empty`, not `error`. | Not applicable       |
| `partial_result`     | Useful data exists but one or more providers or stages failed. Use only with `status: partial`.     | Not applicable       |
| `internal_error`     | Unexpected local exception or uncategorized failure.                                                | Sometimes            |
| `policy_denied`      | Request blocked by local policy, such as proxy bypass rules or host restrictions.                   | No                   |

### Error classification rules

1. Never use a free-form exception string as the taxonomy.
2. `empty_result` and `partial_result` are semantic conditions, not hard failures.
3. HTTP status mapping should be normalized.
4. `400` maps to `invalid_input` if caused by caller input, otherwise `protocol_error`.
5. `401` maps to `auth_required`.
6. `403` maps to `forbidden`, unless challenge or CAPTCHA signals are detected, then it maps to `blocked`.
7. `404` maps to `not_found`.
8. `408` maps to `timeout`.
9. `409` maps to `upstream_error` unless provider semantics justify a narrower kind.
10. `429` maps to `rate_limited`.
11. `500-599` maps to `upstream_error`.
12. HTML challenge pages, CAPTCHA, or bot-detection markers classify as `blocked` even if the HTTP status is `200`.
13. Local missing modules, missing binaries, or subprocess spawn failures classify as `dependency_error`.
14. A provider returning malformed JSON after a valid fetch classifies as `protocol_error` or `parse_error`, not `internal_error`.

### Stage values

The `stage` field on both the envelope and the `error` object must come from a bounded set.

| Stage              | Meaning                                              |
| ------------------ | ---------------------------------------------------- |
| `validate_input`   | Input validation and normalization                   |
| `load_config`      | Local config load, env load, credential load         |
| `resolve_proxy`    | Proxy policy resolution                              |
| `build_request`    | URL, params, headers, or request object construction |
| `connect`          | DNS, TCP, TLS, proxy tunnel setup                    |
| `fetch`            | Upstream HTTP request in flight                      |
| `read_response`    | Response body download                               |
| `parse`            | Structured parsing or extraction                     |
| `discovery`        | Search or candidate discovery stage                  |
| `transcript_fetch` | Transcript retrieval stage                           |
| `fallback`         | Switching to alternate provider or strategy          |
| `serialize_output` | Formatting final payload                             |
| `completed`        | Successful completion                                |
| `failed`           | Terminal failure after attempts exhausted            |

### Partial result rules

Use `status: partial` when:

- one provider in a fallback chain failed but another produced usable data
- one page out of several failed but the rest succeeded
- metadata was fetched but detailed content was unavailable
- ASR fallback succeeded after first-party transcript providers failed

When `status` is `partial`:

- `ok` must be `true`
- `data` must contain the usable portion
- `error.kind` should usually be `partial_result`
- `diagnostics.partial_failures` should list the failed stages or providers

## Proxy Policy

All networked custom tools must use one shared proxy policy resolver.

### Policy goals

- One place to decide whether a request uses proxy or direct routing
- No implicit dependence on random ambient library defaults
- No secrets returned to the model
- Per-host and per-tool overrides supported
- Browser automation remains compatible with authenticated proxy limitations

### Proxy modes

| Mode       | Meaning                                                                                              |
| ---------- | ---------------------------------------------------------------------------------------------------- |
| `auto`     | Default. Use configured proxy when policy allows it; use direct routing for explicit bypass targets. |
| `required` | Fail if no usable proxy is configured. Do not silently fall back to direct.                          |
| `direct`   | Force direct connection; ignore configured proxy for this request.                                   |
| `disabled` | Same routing behavior as `direct`, but indicates proxy support is intentionally turned off globally. |

### Proxy sources

Proxy configuration should be resolved in this order:

1. Explicit runtime config for the shared execution layer
2. Dedicated proxy config file, currently `~/.config/proxy-conf`
3. Process environment variables such as `HTTP_PROXY` and `HTTPS_PROXY`

Rules:

- Credentials must be parsed and stored separately from the redacted route string.
- Returned diagnostics must never include raw username, password, token, or full proxy URL.
- If config file and environment disagree, the resolved source must be recorded in diagnostics.

### Default routing rules

1. Networked HTTP custom tools default to `auto`.
2. Browser automation tools using Chromium or Playwright default to `direct` because authenticated proxy URLs cannot be passed through reliably in the current setup.
3. Local hosts must bypass proxy by default.

Default bypass targets:

- `localhost`
- `127.0.0.1`
- `::1`
- RFC1918 private IP ranges when the target is explicitly local infrastructure
- hosts served by local MCP endpoints, such as `localhost:3002`

4. Public HTTP API tools may use the configured proxy unless a host override says otherwise.

### Per-host overrides

The shared policy layer must support three host-level actions:

- `force_proxy`
- `force_direct`
- `deny`

Examples:

- `localhost` -> `force_direct`
- `127.0.0.1` -> `force_direct`
- `*.internal` -> `force_direct` or `deny`, depending on environment
- Browser-driven retail targets -> handled by tool-level `direct` policy rather than host-level exception sprawl

### Fallback behavior

Proxy fallback must be explicit, not silent.

Rules:

1. In `required` mode, never retry direct after proxy failure.
2. In `auto` mode, direct fallback is allowed only if policy explicitly marks the host or tool as `allow_direct_fallback`.
3. If direct fallback occurs, record it in `fallbacks.tried` and `diagnostics.route_transitions`.
4. A request that switches from proxy to direct must still keep the same `request_id`.
5. Proxy authentication failures should not repeatedly retry with the same bad credentials.

### Proxy diagnostics requirements

Every networked result envelope must report:

- resolved proxy mode
- whether proxy was actually used
- config source used
- whether bypass occurred
- sanitized route summary such as `http://***@geo.iproyal.com:12321`
- route transition history if a fallback happened

## Retry and Backoff Policy

Retries belong in the shared execution layer, not in prompt prose.

### Default retry budget

For idempotent network stages such as GET-based search, lookup, and fetch:

- maximum attempts: 3 total
- initial attempt: immediate
- retry count after initial attempt: 2

For multi-provider workflows, such as transcript retrieval:

- per provider attempt budget: 2
- provider chain budget: all configured providers may be tried once their per-provider budget is exhausted
- final status should reflect whether success came from primary or fallback provider

For non-idempotent operations, retries must be opt-in. This phase assumes current tools are read-only and can use the default idempotent policy.

### Retryable conditions

Retry by default for:

- `dns_failed`
- `connect_failed`
- `timeout`
- `rate_limited`
- `upstream_error`
- selected `protocol_error` cases that are known transient transport truncations

Do not retry by default for:

- `invalid_input`
- `config_error`
- `dependency_error`
- `proxy_config_error`
- `auth_required`
- `forbidden`
- `not_found`
- `blocked`
- deterministic `parse_error`
- repeated `proxy_auth_failed`

### Backoff formula

Use exponential backoff with jitter:

- base delay: 500 ms
- multiplier: 2.0
- jitter: full jitter between `0` and the computed delay
- maximum sleep between attempts: 8000 ms
- maximum retry window per stage: 15000 ms unless the tool defines a larger budget

Example nominal delays before jitter:

- attempt 2: 500 ms
- attempt 3: 1000 ms
- attempt 4: 2000 ms

### `Retry-After` handling

If the provider returns `Retry-After`:

- honor it when it is parseable and within the stage time budget
- cap it at the stage budget unless the caller explicitly permits a longer wait
- record the chosen delay in `error.retry_after_ms` and `diagnostics.retry_schedule_ms`

### Stage-aware retry rules

| Stage              | Default policy                                                                                         |
| ------------------ | ------------------------------------------------------------------------------------------------------ |
| `resolve_proxy`    | No retry for malformed config; retry once only for transient file read race if clearly applicable      |
| `connect`          | Retry on DNS/connect/timeouts within budget                                                            |
| `fetch`            | Retry on timeout, 429, and 5xx within budget                                                           |
| `read_response`    | Retry on truncation or connection reset if safe                                                        |
| `parse`            | No blind retry; retry only if a fallback parser or alternate provider exists                           |
| `discovery`        | Retry transient transport failures; if still failing, fall through to next discovery source if defined |
| `transcript_fetch` | Retry per provider, then move to next provider in fallback chain                                       |

### Stop conditions

Stop retrying when any of the following is true:

- a non-retriable error is encountered
- max attempts for the stage are exhausted
- max time budget is exhausted
- a stronger fallback path is available and policy says to switch now
- a partial result already satisfies the minimum success threshold for the tool

## Logging and Diagnostic Fields

Diagnostics must support debugging, test assertions, and postmortem analysis without leaking secrets.

### Redaction rules

Never log or return:

- proxy usernames or passwords
- API keys
- bearer tokens
- cookies
- authorization headers
- full query strings if they contain secrets
- raw stack traces in agent-facing output

If a low-level exception is preserved, keep it in sanitized form under `diagnostics.exception_summary`.

### Required diagnostic fields

| Field               | Type            | Meaning                                             |
| ------------------- | --------------- | --------------------------------------------------- |
| `timestamp`         | string          | RFC 3339 start time of the invocation               |
| `tool_version`      | string          | Tool implementation version or git SHA if available |
| `host`              | string or null  | Target host, if networked                           |
| `http_method`       | string or null  | Usually `GET` for current tools                     |
| `http_status`       | integer or null | Final HTTP status when applicable                   |
| `attempt_count`     | integer         | Total attempts made                                 |
| `retry_schedule_ms` | array           | Sleep schedule actually used                        |
| `timeouts`          | object          | Connect, read, and total timeout budgets            |
| `bytes_received`    | integer or null | Response size when known                            |
| `content_type`      | string or null  | Final response content type                         |
| `provider_chain`    | array           | Providers or fallbacks considered in order          |
| `selected_provider` | string or null  | Provider that produced the final output             |
| `route_transitions` | array           | Proxy/direct routing changes, if any                |
| `partial_failures`  | array           | Structured list of degraded stages or providers     |
| `exception_summary` | string or null  | Sanitized exception class plus concise message      |

### Recommended diagnostic fields

| Field                 | Type            | Meaning                                                              |
| --------------------- | --------------- | -------------------------------------------------------------------- |
| `url_redacted`        | string or null  | URL with sensitive query params removed or redacted                  |
| `response_sha256`     | string or null  | Hash of raw response bytes for fixture capture or dedupe             |
| `parse_strategy`      | string or null  | Parser or extractor path used                                        |
| `records_found`       | integer or null | Number of candidate records fetched                                  |
| `records_returned`    | integer or null | Number of records returned in `data`                                 |
| `cache_hit`           | boolean         | Whether a local cache was used                                       |
| `cache_key`           | string or null  | Sanitized cache key                                                  |
| `dependency_versions` | object          | Versions of key runtime libraries used by the tool                   |
| `policy_flags`        | object          | Feature flags relevant to execution, such as `allow_direct_fallback` |

### Structured log event shape

If the shared execution layer emits internal logs, each event should use a normalized shape.

```json
{
  "event": "http_attempt",
  "request_id": "01HTX3Q6T2K5W5Y6Y2B3N7D9QG",
  "tool": "web_scraper",
  "action": "fetch",
  "stage": "fetch",
  "attempt": 2,
  "host": "open.fda.gov",
  "proxy_mode": "auto",
  "proxy_used": true,
  "status": 429,
  "duration_ms": 611,
  "retryable": true
}
```

Minimum internal event types:

- `request_started`
- `proxy_resolved`
- `http_attempt`
- `fallback_selected`
- `parse_completed`
- `request_completed`
- `request_failed`

## Canonical Examples

### Success

```json
{
  "contract_version": "tool-result/v1",
  "ok": true,
  "status": "ok",
  "tool": "fda_510k",
  "action": "lookup",
  "provider": "openfda",
  "stage": "completed",
  "request_id": "01HTX4AB7N0ME1S0R2YJ7M2T4P",
  "duration_ms": 923,
  "attempts": {
    "total": 1,
    "per_stage": {
      "fetch": 1,
      "parse": 1
    }
  },
  "proxy": {
    "mode": "auto",
    "used": true,
    "source": "proxy-conf",
    "route": "redacted",
    "bypassed": false,
    "bypass_reason": null
  },
  "fallbacks": {
    "available": [],
    "tried": [],
    "selected": null
  },
  "data": {
    "results": [
      {
        "k_number": "K123456",
        "device_name": "Example Device"
      }
    ]
  },
  "error": null,
  "diagnostics": {
    "timestamp": "2026-04-10T12:00:00Z",
    "host": "api.fda.gov",
    "http_method": "GET",
    "http_status": 200,
    "attempt_count": 1,
    "retry_schedule_ms": [],
    "provider_chain": ["openfda"],
    "selected_provider": "openfda",
    "records_found": 1,
    "records_returned": 1,
    "exception_summary": null
  }
}
```

### Empty result

```json
{
  "contract_version": "tool-result/v1",
  "ok": true,
  "status": "empty",
  "tool": "startup_data",
  "action": "search",
  "provider": "edgar",
  "stage": "completed",
  "request_id": "01HTX4K6P4F0A5B8YQ6N8T8N9R",
  "duration_ms": 701,
  "attempts": {
    "total": 1,
    "per_stage": {
      "fetch": 1,
      "parse": 1
    }
  },
  "proxy": {
    "mode": "auto",
    "used": true,
    "source": "proxy-conf",
    "route": "redacted",
    "bypassed": false,
    "bypass_reason": null
  },
  "fallbacks": {
    "available": [],
    "tried": [],
    "selected": null
  },
  "data": {
    "results": []
  },
  "error": null,
  "diagnostics": {
    "host": "www.sec.gov",
    "http_status": 200,
    "records_found": 0,
    "records_returned": 0
  }
}
```

### Partial result via fallback

```json
{
  "contract_version": "tool-result/v1",
  "ok": true,
  "status": "partial",
  "tool": "youtube",
  "action": "transcript",
  "provider": "whisper",
  "stage": "fallback",
  "request_id": "01HTX4S6J3QQP0S8N0C7S2Y5JA",
  "duration_ms": 12443,
  "attempts": {
    "total": 4,
    "per_stage": {
      "transcript_fetch": 3,
      "fallback": 1
    }
  },
  "proxy": {
    "mode": "auto",
    "used": true,
    "source": "proxy-conf",
    "route": "redacted",
    "bypassed": false,
    "bypass_reason": null
  },
  "fallbacks": {
    "available": ["youtube-transcript", "youtube-transcript-api", "whisper"],
    "tried": ["youtube-transcript", "youtube-transcript-api", "whisper"],
    "selected": "whisper"
  },
  "data": {
    "transcript": "..."
  },
  "error": {
    "kind": "partial_result",
    "code": "TRANSCRIPT_PRIMARY_UNAVAILABLE",
    "message": "Primary transcript providers failed; ASR fallback used",
    "retriable": false,
    "temporary": false,
    "stage": "fallback",
    "provider": "whisper",
    "http_status": null,
    "retry_after_ms": null,
    "details": {
      "failed_providers": ["youtube-transcript", "youtube-transcript-api"]
    }
  },
  "diagnostics": {
    "provider_chain": [
      "youtube-transcript",
      "youtube-transcript-api",
      "whisper"
    ],
    "selected_provider": "whisper",
    "partial_failures": [
      {
        "provider": "youtube-transcript",
        "kind": "not_found"
      },
      {
        "provider": "youtube-transcript-api",
        "kind": "rate_limited"
      }
    ]
  }
}
```

### Hard failure

```json
{
  "contract_version": "tool-result/v1",
  "ok": false,
  "status": "error",
  "tool": "web_scraper",
  "action": "fetch",
  "provider": "requests",
  "stage": "failed",
  "request_id": "01HTX53DMF8S9Y7T4K2M6M7ZP1",
  "duration_ms": 3521,
  "attempts": {
    "total": 3,
    "per_stage": {
      "fetch": 3
    }
  },
  "proxy": {
    "mode": "required",
    "used": true,
    "source": "proxy-conf",
    "route": "redacted",
    "bypassed": false,
    "bypass_reason": null
  },
  "fallbacks": {
    "available": [],
    "tried": [],
    "selected": null
  },
  "data": null,
  "error": {
    "kind": "proxy_auth_failed",
    "code": "PROXY_407",
    "message": "Proxy authentication failed",
    "retriable": false,
    "temporary": false,
    "stage": "connect",
    "provider": "requests",
    "http_status": 407,
    "retry_after_ms": null,
    "details": {
      "host": "example.com"
    }
  },
  "diagnostics": {
    "attempt_count": 1,
    "route_transitions": [],
    "exception_summary": "ProxyError: 407 Proxy Authentication Required"
  }
}
```

## Adoption Rules

When Phase 3 implementation begins, every networked custom tool should adopt this contract in this order:

1. shared execution layer for HTTP and subprocess-backed network flows
2. shared error normalizer
3. shared envelope serializer
4. fixture-backed contract tests for `ok`, `empty`, `partial`, and `error`

## Decision Summary

- Result contract: one versioned JSON envelope for all custom tools
- Error system: bounded taxonomy plus stage-aware classification
- Proxy behavior: explicit shared policy with redaction and per-host overrides
- Retry behavior: bounded exponential backoff with jitter and `Retry-After` support
- Diagnostics: structured, safe, and testable
