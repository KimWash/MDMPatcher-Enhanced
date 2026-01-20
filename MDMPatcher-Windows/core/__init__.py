"""
Core modules for MDMPatcher Windows Edition
"""

from .device_detector import USBDeviceWatcher, IOSDevice, scan_for_ios_devices
from .device_info import DeviceInfoExtractor, DeviceInfo, get_device_information_xml
from .decryption import RNCryptorDecryptor, decrypt_template_file
from .plist_handler import PlistCustomizer
from .backup_restore import BackupRestorer, BackupWorkflow

__all__ = [
    'USBDeviceWatcher',
    'IOSDevice',
    'scan_for_ios_devices',
    'DeviceInfoExtractor',
    'DeviceInfo',
    'get_device_information_xml',
    'RNCryptorDecryptor',
    'decrypt_template_file',
    'PlistCustomizer',
    'BackupRestorer',
    'BackupWorkflow',
]
