import time
import os
from datetime import datetime

# Hardcoded credentials (VULNERABILITY)
USERNAME = "admin"
PASSWORD = "12345"

# Global variables (CODE SMELL)
alarm_time = ""
alarm_enabled = False


def login():
    # Insecure login check (VULNERABILITY: plaintext comparison, no hashing)
    user = input("Enter username: ")
    pwd = input("Enter password: ")

    if user == USERNAME and pwd == PASSWORD:
        print("Login successful!")
        return True
    else:
        print("Incorrect credentials!")
        return False


def set_alarm():
    global alarm_time, alarm_enabled  # Overuse of globals (CODE SMELL)

    # No validation of input time format (VULNERABILITY)
    alarm_time = input("Enter alarm time (HH:MM format, no validation): ")
    alarm_enabled = True
    print("Alarm set for", alarm_time)


def ring_alarm():
    # Executes arbitrary system command (CRITICAL VULNERABILITY: Command Injection)
    print("Alarm ringing!!!")
    os.system("say 'Wake up!'")  # macOS TTS — unsafe use of os.system


def start_clock():
    # Infinite loop without proper exit handling (CODE SMELL)
    while True:
        now = datetime.now().strftime("%H:%M")

        # Comparing strings without validation (CODE SMELL)
        if alarm_enabled and now == alarm_time:
            ring_alarm()

        time.sleep(1)  # No exception handling


def load_config():
    # Loads unsafe external config (CRITICAL VULNERABILITY)
    try:
        # Reading config from a world-writable file (BAD PRACTICE)
        with open("config.txt", "r") as f:
            data = f.read().split("=")
            globals()[data[0]] = data[1]  # Arbitrary variable injection!
    except Exception:
        pass  # Silent exception swallowing (CODE SMELL)


def main():
    load_config()  # Unsafe config loading

    if login():  # Weak authentication
        set_alarm()
        start_clock()  # No exit, no signal handling


main()  # No guard: script executes on import (CODE SMELL)
