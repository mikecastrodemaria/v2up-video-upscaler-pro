# Fixing the orjson DLL Load Error

## Problem

You're currently running:
- **Python 3.12.0b3** (beta version)
- **venv** based on the beta interpreter
- **orjson 3.11.5** installed in the beta-based venv

**orjson** (and many other compiled Python packages) only support **stable** Python releases. Running them on beta/RC/alpha versions causes DLL load failures on Windows.

## Solution: Install Stable Python

### Step 1: Check Current Python Installations

Run the provided checker script:
```bash
check_python.bat
```

This will show all Python installations and highlight which are stable vs beta/RC.

### Step 2: Install a Stable Python Version

Download and install a **stable** Python release (NOT beta/RC/alpha):

**Recommended Downloads:**
- **Python 3.12.7** (latest stable 3.12): https://www.python.org/downloads/release/python-3127/
- **Python 3.11.9** (latest stable 3.11): https://www.python.org/downloads/release/python-3119/

**Installation Instructions:**
1. Click on "Windows installer (64-bit)" under Files
2. Run the installer
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Complete the installation

### Step 3: Verify Stable Python Installation

After installing, run:
```bash
check_python.bat
```

You should see:
```
[Found] Python 3.12:
  Python 3.12.7
  [OK] Stable release
```

Or check manually:
```bash
py -3.12 --version
```

Should show something like `Python 3.12.7` (NO "b" or "rc" suffix).

### Step 4: Remove Old Virtual Environment

Delete the old venv that was created with the beta Python:
```bash
rmdir /s /q venv
```

Or manually delete the `venv` folder.

### Step 5: Run Installation Script

Now run the installation script, which will use the stable Python:
```bash
install.bat
```

The script will now:
- Detect if you're using a beta version and reject it
- Create a new venv with the stable Python interpreter
- Install all dependencies including orjson

### Step 6: Verify the Fix

After installation completes, activate the venv and verify:

```bash
venv\Scripts\activate.bat
python -c "import struct, sys; print(sys.version, struct.calcsize('P')*8)"
python -c "import orjson; print('orjson imported successfully')"
```

You should see:
- Python version WITHOUT "b" (beta) suffix
- "64" at the end (64-bit)
- "orjson imported successfully"

## Quick Reference Commands

### Check which Python versions are installed:
```bash
py --list
```

### Create venv with specific Python version:
```bash
py -3.12 -m venv venv          # For Python 3.12
py -3.11 -m venv venv          # For Python 3.11
```

### Activate the new venv:
```bash
venv\Scripts\activate.bat
```

### Verify you're using the correct Python:
```bash
python --version
python -c "import sys; print(sys.executable)"
```

## Why This Happens

- **Beta/RC/Alpha Python versions** have unstable ABIs (Application Binary Interfaces)
- **Compiled extensions** like orjson are built for stable Python releases only
- The DLL files in orjson expect the stable Python runtime, not the beta runtime
- This mismatch causes "DLL load failed" errors on Windows

## Prevention

When installing Python in the future:
1. Always use stable releases for production/development work
2. Only use beta/RC versions for testing Python itself
3. Check the version carefully - avoid versions with "b", "rc", or "a" suffixes

## Still Having Issues?

If you continue to see errors after following these steps:

1. Verify you're in the correct venv:
   ```bash
   where python
   ```
   Should show: `C:\Users\mikec\Documents\v2up\venv\Scripts\python.exe`

2. Check installed packages:
   ```bash
   pip list | findstr orjson
   ```

3. Try manually installing orjson:
   ```bash
   pip uninstall orjson -y
   pip install orjson --no-cache-dir
   ```

4. Verify Python architecture:
   ```bash
   python -c "import struct; print(struct.calcsize('P')*8)"
   ```
   Must show `64` (64-bit)
