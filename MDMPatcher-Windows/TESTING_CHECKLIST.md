# Testing Checklist for MDMPatcher Windows Edition

This document provides a comprehensive testing checklist for validating the Windows port of MDMPatcher Enhanced.

## Pre-Testing Setup

### Environment Setup
- [ ] Windows 10 (64-bit) or Windows 11 installed
- [ ] Python 3.8+ installed and in PATH
- [ ] pip installed and working
- [ ] Git installed (optional, for cloning)

### Dependencies Installation
- [ ] PyQt6 installed: `pip install PyQt6`
- [ ] pyusb installed: `pip install pyusb`
- [ ] pycryptodome installed: `pip install pycryptodome`
- [ ] All dependencies: `pip install -r requirements.txt`

### External Tools
- [ ] iTunes or Apple Mobile Device Support installed
- [ ] libimobiledevice tools installed (ideviceinfo, idevicebackup2, idevice_id)
- [ ] Tools available in PATH or local directory

### Template Files
- [ ] extension1.pdf exists in resources/templates/
- [ ] extension2.pdf exists in resources/templates/
- [ ] libiMobileeDevice.dylib exists in resources/templates/

---

## Unit Testing

### Module Import Tests
Run `python test_installation.py` and verify:
- [ ] Python version check passes
- [ ] All dependencies detected
- [ ] libimobiledevice tools detected
- [ ] Template files found
- [ ] Core modules import successfully
- [ ] UI modules import successfully

### Individual Module Tests

#### Decryption Module
```python
python -c "from core.decryption import RNCryptorDecryptor; print('Password:', RNCryptorDecryptor.calculate_password())"
```
- [ ] Password calculation succeeds
- [ ] Password matches expected format

#### Device Detector Module
```python
python -c "from core.device_detector import scan_for_ios_devices; print('Devices:', scan_for_ios_devices())"
```
- [ ] USB scan completes without errors
- [ ] Returns empty list if no devices connected
- [ ] Detects connected iOS devices (if available)

#### Device Info Module
```python
python -c "from core.device_info import DeviceInfoExtractor; e = DeviceInfoExtractor(); print('Tools OK')"
```
- [ ] Module imports successfully
- [ ] ideviceinfo path resolves

---

## Integration Testing

### Application Launch
- [ ] Launch with `python main.py`
- [ ] Window opens successfully
- [ ] No Python errors in console
- [ ] Legal disclaimer displayed in console

### UI Elements
- [ ] Main window displays correctly
- [ ] Title shows "MDMPatcher Enhanced - Windows Edition"
- [ ] Device information fields visible
- [ ] PATCH button visible (disabled initially)
- [ ] Progress bar hidden initially
- [ ] Log window displays initial messages

### USB Device Detection

#### Without Device
- [ ] Application starts with "Not connected" status
- [ ] PATCH button is disabled
- [ ] Log shows "Waiting for iOS device"

#### With Device Connected (Normal Mode)
- [ ] Plug in iOS device (unlocked, trusted)
- [ ] Log shows device connection
- [ ] Device info fields populate (or remain empty if not in Recovery Mode)

#### With Device in Recovery Mode
Prerequisites:
- [ ] Device put into Recovery Mode (shows iTunes logo + USB cable)
- [ ] Device connected via USB

Expected Results:
- [ ] Application detects device (Product ID 4776 or 4779)
- [ ] Log shows "Device is in Recovery Mode"
- [ ] Device information appears:
  - [ ] Model (e.g., "iPhone14,2")
  - [ ] Serial Number
  - [ ] UDID (40 characters)
  - [ ] iOS Version and Build (e.g., "18.0 (22A3354)")
  - [ ] IMEI (if cellular) or "N/A"
- [ ] PATCH button becomes enabled

### Device Disconnection
- [ ] Disconnect device
- [ ] Log shows "Device disconnected"
- [ ] Device info fields clear
- [ ] PATCH button becomes disabled

---

## Functional Testing (Full Workflow)

⚠️ **WARNING**: This will restore the device. Ensure you have a backup and know what you're doing!

### Preparation
- [ ] Device restored to fresh iOS (from IPSW)
- [ ] Device completed setup to Wi-Fi screen
- [ ] Device NOT connected to Wi-Fi
- [ ] Device in Recovery Mode
- [ ] MDMPatcher detects device and shows info

### Patching Process
1. Click PATCH Button
   - [ ] Confirmation dialog appears
   - [ ] Device info shown in dialog
   - [ ] Can cancel or proceed

2. Confirm Patching
   - [ ] PATCH button disables
   - [ ] Progress bar appears (indeterminate animation)
   - [ ] Log shows "Starting patching process..."

3. Decryption Phase
   - [ ] Log: "Decrypting template files..."
   - [ ] Log: "Decryption completed!"
   - [ ] No errors in console

4. Customization Phase
   - [ ] Log: "Customizing backup files..."
   - [ ] Log: "Plist customization completed!"

