import os
import hashlib
from datetime import datetime
from config import PROTECTED_PATHS


def is_protected(filepath: str) -> bool:
    for protected in PROTECTED_PATHS:
        if filepath.lower().startswith(protected.lower()):
            return True
    return False


def get_sha256(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_file_info(filepath: str) -> dict:
    stat = os.stat(filepath)
    return {
        "path": filepath,
        "size_bytes": stat.st_size,
        "permissions": oct(stat.st_mode),
        "sha256": get_sha256(filepath),
        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "accessed_at": datetime.fromtimestamp(stat.st_atime).isoformat(),
    }


def delete_file(filepath: str) -> dict:
    if is_protected(filepath):
        return {"status": "blocked", "message": "Path is protected and cannot be deleted."}

    if not os.path.exists(filepath):
        return {"status": "error", "message": "File not found."}

    if os.path.isdir(filepath):
        return {"status": "error", "message": "Path points to a directory, not a file."}

    try:
        os.remove(filepath)
        return {"status": "success", "message": "File deleted successfully."}
    except PermissionError:
        return {"status": "error", "message": "Permission denied."}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}
