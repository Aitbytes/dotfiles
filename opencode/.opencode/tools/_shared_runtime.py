#!/usr/bin/env python3

from __future__ import annotations

import ipaddress
import json
import os
import random
import re
import time
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import SplitResult, urlsplit, urlunsplit

import requests
import certifi
DEFAULT_PROXY_CONF = Path.home() / ".config/proxy-conf"
DEFAULT_HOST_OVERRIDES = {
    "localhost": "force_direct",
    "127.0.0.1": "force_direct",
    "::1": "force_direct",
}
ALLOWED_HOST_ACTIONS = {"force_proxy", "force_direct", "deny"}


@dataclass(frozen=True)
class TimeoutConfig:
    connect: float = 10.0
    read: float = 30.0
    total: float | None = None

    def as_requests_timeout(self) -> tuple[float, float]:
        return (self.connect, self.read)


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay: float = 0.5
    multiplier: float = 2.0
    max_delay: float = 8.0
    max_retry_window: float = 15.0
    jitter: bool = True


@dataclass(frozen=True)
class ProxyConfig:
    http: str | None = None
    https: str | None = None
    source: str = "none"

    @property
    def enabled(self) -> bool:
        return bool(self.http or self.https)


@dataclass(frozen=True)
class ProxyDecision:
    mode: str
    used: bool
    source: str
    proxies: dict[str, str] = field(default_factory=dict)
    route: str | None = None
    bypassed: bool = False
    bypass_reason: str | None = None


@dataclass
class RequestResult:
    response: requests.Response
    proxy: ProxyDecision
    attempts: int
    retry_schedule_ms: list[int] = field(default_factory=list)
    route_transitions: list[dict[str, Any]] = field(default_factory=list)
    duration_ms: int = 0


class ToolRuntimeError(Exception):
    def __init__(
        self,
        kind: str,
        message: str,
        *,
        stage: str,
        provider: str | None = None,
        retriable: bool = False,
        temporary: bool | None = None,
        http_status: int | None = None,
        retry_after_ms: int | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.kind = kind
        self.message = message
        self.stage = stage
        self.provider = provider
        self.retriable = retriable
        self.temporary = retriable if temporary is None else temporary
        self.http_status = http_status
        self.retry_after_ms = retry_after_ms
        self.code = code or kind.upper()
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "code": self.code,
            "message": self.message,
            "retriable": self.retriable,
            "temporary": self.temporary,
            "stage": self.stage,
            "provider": self.provider,
            "http_status": self.http_status,
            "retry_after_ms": self.retry_after_ms,
            "details": self.details,
        }


def create_error(
    kind: str,
    message: str,
    *,
    stage: str,
    provider: str | None = None,
    retriable: bool = False,
    temporary: bool | None = None,
    http_status: int | None = None,
    retry_after_ms: int | None = None,
    code: str | None = None,
    details: dict[str, Any] | None = None,
) -> ToolRuntimeError:
    return ToolRuntimeError(
        kind,
        message,
        stage=stage,
        provider=provider,
        retriable=retriable,
        temporary=temporary,
        http_status=http_status,
        retry_after_ms=retry_after_ms,
        code=code,
        details=details,
    )


def format_error(error: ToolRuntimeError) -> str:
    suffix = []
    if error.provider:
        suffix.append(f"provider={error.provider}")
    if error.stage:
        suffix.append(f"stage={error.stage}")
    if error.http_status is not None:
        suffix.append(f"http_status={error.http_status}")
    meta = f" ({', '.join(suffix)})" if suffix else ""
    return f"{error.kind}: {error.message}{meta}"


def normalize_timeout(timeout: float | int | TimeoutConfig | None, *, connect: float = 10.0, read: float = 30.0) -> TimeoutConfig:
    if isinstance(timeout, TimeoutConfig):
        return timeout
    if timeout is None:
        return TimeoutConfig(connect=connect, read=read, total=read)
    value = float(timeout)
    return TimeoutConfig(connect=min(connect, value), read=value, total=value)


def load_proxy_config(config_path: str | Path | None = None) -> ProxyConfig:
    path = Path(config_path) if config_path else DEFAULT_PROXY_CONF
    if path.exists():
        values: dict[str, str] = {}
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            match = re.match(r'(?:export\s+)?(HTTP_PROXY|HTTPS_PROXY)=(.*)', line)
            if not match:
                continue
            key = match.group(1)
            value = match.group(2).strip().strip('"').strip("'")
            values[key] = value
        return ProxyConfig(
            http=values.get("HTTP_PROXY"),
            https=values.get("HTTPS_PROXY") or values.get("HTTP_PROXY"),
            source="proxy-conf",
        )

    http = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    https = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy") or http
    if http or https:
        return ProxyConfig(http=http, https=https, source="env")
    return ProxyConfig(source="none")


