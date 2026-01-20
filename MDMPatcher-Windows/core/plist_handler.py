"""
Plist Handler for customizing Info.plist and Manifest.plist files.
Replaces device-specific information in the backup plists.
"""

import plistlib
from pathlib import Path
from typing import Optional


class PlistCustomizer:
    """Handles plist file customization for MDM patching"""
    
    # Default placeholder values (from Swift code)
    DEFAULT_BUILD_VERSION = "18C66"
    DEFAULT_IMEI = "357145413514797"
    DEFAULT_PRODUCT_TYPE = "iPhone12,8"
    DEFAULT_SERIAL_NUMBER = "F17F4MLSPLK2"
    DEFAULT_UDID = "00008030-001854E42E06402E"
    
    def __init__(self):
        pass
    
    @staticmethod
    def customize_info_plist(
        input_path: str,
        output_path: str,
        build_version: str,
        product_type: str,
        serial_number: str,
        udid: str,
        imei: Optional[str] = None
    ) -> bool:
        """
        Customize Info.plist with device-specific information
        
        Args:
            input_path: Path to template Info.plist
            output_path: Path to write customized Info.plist
            build_version: iOS build version (e.g., "18C66")
            product_type: Device model (e.g., "iPhone12,8")
            serial_number: Device serial number
            udid: Device UDID
            imei: Device IMEI (optional, for cellular devices)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read template plist
            with open(input_path, 'rb') as f:
                plist_data = plistlib.load(f)
            
            # Replace build version
            if "Build Version" in plist_data:
                plist_data["Build Version"] = build_version
            
            # Replace product type
            if "Product Type" in plist_data:
                plist_data["Product Type"] = product_type
            
            # Replace serial number
            if "Serial Number" in plist_data:
                plist_data["Serial Number"] = serial_number
            
            # Replace UDID (might be in multiple fields)
            if "Target Identifier" in plist_data:
                plist_data["Target Identifier"] = udid
            if "Unique Identifier" in plist_data:
                plist_data["Unique Identifier"] = udid
            if "UDID" in plist_data:
                plist_data["UDID"] = udid
            
            # Handle IMEI - remove key if device doesn't have IMEI (WiFi-only)
            if imei and imei.strip():
                if "IMEI" in plist_data:
                    plist_data["IMEI"] = imei
            else:
                # Remove IMEI key for WiFi-only devices
                plist_data.pop("IMEI", None)
            
            # Write customized plist
            with open(output_path, 'wb') as f:
                plistlib.dump(plist_data, f, fmt=plistlib.FMT_XML)
            
            print(f"[SUCCESS] Customized Info.plist: {output_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to customize Info.plist: {e}")
            return False
    
    @staticmethod
    def customize_info_plist_from_string(
        plist_string: str,
        output_path: str,
        build_version: str,
        product_type: str,
        serial_number: str,
        udid: str,
        imei: Optional[str] = None
    ) -> bool:
        """
        Customize Info.plist from a string (decrypted template)
        Uses string replacement like the Swift version for compatibility.
        
        Args:
            plist_string: Template plist as string
            output_path: Path to write customized plist
            build_version: iOS build version
            product_type: Device model
            serial_number: Device serial number
            udid: Device UDID
            imei: Device IMEI (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Replace build version
            plist_string = plist_string.replace(
                PlistCustomizer.DEFAULT_BUILD_VERSION,
                build_version
            )
            
            # Replace IMEI or remove IMEI entry
            if imei and imei.strip():
                plist_string = plist_string.replace(
                    PlistCustomizer.DEFAULT_IMEI,
                    imei
                )
            else:
                # Remove IMEI key and value (as per Swift code)
                imei_pattern = "\t<key>IMEI</key>\n\t<string>357145413514797</string>\n"
                plist_string = plist_string.replace(imei_pattern, "")
            
            # Replace product type
            plist_string = plist_string.replace(
                PlistCustomizer.DEFAULT_PRODUCT_TYPE,
                product_type
            )
            
            # Replace serial number
            plist_string = plist_string.replace(
                PlistCustomizer.DEFAULT_SERIAL_NUMBER,
                serial_number
            )
            
            # Replace UDID (appears in multiple places)
            plist_string = plist_string.replace(
                PlistCustomizer.DEFAULT_UDID,
                udid
            )
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(plist_string)
            
            print(f"[SUCCESS] Customized Info.plist: {output_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to customize Info.plist from string: {e}")
            return False
    
    @staticmethod
    def customize_manifest_plist_from_string(
        plist_string: str,
        output_path: str,
        build_version: str,
        product_type: str,
        serial_number: str,
        udid: str
    ) -> bool:
        """
        Customize Manifest.plist from a string (decrypted template)
        
        Args:
            plist_string: Template plist as string
            output_path: Path to write customized plist
            build_version: iOS build version
            product_type: Device model
            serial_number: Device serial number
            udid: Device UDID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Replace build version
            plist_string = plist_string.replace(
                PlistCustomizer.DEFAULT_BUILD_VERSION,
                build_version
            )
            
            # Replace product type
            plist_string = plist_string.replace(
                PlistCustomizer.DEFAULT_PRODUCT_TYPE,
                product_type
            )
            
            # Replace serial number
            plist_string = plist_string.replace(
                PlistCustomizer.DEFAULT_SERIAL_NUMBER,
                serial_number
            )
            
            # Replace UDID
            plist_string = plist_string.replace(
                PlistCustomizer.DEFAULT_UDID,
                udid
            )
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(plist_string)
            
            print(f"[SUCCESS] Customized Manifest.plist: {output_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to customize Manifest.plist: {e}")
            return False


if __name__ == "__main__":
    # Test plist customization
    print("=== Plist Customizer Test ===\n")
    
    # Example usage
    customizer = PlistCustomizer()
    
    # Test values
    test_info = {
        "build_version": "22C65",
        "product_type": "iPhone14,2",
        "serial_number": "TESTSERIAL123",
        "udid": "00001234-567890ABCDEF1234",
        "imei": "123456789012345"
    }
    
    print(f"Test device info:")
    for key, value in test_info.items():
        print(f"  {key}: {value}")
    
    print("\nReady to customize plist files with device-specific information")
