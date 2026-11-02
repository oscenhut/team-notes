# Engineering Review: Multi-Team Note-Taking System (3-Hour MVP)

**Author:** Principal Software Engineer

**Target Delivery Window:** 3 Hours

**Stack Profile:** Python, FastAPI, SQLAlchemy, SQLite

## 1. Functional Requirements

* **User Management & Authentication:** 
  * Register users with `Id`, `Email`, `Name`, and `PasswordHash`.
  * Authenticate users and establish session/token context.
  * Endpoint to verify identity/current authenticated state.

* **Team & Membership Management:**
  * Create teams.
  * Associate users with teams via a junction table (`user_teams`) with explicit roles (`OWNER`, `MEMBER`).

* **Note Lifecycle & Visibility:**
  * Create, read, update, and delete notes.
  * Support three distinct visibility tiers:
    * `PRIVATE`: Accessible solely by the owner user.
    * `TEAM`: Accessible by members of the assigned team.
    * `PUBLIC`: Accessible across the system (or filtered appropriately).

* **System Health:**
  * Endpoint to verify operational status of the service and database connectivity.

## 2. Non-Functional Requirements

* **Speed to Execution:** Entirely runnable locally with zero external dependencies (SQLite file).

* **API Documentation:** Auto-generated interactive Swagger UI (`/docs`) serving as the client interface to bypass frontend development overhead.

* **Data Integrity:** Foreign key constraints with cascading deletes for proper cleanup of memberships and ownership links.

## 3. Assumptions

* **Session / Auth Strategy:** Lightweight token or session ID returned upon login and passed via Authorization headers for subsequent requests.
* **Single-Tenant Infrastructure:** SQLite is acceptable for local persistence to eliminate Docker container setup overhead.
* **No Real-Time Sync:** WebSockets or SSE are out of scope; standard request-response HTTP operations fulfill the assessment requirements.

## 4. Ambiguities Requiring Clarification

* *Note-to-Team Association on Private Notes:* Can a note have a `team_id` specified while its visibility is `PRIVATE`? *(Assumption: If `PRIVATE`, `team_id` is optional and ignored for access control).*
* *Team Deletion Policy:* Should deleting a team cascade-delete its notes, or unassign them (`SET NULL`)? *(Assumption: `SET NULL` or soft association depending on note ownership).*

## 5. Simplest Architecture

A monolithic, single-process FastAPI application communicating directly with a local SQLite database via SQLAlchemy ORM.

```
+-------------------------------------------------------+
|                       FastAPI                         |
|  - Routers (/auth, /users, /teams, /notes, /health)   |
|  - Auth & Dependency Injection (DB Session, User)    |
+---------------------------+---------------------------+
                            | SQLAlchemy ORM
                            v
+-------------------------------------------------------+
|                    SQLite Database                    |
|          (users, teams, user_teams, notes)            |
+-------------------------------------------------------+
```

## 6. Domain Model

* **User:** Represents a system actor with identity credentials and personal settings. Maintains a 1-to-Many relationship with Notes and a Many-to-Many relationship with Teams.
* **Team:** A collaborative workspace. Maintains a 1-to-Many relationship with Notes and a Many-to-Many relationship with Users.
* **UserTeam:** Junction entity defining membership with a role attribute (`OWNER` or `MEMBER`).
* **Note:** The core domain object containing text content, ownership reference (`owner_user_id`), optional team scope (`team_id`), and an access rule (`visibility`).

## 7. Suggested Database Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE user_teams (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
    role VARCHAR(20) CHECK (role IN ('OWNER', 'MEMBER')) DEFAULT 'MEMBER',
    PRIMARY KEY (user_id, team_id)
);

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    owner_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    team_id INTEGER REFERENCES teams(id) ON DELETE SET NULL,
    text TEXT NOT NULL,
    visibility VARCHAR(20) CHECK (visibility IN ('PRIVATE', 'TEAM', 'PUBLIC')) DEFAULT 'TEAM'
);
```

## 8. REST API Endpoints

| Category | Method | Endpoint | Access | Description |
| --- | --- | --- | --- | --- |
| **System** | `GET` | `/health` | Public | Service healthcheck & DB connectivity check |
| **Auth** | `POST` | `/auth/login` | Public | Authenticate user & return token/session |
| **Auth** | `GET` | `/auth/me` | Authenticated | Get current logged-in user profile |
| **Users** | `POST` | `/users` | Public | Register a new user |
| **Teams** | `POST` | `/teams` | Authenticated | Create a new team workspace |
| **Teams** | `POST` | `/teams/{team_id}/members` | Team Owner | Add a user to a team with a specified role |
| **Notes** | `POST` | `/notes` | Authenticated | Create a note (visibility + optional team_id) |
| **Notes** | `GET` | `/notes` | Authenticated | Retrieve visible notes for current user |
| **Notes** | `GET` | `/notes/{note_id}` | Authenticated | Retrieve a specific note if permissions pass |
| **Notes** | `PUT` | `/notes/{note_id}` | Owner | Update note text or visibility |
| **Notes** | `DELETE` | `/notes/{note_id}` | Owner/Team Owner | Delete a note |