def _validate_host_override(pattern: str, action: str) -> None:
    if action not in ALLOWED_HOST_ACTIONS:
        raise create_error(
            "config_error",
            f"Unsupported host override action '{action}' for pattern '{pattern}'",
            stage="load_config",
        )


def load_host_overrides(overrides: Mapping[str, str] | None = None) -> dict[str, str]:
    merged = dict(DEFAULT_HOST_OVERRIDES)
    raw_env = os.getenv("OPENCODE_HOST_OVERRIDES", "").strip()
    if raw_env:
        try:
            env_overrides = json.loads(raw_env)
        except json.JSONDecodeError as exc:
            raise create_error(
                "config_error",
                f"OPENCODE_HOST_OVERRIDES is not valid JSON: {exc}",
                stage="load_config",
            )
        if not isinstance(env_overrides, dict):
            raise create_error(
                "config_error",
                "OPENCODE_HOST_OVERRIDES must be a JSON object mapping host patterns to actions",
                stage="load_config",
            )
        for pattern, action in env_overrides.items():
            _validate_host_override(str(pattern), str(action))
            merged[str(pattern)] = str(action)
    if overrides:
        for pattern, action in overrides.items():
            _validate_host_override(str(pattern), str(action))
            merged[str(pattern)] = str(action)
    return merged


def sanitize_proxy_url(proxy_url: str | None) -> str | None:
    if not proxy_url:
        return None
    parts = urlsplit(proxy_url)
    host = parts.hostname or ""
    port = f":{parts.port}" if parts.port else ""
    netloc = host + port
    if parts.username or parts.password:
        netloc = f"***@{netloc}"
    return urlunsplit((parts.scheme, netloc, "", "", ""))


def sanitize_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit(SplitResult(parts.scheme, parts.netloc, parts.path, "", ""))


def _is_private_host(hostname: str) -> bool:
    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        return False
    return ip.is_private or ip.is_loopback


def _host_override_action(hostname: str | None, overrides: Mapping[str, str]) -> str | None:
    if not hostname:
        return None
    host = hostname.lower()
    for pattern, action in overrides.items():
        if fnmatch(host, pattern.lower()):
            return action
    if _is_private_host(host):
        return "force_direct"
    return None


def resolve_proxy_decision(
    url: str,
    *,
    proxy_mode: str = "auto",
    host_overrides: Mapping[str, str] | None = None,
    config_path: str | Path | None = None,
) -> ProxyDecision:
    if proxy_mode not in {"auto", "required", "direct", "disabled"}:
        raise create_error("config_error", f"Unsupported proxy mode '{proxy_mode}'", stage="resolve_proxy")

    proxy_config = load_proxy_config(config_path)
    overrides = load_host_overrides(host_overrides)
    host = urlsplit(url).hostname
    action = _host_override_action(host, overrides)

    if action == "deny":
        raise create_error(
            "policy_denied",
            f"Access to host '{host}' denied by host override policy",
            stage="resolve_proxy",
            details={"host": host},
        )

    if proxy_mode in {"direct", "disabled"} or action == "force_direct":
        reason = "mode_direct" if proxy_mode in {"direct", "disabled"} else "host_override"
        return ProxyDecision(
            mode=proxy_mode,
            used=False,
            source=proxy_config.source,
            proxies={},
            route=None,
            bypassed=True,
            bypass_reason=reason,
        )

    if not proxy_config.enabled:
        if proxy_mode == "required" or action == "force_proxy":
            raise create_error(
                "proxy_config_error",
                "Proxy required but no usable proxy configuration was found",
                stage="resolve_proxy",
                details={"host": host},
            )
        return ProxyDecision(
            mode=proxy_mode,
            used=False,
            source=proxy_config.source,
            proxies={},
            route=None,
            bypassed=True,
            bypass_reason="no_proxy_config",
        )

    proxies = {
        "http": proxy_config.http or proxy_config.https or "",
        "https": proxy_config.https or proxy_config.http or "",
    }
    route = sanitize_proxy_url(proxies.get("https") or proxies.get("http"))
    return ProxyDecision(
        mode=proxy_mode,
        used=True,
        source=proxy_config.source,
        proxies=proxies,
        route=route,
        bypassed=False,
        bypass_reason=None,
    )


