"""
USB Device Detection for iOS devices on Windows.
Monitors USB connections and identifies iOS devices in Recovery/DFU mode.
"""

import time
import threading
from typing import Optional, Callable

USB_AVAILABLE = False
USB_ERROR_MESSAGE = None

try:
    import usb.core
    import usb.util
    USB_AVAILABLE = True
except ImportError as e:
    USB_ERROR_MESSAGE = f"pyusb module not installed: {e}"
    print(f"Warning: pyusb not available - {USB_ERROR_MESSAGE}")
    print("Install with: pip install pyusb")
except Exception as e:
    USB_ERROR_MESSAGE = f"USB import error: {e}"
    print(f"Warning: USB detection error - {USB_ERROR_MESSAGE}")


class IOSDevice:
    """Represents a connected iOS device"""
    
    def __init__(self, vendor_id: int, product_id: int, serial: str = None):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.serial = serial or "Unknown"
        self.name = self._get_device_name(product_id)
    
    def _get_device_name(self, product_id: int) -> str:
        """Get device name based on product ID"""
        device_names = {
            0x12a8: "iOS Device (Recovery Mode)",
            0x1281: "iOS Device (DFU Mode)",
            0x1227: "iOS Device (Normal Mode)",
            0x12ab: "iOS Device (Recovery Mode)",
        }
        return device_names.get(product_id, f"iOS Device (PID: {hex(product_id)})")
    
    def is_recovery_mode(self) -> bool:
        """Check if device is in recovery mode (Product ID 4776/4779 = 0x12a8/0x12ab)"""
        return self.product_id in [0x12a8, 0x12ab, 4776, 4779]
    
    def __str__(self):
        return f"{self.name} (VID: {hex(self.vendor_id)}, PID: {hex(self.product_id)}, Serial: {self.serial})"


