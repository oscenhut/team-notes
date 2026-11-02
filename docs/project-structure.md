team_notes/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── team.py
│   │   ├── user_team.py
│   │   └── note.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── team.py
│   │   ├── user_team.py
│   │   └── note.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── team.py
│   │   └── note.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── team.py
│   │   └── note.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── users.py
│       ├── teams.py
│       ├── notes.py
│       └── health.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_teams.py
│   ├── test_notes.py
│   └── test_health.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── alembic.ini