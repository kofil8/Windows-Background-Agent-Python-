## 🧠 README.md

```markdown
# 🪶 Windows Background Agent (Python)

### 🔧 Developed by [Mohammad Kofil](https://github.com/kofil8)

A **lightweight Windows background agent** built with Python that runs silently, starts automatically for all users at system boot, and logs user login/logout activities into separate text files per user.

This agent is fully self-contained and can be compiled into a `.exe` to run on any Windows system **without needing Python installed**.

---

## 🚀 Features

✅ Runs silently in the background (no visible console)  
✅ Auto-starts on system boot for all users  
✅ Logs all user login/logout activities  
✅ Creates a **separate log file per user**  
✅ Prevents duplicate running instances  
✅ Works as a standalone `.exe` (built with PyInstaller)  
✅ Compatible with Windows 10 and 11

---

## 🗂️ Project Structure
```

windows_agent/
│
├── agent.py # Main agent script
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── dist/ # (Generated) Folder containing compiled .exe after build

````

---

## ⚙️ Requirements

- Windows 10 / 11
- Python 3.9 or newer
- Administrator privileges (for registry access)

---

## 🧩 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/kofil8/windows-agent.git
cd windows-agent
````

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies:

- `pywin32` → Access Windows APIs (Event Log + Registry)
- `psutil` → Manage running processes
- `pyinstaller` → Build the executable

---

## 🧪 Running the Agent (Test Mode)

You can test the script before building it into an executable.

```bash
python agent.py
```

Expected console output:

```
[✓] Single instance ensured.
[✓] Added to startup (All Users).
[✓] Monitoring Windows Security Event Logs...
```

Now log in/out or lock/unlock your computer — logs will appear under:

```
C:\UserActivityLogs\
```

Each user will have their own log file, e.g.:

```
C:\UserActivityLogs\john.txt
C:\UserActivityLogs\mary.txt
```

Each log entry includes a timestamp and event type:

```
[2025-10-20 19:31:20] LOGIN
[2025-10-20 19:45:33] LOGOUT
```

---

## 🏗️ Building the Executable

To create a standalone `.exe` that runs on any Windows system:

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build the Binary

```bash
pyinstaller --noconsole --onefile agent.py
```

This generates:

```
dist/agent.exe
```

✅ The `--noconsole` flag hides the terminal window
✅ The `--onefile` flag bundles everything into a single `.exe`

---

## 🧰 Deployment

### 🪄 1️⃣ Run the `.exe` as Administrator

Right-click → “Run as administrator”

It will:

- Add itself to Windows Startup (`HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run`)
- Start monitoring login/logout events automatically

---

### 🪄 2️⃣ Auto-Startup Verification

Open Registry Editor:

```
Win + R → regedit
```

Navigate to:

```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```

You’ll see:

```
WindowsAgent    REG_SZ    C:\path\to\agent.exe
```

That confirms persistent startup ✅

---

### 🪄 3️⃣ Log Verification

After some usage or after reboot, check:

```
C:\UserActivityLogs\
```

You’ll see per-user text logs like:

```
[2025-10-20 10:12:30] LOGIN
[2025-10-20 11:05:42] LOGOUT
```

---

## 🧹 Uninstall / Remove Agent

If you want to stop and remove the agent:

1. Delete registry entry:

   ```
   HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\WindowsAgent
   ```

2. Delete the log folder:

   ```
   C:\UserActivityLogs\
   ```

3. Delete the `agent.exe` file.

---

## 🧩 Optional: Create a Windows Installer (Inno Setup)

To distribute professionally, you can wrap the `.exe` into a silent installer.

Example Inno Setup script (`windows_agent_installer.iss`):

```iss
[Setup]
AppName=Windows Agent
AppVersion=1.0
DefaultDirName={pf}\WindowsAgent
DefaultGroupName=WindowsAgent
OutputBaseFilename=WindowsAgent_Installer

[Files]
Source: "dist\agent.exe"; DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "{app}\agent.exe"; Flags: runhidden
```

Then build it using [Inno Setup](https://jrsoftware.org/isinfo.php).

---

## 🧠 Technical Notes

- Uses Windows Security Event Log to capture event IDs:

  - `4624` → Login
  - `4634` → Logout

- Uses `winreg` to persist startup for all users
- Prevents duplicates using `psutil`
- Automatically recreates missing log directories

---

## 🧑‍💻 Developer Info

**Author:** Mohammad Kofil
**Email:** [contact@devsyncbd.vercel.app](mailto:contact@devsyncbd.vercel.app)
**Website:** [https://devsyncbd.vercel.app](https://devsyncbd.vercel.app)

---

## 🪄 License

This project is released under the **MIT License** — you’re free to use and modify it for personal or commercial purposes.
