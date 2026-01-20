"""
Device Information Extraction using libimobiledevice.
Extracts UDID, model, serial number, IMEI, build version, etc.
"""

import subprocess
import plistlib
import xml.etree.ElementTree as ET
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class DeviceInfo:
    """Container for iOS device information"""
    udid: str = ""
    product_type: str = ""
    product_version: str = ""
    build_version: str = ""
    serial_number: str = ""
    imei: str = ""
    device_name: str = ""
    device_class: str = ""
    activation_state: str = ""
    baseband_status: str = ""
    
    def is_valid(self) -> bool:
        """Check if device info is valid (has essential fields)"""
        return bool(self.udid and self.product_type and self.build_version)
    
    def __str__(self):
        lines = []
        if self.device_name:
            lines.append(f"Device Name: {self.device_name}")
        if self.product_type:
            lines.append(f"Model: {self.product_type}")
        if self.serial_number:
            lines.append(f"Serial: {self.serial_number}")
        if self.udid:
            lines.append(f"UDID: {self.udid}")
        if self.product_version and self.build_version:
            lines.append(f"iOS: {self.product_version} ({self.build_version})")
        if self.imei:
            lines.append(f"IMEI: {self.imei}")
        if self.activation_state:
            lines.append(f"Activation State: {self.activation_state}")
        return "\n".join(lines) if lines else "No device information available"


class DeviceInfoExtractor:
    """
    Extracts device information using libimobiledevice tools.
    Requires ideviceinfo.exe to be available in PATH or in the same directory.
    """
    
    def __init__(self, ideviceinfo_path: str = "ideviceinfo"):
        """
        Initialize device info extractor
        
        Args:
            ideviceinfo_path: Path to ideviceinfo executable (default: search in PATH)
        """
        self.ideviceinfo_path = ideviceinfo_path
    
    def get_device_info(self, udid: Optional[str] = None) -> Optional[DeviceInfo]:
        """
        Get comprehensive device information
        
        Args:
            udid: Optional UDID to target specific device
            
        Returns:
            DeviceInfo object or None if failed
        """
        try:
            # Build command
            cmd = [self.ideviceinfo_path]
            if udid:
                cmd.extend(["-u", udid])
            cmd.append("-x")  # XML output
            
            # Run ideviceinfo
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                print(f"[ERROR] ideviceinfo failed: {result.stderr}")
                return None
            
            # Parse XML output
            return self._parse_device_info(result.stdout)
            
        except FileNotFoundError:
            print(f"[ERROR] ideviceinfo not found at: {self.ideviceinfo_path}")
            print("[INFO] Please install libimobiledevice or place ideviceinfo.exe in PATH")
            return None
        except subprocess.TimeoutExpired:
            print("[ERROR] ideviceinfo timed out")
            return None
        except Exception as e:
            print(f"[ERROR] Failed to get device info: {e}")
            return None
    
    def _parse_device_info(self, xml_output: str) -> Optional[DeviceInfo]:
        """Parse XML output from ideviceinfo"""
        try:
            # Parse as plist
            plist_data = plistlib.loads(xml_output.encode())
            
            info = DeviceInfo()
            
            # Extract common fields
            info.udid = plist_data.get("UniqueDeviceID", "")
            info.product_type = plist_data.get("ProductType", "")
            info.product_version = plist_data.get("ProductVersion", "")
            info.build_version = plist_data.get("BuildVersion", "")
            info.serial_number = plist_data.get("SerialNumber", "")
            info.device_name = plist_data.get("DeviceName", "")
            info.device_class = plist_data.get("DeviceClass", "")
            info.activation_state = plist_data.get("ActivationState", "")
            info.baseband_status = plist_data.get("BasebandStatus", "")
            
            # IMEI might not be present on non-cellular devices
            info.imei = plist_data.get("InternationalMobileEquipmentIdentity", "")
            
            return info
            
        except Exception as e:
            print(f"[ERROR] Failed to parse device info: {e}")
            return None
    
    def get_udid(self) -> Optional[str]:
        """Quick method to get just the UDID"""
        info = self.get_device_info()
        return info.udid if info else None
    
    def list_devices(self) -> list[str]:
        """
        List UDIDs of all connected devices
        
        Returns:
            List of device UDIDs
        """
        try:
            # Use idevice_id to list devices
            cmd = ["idevice_id", "-l"]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return []
            
            # Parse output (one UDID per line)
            udids = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
            return udids
            
        except FileNotFoundError:
            print("[ERROR] idevice_id not found")
            return []
        except Exception as e:
            print(f"[ERROR] Failed to list devices: {e}")
            return []


def get_device_information_xml() -> str:
    """
    Get device information as XML string (compatible with Swift version)
    This mimics the getdeviceInformation() function from the C code.
    
    Returns:
        XML string with device information or "-1" if no device found
    """
    try:
        extractor = DeviceInfoExtractor()
        info = extractor.get_device_info()
        
        if not info or not info.is_valid():
            return "-1"
        
        # Build plist dict
        plist_dict = {
            "UniqueDeviceID": info.udid,
            "ProductType": info.product_type,
            "ProductVersion": info.product_version,
            "BuildVersion": info.build_version,
            "SerialNumber": info.serial_number,
            "DeviceName": info.device_name,
            "DeviceClass": info.device_class,
            "ActivationState": info.activation_state,
            "BasebandStatus": info.baseband_status,
        }
        
        if info.imei:
            plist_dict["InternationalMobileEquipmentIdentity"] = info.imei
        
        # Convert to XML plist format
        xml_data = plistlib.dumps(plist_dict, fmt=plistlib.FMT_XML)
        return xml_data.decode('utf-8')
        
    except Exception as e:
        print(f"[ERROR] Failed to get device information: {e}")
        return "-1"


if __name__ == "__main__":
    # Test device info extraction
    print("=== iOS Device Information Extractor ===\n")
    
    extractor = DeviceInfoExtractor()
    
    # List devices
    print("Scanning for devices...")
    devices = extractor.list_devices()
    
    if not devices:
        print("No devices found. Make sure:")
        print("  1. iOS device is connected via USB")
        print("  2. Device is trusted (check device screen)")
        print("  3. iTunes or Apple Mobile Device Support is installed")
        print("  4. libimobiledevice tools are in PATH")
    else:
        print(f"Found {len(devices)} device(s):\n")
        
        for udid in devices:
            print(f"Device UDID: {udid}")
            info = extractor.get_device_info(udid)
            
            if info:
                print(info)
                print("\nDevice is valid for patching!" if info.is_valid() else "Device info incomplete")
            else:
                print("Failed to get device information")
            
            print("\n" + "="*50 + "\n")
