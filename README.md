# TeamNotes API

A high-performance, asynchronous RESTful API built with **FastAPI**, **SQLAlchemy 2.0**, and **SQLite**. Designed for managing users, teams, and persistent team notes with authorization and isolated test infrastructure.

---

## Features

- **Authentication & Authorization**: Bearer token authentication and user authorization checks.
- **Team Management**: Create teams, invite members, and manage team associations.
- **Notes Lifecycle**: Scoped access to team notes and private notes.
- **Isolated Multi-threaded Test Suite**: Standardized Pytest suite running against shared URI-mode SQLite in-memory databases.
- **Single-Container Docker Deployment**: Production-ready Docker and Docker Compose configuration with volume persistence.

---

## Project Structure

```text
team-notes/
├── app/
│   ├── config.py         # App settings & environment resolution
│   ├── database.py       # Lazy SQLAlchemy engine & session factory
│   ├── main.py           # FastAPI application entry point
│   ├── models/           # SQLAlchemy ORM models (User, Team, Note)
│   └── routers/          # Route handlers (auth, users, teams, notes)
├── tests/                # Automated pytest suite
│   ├── conftest.py       # Fixtures & shared memory DB setup
│   ├── test_auth.py
│   ├── test_notes.py
│   └── test_teams.py
├── .gitignore            # Git exclusion rules
├── Dockerfile            # Container build specification
├── docker-compose.yml    # Service orchestration & volume mounting
├── pyproject.toml        # Build configuration & project metadata
└── requirements.txt      # Python dependencies
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional, for containerized execution)

### Local Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/team-notes.git
   cd team-notes
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the local development server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   Access the interactive API documentation at `http://127.0.0.1:8000/docs`.

---

## Running Tests

The test suite relies on Pytest and SQLite in-memory database configuration:

```bash
# Run the entire test suite
PYTHONPATH=. pytest -v

# Run tests with verbose output and stdout print statements
PYTHONPATH=. pytest -s -v
```

---

## Docker Deployment

Deploy the single-container setup using Docker Compose. Database files persist across container lifecycles in a mounted named volume (`sqlite_data`).

1. **Start the service:**
   ```bash
   docker compose up -d --build
   ```

2. **Check container logs:**
   ```bash
   docker compose logs -f
   ```

3. **Stop the service:**
   ```bash
   docker compose down
   ```

---

## Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `DATABASE_URL` | SQLAlchemy database connection URI | `sqlite:////app/data/app.db` |
| `ENVIRONMENT` | Application run mode (`development` / `production`) | `production` |