def configure_requests_session(
    session: requests.Session | None = None,
    *,
    url: str,
    user_agent: str | None = None,
    headers: Mapping[str, str] | None = None,
    proxy_mode: str = "auto",
    host_overrides: Mapping[str, str] | None = None,
    config_path: str | Path | None = None,
) -> tuple[requests.Session, ProxyDecision]:
    sess = session or requests.Session()
    sess.trust_env = False
    sess.verify = certifi.where()
    decision = resolve_proxy_decision(
        url,
        proxy_mode=proxy_mode,
        host_overrides=host_overrides,
        config_path=config_path,
    )
    sess.proxies.clear()
    if decision.used:
        sess.proxies.update(decision.proxies)
    if user_agent:
        sess.headers["User-Agent"] = user_agent
    if headers:
        sess.headers.update(headers)
    return sess, decision


def compute_backoff_delay(policy: RetryPolicy, attempt: int) -> float:
    nominal = min(policy.base_delay * (policy.multiplier ** max(0, attempt - 1)), policy.max_delay)
    if not policy.jitter:
        return nominal
    return random.uniform(0.0, nominal)


def should_retry(error: ToolRuntimeError, *, attempt: int, started_at: float, policy: RetryPolicy) -> bool:
    if not error.retriable:
        return False
    if attempt >= policy.max_attempts:
        return False
    elapsed = time.monotonic() - started_at
    return elapsed < policy.max_retry_window


def parse_retry_after_ms(value: str | None) -> int | None:
    if not value:
        return None
    value = value.strip()
    if value.isdigit():
        return int(value) * 1000
    return None


def error_from_response(response: requests.Response, *, stage: str, provider: str | None = None) -> ToolRuntimeError:
    status = response.status_code
    retry_after_ms = parse_retry_after_ms(response.headers.get("Retry-After"))
    details = {
        "url": sanitize_url(response.url),
        "host": urlsplit(response.url).hostname,
    }
    if status == 400:
        return create_error("invalid_input", "Upstream rejected the request", stage=stage, provider=provider, http_status=status, details=details)
    if status == 401:
        return create_error("auth_required", "Authentication required", stage=stage, provider=provider, http_status=status, details=details)
    if status == 403:
        return create_error("forbidden", "Upstream denied access", stage=stage, provider=provider, http_status=status, details=details)
    if status == 404:
        return create_error("not_found", "Requested resource was not found", stage=stage, provider=provider, http_status=status, details=details)
    if status == 408:
        return create_error("timeout", "Upstream timed out", stage=stage, provider=provider, retriable=True, http_status=status, details=details)
    if status == 429:
        return create_error(
            "rate_limited",
            "Upstream rate limit exceeded",
            stage=stage,
            provider=provider,
            retriable=True,
            http_status=status,
            retry_after_ms=retry_after_ms,
            details=details,
        )
    if 500 <= status <= 599:
        return create_error(
            "upstream_error",
            f"Upstream server error ({status})",
            stage=stage,
            provider=provider,
            retriable=True,
            http_status=status,
            details=details,
        )
    return create_error(
        "protocol_error",
        f"Unexpected upstream response ({status})",
        stage=stage,
        provider=provider,
        http_status=status,
        details=details,
    )


def detect_blocked_response(response: requests.Response, extra_markers: list[str] | None = None) -> bool:
    markers = {
        "captcha",
        "access denied",
        "automated queries",
        "just a moment",
        "cloudflare",
        "validatecaptcha",
        "robot check",
    }
    if extra_markers:
        markers.update(marker.lower() for marker in extra_markers)
    content_type = response.headers.get("Content-Type", "").lower()
    if "html" not in content_type and response.status_code not in {403, 429}:
        return False
    body = response.text[:5000].lower()
    return any(marker in body for marker in markers)


