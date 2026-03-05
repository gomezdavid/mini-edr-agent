from fastapi import FastAPI, Depends, HTTPException, Request
import sqlite3
from fastapi.responses import JSONResponse
from database import get_db, init_db
from models import LoginRequest, TokenResponse, FileInfo, DeleteResponse, AuditLog
from auth import create_token, authenticate_user, verify_token
from files import get_file_info, delete_file, is_protected
from audit import log_action
from config import DB_PATH

app = FastAPI(
    title="EDR Agent",
    description="Endpoint Detection and Response agent API",
    version="1.0.0"
)

init_db()


# Middleware: solo localhost

@app.middleware("http")
async def localhost_only(request: Request, call_next):
    if request.client is None or request.client.host not in ("127.0.0.1", "::1", "testclient"):
        return JSONResponse(status_code=403, content={"detail": "Forbidden"})
    return await call_next(request)


# Auth

@app.post("/auth/login", response_model=TokenResponse, tags=["Auth"])
def login(credentials: LoginRequest):
    if not authenticate_user(credentials.username, credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    token = create_token(credentials.username)
    return TokenResponse(access_token=token, token_type="bearer")


# Files

@app.get("/files/info", response_model=FileInfo, tags=["Files"])
def file_info(
    path: str,
    username: str = Depends(verify_token)
):
    import os
    if not os.path.exists(path):
        log_action("INFO", path, "ERROR", "File not found")
        raise HTTPException(status_code=404, detail="File not found.")
    if os.path.isdir(path):
        log_action("INFO", path, "ERROR", "Path is a directory")
        raise HTTPException(
            status_code=400, detail="Path points to a directory.")
    if is_protected(path):
        log_action("INFO", path, "BLOCKED", "Protected path")
        raise HTTPException(status_code=403, detail="Path is protected.")

    info = get_file_info(path)
    log_action("INFO", path, "SUCCESS")
    return FileInfo(**info)


@app.delete("/files", response_model=DeleteResponse, tags=["Files"])
def delete(
    path: str,
    username: str = Depends(verify_token)
):
    result = delete_file(path)
    log_action("DELETE", path, result["status"].upper(), result["message"])

    if result["status"] == "blocked":
        raise HTTPException(status_code=403, detail=result["message"])
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return DeleteResponse(path=path, status=result["status"], message=result["message"])


# Audit logs

@app.get("/audit", response_model=list[AuditLog], tags=["Audit"])
def get_audit_logs(
    db: sqlite3.Connection = Depends(get_db),
    username: str = Depends(verify_token)
):
    rows = db.execute(
        "SELECT * FROM audit_logs ORDER BY timestamp DESC").fetchall()
    return [AuditLog(**dict(r)) for r in rows]
