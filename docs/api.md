# TeamNotes: REST API Documentation

**Base Environment URLs:**
* **Local Development:** `http://localhost:8000/api/v1`
* **Production:** `https://api.teamnotes.com/api/v1` *(Configurable via `API_BASE_URL` env variable)*

**Authentication Strategy:** Bearer Token (`Authorization: Bearer <token>`) or `X-User-ID` Header (for rapid prototyping/testing)

---

## 1. System & Health

### `GET /health`

Verify application status, server connectivity, and SQLite database responsiveness.

* **Authentication:** None (Public)
* **Response (200 OK):**

```json
{
  "status": "healthy",
  "database": "connected",
  "environment": "development",
  "timestamp": "2026-11-02T09:37:00Z"
}
```

---

## 2. Authentication & Identity

### `POST /auth/login`

Authenticate existing user credentials and return an access token or session handle.

* **Authentication:** None (Public)
* **Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

* **Response (200 OK):**

```json
{
  "access_token": "mock-token-user-id-1",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "Jane Doe"
  }
}
```

### `GET /auth/me`

Retrieve profile details for the currently authenticated user session.

* **Authentication:** Required
* **Response (200 OK):**

```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "Jane Doe"
}
```

---

## 3. User Management

### `POST /users`

Register a new system user.

* **Authentication:** None (Public)
* **Request Body:**

```json
{
  "email": "newuser@example.com",
  "name": "John Smith",
  "password": "Password123!"
}
```

* **Response (201 Created):**

```json
{
  "id": 2,
  "email": "newuser@example.com",
  "name": "John Smith"
}
```

---

## 4. Team Workspaces & Membership

### `POST /teams`

Create a new team workspace. The creating user automatically becomes the team `OWNER`.

* **Authentication:** Required
* **Request Body:**

```json
{
  "name": "Backend Engineering"
}
```

* **Response (201 Created):**

```json
{
  "id": 10,
  "name": "Backend Engineering",
  "role": "OWNER"
}
```

### `POST /teams/{team_id}/members`

Add a user to an existing team with a specified role (`OWNER` or `MEMBER`).

* **Authentication:** Required (Must be Team `OWNER`)
* **Path Parameters:**
  * `team_id` (integer): ID of the team.
* **Request Body:**

```json
{
  "user_id": 2,
  "role": "MEMBER"
}
```

* **Response (200 OK):**

```json
{
  "team_id": 10,
  "user_id": 2,
  "role": "MEMBER",
  "message": "User successfully added to team."
}
```

---

## 5. Note Operations

### `POST /notes`

Create a note with a defined visibility (`PRIVATE`, `TEAM`, or `PUBLIC`).

* **Authentication:** Required
* **Request Body:**

```json
{
  "text": "Sprint planning notes for Q4 API updates.",
  "visibility": "TEAM",
  "team_id": 10
}
```

* **Response (201 Created):**

```json
{
  "id": 101,
  "owner_user_id": 1,
  "team_id": 10,
  "text": "Sprint planning notes for Q4 API updates.",
  "visibility": "TEAM"
}
```

### `GET /notes`

List notes accessible to the requesting user based on ownership, team memberships, or public visibility.

* **Authentication:** Required
* **Query Parameters:**
  * `team_id` (optional integer): Filter notes by a specific team context.
  * `visibility` (optional string): Filter by `PRIVATE`, `TEAM`, or `PUBLIC`.
* **Response (200 OK):**

```json
[
  {
    "id": 101,
    "owner_user_id": 1,
    "team_id": 10,
    "text": "Sprint planning notes for Q4 API updates.",
    "visibility": "TEAM"
  },
  {
    "id": 102,
    "owner_user_id": 1,
    "team_id": null,
    "text": "Personal reminder.",
    "visibility": "PRIVATE"
  }
]
```

### `GET /notes/{note_id}`

Retrieve a single note by ID. Access is granted if:
1. User is the note owner.
2. Note visibility is `PUBLIC`.
3. Note visibility is `TEAM` and user belongs to the associated `team_id`.

* **Authentication:** Required
* **Response (200 OK):**

```json
{
  "id": 101,
  "owner_user_id": 1,
  "team_id": 10,
  "text": "Sprint planning notes for Q4 API updates.",
  "visibility": "TEAM"
}
```

### `PUT /notes/{note_id}`

Update the content or visibility of a note.

* **Authentication:** Required (Must be Note Owner)
* **Request Body:**

```json
{
  "text": "Updated sprint planning notes with revised timelines.",
  "visibility": "TEAM"
}
```

* **Response (200 OK):**

```json
{
  "id": 101,
  "owner_user_id": 1,
  "team_id": 10,
  "text": "Updated sprint planning notes with revised timelines.",
  "visibility": "TEAM"
}
```

### `DELETE /notes/{note_id}`

Delete a note.

* **Authentication:** Required (Must be Note Owner or Team `OWNER` of the associated team)
* **Response (204 No Content)**

---

## 6. Standard Error Responses

| Status Code | Code | Reason |
| --- | --- | --- |
| `400 Bad Request` | `INVALID_INPUT` | Payload missing required fields or validation failed. |
| `401 Unauthorized` | `UNAUTHENTICATED` | Session token missing or invalid. |
| `403 Forbidden` | `PERMISSION_DENIED` | Insufficient permissions to access or modify resource. |
| `404 Not Found` | `NOT_FOUND` | Note, Team, or User ID does not exist. |