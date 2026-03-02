# Mini EDR
A lightweight Endpoint Detection and Response agent built with FastAPI and SQLite. The agent monitors the local system and exposes an HTTP API to query real-time data about running processes and active network connections.

## Technologies
- **FastAPI** — HTTP API framework
- **SQLite** — local persistence for system events
- **psutil** — system and process monitoring
- **Pydantic** — data validation and serialization
- **Uvicorn** — ASGI server

## Concepts applied
- Separation of concerns across multiple modules (`database.py`, `models.py`, `agent.py`, `main.py`)
- SQLite persistence with timestamped event snapshots
- Dependency injection with `Depends` for database connection management
- OS-level introspection with `psutil` (processes, network connections)
- Automatic error handling for volatile system data (`NoSuchProcess`, `AccessDenied`)

## Installation

```bash
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate     # Linux/Mac

# Install dependencies
pip install fastapi uvicorn psutil

# Run the agent
fastapi dev main.py
```

Interactive documentation available at `http://localhost:8000/docs`.

The database file `edr.db` is created automatically on first run.

## Endpoints
### GET /processes
Captures a snapshot of all currently running processes and stores it in the database. Returns the full history of recorded snapshots.

```
GET /processes
```

Response fields: `pid`, `name`, `username`, `cpu`, `memory`, `timestamp`

### GET /connections
Captures a snapshot of all active network connections and stores it in the database. Returns the full history of recorded snapshots.

```
GET /connections
```

Response fields: `local_ip`, `local_port`, `remote_ip`, `remote_port`, `status`, `timestamp`

## Project structure

```
.
├── main.py       # FastAPI app and endpoints
├── agent.py      # system data collection logic (psutil)
├── database.py   # SQLite connection and table initialization
├── models.py     # Pydantic models
└── edr.db        # SQLite database (auto-generated)
```

* will be adding new futures
