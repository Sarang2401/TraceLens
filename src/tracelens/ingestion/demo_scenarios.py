"""
Realistic mock CloudWatch Logs Insights data for demo purposes.

Each scenario simulates a distributed system failure with log entries
that match the format returned by CloudWatch Logs Insights queries.
The logs are structured to trigger specific failure patterns in the
RAG knowledge base.
"""

from typing import Dict, List

# ---------------------------------------------------------------------------
# Scenario 1 — Database Connection Pool Exhaustion
# ---------------------------------------------------------------------------
# Story: An e-commerce checkout request flows through api-gateway →
# order-service → payment-service.  The order-service exhausts its
# database connection pool under load, causing cascading failures.
# ---------------------------------------------------------------------------

DB_POOL_SCENARIO: Dict = {
    "trace_id": "demo-trace-db-pool-001",
    "name": "Database Connection Pool Exhaustion",
    "description": (
        "An e-commerce checkout triggers a cascade of failures when "
        "the order-service exhausts its PostgreSQL connection pool "
        "under sustained high traffic."
    ),
    "logs": [
        {
            "@timestamp": "2026-02-21T08:15:01.102Z",
            "@message": "Incoming POST /api/v1/checkout received from client 192.168.1.42",
            "@logStream": "api-gateway/prod/i-0a1b2c3d4e5f",
            "@log": "/aws/lambda/api-gateway",
            "trace_id": "demo-trace-db-pool-001",
            "service": "api-gateway",
            "component": "http-handler",
            "level": "INFO",
            "event_type": "HTTP_REQUEST",
            "request_id": "req-7a8b9c0d",
            "http_status": "200",
            "latency_ms": "12",
        },
        {
            "@timestamp": "2026-02-21T08:15:01.250Z",
            "@message": "Forwarding checkout request to order-service for order ORD-98234",
            "@logStream": "api-gateway/prod/i-0a1b2c3d4e5f",
            "@log": "/aws/lambda/api-gateway",
            "trace_id": "demo-trace-db-pool-001",
            "service": "api-gateway",
            "component": "router",
            "level": "INFO",
            "event_type": "SERVICE_CALL",
            "request_id": "req-7a8b9c0d",
            "dependency": "order-service",
        },
        {
            "@timestamp": "2026-02-21T08:15:01.480Z",
            "@message": "Processing order ORD-98234, attempting to persist to database",
            "@logStream": "order-service/prod/i-1f2e3d4c5b",
            "@log": "/aws/lambda/order-service",
            "trace_id": "demo-trace-db-pool-001",
            "service": "order-service",
            "component": "order-processor",
            "level": "INFO",
            "event_type": "DB_WRITE",
            "request_id": "req-7a8b9c0d",
        },
        {
            "@timestamp": "2026-02-21T08:15:03.970Z",
            "@message": "WARN: connection pool utilization at 95%, active=19/20 connections",
            "@logStream": "order-service/prod/i-1f2e3d4c5b",
            "@log": "/aws/lambda/order-service",
            "trace_id": "demo-trace-db-pool-001",
            "service": "order-service",
            "component": "db-pool-monitor",
            "level": "WARN",
            "event_type": "RESOURCE_WARNING",
            "request_id": "req-7a8b9c0d",
        },
        {
            "@timestamp": "2026-02-21T08:15:06.510Z",
            "@message": "ERROR: timeout acquiring connection from pool after 5000ms — too many connections in use, connection pool exhausted",
            "@logStream": "order-service/prod/i-1f2e3d4c5b",
            "@log": "/aws/lambda/order-service",
            "trace_id": "demo-trace-db-pool-001",
            "service": "order-service",
            "component": "hikari-pool",
            "level": "ERROR",
            "event_type": "DB_ERROR",
            "request_id": "req-7a8b9c0d",
            "exception_type": "ConnectionPoolExhaustedException",
            "dependency": "postgresql-primary",
            "latency_ms": "5012",
        },
        {
            "@timestamp": "2026-02-21T08:15:06.520Z",
            "@message": "Failed to persist order ORD-98234: could not acquire database connection",
            "@logStream": "order-service/prod/i-1f2e3d4c5b",
            "@log": "/aws/lambda/order-service",
            "trace_id": "demo-trace-db-pool-001",
            "service": "order-service",
            "component": "order-processor",
            "level": "ERROR",
            "event_type": "ORDER_FAILURE",
            "request_id": "req-7a8b9c0d",
            "exception_type": "PersistenceException",
            "stacktrace": "PersistenceException: could not acquire database connection\n  at OrderRepository.save(OrderRepository.java:142)\n  at OrderProcessor.process(OrderProcessor.java:87)",
        },
        {
            "@timestamp": "2026-02-21T08:15:06.580Z",
            "@message": "Payment request for order ORD-98234 aborted — upstream order-service returned 503",
            "@logStream": "payment-service/prod/i-2d3e4f5a6b",
            "@log": "/aws/lambda/payment-service",
            "trace_id": "demo-trace-db-pool-001",
            "service": "payment-service",
            "component": "payment-handler",
            "level": "ERROR",
            "event_type": "PAYMENT_ABORT",
            "request_id": "req-7a8b9c0d",
            "http_status": "503",
        },
        {
            "@timestamp": "2026-02-21T08:15:06.640Z",
            "@message": "Returning 503 Service Unavailable for POST /api/v1/checkout — order processing failed",
            "@logStream": "api-gateway/prod/i-0a1b2c3d4e5f",
            "@log": "/aws/lambda/api-gateway",
            "trace_id": "demo-trace-db-pool-001",
            "service": "api-gateway",
            "component": "http-handler",
            "level": "ERROR",
            "event_type": "HTTP_RESPONSE",
            "request_id": "req-7a8b9c0d",
            "http_status": "503",
            "latency_ms": "5538",
        },
    ],
}


