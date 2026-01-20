#!/usr/bin/env python3
"""
USB Troubleshooting Script for MDMPatcher Windows
Helps diagnose pyusb installation and backend issues.
"""

import sys
import platform

print("="*70)
print("MDMPatcher - USB / pyusb Troubleshooting")
print("="*70)
print()

# Check Python version
print(f"Python Version: {sys.version}")
print(f"Platform: {platform.platform()}")
print()

# Check if pyusb is installed
print("="*70)
print("Checking pyusb installation...")
print("="*70)

try:
    import usb
    print(f"✓ pyusb is installed")
    print(f"  Version: {usb.__version__}")
    print(f"  Location: {usb.__file__}")
except ImportError as e:
    print(f"✗ pyusb is NOT installed")
    print(f"  Error: {e}")
    print()
    print("Solution:")
    print("  pip install pyusb")
    sys.exit(1)

print()

# Check if usb.core can be imported
print("="*70)
print("Checking usb.core module...")
print("="*70)

try:
    import usb.core
    print("✓ usb.core imported successfully")
except ImportError as e:
    print(f"✗ Failed to import usb.core")
    print(f"  Error: {e}")
    sys.exit(1)

print()

# Try to find USB devices (this will reveal backend issues)
print("="*70)
print("Checking USB backend...")
print("="*70)

try:
    # Try to find any USB device
    devices = list(usb.core.find(find_all=True))
    print(f"✓ USB backend is working!")
    print(f"  Found {len(devices)} USB device(s)")
    
    # Try to find Apple devices specifically
    apple_devices = list(usb.core.find(find_all=True, idVendor=0x05ac))
    if apple_devices:
        print(f"✓ Found {len(apple_devices)} Apple device(s):")
        for dev in apple_devices:
            print(f"    - Vendor: {hex(dev.idVendor)}, Product: {hex(dev.idProduct)}")
    else:
        print("  No Apple devices detected (this is OK if none are connected)")
    
except usb.core.NoBackendError as e:
    print("✗ USB backend is NOT available!")
    print(f"  Error: {e}")
    print()
    print("This is the most common issue on Windows.")
    print()
    print("Solutions:")
    print()
    print("1. Install libusb1 Python package (RECOMMENDED):")
    print("   pip install libusb1")
    print()
    print("2. Or manually install libusb DLL:")
    print("   - Download from: https://github.com/libusb/libusb/releases")
    print("   - Look for 'libusb-1.0.XX.7z' (latest version)")
    print("   - Extract 'libusb-1.0.dll' from VS2019/MS64/dll/ folder")
    print("   - Place it in one of:")
    print("     * C:\\Windows\\System32\\ (requires admin)")
    print("     * Same folder as this script")
    print("     * Any folder in your PATH")
    print()
    print("3. After installing, run this script again to verify")
    sys.exit(1)

except Exception as e:
    print(f"✗ Unexpected error accessing USB:")
    print(f"  Error: {e}")
    print()
    print("This might be a permissions issue.")
    print("Try running this script as Administrator.")
    sys.exit(1)

print()

# Check if libusb1 package is installed (Python wrapper)
print("="*70)
print("Checking libusb1 Python package...")
print("="*70)

try:
    import usb1
    print("✓ libusb1 package is installed")
    print(f"  Version: {usb1.__version__ if hasattr(usb1, '__version__') else 'unknown'}")
except ImportError:
    print("⚠ libusb1 package is NOT installed")
    print("  This is optional but recommended for Windows")
    print("  Install with: pip install libusb1")

print()

# Summary
print("="*70)
print("SUMMARY")
print("="*70)
print()
print("✓ pyusb is installed and working correctly!")
print("✓ USB backend is available")
print("✓ MDMPatcher should be able to detect iOS devices")
print()
print("Next steps:")
print("1. Connect your iOS device in Recovery Mode")
print("2. Run: python main.py")
print("3. The device should be detected automatically")
print()
print("If you still have issues, check:")
print("- Device is in Recovery Mode (iTunes logo + USB cable)")
print("- USB cable is properly connected")
print("- iTunes or Apple Mobile Device Support is installed")
print()
