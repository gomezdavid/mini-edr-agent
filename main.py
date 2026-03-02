import sqlite3
from fastapi import FastAPI, Depends
from database import get_db, init_db
from models import Process, Connection
from agent import collect_processes, collect_connections

app = FastAPI(title="Mini EDR")

init_db()


@app.get("/")
def root():
    return {"message": "Mini EDR running"}


@app.get("/processes", response_model=list[Process])
def get_processes(db: sqlite3.Connection = Depends(get_db)):
    processes = collect_processes()
    for p in processes:
        db.execute(
            "INSERT INTO processes (pid, name, username, cpu, memory, timestamp) VALUES (?,?,?,?,?,?)",
            (p["pid"], p["name"], p["username"],
             p["cpu"], p["memory"], p["timestamp"])
        )
    db.commit()
    rows = db.execute("SELECT * FROM processes").fetchall()
    return [Process(**dict(r)) for r in rows]


@app.get("/connections", response_model=list[Connection])
def get_connections(db: sqlite3.Connection = Depends(get_db)):
    connections = collect_connections()
    for c in connections:
        db.execute(
            "INSERT INTO connections (local_ip, local_port, remote_ip, remote_port, status, timestamp) VALUES (?,?,?,?,?,?)",
            (c["local_ip"], c["local_port"], c["remote_ip"],
             c["remote_port"], c["status"], c["timestamp"])
        )
    db.commit()
    rows = db.execute("SELECT * FROM connections").fetchall()
    return [Connection(**dict(r)) for r in rows]
