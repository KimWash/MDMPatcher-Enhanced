"""
Test and Verification Script for MDMPatcher Windows Edition
Run this to verify your installation and check dependencies.
"""

import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def check_python_version():
    """Check Python version"""
    print_header("Python Version Check")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ FAILED: Python 3.8 or higher required")
        return False
    
    print("✓ OK: Python version is compatible")
    return True

def check_module(module_name, import_name=None):
    """Check if a Python module is installed"""
    if import_name is None:
        import_name = module_name
    
    try:
        __import__(import_name)
        print(f"✓ {module_name}: Installed")
        return True
    except ImportError:
        print(f"❌ {module_name}: NOT installed")
        return False

def check_dependencies():
    """Check all required dependencies"""
    print_header("Python Dependencies Check")
    
    deps = [
        ("pyusb", "usb"),
        ("pycryptodome", "Crypto"),
    ]
    
    all_ok = True
    for name, import_name in deps:
        if not check_module(name, import_name):
            all_ok = False
    
    if not all_ok:
        print("\n💡 Install missing dependencies with:")
        print("   pip install -r requirements.txt")
    
    return all_ok

def check_libimobiledevice_tool(tool_name):
    """Check if a libimobiledevice tool is available"""
    try:
        result = subprocess.run(
            [tool_name, "--version"],
            capture_output=True,
            text=True,
            timeout=2
        )
        print(f"✓ {tool_name}: Available")
        return True
    except FileNotFoundError:
        print(f"❌ {tool_name}: NOT found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print(f"⚠️  {tool_name}: Found but timed out")
        return False

def check_libimobiledevice():
    """Check libimobiledevice tools"""
    print_header("libimobiledevice Tools Check")
    
    tools = ["ideviceinfo", "idevicebackup2", "idevice_id"]
    all_ok = True
    
    for tool in tools:
        if not check_libimobiledevice_tool(tool):
            all_ok = False
    
    if not all_ok:
        print("\n💡 Install libimobiledevice:")
        print("   - Via Chocolatey: choco install libimobiledevice")
        print("   - Manual: Download from https://github.com/libimobiledevice-win32/imobiledevice-net/releases")
        print("   - Or place .exe files in this directory")
    
    return all_ok

def check_templates():
    """Check if template files exist"""
    print_header("Template Files Check")
    
    templates_dir = Path(__file__).parent / "resources" / "templates"
    templates = ["extension1.pdf", "extension2.pdf", "libiMobileeDevice.dylib"]
    
    all_ok = True
    for template in templates:
        template_path = templates_dir / template
        if template_path.exists():
            size_kb = template_path.stat().st_size / 1024
            print(f"✓ {template}: Found ({size_kb:.1f} KB)")
        else:
            print(f"❌ {template}: NOT found")
            all_ok = False
    
    if not all_ok:
        print("\n💡 Template files are missing!")
        print("   Copy them from the macOS version:")
        print("   - extension1.pdf")
        print("   - extension2.pdf")
        print("   - libiMobileeDevice.dylib")
    
    return all_ok

def test_core_modules():
    """Test core module imports"""
    print_header("Core Modules Test")
    
    try:
        from core import (
            USBDeviceWatcher, IOSDevice,
            DeviceInfoExtractor, DeviceInfo,
            RNCryptorDecryptor, PlistCustomizer,
            BackupRestorer
        )
        print("✓ All core modules import successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import core modules: {e}")
        return False

def test_ui_modules():
    """Test UI modules"""
    print_header("CLI Interface Test")
    
    try:
        # Just check if main.py exists and can be imported
        import importlib.util
        spec = importlib.util.spec_from_file_location("main", "main.py")
        if spec and spec.loader:
            print("✓ CLI main module exists")
            return True
        else:
            print("✗ CLI main module not found")
            return False
    except Exception as e:
        print(f"✗ Failed to check CLI module: {e}")
        return False

def test_usb_detection():
    """Test USB device detection"""
    print_header("USB Detection Test")
    
    try:
        from core import scan_for_ios_devices
        devices = scan_for_ios_devices()
        
        if devices:
            print(f"✓ USB detection working - Found {len(devices)} iOS device(s):")
            for device in devices:
                print(f"  - {device}")
        else:
            print("⚠️  USB detection working but no iOS devices found")
            print("   This is normal if no device is connected")
        
        return True
    except Exception as e:
        print(f"❌ USB detection test failed: {e}")
        return False

def test_decryption():
    """Test decryption functionality"""
    print_header("Decryption Module Test")
    
    try:
        from core import RNCryptorDecryptor
        password = RNCryptorDecryptor.calculate_password()
        print(f"✓ Password calculation: OK")
        print(f"  Computed password length: {len(password)} characters")
        return True
    except Exception as e:
        print(f"❌ Decryption test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and checks"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║   MDMPatcher Enhanced - Windows Edition                           ║")
    print("║   Installation Verification & Test Suite                          ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    results = []
    
    # Critical checks
    results.append(("Python Version", check_python_version()))
    results.append(("Python Dependencies", check_dependencies()))
    
    # Important checks
    results.append(("libimobiledevice Tools", check_libimobiledevice()))
    results.append(("Template Files", check_templates()))
    
    # Module tests
    results.append(("Core Modules", test_core_modules()))
    results.append(("UI Modules", test_ui_modules()))
    
    # Functionality tests
    results.append(("USB Detection", test_usb_detection()))
    results.append(("Decryption Module", test_decryption()))
    
    # Summary
    print_header("Test Summary")
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status:8} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! MDMPatcher is ready to use.")
        print("\n💡 Launch the application with:")
        print("   python main.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("Please fix the issues above before using MDMPatcher.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    
    print("\n" + "="*70)
    input("\nPress Enter to exit...")
    
    sys.exit(0 if success else 1)
