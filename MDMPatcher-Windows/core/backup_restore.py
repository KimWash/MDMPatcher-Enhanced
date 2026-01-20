"""
Backup Restoration Module
Handles creating and restoring MDM bypass backup structure.
"""

import os
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Optional


class BackupRestorer:
    """
    Manages iOS backup creation and restoration for MDM patching.
    Uses idevicebackup2 from libimobiledevice.
    """
    
    def __init__(self, idevicebackup2_path: str = "idevicebackup2"):
        """
        Initialize backup restorer
        
        Args:
            idevicebackup2_path: Path to idevicebackup2 executable
        """
        self.idevicebackup2_path = idevicebackup2_path
    
    def extract_backup_archive(self, archive_path: str, destination: str) -> bool:
        """
        Extract backup archive (ZIP) to destination
        
        Args:
            archive_path: Path to backup ZIP file
            destination: Directory to extract to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"[INFO] Extracting backup archive to: {destination}")
            
            # Create destination directory if it doesn't exist
            os.makedirs(destination, exist_ok=True)
            
            # Extract ZIP
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(destination)
            
            print(f"[SUCCESS] Extracted backup archive")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to extract backup archive: {e}")
            return False
    
    def prepare_mdmb_directory(self, temp_dir: str) -> str:
        """
        Create MDMB directory structure for backup
        
        Args:
            temp_dir: Temporary directory base path
            
        Returns:
            Path to MDMB directory
        """
        mdmb_dir = os.path.join(temp_dir, "MDMB")
        os.makedirs(mdmb_dir, exist_ok=True)
        print(f"[INFO] Created MDMB directory: {mdmb_dir}")
        return mdmb_dir
    
    def restore_backup(
        self,
        backup_dir: str,
        udid: Optional[str] = None,
        password: Optional[str] = None,
        source_udid: str = "MDMB"
    ) -> bool:
        """
        Restore backup to iOS device using idevicebackup2
        
        Args:
            backup_dir: Path to backup directory
            udid: Optional device UDID
            password: Optional backup password
            source_udid: Source UDID subdirectory name (default: "MDMB")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"[INFO] Starting backup restoration...")
            print(f"[INFO] Backup directory: {backup_dir}")
            print(f"[INFO] Source UDID: {source_udid}")
            
            # Build command
            cmd = [self.idevicebackup2_path, "restore"]
            
            if udid:
                cmd.extend(["-u", udid])
            
            # Add source UDID parameter (which subdirectory to use)
            cmd.extend(["--source", source_udid])
            
            if password:
                cmd.extend(["--password", password])
            
            # Add backup directory
            cmd.append(backup_dir)
            
            print(f"[INFO] Running: {' '.join(cmd)}")
            
            # Run idevicebackup2 restore
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Stream output
            for line in process.stdout:
                print(f"[RESTORE] {line.strip()}")
            
            # Wait for completion
            return_code = process.wait()
            
            if return_code == 0:
                print("[SUCCESS] Backup restored successfully!")
                print("[INFO] Device will now reboot...")
                return True
            else:
                stderr = process.stderr.read()
                print(f"[ERROR] Backup restoration failed with code {return_code}")
                if stderr:
                    print(f"[ERROR] {stderr}")
                return False
                
        except FileNotFoundError:
            print(f"[ERROR] idevicebackup2 not found at: {self.idevicebackup2_path}")
            print("[INFO] Please install libimobiledevice or place idevicebackup2.exe in PATH")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to restore backup: {e}")
            return False
    
    def create_manifest_mbdb(self, destination: str) -> bool:
        """
        Create Manifest.mbdb file (binary backup database)
        
        iOS backups use Manifest.mbdb (binary format) for older iOS versions
        and Manifest.plist (XML format) for newer versions. Some versions of
        idevicebackup2 require Manifest.mbdb even when Manifest.plist exists.
        
        Args:
            destination: Directory to create Manifest.mbdb in
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Manifest.mbdb format:
            # Header: "mbdb\x05\x00" (magic number + version 5)
            # Followed by file entries (empty for MDM bypass)
            mbdb_data = b'mbdb\x05\x00'
            
            mbdb_path = os.path.join(destination, "Manifest.mbdb")
            with open(mbdb_path, 'wb') as f:
                f.write(mbdb_data)
            
            print(f"[INFO] Created Manifest.mbdb at: {mbdb_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to create Manifest.mbdb: {e}")
            return False
    
    def create_status_plist(self, destination: str) -> bool:
        """
        Create Status.plist file indicating successful backup
        
        Args:
            destination: Directory to create Status.plist in
            
        Returns:
            True if successful, False otherwise
        """
        try:
            status_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
\t<key>BackupState</key>
\t<string>new</string>
\t<key>Date</key>
\t<date>2024-01-01T00:00:00Z</date>
\t<key>IsFullBackup</key>
\t<false/>
\t<key>SnapshotState</key>
\t<string>finished</string>
\t<key>Version</key>
\t<string>2.4</string>
</dict>
</plist>
'''
            status_path = os.path.join(destination, "Status.plist")
            with open(status_path, 'w', encoding='utf-8') as f:
                f.write(status_content)
            
            print(f"[INFO] Created Status.plist at: {status_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to create Status.plist: {e}")
            return False
    
    def create_backup_structure(
        self,
        temp_dir: str,
        archive_path: str,
        info_plist_path: str,
        manifest_plist_path: str
    ) -> Optional[str]:
        """
        Create complete backup structure ready for restoration
        
        Args:
            temp_dir: Temporary directory for backup
            archive_path: Path to decrypted backup archive (ZIP)
            info_plist_path: Path to customized Info.plist
            manifest_plist_path: Path to customized Manifest.plist
            
        Returns:
            Path to backup directory or None if failed
        """
        try:
            # Create MDMB directory (this will be the parent backup directory)
            mdmb_parent_dir = self.prepare_mdmb_directory(temp_dir)
            
            # Create MDMB subdirectory inside (this is the UDID directory)
            # idevicebackup2 expects: backup_dir/UDID/Info.plist
            # We use "MDMB" as the UDID (same as macOS version)
            mdmb_backup_dir = os.path.join(mdmb_parent_dir, "MDMB")
            os.makedirs(mdmb_backup_dir, exist_ok=True)
            print(f"[INFO] Created backup UDID directory: {mdmb_backup_dir}")
            
            # Extract backup files into the UDID subdirectory
            if not self.extract_backup_archive(archive_path, mdmb_backup_dir):
                return None
            
            # Create Manifest.mbdb (required by some idevicebackup2 versions)
            if not self.create_manifest_mbdb(mdmb_backup_dir):
                return None
            
            # Create Status.plist (required by idevicebackup2 restore)
            if not self.create_status_plist(mdmb_backup_dir):
                return None
            
            # Copy customized plists into the UDID subdirectory
            shutil.copy2(info_plist_path, os.path.join(mdmb_backup_dir, "Info.plist"))
            shutil.copy2(manifest_plist_path, os.path.join(mdmb_backup_dir, "Manifest.plist"))
            
            print("[SUCCESS] Backup structure created")
            # Return the parent directory (not the UDID subdirectory)
            return mdmb_parent_dir
            
        except Exception as e:
            print(f"[ERROR] Failed to create backup structure: {e}")
            return None
    
    def cleanup_temp_files(self, temp_dir: str):
        """
        Clean up temporary files and directories
        
        Args:
            temp_dir: Temporary directory to remove
        """
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                print(f"[INFO] Cleaned up temporary files: {temp_dir}")
        except Exception as e:
            print(f"[WARN] Failed to cleanup temp files: {e}")


class BackupWorkflow:
    """
    High-level workflow for MDM patching via backup restoration.
    Combines all steps from decryption to restoration.
    """
    
    def __init__(self):
        self.restorer = BackupRestorer()
    
    def execute_patch(
        self,
        temp_dir: str,
        decrypted_archive: str,
        info_plist: str,
        manifest_plist: str,
        udid: str
    ) -> bool:
        """
        Execute complete patching workflow
        
        Args:
            temp_dir: Temporary directory for work
            decrypted_archive: Path to decrypted backup ZIP
            info_plist: Path to customized Info.plist
            manifest_plist: Path to customized Manifest.plist
            udid: Device UDID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create backup structure
            backup_dir = self.restorer.create_backup_structure(
                temp_dir,
                decrypted_archive,
                info_plist,
                manifest_plist
            )
            
            if not backup_dir:
                return False
            
            # Restore to device
            success = self.restorer.restore_backup(backup_dir, udid)
            
            return success
            
        except Exception as e:
            print(f"[ERROR] Patch workflow failed: {e}")
            return False
        finally:
            # Always cleanup
            self.restorer.cleanup_temp_files(temp_dir)


if __name__ == "__main__":
    print("=== Backup Restoration Module ===\n")
    
    restorer = BackupRestorer()
    
    print("This module handles iOS backup restoration for MDM patching.")
    print("\nRequired tools:")
    print("  - idevicebackup2 (from libimobiledevice)")
    print("\nMake sure the tool is in your PATH or specify the full path.")
