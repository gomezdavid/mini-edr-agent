from typing import Optional
from pydantic import BaseModel

class Process(BaseModel):
    id: Optional[int] = None
    pid: int
    name: str
    username: Optional[str] = None
    cpu: Optional[float] = None
    memory: Optional[float] = None
    timestamp: str

class Connection(BaseModel):
    id: Optional[int] = None
    local_ip: Optional[str] = None
    local_port: Optional[int] = None
    remote_ip: Optional[str] = None
    remote_port: Optional[int] = None
    status: Optional[str] = None
    timestamp: str

class FileEvent(BaseModel):
    id: Optional[int] = None
    path: str
    event: str
    timestamp: str