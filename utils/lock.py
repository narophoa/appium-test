from filelock import FileLock
import os

LOCK_FILE = os.path.join(os.getcwd(), "init.lock")
init_lock = FileLock(LOCK_FILE)
