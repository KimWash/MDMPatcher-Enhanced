#!/usr/bin/env python3
"""
MDMPatcher Enhanced - Windows Edition (CLI)
Command-line interface for MDM patching

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
import time
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))


def check_dependencies():
    """Check if all required dependencies are installed"""
    missing = []
    
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
    print("MDMPatcher Enhanced - Windows Edition (CLI)")
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


def wait_for_device():
    """Wait for an iOS device to be connected in Recovery Mode"""
    from core import USBDeviceWatcher, IOSDevice
    
    print("Waiting for iOS device in Recovery Mode...")
    print("Please connect your device (Product ID: 4776 or 4779)")
    print()
    
    device_found = [None]  # Use list to allow modification in closure
    
    def on_device_added(device: IOSDevice):
        if device.is_recovery_mode():
            print(f"\n✓ Device detected: {device}")
            device_found[0] = device
    
    def on_device_removed(device: IOSDevice):
        if device_found[0]:
            print(f"\n✗ Device disconnected: {device}")
            device_found[0] = None
    
    watcher = USBDeviceWatcher(
        on_device_added=on_device_added,
        on_device_removed=on_device_removed
    )
    watcher.start()
    
    # Wait for device
    print("Monitoring USB... (Press Ctrl+C to cancel)")
    try:
        while not device_found[0]:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        watcher.stop()
        return None
    
    watcher.stop()
    return device_found[0]


def get_device_info():
    """Get device information"""
    from core import DeviceInfoExtractor
    
    print("\nFetching device information...")
    
    extractor = DeviceInfoExtractor()
    info = extractor.get_device_info()
    
    if not info or not info.is_valid():
        print("✗ Failed to retrieve device information")
        return None
    
    print("\n" + "="*70)
    print("DEVICE INFORMATION")
    print("="*70)
    print(info)
    print("="*70)
    
    return info


def confirm_patch(device_info):
    """Ask user to confirm patching"""
    print("\n⚠️  WARNING: This will restore a backup to your device!")
    print("This action cannot be undone.")
    print()
    response = input("Do you want to continue? (yes/no): ")
    
    return response.lower() in ['yes', 'y']


def execute_patch(device_info):
    """Execute the patching process"""
    from core import (
        decrypt_template_file, PlistCustomizer, 
        BackupWorkflow, RNCryptorDecryptor
    )
    
    print("\n" + "="*70)
    print("STARTING MDM PATCH PROCESS")
    print("="*70)
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp(prefix="mdmpatcher_")
    print(f"\nTemp directory: {temp_dir}")
    
    try:
        # Get paths
        app_dir = Path(__file__).parent
        templates_dir = app_dir / "resources" / "templates"
        
        # Step 1: Decrypt template files
        print("\n[1/4] Decrypting template files...")
        
        password = RNCryptorDecryptor.calculate_password()
        
        # Decrypt Info.plist template
        info_template = templates_dir / "extension1.pdf"
        info_decrypted = Path(temp_dir) / "info_template.plist"
        
        if not decrypt_template_file(str(info_template), str(info_decrypted), password):
            print("✗ Failed to decrypt Info.plist template")
            return False
        
        # Decrypt Manifest.plist template
        manifest_template = templates_dir / "extension2.pdf"
        manifest_decrypted = Path(temp_dir) / "manifest_template.plist"
        
        if not decrypt_template_file(str(manifest_template), str(manifest_decrypted), password):
            print("✗ Failed to decrypt Manifest.plist template")
            return False
        
        # Decrypt backup archive
        archive_template = templates_dir / "libiMobileeDevice.dylib"
        archive_decrypted = Path(temp_dir) / "backup_archive.zip"
        
        if not decrypt_template_file(str(archive_template), str(archive_decrypted), password):
            print("✗ Failed to decrypt backup archive")
            return False
        
        print("✓ Decryption completed!")
        
        # Step 2: Customize plists
        print("\n[2/4] Customizing backup files...")
        
        # Read decrypted templates
        with open(info_decrypted, 'r', encoding='utf-8') as f:
            info_content = f.read()
        
        with open(manifest_decrypted, 'r', encoding='utf-8') as f:
            manifest_content = f.read()
        
        # Customize Info.plist
        info_output = Path(temp_dir) / "Info.plist"
        if not PlistCustomizer.customize_info_plist_from_string(
            info_content,
            str(info_output),
            device_info.build_version,
            device_info.product_type,
            device_info.serial_number,
            device_info.udid,
            device_info.imei
        ):
            print("✗ Failed to customize Info.plist")
            return False
        
        # Customize Manifest.plist
        manifest_output = Path(temp_dir) / "Manifest.plist"
        if not PlistCustomizer.customize_manifest_plist_from_string(
            manifest_content,
            str(manifest_output),
            device_info.build_version,
            device_info.product_type,
            device_info.serial_number,
            device_info.udid
        ):
            print("✗ Failed to customize Manifest.plist")
            return False
        
        print("✓ Plist customization completed!")
        
        # Step 3: Create backup structure
        print("\n[3/4] Creating backup structure...")
        
        workflow = BackupWorkflow()
        
        # Step 4: Restore backup
        print("\n[4/4] Restoring backup to device...")
        print("This may take 2-5 minutes. Please wait...")
        
        success = workflow.execute_patch(
            temp_dir,
            str(archive_decrypted),
            str(info_output),
            str(manifest_output),
            device_info.udid
        )
        
        if success:
            print("\n" + "="*70)
            print("✓ SUCCESS!")
            print("="*70)
            print("\nMDM has been successfully patched on your device!")
            print("Your device will now reboot.")
            print("\nPlease complete the setup process on your device.")
            print("Have fun :-)")
            print()
            return True
        else:
            print("\n✗ Backup restoration failed")
            return False
            
    except Exception as e:
        print(f"\n✗ Error during patching: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup is handled by BackupWorkflow
        pass


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
        print("The application will not work without these tools.")
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    else:
        print("✓ libimobiledevice tools OK")
    
    print()
    
    # Wait for device
    device = wait_for_device()
    if not device:
        sys.exit(1)
    
    # Get device info
    device_info = get_device_info()
    if not device_info:
        print("\nError: Could not retrieve device information")
        print("Please make sure:")
        print("  1. Device is unlocked")
        print("  2. You tapped 'Trust' on the device")
        print("  3. libimobiledevice tools are installed")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Confirm patch
    if not confirm_patch(device_info):
        print("\nOperation cancelled by user")
        sys.exit(0)
    
    # Execute patch
    success = execute_patch(device_info)
    
    if success:
        print("\nPatching completed successfully!")
        input("\nPress Enter to exit...")
        sys.exit(0)
    else:
        print("\nPatching failed!")
        print("Please check the error messages above.")
        print("You may need to:")
        print("  1. Reboot your device")
        print("  2. Re-enter Recovery Mode")
        print("  3. Try again")
        input("\nPress Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
