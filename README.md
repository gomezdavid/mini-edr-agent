# Mini EDR

A lightweight Endpoint Detection and Response agent built with FastAPI and SQLite. The agent monitors the local system and exposes an HTTP API to query real-time data about running processes, active network connections, and file management.

## Technologies

- **FastAPI** — HTTP API framework
- **SQLite** — local persistence for system events and audit logs
- **psutil** — system and process monitoring
- **Pydantic** — data validation and serialization
- **PyJWT** — JWT authentication
- **Uvicorn** — ASGI server

## Concepts applied

- Separation of concerns across multiple modules (`database.py`, `models.py`, `agent.py`, `auth.py`, `files.py`, `audit.py`, `main.py`)
- SQLite persistence with timestamped event snapshots
- Dependency injection with `Depends` for database connection management
- OS-level introspection with `psutil` (processes, network connections)
- Automatic error handling for volatile system data (`NoSuchProcess`, `AccessDenied`)
- JWT authentication with token expiration
- Localhost-only middleware
- Protected paths policy system
- Audit logging to both file and SQLite
- SHA256 file integrity verification

## Installation

```bash
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your values

# Run the agent
uvicorn main:app --reload
```

Interactive documentation available at `http://localhost:8000/docs`.

The database file `edr.db` and audit log `audit.log` are created automatically on first run.

## Authentication

All endpoints except `/auth/login` require a JWT token.

```bash
# 1. Login to get a token
POST /auth/login
{
  "username": "admin",
  "password": "admin123"
}

# 2. Use the token in subsequent requests
Authorization: Bearer <token>
```

## Endpoints

### Auth
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/auth/login` | Returns a JWT token |

### Processes
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/processes` | Captures and returns a snapshot of all running processes |

### Connections
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/connections` | Captures and returns a snapshot of all active network connections |

### Files
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/files/info` | Returns permissions, SHA256 hash and timestamps of a file |
| DELETE | `/files` | Deletes a file — blocked if path is protected |

### Audit
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/audit` | Returns all audit log entries stored in the database |

## Protected paths

The following paths are protected and cannot be deleted:

- `C:\Windows`
- `C:\Windows\System32`
- `C:\Program Files`
- `C:\Program Files (x86)`
- `~\AppData`

Any deletion attempt on these paths is blocked and logged.

## Project structure

```
.
├── main.py         # FastAPI app, endpoints and middleware
├── agent.py        # system data collection logic (psutil)
├── auth.py         # JWT authentication
├── files.py        # file management and protected paths
├── audit.py        # audit logging to file and SQLite
├── database.py     # SQLite connection and table initialization
├── models.py       # Pydantic models
├── config.py       # configuration and protected paths
├── tests/
│   ├── __init__.py
│   └── test_auth.py
├── .env.example
├── requirements.txt
└── edr.db          # SQLite database (auto-generated)
```

## Running tests

```bash
pytest tests/ -v
```