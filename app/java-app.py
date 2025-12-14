import time
import random
import traceback
import os
from datetime import datetime

LOG_DIR = "logs"

LOG_FILES = [
    "application.log",
    "error.log",
    "access.log",
    "audit.log"
]

# --- Ensure log directory and files exist ---
os.makedirs(LOG_DIR, exist_ok=True)

for log_file in LOG_FILES:
    path = os.path.join(LOG_DIR, log_file)
    if not os.path.exists(path):
        open(path, "a").close()
# -------------------------------------------

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

def write(file, line):
    with open(os.path.join(LOG_DIR, file), "a") as f:
        f.write(line + "\n")

def app_log(level, thread, logger, msg):
    write(
        "application.log",
        f"{ts()} {level:<5} [{thread}] {logger:<35} - {msg}"
    )

def error_log(thread, logger, msg):
    write(
        "error.log",
        f"{ts()} ERROR [{thread}] {logger:<35} - {msg}"
    )
    try:
        raise TimeoutError("Query timed out")
    except Exception:
        for l in traceback.format_exc().splitlines():
            write("error.log", f"    {l}")

def access_log():
    write(
        "access.log",
        f'203.0.113.{random.randint(1,255)} - - '
        f'[14/Mar/2025:14:12:01 +0000] '
        f'"GET /api/v1/users/42 HTTP/1.1" '
        f'{random.choice([200,200,200,500])} '
        f'{random.randint(200,1500)} '
        f'{random.randint(10,250)}'
    )

def audit_log():
    write(
        "audit.log",
        f"{ts()} INFO  AUDIT User admin logged in from 192.0.2.{random.randint(1,255)}"
    )

THREADS = [
    "http-nio-8080-exec-1",
    "http-nio-8080-exec-3",
    "http-nio-8080-exec-5"
]

LOGGERS = [
    "c.e.user.UserController",
    "c.e.user.UserService"
]

while True:
    thread = random.choice(THREADS)
    logger = random.choice(LOGGERS)

    app_log("INFO", thread, logger, "Received request GET /api/v1/users/42")
    access_log()

    if random.random() < 0.15:
        error_log(thread, logger, "Database timeout while fetching user id=42")
    else:
        app_log("INFO", thread, logger, "Successfully fetched user id=42")

    if random.random() < 0.2:
        audit_log()

    time.sleep(1)
