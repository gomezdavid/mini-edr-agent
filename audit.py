import logging
from datetime import datetime
from config import LOG_PATH, DB_PATH
import sqlite3

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)

logger = logging.getLogger("edr-audit")


def log_action(action: str, path: str, status: str, detail: str = None):
    timestamp = datetime.now().isoformat()

    # Guarda en el archivo de log
    message = f"{action} | {path} | {status}"
    if detail:
        message += f" | {detail}"
    logger.info(message)

    # Guarda en SQLite
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO audit_logs (timestamp, action, path, status, detail) VALUES (?,?,?,?,?)",
        (timestamp, action, path, status, detail)
    )
    conn.commit()
    conn.close()
