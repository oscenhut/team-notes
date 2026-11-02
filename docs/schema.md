# TeamNotes: Database Schema Specification

**Engine Target:** SQLite 3  
**Compatibility:** PostgreSQL / MySQL compliant ORM models  

---

## 1. Entity-Relationship Overview

```
 +------------------+           +--------------------+           +------------------+
 |      users       |           |     user_teams     |           |      teams       |
 +------------------+           +--------------------+           +------------------+
 | PK  id           |<----+     | PK, FK  user_id    |     +---->| PK  id           |
 |     email        |     +-----| PK, FK  team_id    |-----+     |     name         |
 |     name         |           |         role       |           +------------------+
 |     password_hash|           +--------------------+                    |
 +------------------+                                                     |
          |                                                               |
          | 1:N (Owner)                                                   | 1:N (Optional Workspace)
          v                                                               v
 +----------------------------------------------------------------------------------+
 |                                      notes                                       |
 +----------------------------------------------------------------------------------+
 | PK       id                                                                      |
 | FK       owner_user_id                                                           |
 | FK, Null team_id                                                                 |
 |          text                                                                    |
 |          visibility ('PRIVATE', 'TEAM', 'PUBLIC')                                |
 +----------------------------------------------------------------------------------+
```

---

## 2. Complete SQLite DDL

```sql
-- Enable foreign key support in SQLite (must be executed per connection session)
PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------------
-- Table: users
-- Stores individual user account identity and authentication credentials.
-- -----------------------------------------------------------------------------
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

-- -----------------------------------------------------------------------------
-- Table: teams
-- Stores collaborative workspace units.
-- -----------------------------------------------------------------------------
CREATE TABLE teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- -----------------------------------------------------------------------------
-- Table: user_teams
-- Junction table mapping users to teams with assigned workspace roles.
-- Roles:
--   - OWNER: Full access to manage team workspace and team members.
--   - MEMBER: Standard member access to create and read team notes.
-- -----------------------------------------------------------------------------
CREATE TABLE user_teams (
    user_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    role TEXT CHECK(role IN ('OWNER', 'MEMBER')) DEFAULT 'MEMBER',
    PRIMARY KEY (user_id, team_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- Table: notes
-- Stores note content linked to an owner, optional team workspace, and visibility.
-- Visibility:
--   - PRIVATE: Accessible exclusively by owner_user_id.
--   - TEAM: Accessible by any active member of the linked team_id.
--   - PUBLIC: Accessible across the system.
-- -----------------------------------------------------------------------------
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_user_id INTEGER NOT NULL,
    team_id INTEGER,
    text TEXT NOT NULL,
    visibility TEXT CHECK(visibility IN ('PRIVATE', 'TEAM', 'PUBLIC')) DEFAULT 'TEAM',
    FOREIGN KEY (owner_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL
);
```

---

## 3. Recommended Performance Indexes

```sql
-- Fast lookup of user email during login authentication
CREATE INDEX idx_users_email ON users(email);

-- Fast query resolution for note access filtering by owner
CREATE INDEX idx_notes_owner ON notes(owner_user_id);

-- Fast retrieval of notes scoped to a specific team workspace
CREATE INDEX idx_notes_team ON notes(team_id);

-- Fast join resolution for team membership checks
CREATE INDEX idx_user_teams_team ON user_teams(team_id);
```

---

## 4. Constraint & Cascade Specifications

| Child Table | Foreign Key Column | Parent Table | Action `ON DELETE` | Rationale |
|---|---|---|---|---|
| `user_teams` | `user_id` | `users(id)` | `CASCADE` | Deleting a user removes all their team membership associations. |
| `user_teams` | `team_id` | `teams(id)` | `CASCADE` | Deleting a team purges all membership records for that team. |
| `notes` | `owner_user_id` | `users(id)` | `CASCADE` | Deleting a user account deletes all notes owned by that user. |
| `notes` | `team_id` | `teams(id)` | `SET NULL` | Deleting a team preserves user notes but removes the team binding. |