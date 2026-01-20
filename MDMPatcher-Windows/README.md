# MDMPatcher Enhanced - Windows Edition

<p align="center">
  <img src="../screenshots/banner.png" style="width:100%">
</p>

## ⚠️ **Legal & Technical Disclaimer**

> This project is intended strictly for **educational, diagnostic, and personal device recovery use only**.  
> It must **only** be used on iOS devices that the user **legally owns** and has the right to modify.
>
> **MDMPatcher Enhanced does not jailbreak, exploit or modify firmware**. It relies entirely on public interfaces (AFC, plist editing, USB restore flows).
>
> The tool targets situations like second-hand iOS devices where MDM was not removed correctly.  
> **Using this software on managed, corporate, or institutional devices without permission is prohibited and may be illegal.**

---

## Overview

**MDMPatcher Enhanced - Windows Edition** is a Windows port of the popular macOS MDM bypass tool. It helps remove or bypass Mobile Device Management (MDM) profiles from supervised iPhones and iPads running iOS 15 to iOS 18.5+.

### Key Features

- ✅ **Windows 10/11 Support** - Native Windows application
- ✅ **PyQt6 GUI** - Clean, modern interface similar to macOS version
- ✅ **USB Device Detection** - Automatic iOS device detection in Recovery Mode
- ✅ **Device Information** - Extract UDID, model, serial, IMEI, iOS version
- ✅ **Template Decryption** - RNCryptor-compatible decryption
- ✅ **Backup Restoration** - Automated backup creation and restoration
- ✅ **No Jailbreak Required** - Uses standard iOS restore mechanisms

---

## Requirements

### System Requirements

- **Operating System**: Windows 10 (64-bit) or Windows 11
- **iOS Devices**: iPhone 5s to iPhone 16, All iPads
- **iOS Versions**: iOS 15.0 to iOS 18.5+
- **USB**: USB 2.0 or higher port

### Software Prerequisites

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - ⚠️ **Important**: Check "Add Python to PATH" during installation