class USBDeviceWatcher:
    """
    Monitors USB devices for iOS device connections.
    Similar to the macOS USBWatcher class.
    """
    
    APPLE_VENDOR_ID = 0x05ac  # Apple Inc.
    
    # Product IDs for iOS devices in different modes
    RECOVERY_MODE_PIDS = [0x12a8, 0x12ab, 4776, 4779]  # Recovery mode
    DFU_MODE_PIDS = [0x1281]  # DFU mode
    NORMAL_MODE_PIDS = [0x1227, 0x12a0]  # Normal mode
    
    def __init__(self, on_device_added: Callable[[IOSDevice], None] = None,
                 on_device_removed: Callable[[IOSDevice], None] = None):
        """
        Initialize USB watcher
        
        Args:
            on_device_added: Callback when device is connected
            on_device_removed: Callback when device is disconnected
        """
        self.on_device_added = on_device_added
        self.on_device_removed = on_device_removed
        
        self._running = False
        self._thread = None
        self._known_devices = {}  # Track connected devices by serial
    
    def start(self):
        """Start monitoring USB devices"""
        if not USB_AVAILABLE:
            print("[ERROR] USB detection is not available.")
            if USB_ERROR_MESSAGE:
                print(f"[ERROR] Reason: {USB_ERROR_MESSAGE}")
            print("[INFO] Install pyusb with: pip install pyusb")
            print("[INFO] On Windows, you may also need libusb backend:")
            print("[INFO]   - Download from: https://github.com/libusb/libusb/releases")
            print("[INFO]   - Or install via: pip install libusb1")
            return
        
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        print("[INFO] USB device monitoring started")
    
    def stop(self):
        """Stop monitoring USB devices"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        print("[INFO] USB device monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self._running:
            try:
                self._check_devices()
                time.sleep(0.5)  # Check every 500ms
            except Exception as e:
                print(f"[ERROR] USB monitoring error: {e}")
                time.sleep(1.0)
    
    def _check_devices(self):
        """Check for connected iOS devices"""
        current_devices = {}
        
        try:
            # Find all Apple devices
            devices = usb.core.find(find_all=True, idVendor=self.APPLE_VENDOR_ID)
        except Exception as e:
            # This can happen if libusb backend is not available on Windows
            if "No backend available" in str(e) or "backend" in str(e).lower():
                print(f"[ERROR] USB backend not available: {e}")
                print("[INFO] On Windows, pyusb requires a libusb backend.")
                print("[INFO] Solutions:")
                print("[INFO]   1. Install libusb1: pip install libusb1")
                print("[INFO]   2. Download libusb DLL from: https://github.com/libusb/libusb/releases")
                print("[INFO]   3. Place libusb-1.0.dll in Windows/System32 or the app directory")
                self._running = False  # Stop monitoring since it won't work
            else:
                print(f"[ERROR] USB detection error: {e}")
            return
        
        for dev in devices:
            try:
                # Get serial number
                try:
                    serial = usb.util.get_string(dev, dev.iSerialNumber) if dev.iSerialNumber else None
                except:
                    serial = f"dev_{dev.bus}_{dev.address}"
                
                if not serial:
                    serial = f"dev_{dev.bus}_{dev.address}"
                
                # Check if it's an iOS device
                if dev.idProduct in (self.RECOVERY_MODE_PIDS + self.DFU_MODE_PIDS + self.NORMAL_MODE_PIDS):
                    ios_device = IOSDevice(dev.idVendor, dev.idProduct, serial)
                    current_devices[serial] = ios_device
                    
                    # Check if this is a newly connected device
                    if serial not in self._known_devices:
                        print(f"[DEVICE ADDED] {ios_device}")
                        if self.on_device_added:
                            self.on_device_added(ios_device)
            
            except Exception as e:
                # Silently ignore errors for individual devices
                pass
        
        # Check for removed devices
        removed = set(self._known_devices.keys()) - set(current_devices.keys())
        for serial in removed:
            device = self._known_devices[serial]
            print(f"[DEVICE REMOVED] {device}")
            if self.on_device_removed:
                self.on_device_removed(device)
        
        # Update known devices
        self._known_devices = current_devices
    
    def get_connected_ios_devices(self) -> list[IOSDevice]:
        """Get list of currently connected iOS devices"""
        return list(self._known_devices.values())
    
    def get_recovery_mode_device(self) -> Optional[IOSDevice]:
        """Get the first iOS device in recovery mode"""
        for device in self._known_devices.values():
            if device.is_recovery_mode():
                return device
        return None


def scan_for_ios_devices() -> list[IOSDevice]:
    """
    Scan for connected iOS devices (one-time scan)
    
    Returns:
        List of connected iOS devices
    """
    if not USB_AVAILABLE:
        print("[ERROR] pyusb is not installed")
        return []
    
    devices = []
    apple_devices = usb.core.find(find_all=True, idVendor=USBDeviceWatcher.APPLE_VENDOR_ID)
    
    for dev in apple_devices:
        try:
            serial = None
            try:
                if dev.iSerialNumber:
                    serial = usb.util.get_string(dev, dev.iSerialNumber)
            except:
                pass
            
            ios_device = IOSDevice(dev.idVendor, dev.idProduct, serial)
            devices.append(ios_device)
        except Exception as e:
            pass
    
    return devices


if __name__ == "__main__":
    # Test device detection
    print("Scanning for iOS devices...")
    devices = scan_for_ios_devices()
    
    if devices:
        print(f"\nFound {len(devices)} iOS device(s):")
        for device in devices:
            print(f"  - {device}")
            print(f"    Recovery Mode: {device.is_recovery_mode()}")
    else:
        print("No iOS devices found")
    
    print("\nStarting continuous monitoring (Press Ctrl+C to stop)...")
    
    def on_added(device: IOSDevice):
        print(f"\n>>> Device connected: {device}")
        if device.is_recovery_mode():
            print("    [!] Device is in RECOVERY MODE - ready for patching!")
    
    def on_removed(device: IOSDevice):
        print(f"\n<<< Device disconnected: {device}")
    
    watcher = USBDeviceWatcher(on_device_added=on_added, on_device_removed=on_removed)
    watcher.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        watcher.stop()