def request_with_retries(
    method: str,
    url: str,
    *,
    session: requests.Session | None = None,
    params: dict[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
    json_body: Any = None,
    data: Any = None,
    timeout: float | int | TimeoutConfig | None = None,
    retry_policy: RetryPolicy | None = None,
    proxy_mode: str = "auto",
    host_overrides: Mapping[str, str] | None = None,
    provider: str | None = None,
    allow_redirects: bool = True,
    allowed_statuses: set[int] | None = None,
    block_markers: list[str] | None = None,
    allow_direct_fallback: bool = True,
) -> RequestResult:
    policy = retry_policy or RetryPolicy()
    timeout_cfg = normalize_timeout(timeout)
    retry_schedule_ms: list[int] = []
    route_transitions: list[dict[str, Any]] = []
    started_at = time.monotonic()
    current_proxy_mode = proxy_mode
    direct_fallback_used = False
    last_error: ToolRuntimeError | None = None

    for attempt in range(1, policy.max_attempts + 1):
        req_session, decision = configure_requests_session(
            session,
            url=url,
            headers=headers,
            proxy_mode=current_proxy_mode,
            host_overrides=host_overrides,
        )

        try:
            response = req_session.request(
                method.upper(),
                url,
                params=params,
                headers=headers,
                json=json_body,
                data=data,
                timeout=timeout_cfg.as_requests_timeout(),
                allow_redirects=allow_redirects,
            )
            if detect_blocked_response(response, block_markers):
                raise create_error(
                    "blocked",
                    f"Blocked by upstream challenge on {sanitize_url(url)}",
                    stage="fetch",
                    provider=provider,
                    retriable=False,
                    http_status=response.status_code,
                    details={"url": sanitize_url(url), "host": urlsplit(url).hostname},
                )
            if allowed_statuses and response.status_code in allowed_statuses:
                return RequestResult(
                    response=response,
                    proxy=decision,
                    attempts=attempt,
                    retry_schedule_ms=retry_schedule_ms,
                    route_transitions=route_transitions,
                    duration_ms=int((time.monotonic() - started_at) * 1000),
                )
            if response.status_code >= 400:
                raise error_from_response(response, stage="fetch", provider=provider)
            return RequestResult(
                response=response,
                proxy=decision,
                attempts=attempt,
                retry_schedule_ms=retry_schedule_ms,
                route_transitions=route_transitions,
                duration_ms=int((time.monotonic() - started_at) * 1000),
            )
        except ToolRuntimeError as error:
            last_error = error
        except requests.exceptions.ProxyError as exc:
            last_error = create_error(
                "proxy_auth_failed" if "407" in str(exc) else "connect_failed",
                "Proxy request failed",
                stage="connect",
                provider=provider,
                retriable="407" not in str(exc),
                details={"exception": exc.__class__.__name__, "url": sanitize_url(url)},
            )
        except requests.exceptions.Timeout as exc:
            last_error = create_error(
                "timeout",
                f"Request timed out after {timeout_cfg.read:.0f}s",
                stage="fetch",
                provider=provider,
                retriable=True,
                details={"exception": exc.__class__.__name__, "url": sanitize_url(url)},
            )
        except requests.exceptions.ConnectionError as exc:
            message = str(exc).lower()
            kind = "dns_failed" if "name or service not known" in message or "temporary failure in name resolution" in message else "connect_failed"
            last_error = create_error(
                kind,
                "Network connection failed",
                stage="connect",
                provider=provider,
                retriable=True,
                details={"exception": exc.__class__.__name__, "url": sanitize_url(url)},
            )
        except requests.exceptions.RequestException as exc:
            last_error = create_error(
                "upstream_error",
                "Unexpected request failure",
                stage="fetch",
                provider=provider,
                retriable=True,
                details={"exception": exc.__class__.__name__, "url": sanitize_url(url)},
            )

        if (
            allow_direct_fallback
            and not direct_fallback_used
            and current_proxy_mode == "auto"
            and decision.used
            and last_error.kind in {"proxy_auth_failed", "connect_failed", "timeout"}
        ):
            direct_fallback_used = True
            current_proxy_mode = "direct"
            route_transitions.append({"from": "proxy", "to": "direct", "reason": last_error.kind})

        if not should_retry(last_error, attempt=attempt, started_at=started_at, policy=policy):
            raise last_error

        delay = compute_backoff_delay(policy, attempt)
        retry_schedule_ms.append(int(delay * 1000))
        time.sleep(delay)

    assert last_error is not None
    raise last_error


def request_json(*args: Any, **kwargs: Any) -> tuple[Any, RequestResult]:
    result = request_with_retries(*args, **kwargs)
    try:
        return result.response.json(), result
    except ValueError as exc:
        raise create_error(
            "parse_error",
            "Response body is not valid JSON",
            stage="parse",
            retriable=False,
            details={"exception": exc.__class__.__name__},
        ) from exc


def request_text(*args: Any, **kwargs: Any) -> tuple[str, RequestResult]:
    result = request_with_retries(*args, **kwargs)
    return result.response.text, result
