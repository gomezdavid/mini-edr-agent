from typing import Optional
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# Files

class FileInfo(BaseModel):
    path: str
    size_bytes: int
    permissions: str
    sha256: str
    created_at: str
    modified_at: str
    accessed_at: str


class DeleteResponse(BaseModel):
    path: str
    status: str
    message: str


# Audit

class AuditLog(BaseModel):
    id: Optional[int] = None
    timestamp: str
    action: str
    path: str
    status: str
    detail: Optional[str] = None
