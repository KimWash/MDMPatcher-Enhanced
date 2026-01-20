"""
Main Window UI for MDMPatcher Windows Edition
Built with PyQt6 to match the macOS version's layout and functionality.
"""

import sys
import os
from pathlib import Path
from typing import Optional

try:
    from PyQt6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
        QPushButton, QTextEdit, QGroupBox, QProgressBar, QMessageBox,
        QApplication
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QFont, QIcon
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    print("Warning: PyQt6 not available. UI will not work.")


class PatchWorker(QThread):
    """Worker thread for patching process"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, device_info, temp_dir, templates_dir):
        super().__init__()
        self.device_info = device_info
        self.temp_dir = temp_dir
        self.templates_dir = templates_dir
    
    def run(self):
        """Execute patching in background thread"""
        try:
            from ..core import (
                decrypt_template_file, PlistCustomizer, 
                BackupWorkflow, RNCryptorDecryptor
            )
            
            self.progress.emit("Starting MDM patch process...")
            
            # Create temp directory
            os.makedirs(self.temp_dir, exist_ok=True)
            mdmb_dir = os.path.join(self.temp_dir, "MDMB")
            os.makedirs(mdmb_dir, exist_ok=True)
            
            # Step 1: Decrypt template files
            self.progress.emit("Decrypting template files...")
            
            password = RNCryptorDecryptor.calculate_password()
            
            # Decrypt Info.plist template
            info_template = os.path.join(self.templates_dir, "extension1.pdf")
            info_decrypted = os.path.join(self.temp_dir, "info_template.plist")
            
            if not decrypt_template_file(info_template, info_decrypted, password):
                self.finished.emit(False, "Failed to decrypt Info.plist template")
                return
            
            # Decrypt Manifest.plist template
            manifest_template = os.path.join(self.templates_dir, "extension2.pdf")
            manifest_decrypted = os.path.join(self.temp_dir, "manifest_template.plist")
            
            if not decrypt_template_file(manifest_template, manifest_decrypted, password):
                self.finished.emit(False, "Failed to decrypt Manifest.plist template")
                return
            
            # Decrypt backup archive
            archive_template = os.path.join(self.templates_dir, "libiMobileeDevice.dylib")
            archive_decrypted = os.path.join(self.temp_dir, "backup_archive.zip")
            
            if not decrypt_template_file(archive_template, archive_decrypted, password):
                self.finished.emit(False, "Failed to decrypt backup archive")
                return
            
            self.progress.emit("Decryption completed!")
            
            # Step 2: Customize plists
            self.progress.emit("Customizing backup files...")
            
            # Read decrypted templates
            with open(info_decrypted, 'r', encoding='utf-8') as f:
                info_content = f.read()
            
            with open(manifest_decrypted, 'r', encoding='utf-8') as f:
                manifest_content = f.read()
            
            # Customize Info.plist
            info_output = os.path.join(self.temp_dir, "Info.plist")
            if not PlistCustomizer.customize_info_plist_from_string(
                info_content,
                info_output,
                self.device_info.build_version,
                self.device_info.product_type,
                self.device_info.serial_number,
                self.device_info.udid,
                self.device_info.imei
            ):
                self.finished.emit(False, "Failed to customize Info.plist")
                return
            
            # Customize Manifest.plist
            manifest_output = os.path.join(self.temp_dir, "Manifest.plist")
            if not PlistCustomizer.customize_manifest_plist_from_string(
                manifest_content,
                manifest_output,
                self.device_info.build_version,
                self.device_info.product_type,
                self.device_info.serial_number,
                self.device_info.udid
            ):
                self.finished.emit(False, "Failed to customize Manifest.plist")
                return
            
            self.progress.emit("Plist customization completed!")
            
            # Step 3: Restore backup
            self.progress.emit("Restoring backup to device...")
            
            workflow = BackupWorkflow()
            success = workflow.execute_patch(
                self.temp_dir,
                archive_decrypted,
                info_output,
                manifest_output,
                self.device_info.udid
            )
            
            if success:
                self.finished.emit(True, "MDM patch successful! Device will reboot.")
            else:
                self.finished.emit(False, "Backup restoration failed")
                
        except Exception as e:
            self.finished.emit(False, f"Patching error: {str(e)}")


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.device_info = None
        self.watcher = None
        self.patch_worker = None
        
        self.init_ui()
        self.start_device_monitoring()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("MDMPatcher Enhanced - Windows Edition")
        self.setMinimumSize(600, 500)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel("MDMPatcher Enhanced")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Windows Edition - MDM Profile Bypass Tool")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666;")
        layout.addWidget(subtitle)
        
        # Device Info Group
        device_group = QGroupBox("Device Information")
        device_layout = QVBoxLayout()
        
        self.device_model_label = self._create_info_label("Model:", "Not connected")
        self.device_serial_label = self._create_info_label("Serial:", "Not connected")
        self.device_udid_label = self._create_info_label("UDID:", "Not connected")
        self.device_firmware_label = self._create_info_label("iOS Version:", "Not connected")
        self.device_imei_label = self._create_info_label("IMEI:", "Not connected")
        
        device_layout.addWidget(self.device_model_label)
        device_layout.addWidget(self.device_serial_label)
        device_layout.addWidget(self.device_udid_label)
        device_layout.addWidget(self.device_firmware_label)
        device_layout.addWidget(self.device_imei_label)
        
        device_group.setLayout(device_layout)
        layout.addWidget(device_group)
        
        # Patch button
        self.patch_button = QPushButton("PATCH")
        self.patch_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.patch_button.setMinimumHeight(50)
        self.patch_button.setEnabled(False)
        self.patch_button.clicked.connect(self.on_patch_clicked)
        self.patch_button.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0051D5;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """)
        layout.addWidget(self.patch_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Log output
        log_group = QGroupBox("Log Output")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.setFont(QFont("Consolas", 9))
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # Add stretch at the end
        layout.addStretch()
        
        # Log initial message
        self.log("MDMPatcher Enhanced - Windows Edition")
        self.log("Waiting for iOS device in Recovery Mode...")
        self.log("Product ID: 4776 or 4779")
    
    def _create_info_label(self, label: str, value: str) -> QLabel:
        """Create a formatted info label"""
        lbl = QLabel(f"{label} {value}")
        lbl.setFont(QFont("Arial", 10))
        return lbl
    
    def start_device_monitoring(self):
        """Start USB device monitoring"""
        try:
            from ..core import USBDeviceWatcher
            
            self.watcher = USBDeviceWatcher(
                on_device_added=self.on_device_connected,
                on_device_removed=self.on_device_disconnected
            )
            self.watcher.start()
            self.log("Device monitoring started")
            
        except Exception as e:
            self.log(f"Failed to start device monitoring: {e}")
            QMessageBox.warning(
                self,
                "Warning",
                "USB device monitoring is not available.\n"
                "Please make sure pyusb is installed:\n\n"
                "pip install pyusb"
            )
    
    def on_device_connected(self, device):
        """Handle device connection"""
        self.log(f"Device connected: {device}")
        
        if device.is_recovery_mode():
            self.log("Device is in Recovery Mode - fetching information...")
            self.update_device_info()
        else:
            self.log("Device is not in Recovery Mode (PID: {})".format(hex(device.product_id)))
    
    def on_device_disconnected(self, device):
        """Handle device disconnection"""
        self.log(f"Device disconnected: {device}")
        self.clear_device_info()
    
    def update_device_info(self):
        """Fetch and display device information"""
        try:
            from ..core import DeviceInfoExtractor
            
            extractor = DeviceInfoExtractor()
            info = extractor.get_device_info()
            
            if info and info.is_valid():
                self.device_info = info
                
                # Update labels
                self.device_model_label.setText(f"Model: {info.product_type}")
                self.device_serial_label.setText(f"Serial: {info.serial_number}")
                self.device_udid_label.setText(f"UDID: {info.udid}")
                self.device_firmware_label.setText(
                    f"iOS Version: {info.product_version} ({info.build_version})"
                )
                self.device_imei_label.setText(f"IMEI: {info.imei or 'N/A (WiFi only)'}")
                
                # Enable patch button
                self.patch_button.setEnabled(True)
                
                self.log("Device information retrieved successfully!")
            else:
                self.log("Failed to retrieve device information")
                self.clear_device_info()
                
        except Exception as e:
            self.log(f"Error fetching device info: {e}")
            self.clear_device_info()
    
    def clear_device_info(self):
        """Clear device information display"""
        self.device_info = None
        self.device_model_label.setText("Model: Not connected")
        self.device_serial_label.setText("Serial: Not connected")
        self.device_udid_label.setText("UDID: Not connected")
        self.device_firmware_label.setText("iOS Version: Not connected")
        self.device_imei_label.setText("IMEI: Not connected")
        self.patch_button.setEnabled(False)
    
    def on_patch_clicked(self):
        """Handle patch button click"""
        if not self.device_info:
            QMessageBox.warning(self, "Error", "No device information available")
            return
        
        # Confirm action
        reply = QMessageBox.question(
            self,
            "Confirm Patching",
            f"Are you sure you want to patch this device?\n\n"
            f"Model: {self.device_info.product_type}\n"
            f"Serial: {self.device_info.serial_number}\n"
            f"UDID: {self.device_info.udid}\n\n"
            f"This will restore a backup to bypass MDM.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        self.start_patching()
    
    def start_patching(self):
        """Start the patching process"""
        self.patch_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        
        self.log("Starting patching process...")
        
        # Get paths
        app_dir = Path(__file__).parent.parent
        temp_dir = Path.home() / "AppData" / "Local" / "Temp" / "MDMPatcher"
        templates_dir = app_dir / "resources" / "templates"
        
        # Start worker thread
        self.patch_worker = PatchWorker(self.device_info, str(temp_dir), str(templates_dir))
        self.patch_worker.progress.connect(self.on_patch_progress)
        self.patch_worker.finished.connect(self.on_patch_finished)
        self.patch_worker.start()
    
    def on_patch_progress(self, message: str):
        """Handle progress updates"""
        self.log(message)
    
    def on_patch_finished(self, success: bool, message: str):
        """Handle patching completion"""
        self.progress_bar.setVisible(False)
        self.patch_button.setEnabled(True)
        
        self.log(message)
        
        if success:
            QMessageBox.information(
                self,
                "Success!",
                "MDM has been successfully patched on your device!\n\n"
                "Your device will now reboot.\n"
                "Please complete the setup process.\n\n"
                "Have fun :-)"
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Patching failed:\n\n{message}\n\n"
                "Please reboot your device and try again.\n"
                "If the problem persists, contact the developer."
            )
    
    def log(self, message: str):
        """Add message to log output"""
        self.log_text.append(f"[{self._get_timestamp()}] {message}")
        # Auto-scroll to bottom
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.watcher:
            self.watcher.stop()
        event.accept()


def main():
    """Application entry point"""
    if not PYQT_AVAILABLE:
        print("ERROR: PyQt6 is not installed!")
        print("Install it with: pip install PyQt6")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    app.setApplicationName("MDMPatcher Enhanced")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
