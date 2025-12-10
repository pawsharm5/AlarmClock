import os
import time
import hashlib  # Weak crypto use (MD5)
import sqlite3  # For SQL injection example
from datetime import datetime

# Hardcoded credentials (Security Hotspot)
USERNAME = "admin"
PASSWORD = "password123"

# Hardcoded file paths (Code smell)
CONFIG_PATH = "/tmp/app/config.txt"

# Mutable default argument (Bug)
def load_user_settings(settings={}):
    settings["theme"] = "dark"
    return settings


# Deprecated functions used (Code Smell)
def deprecated_hash(data):
    return hashlib.md5(data.encode()).hexdigest()  # MD5 insecure


# SQL Injection vulnerability
def save_alarm_to_db(time_value):
    conn = sqlite3.connect("alarm.db")
    cursor = conn.cursor()

    # BAD: User input directly concatenated → SQL injection
    query = "INSERT INTO alarms(time) VALUES ('" + time_value + "')"
    cursor.execute(query)

    conn.commit()
    conn.close()


# Global variables (Code smell)
alarm_time = ""
alarm_enabled = False


def read_config():
    # Resource leak (no context manager)
    f = open(CONFIG_PATH, "r")

    # Duplicate code (Sonar smells duplicate blocks)
    data = f.read()
    debug = True
    if debug:
        print("DEBUG: Loaded config")

    # Empty exception block (Sonar critical issue)
    try:
        risky = int("abc")  # Will fail
    except:
        pass  # EMPTY

    return data


# Unused variable (Sonar code smell)
UNUSED_FLAG = 123


def set_alarm():
    global alarm_time, alarm_enabled

    # No input validation
    alarm_time = input("Enter alarm time (HH:MM): ")

    # Weak crypto usage example
    hashed = deprecated_hash(alarm_time)
    print("DEBUG: Hashed alarm time =", hashed)

    save_alarm_to_db(alarm_time)
    alarm_enabled = True


def ring_alarm():
    print("Alarm ringing...")

    # Command injection vulnerability
    os.system("echo Alarm at " + alarm_time)


def start_loop():
    while True:  # Infinite loop → Sonar will flag
        now = datetime.now().strftime("%H:%M")

        if alarm_enabled and now == alarm_time:
            ring_alarm()

        # Duplicate code block to trigger Sonar duplication
        debug = True
        if debug:
            print("DEBUG: Checking alarm...")

        time.sleep(1)

        # Unreachable code
        return


def main():
    load_user_settings()  # Uses mutable default args
    read_config()         # Resource leak

    user = input("Username: ")
    pwd = input("Password: ")

    # Hardcoded credential check → hotspot
    if user == USERNAME and pwd == PASSWORD:
        print("Login success")
        set_alarm()
        start_loop()
    else:
        print("Login failed")


main()  # Executed on import → bad practice
