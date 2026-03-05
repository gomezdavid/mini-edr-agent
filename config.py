import os
from dotenv import load_dotenv

load_dotenv()

#JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

#Credentials
VALID_USERNAME = os.getenv("VALID_USERNAME")
VALID_PASSWORD = os.getenv("VALID_PASSWORD")

#Protected Paths
PROTECTED_PATHS = [
    "C:\\Windows",
    "C:\\Windows\\System32",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    os.path.expanduser("~\\AppData"),
]

#DDBB and LOGS
DB_PATH = "edr.db"
LOG_PATH = "audit.log"