# TeamNotes API - Architectural Debt & Code Review Findings

**Author:** Principal Software Engineer  
**Date:** November 2026  
**Status:** Accepted / Technical Backlog  

---

## Overview

This document outlines key architectural trade-offs, design weaknesses, API inconsistencies, security gaps, and missing test scenarios identified during code review. It serves as technical documentation for the current team and future maintainers.

---

## 1. Architectural & Design Weaknesses

### 1.1 File-Based SQLite Concurrency Limits in Production
* **Issue:** Deploying a file-backed SQLite database (`sqlite:////app/data/app.db`) mounted via a Docker named volume introduces write-concurrency limits. Under concurrent asynchronous workloads, SQLite will encounter `database is locked` operational errors.
* **Mitigation / Next Steps:** If vertical scale demands higher write throughput, enable Write-Ahead Logging (WAL) mode (`PRAGMA journal_mode=WAL;`) and configure `busy_timeout` inside SQLAlchemy connection arguments. For multi-instance scaling, migrate to PostgreSQL.

### 1.2 Global Lazy-Loaded Database Proxies
* **Issue:** Global proxies (`_LazyEngineProxy`, `_LazySessionLocalProxy`) in `app/database.py` mask engine initialization order and tightly couple state across threads.
* **Mitigation / Next Steps:** Replace lazy proxy classes with FastAPI's explicit dependency injection pattern (`Depends(get_db)`) across all application layers and background tasks.

---

## 2. API Design Weaknesses

### 2.1 Redundant Request Payload Parameters
* **Issue:** Endpoints like `POST /teams/{team_id}/members` require `team_id` in both the URL path parameter and the JSON request body.
* **Mitigation / Next Steps:** Remove `team_id` from request body schemas where path parameters already establish the parent resource context.

### 2.2 Ambiguous HTTP Status Code Contracts
* **Issue:** Inconsistent application of `200 OK` vs. `201 Created` on resource creation routes.
* **Mitigation / Next Steps:** Standardize all creation endpoints to return `201 Created` alongside appropriate response headers.

---

## 3. Security Concerns

### 3.1 Unconstrained CORS and Rate Limiting
* **Issue:** The application lacks CORS policy configuration and rate-limiting middleware on public routes (`/auth/token`, `/users`).
* **Mitigation / Next Steps:** Implement `fastapi.middleware.cors.CORSMiddleware` with explicit origin white-listing, and introduce `slowapi` or redis-backed rate-limiting for auth routes.

### 3.2 JWT Token Validation Rigor
* **Issue:** Token decoding dependencies must ensure strict algorithm whitelisting and explicit expiration enforcement to prevent signature bypass attacks.
* **Mitigation / Next Steps:** Enforce strict algorithm parameters (`algorithms=["HS256"]`) and reject unverified claims in authentication helper routes.

---

## 4. Missing Test Coverage

* **Multi-Threaded Lock Contention:** Add concurrency stress tests to verify SQLite lock handling during parallel writes.
* **Cross-Tenant Authorization Boundaries:** Implement explicit negative tests asserting that unauthorized users cannot read or modify resources belonging to teams they are not assigned to.

---

## 5. Architectural Simplifications & Documented Trade-Offs

### 5.1 Single-Container Deployment Model
The application is explicitly designed as a single-instance container deployment using Docker Compose and volume-backed storage. Horizontal scaling is intentionally unsupported under this layout; vertical resource scaling is prioritized.

### 5.2 SQLite URI Shared Memory Test Harness
The pytest suite uses SQLite's in-memory database (sqlite:///:memory:) with SQLAlchemy's StaticPool connection pooling strategy.
This configuration maintains a single shared database connection across the FastAPI test client and application threads, ensuring that all test requests access the same in-memory database without creating temporary files on disk.
The check_same_thread=False connection argument allows the SQLite connection to be accessed from different threads.
The test database schema is initialized centrally through pytest fixtures and cleaned between tests.