2. **iTunes or Apple Mobile Device Support**
   - Required for iOS device drivers
   - Download iTunes from [apple.com](https://www.apple.com/itunes/download/)
   - Or install Apple Mobile Device Support separately

3. **libimobiledevice for Windows**
   - Required for device communication
   - Download from [libimobiledevice-win32 releases](https://github.com/libimobiledevice-win32/imobiledevice-net/releases)
   - Extract and add to PATH, or place `ideviceinfo.exe`, `idevicebackup2.exe`, and `idevice_id.exe` in the MDMPatcher-Windows directory

---

## Installation

### Option 1: Run from Source (Recommended for Development)

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/KimWash/MDMPatcher-Enhanced.git
   cd MDMPatcher-Enhanced/MDMPatcher-Windows
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Copy template files**
   - Copy `extension1.pdf`, `extension2.pdf`, and `libiMobileeDevice.dylib` from the macOS version
   - Place them in `MDMPatcher-Windows/resources/templates/`

4. **Run the application**
   ```bash
   python main.py
   ```

### Option 2: Executable (Coming Soon)

Pre-built Windows executable will be available in the Releases section.

---

## Usage Instructions

### Preparing Your Device

1. **Download IPSW File**
   - Get the correct IPSW for your device from [ipsw.me](https://ipsw.me)
   - Match your device model number (found on the back of the device)
   - Choose Cellular or Wi-Fi version based on your device

2. **Enter Recovery Mode**
   - **iPads without Home button**: Press and hold Top button while connecting USB
   - **iPads with Home button**: Hold Home button while connecting USB
   - **iPhones with Face ID / iPhone 8+**: Hold Side button while connecting USB
   - **iPhone 7/7 Plus**: Hold Volume Down button while connecting USB
   - **iPhone 6s and earlier**: Hold Home button while connecting USB

3. **Restore iOS**
   - When prompted in iTunes, hold **Shift** (Windows) and click **Restore** or **Update**
   - Select your downloaded IPSW file
   - Wait for restoration to complete

4. **Initial Setup**
   - Complete setup **until you reach the Wi-Fi selection screen**
   - **⚠️ DO NOT CONNECT TO ANY NETWORK!**
   - Keep device on Wi-Fi selection screen

### Running MDMPatcher

1. **Launch MDMPatcher Enhanced**
   ```bash
   python main.py
   ```

2. **Connect Device**
   - Connect your iOS device via USB
   - The app will automatically detect devices in Recovery Mode
   - Device information will appear (UDID, Model, Serial, iOS version)

3. **Patch MDM**
   - Click the **PATCH** button
   - Wait for the process to complete (may take 2-5 minutes)
   - Device will automatically reboot

4. **Complete Setup**
   - After reboot, complete the remaining iOS setup steps
   - MDM profile will be bypassed

---

## Troubleshooting

### Device Not Detected

**Problem**: No device appears in MDMPatcher

**Solutions**:
1. Ensure iTunes or Apple Mobile Device Support is installed
2. Check that USB cable is properly connected
3. Try a different USB port (preferably USB 2.0)
4. Verify device is in Recovery Mode (shows iTunes logo on screen)
5. Restart MDMPatcher and reconnect device

### pyusb / USB Detection Error

**Problem**: Import error or "No backend available" when using pyusb

**Solutions**:
1. Install the libusb backend:
   ```bash
   pip install libusb1
   ```
2. Or manually download `libusb-1.0.dll` from [libusb releases](https://github.com/libusb/libusb/releases)
3. Place the DLL in `C:\Windows\System32\` or the application folder
4. Verify with: `python -c "import usb.core; print('OK')"`

**Note**: This is now included in `requirements.txt`, so `pip install -r requirements.txt` will install it automatically.

### libimobiledevice Tools Not Found

**Problem**: Error about missing `ideviceinfo` or `idevicebackup2`

**Solutions**:
1. Download libimobiledevice-win32 from [releases page](https://github.com/libimobiledevice-win32/imobiledevice-net/releases)
2. Extract the ZIP file
3. Add the directory to your system PATH, OR
4. Copy `ideviceinfo.exe`, `idevicebackup2.exe`, and `idevice_id.exe` to the `MDMPatcher-Windows` directory

### Python Dependencies Error

**Problem**: ModuleNotFoundError or ImportError

**Solutions**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If you have multiple Python versions:
```bash
python -m pip install -r requirements.txt
```

### USB Device Access Denied

**Problem**: Cannot access USB device

**Solutions**:
1. Run MDMPatcher as Administrator (Right-click → Run as administrator)
2. Install/reinstall Apple Mobile Device USB Driver
3. Check Device Manager for driver issues

### Patching Failed

**Problem**: Backup restoration fails

**Solutions**:
1. Ensure device is at Wi-Fi selection screen (not connected to network)
2. Reboot device and try again
3. Re-enter Recovery Mode and restore with fresh IPSW
4. Check that libimobiledevice tools are working: `ideviceinfo -u <UDID>`

### Windows Defender Warning

**Problem**: Windows Defender blocks execution

**Solutions**:
1. Add MDMPatcher directory to Windows Defender exclusions
2. Click "More info" → "Run anyway" when prompted
3. Temporarily disable real-time protection (not recommended)

---

## Project Structure

```
MDMPatcher-Windows/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── ui/
│   ├── __init__.py
│   └── main_window.py      # Main GUI window (PyQt6)
├── core/
│   ├── __init__.py
│   ├── device_detector.py  # USB device detection
│   ├── device_info.py      # Device information extraction
│   ├── decryption.py       # RNCryptor decryption
│   ├── plist_handler.py    # Plist customization
│   └── backup_restore.py   # Backup restoration logic
└── resources/
    ├── templates/          # Encrypted template files
    │   ├── extension1.pdf
    │   ├── extension2.pdf
    │   └── libiMobileeDevice.dylib
    └── assets/             # Icons, images
```

---

## Technical Details

### How It Works

1. **USB Detection**: Monitors USB devices for iOS devices in Recovery Mode (Product ID 4776/4779)
2. **Device Info**: Extracts UDID, model, serial, IMEI, iOS version using libimobiledevice
3. **Template Decryption**: Decrypts encrypted template files using RNCryptor (AES-256-CBC)
4. **Plist Customization**: Replaces placeholder values with actual device information
5. **Backup Creation**: Generates a custom backup structure with modified plists
6. **Restoration**: Restores the backup to the device, bypassing MDM enrollment

### Security

- **No Network Communication**: All operations are performed locally
- **No Jailbreak**: Uses standard iOS backup restoration API
- **No Firmware Modification**: Only modifies configuration files
- **No Data Collection**: No telemetry or data collection

### Differences from macOS Version

| Feature | macOS Version | Windows Version |
|---------|---------------|-----------------|
| Language | Swift | Python 3 |
| GUI Framework | Cocoa/AppKit | PyQt6 |
| USB Detection | IOKit | pyusb |
| Device Communication | libimobiledevice (embedded) | libimobiledevice (external) |
| Build System | Xcode | pip + requirements.txt |
| Distribution | .app bundle | Python script / .exe |

---

## Building Executable (Optional)

To create a standalone Windows executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "MDMPatcher-Enhanced" main.py
```

The executable will be in the `dist/` folder.

---

## Development

### Running Tests

```bash
# Test device detection
python -m core.device_detector

# Test device info extraction
python -m core.device_info

# Test decryption
python -m core.decryption
```

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on Windows 10/11
5. Submit a pull request

---

## Known Limitations

- Requires device to be in Recovery Mode (DFU mode not supported yet)
- Requires iTunes or Apple Mobile Device Support drivers
- Some USB 3.0 controllers may have compatibility issues
- Windows 7/8 support is not guaranteed

---

## FAQ

**Q: Is this safe to use?**  
A: Yes, if used on personally-owned devices. It does not modify firmware or exploit vulnerabilities.

**Q: Will this work on company-owned devices?**  
A: You should NEVER use this on devices you don't personally own. It may be illegal.

**Q: Does this require internet connection?**  
A: No, all operations are performed offline.

**Q: Will this delete my data?**  
A: The device must be restored to factory settings before patching, so yes.

**Q: Can I use this on iPad?**  
A: Yes, it supports all iPad models from iPad Air onwards.

**Q: Why do I need libimobiledevice?**  
A: It provides tools to communicate with iOS devices over USB.

---

## Credits

- **Original macOS Version**: [fled-dev/MDMPatcher-Enhanced](https://github.com/fled-dev/MDMPatcher-Enhanced)
- **libimobiledevice**: [libimobiledevice.org](https://libimobiledevice.org/)
- **RNCryptor**: [RNCryptor Specification](https://github.com/RNCryptor/RNCryptor-Spec)
- **PyQt6**: [riverbankcomputing.com](https://www.riverbankcomputing.com/software/pyqt/)

---

## License

This project is for educational purposes only. Use at your own risk.

---

## Support

For issues, questions, or feedback:
- Open an issue on GitHub
- Check the [Troubleshooting](#troubleshooting) section
- Review the original macOS documentation

---

**Remember**: This tool is for personal device recovery only. Always respect device ownership and applicable laws.