5. Restoration Phase
   - [ ] Log: "Restoring backup to device..."
   - [ ] idevicebackup2 output appears in log
   - [ ] Process may take 2-5 minutes

6. Completion
   - [ ] Success dialog appears OR error dialog with details
   - [ ] Device reboots automatically (if successful)
   - [ ] Progress bar disappears
   - [ ] PATCH button re-enables

### Post-Patch Verification
- [ ] Device reboots successfully
- [ ] MDM enrollment screen skipped
- [ ] Device setup completes normally
- [ ] Device functions normally

---

## Error Handling Tests

### Missing Dependencies
- [ ] Uninstall PyQt6: Error message shows installation command
- [ ] Uninstall pyusb: Warning about USB detection
- [ ] Uninstall pycryptodome: Import error handled gracefully

### Missing libimobiledevice
- [ ] Rename/remove ideviceinfo: Warning shown, option to continue
- [ ] Click PATCH without tools: Error message with installation guide

### Missing Template Files
- [ ] Remove extension1.pdf: Error during decryption phase
- [ ] Error message indicates which file is missing

### Device Issues
- [ ] Device not trusted: Error accessing device info
- [ ] Device locked: Cannot get device info
- [ ] Device not in Recovery Mode: Warning in log
- [ ] Device disconnected during patch: Error message shown

### USB Issues
- [ ] No USB drivers: Device not detected
- [ ] USB 3.0 port issues: Test with USB 2.0 port

---

## Performance Testing

### Memory Usage
- [ ] Monitor memory usage during idle (should be ~50-100MB)
- [ ] Monitor memory during patching (should not exceed 500MB)
- [ ] No memory leaks after multiple device connects/disconnects

### Response Time
- [ ] UI responds within 100ms to clicks
- [ ] Device detection within 1 second of connection
- [ ] Device info retrieval within 2 seconds

### Stability
- [ ] Run for 30 minutes without crashes
- [ ] Connect/disconnect device 10 times without issues
- [ ] No freezing or hanging

---

## Cross-Version Testing

### Windows Versions
- [ ] Windows 10 (21H2)
- [ ] Windows 10 (22H2)
- [ ] Windows 11 (21H2)
- [ ] Windows 11 (22H2)

### Python Versions
- [ ] Python 3.8
- [ ] Python 3.9
- [ ] Python 3.10
- [ ] Python 3.11
- [ ] Python 3.12

### iOS Versions
- [ ] iOS 15.x
- [ ] iOS 16.x
- [ ] iOS 17.x
- [ ] iOS 18.x

### Device Models
- [ ] iPhone (newer models with Face ID)
- [ ] iPhone (older models with Touch ID)
- [ ] iPad (newer models)
- [ ] iPad (older models)
- [ ] WiFi-only devices
- [ ] Cellular devices

---

## Security Testing

### Code Review
- [ ] No hardcoded credentials
- [ ] No network communication (except libimobiledevice)
- [ ] Sensitive data not logged
- [ ] Temporary files cleaned up

### Windows Defender
- [ ] Application not flagged as malware
- [ ] Can be added to exclusions if needed
- [ ] SmartScreen allows execution

### User Permissions
- [ ] Runs without admin rights (preferred)
- [ ] Request admin only if USB access requires it

---

## Documentation Testing

### README Accuracy
- [ ] All installation steps work as documented
- [ ] All commands execute successfully
- [ ] Screenshots match actual UI (if added)
- [ ] Links work correctly

### Error Messages
- [ ] All error messages are clear and actionable
- [ ] Error messages include next steps
- [ ] Technical details provided when relevant

### Help Resources
- [ ] Troubleshooting section covers common issues
- [ ] FAQ answers real questions
- [ ] Contact information is correct

---

## Regression Testing

After any code changes, verify:
- [ ] Application still launches
- [ ] Device detection still works
- [ ] Patching workflow still completes
- [ ] No new errors introduced
- [ ] Performance not degraded

---

## Known Issues to Verify

Document any issues found:

1. **Issue**: _____________________
   - **Steps to Reproduce**: _____________________
   - **Expected**: _____________________
   - **Actual**: _____________________
   - **Severity**: Critical / High / Medium / Low
   - **Workaround**: _____________________

2. **Issue**: _____________________
   - **Steps to Reproduce**: _____________________
   - **Expected**: _____________________
   - **Actual**: _____________________
   - **Severity**: Critical / High / Medium / Low
   - **Workaround**: _____________________

---

## Test Results Summary

**Tester Name**: _____________________  
**Test Date**: _____________________  
**Environment**: _____________________  

**Results**:
- Total Tests: _____
- Passed: _____
- Failed: _____
- Skipped: _____

**Overall Assessment**: Pass / Fail / Needs Work

**Recommendation**: Release / Fix Issues / Major Revision

**Additional Notes**:
_____________________
_____________________
_____________________

---

## Sign-Off

**Tested By**: _____________________  
**Date**: _____________________  
**Signature**: _____________________

**Approved By**: _____________________  
**Date**: _____________________  
**Signature**: _____________________
