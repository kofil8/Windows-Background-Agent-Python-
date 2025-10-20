"""
Windows Background Agent - Python Edition
-----------------------------------------
Author: Mohammad Kofil
Description:
    Lightweight Windows background agent that:
    - Starts automatically at system boot
    - Runs silently (no console window)
    - Monitors user login/logout events
    - Creates separate log files per user
    - Ensures only one instance runs
    - Can be built into a standalone .exe using PyInstaller
"""

import os
import sys
import time
import psutil
import winreg
import win32evtlog
import win32evtlogutil
from pathlib import Path
from datetime import datetime

# ----------------------------
# CONFIGURATION
# ----------------------------
LOG_DIR = Path("C:/UserActivityLogs")          # Log folder
EVENT_LOG_TYPE = "Security"                    # Windows Event Log type
LOGIN_EVENT_ID = 4624                          # Successful login
LOGOUT_EVENT_ID = 4634                         # Logoff
CHECK_INTERVAL = 10                            # Seconds between event scans

# ----------------------------
# SINGLE INSTANCE CHECK
# ----------------------------
def ensure_single_instance():
    """Prevents duplicate instances of the agent."""
    current_pid = os.getpid()
    current_name = os.path.basename(sys.argv[0])

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == current_name and proc.info['pid'] != current_pid:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    print("[✓] Single instance ensured.")

# ----------------------------
# ADD TO WINDOWS STARTUP
# ----------------------------
def add_to_startup():
    """Adds the agent to Windows startup (for all users)."""
    try:
        exe_path = os.path.abspath(sys.argv[0])
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"

        # Open the registry key and add a startup entry
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_ALL_ACCESS) as reg_key:
            winreg.SetValueEx(reg_key, "WindowsAgent", 0, winreg.REG_SZ, exe_path)

        print("[✓] Added to startup (All Users).")
    except PermissionError:
        print("[!] Administrator privileges required to add to startup.")
    except Exception as e:
        print(f"[!] Failed to add to startup: {e}")

# ----------------------------
# LOGGING FUNCTION
# ----------------------------
def log_event(username: str, event_type: str):
    """Writes a timestamped event to a user's log file."""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOG_DIR / f"{username}.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {event_type}\n")
    except Exception as e:
        print(f"[!] Logging failed: {e}")

# ----------------------------
# EVENT MONITOR FUNCTION
# ----------------------------
def monitor_user_activity():
    """Continuously monitors login/logout events using Windows Event Logs."""
    print("[✓] Monitoring Windows Security Event Logs...")

    server = 'localhost'
    handle = win32evtlog.OpenEventLog(server, EVENT_LOG_TYPE)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    processed_records = set()

    while True:
        try:
            events = win32evtlog.ReadEventLog(handle, flags, 0)
            if not events:
                time.sleep(CHECK_INTERVAL)
                continue

            for event in events:
                if event.RecordNumber in processed_records:
                    continue
                processed_records.add(event.RecordNumber)

                if event.EventID in [LOGIN_EVENT_ID, LOGOUT_EVENT_ID]:
                    username = "Unknown"

                    # Extract username from event data
                    try:
                        if event.StringInserts:
                            for s in event.StringInserts:
                                if "\\" in s:  # domain\username pattern
                                    username = s.split("\\")[-1]
                                    break
                    except Exception:
                        pass

                    event_type = "LOGIN" if event.EventID == LOGIN_EVENT_ID else "LOGOUT"
                    log_event(username, event_type)

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print(f"[!] Event monitor error: {e}")
            time.sleep(15)

# ----------------------------
# MAIN EXECUTION
# ----------------------------
if __name__ == "__main__":
    ensure_single_instance()
    add_to_startup()
    monitor_user_activity()