# ---------------------------------------------------------------------------
# Scenario 2 — Downstream Service Timeout
# ---------------------------------------------------------------------------
# Story: A user profile update triggers a notification to
# notification-service, which calls an external SMS provider that is
# experiencing a latency spike, causing the whole chain to time out.
# ---------------------------------------------------------------------------

TIMEOUT_SCENARIO: Dict = {
    "trace_id": "demo-trace-timeout-001",
    "name": "Downstream Service Timeout",
    "description": (
        "A user profile update triggers a notification through "
        "notification-service, which times out waiting for the "
        "external SMS provider, causing upstream failures."
    ),
    "logs": [
        {
            "@timestamp": "2026-02-21T09:30:00.200Z",
            "@message": "Incoming PUT /api/v1/users/usr-44291/profile received",
            "@logStream": "api-gateway/prod/i-0a1b2c3d4e5f",
            "@log": "/aws/lambda/api-gateway",
            "trace_id": "demo-trace-timeout-001",
            "service": "api-gateway",
            "component": "http-handler",
            "level": "INFO",
            "event_type": "HTTP_REQUEST",
            "request_id": "req-e5f6a7b8",
            "http_status": "200",
            "latency_ms": "8",
        },
        {
            "@timestamp": "2026-02-21T09:30:00.450Z",
            "@message": "Profile updated for user usr-44291, dispatching notification",
            "@logStream": "user-service/prod/i-3c4d5e6f7a",
            "@log": "/aws/lambda/user-service",
            "trace_id": "demo-trace-timeout-001",
            "service": "user-service",
            "component": "profile-handler",
            "level": "INFO",
            "event_type": "PROFILE_UPDATE",
            "request_id": "req-e5f6a7b8",
        },
        {
            "@timestamp": "2026-02-21T09:30:00.520Z",
            "@message": "Sending SMS notification to +91-XXXX-7890 via external provider",
            "@logStream": "notification-service/prod/i-4b5c6d7e8f",
            "@log": "/aws/lambda/notification-service",
            "trace_id": "demo-trace-timeout-001",
            "service": "notification-service",
            "component": "sms-sender",
            "level": "INFO",
            "event_type": "EXTERNAL_CALL",
            "request_id": "req-e5f6a7b8",
            "dependency": "twilio-sms-api",
        },
        {
            "@timestamp": "2026-02-21T09:30:05.530Z",
            "@message": "WARN: external SMS API response delayed — latency 5010ms, threshold 3000ms",
            "@logStream": "notification-service/prod/i-4b5c6d7e8f",
            "@log": "/aws/lambda/notification-service",
            "trace_id": "demo-trace-timeout-001",
            "service": "notification-service",
            "component": "sms-sender",
            "level": "WARN",
            "event_type": "LATENCY_WARNING",
            "request_id": "req-e5f6a7b8",
            "latency_ms": "5010",
            "dependency": "twilio-sms-api",
        },
        {
            "@timestamp": "2026-02-21T09:30:10.540Z",
            "@message": "ERROR: request timed out waiting for downstream dependency twilio-sms-api after 10000ms — dependency timeout exceeded",
            "@logStream": "notification-service/prod/i-4b5c6d7e8f",
            "@log": "/aws/lambda/notification-service",
            "trace_id": "demo-trace-timeout-001",
            "service": "notification-service",
            "component": "http-client",
            "level": "ERROR",
            "event_type": "TIMEOUT",
            "request_id": "req-e5f6a7b8",
            "exception_type": "HttpTimeoutException",
            "dependency": "twilio-sms-api",
            "latency_ms": "10020",
        },
        {
            "@timestamp": "2026-02-21T09:30:10.560Z",
            "@message": "Notification delivery failed for user usr-44291 — upstream timeout from notification-service",
            "@logStream": "user-service/prod/i-3c4d5e6f7a",
            "@log": "/aws/lambda/user-service",
            "trace_id": "demo-trace-timeout-001",
            "service": "user-service",
            "component": "notification-dispatcher",
            "level": "ERROR",
            "event_type": "NOTIFICATION_FAILURE",
            "request_id": "req-e5f6a7b8",
            "dependency": "notification-service",
        },
        {
            "@timestamp": "2026-02-21T09:30:10.610Z",
            "@message": "Returning 504 Gateway Timeout for PUT /api/v1/users/usr-44291/profile — dependency timeout in notification chain",
            "@logStream": "api-gateway/prod/i-0a1b2c3d4e5f",
            "@log": "/aws/lambda/api-gateway",
            "trace_id": "demo-trace-timeout-001",
            "service": "api-gateway",
            "component": "http-handler",
            "level": "ERROR",
            "event_type": "HTTP_RESPONSE",
            "request_id": "req-e5f6a7b8",
            "http_status": "504",
            "latency_ms": "10410",
        },
    ],
}


# ---------------------------------------------------------------------------
# Registry — all demo scenarios indexed by trace_id
# ---------------------------------------------------------------------------

DEMO_SCENARIOS: Dict[str, Dict] = {
    DB_POOL_SCENARIO["trace_id"]: DB_POOL_SCENARIO,
    TIMEOUT_SCENARIO["trace_id"]: TIMEOUT_SCENARIO,
}
