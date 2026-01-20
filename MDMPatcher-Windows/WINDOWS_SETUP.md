# Windows Installation & Setup Guide

## Prerequisites Installation

### 1. Install Python

1. Download Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

### 2. Install iTunes (for iOS Device Drivers)

**Option A: Full iTunes**
1. Download from [apple.com/itunes](https://www.apple.com/itunes/download/)
2. Install and restart your computer
3. You don't need to run iTunes, just have it installed for the drivers

**Option B: Apple Mobile Device Support Only** (Advanced)
1. Download iTunes installer but don't run it
2. Extract it using 7-Zip or similar
3. Install only these components:
   - AppleMobileDeviceSupport64.msi
   - AppleApplicationSupport.msi

### 3. Install libimobiledevice Tools

**Option A: Using Chocolatey (Recommended)**

1. Install Chocolatey package manager:
   - Open PowerShell as Administrator
   - Run:
     ```powershell
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
     ```

2. Install libimobiledevice:
   ```cmd
   choco install libimobiledevice
   ```

**Option B: Manual Installation**

1. Download from [libimobiledevice-win32 releases](https://github.com/libimobiledevice-win32/imobiledevice-net/releases)
2. Download the latest `imobiledevice-net-x.x.x.zip`
3. Extract the ZIP file
4. Add to PATH:
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment Variables
   - Under "System Variables", find "Path" and click Edit
   - Click "New" and add the path to the extracted folder
   - Click OK on all dialogs
   - Restart Command Prompt

5. Verify installation:
   ```cmd
   ideviceinfo --version
   idevicebackup2 --version
   idevice_id --version
   ```

**Option C: Place in MDMPatcher Directory**

If you can't modify PATH, copy these files to the `MDMPatcher-Windows` folder:
- `ideviceinfo.exe`
- `idevicebackup2.exe`
- `idevice_id.exe`
- All required DLL files

---

## Installing MDMPatcher

### Step 1: Download MDMPatcher

```cmd
git clone https://github.com/KimWash/MDMPatcher-Enhanced.git
cd MDMPatcher-Enhanced\MDMPatcher-Windows
```

Or download and extract the ZIP from GitHub.

### Step 2: Install Python Dependencies

Open Command Prompt in the `MDMPatcher-Windows` folder:

```cmd
pip install -r requirements.txt
```

If you encounter permission errors:
```cmd
pip install --user -r requirements.txt
```

### Step 3: Verify Installation

```cmd
python main.py
```

You should see the MDMPatcher window open.

---

## USB Driver Setup

### Installing USB Drivers for iOS Devices

1. **With iTunes**: Drivers are installed automatically
2. **Without iTunes**: You need Apple Mobile Device Support

### Troubleshooting USB Issues

**Device Not Recognized**

1. Open Device Manager (Win + X → Device Manager)
2. Look for your iOS device under "Portable Devices" or "Universal Serial Bus devices"
3. If you see a yellow exclamation mark:
   - Right-click → Update Driver
   - Browse my computer for drivers
   - Select the iTunes driver folder (usually `C:\Program Files\Common Files\Apple\Mobile Device Support\Drivers`)

**USB Port Issues**

- Try different USB ports
- Use USB 2.0 ports instead of USB 3.0 if possible
- Avoid USB hubs, connect directly to the computer
- Try a different USB cable

---

## Running MDMPatcher

### Basic Usage

1. Open Command Prompt
2. Navigate to MDMPatcher-Windows folder:
   ```cmd
   cd path\to\MDMPatcher-Enhanced\MDMPatcher-Windows
   ```
3. Run:
   ```cmd
   python main.py
   ```

### Creating a Shortcut

1. Right-click on `main.py`
2. Create shortcut
3. Right-click the shortcut → Properties
4. In "Target" field, add `python` before the path:
   ```
   python "C:\path\to\MDMPatcher-Windows\main.py"
   ```
5. Change "Start in" to the MDMPatcher-Windows folder
6. Click OK

### Running as Administrator (if needed)

Some USB operations may require admin rights:

1. Right-click Command Prompt
2. Select "Run as administrator"
3. Navigate to folder and run `python main.py`

---

## Windows Defender & Antivirus

### Adding Exclusions

Windows Defender may flag the application:

1. Open Windows Security
2. Go to Virus & threat protection
3. Manage settings
4. Scroll to Exclusions
5. Add an exclusion
6. Choose "Folder"
7. Select the `MDMPatcher-Windows` folder

### Allowing Python Scripts

If Windows SmartScreen blocks execution:

1. Click "More info"
2. Click "Run anyway"

---

## Troubleshooting

### Python Not Found

**Error**: `'python' is not recognized as an internal or external command`

**Solutions**:
1. Reinstall Python and check "Add Python to PATH"
2. Or use full path:
   ```cmd
   C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\python.exe main.py
   ```

### Module Not Found Errors

**Error**: `ModuleNotFoundError: No module named 'PyQt6'`

**Solutions**:
```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### libusb Error

**Error**: `libusb is not found`

**Solutions**:
1. Install libusb via Chocolatey:
   ```cmd
   choco install libusb
   ```
2. Or download from [libusb.info](https://libusb.info/)

### Access Denied Errors

**Solutions**:
1. Run as Administrator
2. Check antivirus isn't blocking access
3. Ensure device is unlocked and trusted

### Device Trust Issues

**Problem**: Device asks to "Trust This Computer"

**Solutions**:
1. Unlock device with passcode
2. Tap "Trust" on device
3. Wait 10 seconds
4. Reconnect device

---

## Command Line Options (Future)

```cmd
# Check version
python main.py --version

# Verbose logging
python main.py --verbose

# Specify libimobiledevice path
python main.py --tools-path "C:\path\to\tools"
```

---

## Building Standalone Executable

### Using PyInstaller

1. Install PyInstaller:
   ```cmd
   pip install pyinstaller
   ```

2. Build executable:
   ```cmd
   pyinstaller --onefile --windowed --name "MDMPatcher-Enhanced" --icon=icon.ico main.py
   ```

3. Find executable in `dist\` folder

4. Copy required files:
   - `resources\` folder
   - libimobiledevice tools (if not in PATH)

### Distribution Package

Create a folder with:
```
MDMPatcher-Enhanced/
├── MDMPatcher-Enhanced.exe
├── resources/
│   └── templates/
│       ├── extension1.pdf
│       ├── extension2.pdf
│       └── libiMobileeDevice.dylib
├── tools/                    # libimobiledevice tools
│   ├── ideviceinfo.exe
│   ├── idevicebackup2.exe
│   └── idevice_id.exe
│       └── (all required DLLs)
└── README.txt
```

---

## Performance Tips

1. **Disable Antivirus Temporarily**: During patching for better performance
2. **Close Other Applications**: Especially iTunes
3. **Use USB 2.0 Ports**: Better compatibility
4. **Keep Device Unlocked**: During the process

---

## Getting Help

If you encounter issues:

1. Check this guide first
2. Review the main README.md
3. Search for similar issues on GitHub
4. Create a new issue with:
   - Windows version
   - Python version
   - Full error message
   - Steps to reproduce

---

## Advanced Configuration

### Custom Tool Paths

Edit `main.py` to specify tool locations:

```python
# Custom paths
IDEVICEINFO_PATH = r"C:\tools\ideviceinfo.exe"
IDEVICEBACKUP2_PATH = r"C:\tools\idevicebackup2.exe"
```

### Debug Mode

Add debug output:

```cmd
python main.py --debug
```

Or set environment variable:
```cmd
set MDMPATCHER_DEBUG=1
python main.py
```

---

## Security Considerations

- **Run from Trusted Source**: Only download from official GitHub
- **Verify File Hashes**: Check SHA-256 hashes of downloads
- **Use Antivirus**: Keep Windows Defender enabled
- **No Network Access**: Application works offline
- **Review Code**: Python source is readable and auditable

---

## Updating MDMPatcher

```cmd
cd MDMPatcher-Enhanced
git pull origin main
cd MDMPatcher-Windows
pip install --upgrade -r requirements.txt
```

---

## Uninstalling

1. Delete the `MDMPatcher-Enhanced` folder
2. Uninstall Python packages (optional):
   ```cmd
   pip uninstall PyQt6 pyusb pycryptodome
   ```
3. Remove libimobiledevice (if installed via Chocolatey):
   ```cmd
   choco uninstall libimobiledevice
   ```

---

## FAQ

**Q: Do I need to keep iTunes running?**  
A: No, just installed for drivers.

**Q: Can I use this on Windows 7?**  
A: Not tested, Windows 10/11 recommended.

**Q: Why does it take so long?**  
A: Backup restoration can take 2-5 minutes depending on device.

**Q: Can I run multiple instances?**  
A: No, only one instance per device.

**Q: Does this work with wireless debugging?**  
A: No, USB connection required.

---

**Last Updated**: 2026-01-20
