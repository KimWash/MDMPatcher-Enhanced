#!/usr/bin/env python3
import usb
"""
MDMPatcher Enhanced - Windows Edition
Main entry point for the application

This tool helps remove or bypass Mobile Device Management (MDM) profiles 
from supervised iPhones and iPads on Windows.

LEGAL NOTICE:
This tool is intended strictly for educational, diagnostic, and personal 
device recovery use only. It must ONLY be used on iOS devices that the user 
legally owns and has the right to modify.

Using this software on managed, corporate, or institutional devices without 
permission is prohibited and may be illegal.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing = []
    
    try:
        import PyQt6
    except ImportError:
        missing.append("PyQt6")
    
    try:
        import usb
    except ImportError:
        missing.append("pyusb")
    
    try:
        from Crypto.Cipher import AES
    except ImportError:
        missing.append("pycryptodome")
    
    if missing:
        print("ERROR: Missing required dependencies:")
        for dep in missing:
            print(f"  - {dep}")
        print("\nInstall missing dependencies with:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    return True


def check_libimobiledevice():
    """Check if libimobiledevice tools are available"""
    import subprocess
    
    tools = ["ideviceinfo", "idevicebackup2", "idevice_id"]
    missing = []
    
    for tool in tools:
        try:
            subprocess.run(
                [tool, "--version"],
                capture_output=True,
                timeout=2
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            missing.append(tool)
    
    if missing:
        print("WARNING: libimobiledevice tools not found in PATH:")
        for tool in missing:
            print(f"  - {tool}")
        print("\nThese tools are required for device communication.")
        print("You can download them from:")
        print("  https://github.com/libimobiledevice-win32/imobiledevice-net/releases")
        print("\nOr install via:")
        print("  - Chocolatey: choco install libimobiledevice")
        print("  - Manual: Download and add to PATH")
        return False
    
    return True


def show_legal_notice():
    """Display legal notice"""
    print("="*70)
    print("MDMPatcher Enhanced - Windows Edition")
    print("="*70)
    print()
    print("⚠️  LEGAL & TECHNICAL DISCLAIMER")
    print()
    print("This project is intended strictly for:")
    print("  • Educational purposes")
    print("  • Diagnostic use")
    print("  • Personal device recovery")
    print()
    print("It must ONLY be used on iOS devices that you:")
    print("  • Legally own")
    print("  • Have the right to modify")
    print()
    print("MDMPatcher Enhanced does NOT:")
    print("  • Jailbreak devices")
    print("  • Exploit vulnerabilities")
    print("  • Modify firmware")
    print()
    print("It relies entirely on public interfaces:")
    print("  • AFC (Apple File Conduit)")
    print("  • Plist editing")
    print("  • USB restore flows")
    print()
    print("⚠️  WARNING:")
    print("Using this software on managed, corporate, or institutional")
    print("devices without permission is PROHIBITED and may be ILLEGAL.")
    print()
    print("="*70)
    print()


def main():
    """Main application entry point"""
    # Show legal notice
    show_legal_notice()
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        print("\nFailed to start: Missing Python dependencies")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("✓ Python dependencies OK")
    
    # Check libimobiledevice (warning only, not fatal)
    if not check_libimobiledevice():
        print("\n⚠️  Warning: libimobiledevice tools not found")
        print("The application will start, but device operations will fail.")
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    else:
        print("✓ libimobiledevice tools OK")
    
    print("\nStarting MDMPatcher Enhanced...\n")
    
    # Start GUI
    try:
        from ui import main as ui_main
        ui_main()
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
