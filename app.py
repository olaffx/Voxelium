import sys
import os
import uuid
import plistlib
import shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QCheckBox, QPushButton, QLabel, QScrollArea, QMessageBox,
    QFileDialog, QProgressBar, QLineEdit
)
from PySide6.QtCore import Qt, QThread, Signal

if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ALL_RESTRICTIONS = {
    # Core Restrictions
    "AirDrop": "allowAirDrop",
    "App Installation": "allowAppInstallation",
    "App Removal": "allowAppRemoval",
    "Camera": "allowCamera",
    "Screenshots": "allowScreenShot",
    "Game Center": "allowGameCenter",
    "In-App Purchases": "allowInAppPurchases",
    "Safari": "allowSafari",
    "Explicit Content": "allowExplicitContent",
    "iMessage": "allowiMessage",
    "FaceTime": "allowFaceTime",
    
    # Additional Media & Apps
    "Music Videos": "allowMusicVideos",
    "Radio": "allowRadio",
    "Audiobooks": "allowAudiobooks",
    "Reminders": "allowReminders",
    "Notes": "allowNotes",
    "Voice Memos": "allowVoiceMemos",
    "NFC": "allowNFC",
    "Lock Screen": "allowLockScreen",
    
    # System Services
    "OTA Updates": "allowSoftwareUpdate",
    "Diagnostics & Usage": "allowDiagnosticSubmission",
    "Logs & Crash Reports": "allowDiagnosticSubmission",
    "Usage Tracking": "allowDiagnosticSubmission",
    "Background App Refresh": "allowGlobalBackgroundFetch",
    "Auto Lock": "allowAutoLock",
    "Device Name Modification": "allowDeviceNameModification",
    "Emergency SOS": "allowEmergencySOS",
    "SOS": "allowSOS",
    
    # iCloud Services
    "iCloud Backup": "allowCloudBackup",
    "iCloud Drive": "allowCloudDocumentSync",
    "iCloud Keychain": "allowCloudKeychainSync",
    "iCloud (General)": "allowCloudSettings",
    "Find My Friends": "allowFindMyFriends",
    "Find My iPhone": "allowFindMyDevice",
    "Find My Device": "allowFindMyDevice",
    "Cloud Photo Library": "allowCloudPhotoLibrary",
    "Shared Photo Stream": "allowSharedPhotoStream",
    "My Photo Stream": "allowMyPhotoStream",
    "Photo Sharing": "allowPhotoSharing",
    
    # Apple Apps
    "Siri": "allowAssistant",
    "Dictation": "allowDictation",
    "Tips": "allowTips",
    "Voice Control": "allowVoiceControl",
    "Assistive Touch": "allowAssistiveTouch",
    "Apple Books": "allowBookstore",
    "Podcasts": "allowPodcasts",
    "News": "allowNews",
    "Stocks": "allowStocks",
    "Calculator": "allowCalculator",
    "Mail": "allowMail",
    "Maps": "allowMaps",
    "Music": "allowMusic",
    "Photos": "allowPhotos",
    "Weather": "allowWeather",
    "HealthKit": "allowHealthKit",
    "Wallet": "allowWallet",
    "Wallet Notifications": "allowWalletNotifications",
    
    # Network & Connectivity
    "Cellular Data": "allowCellularData",
    "Cellular Plan Modification": "allowCellularPlanModification",
    "Data Roaming": "allowDataRoaming",
    "Personal Hotspot": "allowPersonalHotspot",
    "VPN Creation": "allowVPNCreation",
    "WiFi": "allowWiFi",
    "WiFi Modification": "allowWiFiModification",
    "Bluetooth": "allowBluetooth",
    "Bluetooth Sharing": "allowBluetoothSharing",
    "AirPrint": "allowPrinting",
    "Voice Roaming": "allowVoiceRoaming",
    "Chinese WLAN Service": "allowChinaWLAN",
    
    # Security & Lock Screen
    "Lock Screen Control Center": "allowLockScreenControlCenter",
    "Lock Screen Notifications": "allowLockScreenNotificationsView",
    "Lock Screen Today View": "allowLockScreenTodayView",
    "Passcode": "allowPasscode",
    "Simple Passcode": "allowSimplePasscode",
    "Touch ID": "allowFingerprint",
    "Face ID": "allowFaceID",
    "Auto Unlock": "allowAutoUnlock",
    "Screen Recording": "allowScreenRecording",
    
    # App Store & Installation
    "App Store": "allowAppStore",
    "App Store Updates": "allowAppStoreUpdates",
    "App Store Installation": "allowAppStoreAppInstallation",
    "App Store Removal": "allowAppStoreAppRemoval",
    "Free Apps Only": "allowFreeApps",
    "Rating Apps": "allowRatingApps",
    "App Clips": "allowAppClips",
    
    # Safari & Web
    "Safari AutoFill": "allowSafariAutoFill",
    "JavaScript": "allowJavaScript",
    "Popups": "allowPopups",
    "Cookies": "allowCookies",
    "Fraud Warning": "allowFraudWarning",
    
    # System Features
    "Multitasking": "allowMultitasking",
    "Wallpaper Modification": "allowWallpaperModification",
    "Notification Center": "allowNotificationCenter",
    "Control Center": "allowControlCenter",
    "Today View": "allowTodayView",
    "Spotlight": "allowSpotlight",
    "Handoff": "allowHandoff",
    "Keyboard Shortcuts": "allowKeyboardShortcuts",
    "Predictive Keyboard": "allowPredictiveKeyboard",
    "Swipe Typing": "allowContinuousPathKeyboard",
    "Auto Fill": "allowAutoFill",
    "Password Auto Fill": "allowPasswordAutoFill",
    
    # Messages & Communication
    "MMS": "allowMMS",
    "SMS": "allowSMS",
    "Video Conferencing": "allowVideoConferencing",
    
    # Game Center
    "Multiplayer Gaming": "allowMultiplayerGaming",
    "Add Game Center Friends": "allowAddingGameCenterFriends",
    
    # CarPlay
    "CarPlay": "allowCarPlay",
    "CarPlay While Locked": "allowCarPlayWhileLocked",
    
    # Accessibility
    "VoiceOver": "allowVoiceOver",
    "Zoom": "allowZoom",
    "Invert Colors": "allowInvertColors",
    "Mono Audio": "allowMonoAudio",
    "Speech": "allowSpeech",
    
    # Accounts & Calendar
    "Account Modification": "allowAccountModification",
    "Calendar Modification": "allowCalendarModification",
    "Calendar": "allowCalendar",
}

ALL_RESTRICTIONS = dict(dict.fromkeys(ALL_RESTRICTIONS))

RISKY_SERVICES = [
    "VPN Creation",
    "Personal Hotspot",
    "Cellular Data",
    "HealthKit",
    "iCloud (General)",
    "Wallet",
    "Find My iPhone",
    "Find My Friends",
    "Passcode",
    "Touch ID",
    "Face ID",
    "NFC",
]

KIOSK_SERVICES = [
    "App Installation", "App Removal", "Multitasking",
    "Notification Center", "Control Center", "Today View",
    "Spotlight", "Siri", "Dictation", "Screen Recording",
    "AirDrop", "Wallpaper Modification", "iCloud Backup",
    "iCloud Drive", "iCloud Keychain", "Find My Friends",
    "Find My iPhone", "Diagnostics & Usage", "OTA Updates",
    "Logs & Crash Reports", "Usage Tracking", "Game Center",
    "Tips", "Personal Hotspot", "VPN Creation", 
    "Account Modification", "HealthKit", "Voice Control",
    "Assistive Touch", "AirPrint", "Wallet", "iCloud (General)",
    "Camera", "FaceTime", "Safari", "Mail", "Maps",
    "Music", "Photos", "Weather", "Stocks", "Podcasts",
    "News", "Apple Books", "Calculator", "App Store",
    "In-App Purchases", "iMessage", "CarPlay", "Explicit Content",
    "Screenshots", "Reminders", "Notes", "Voice Memos", "NFC",
]

KIOSK_SERVICES = [s for s in KIOSK_SERVICES if s in ALL_RESTRICTIONS]

class ProfileGenerator(QThread):
    progress = Signal(int)
    finished = Signal(str, str)

    def __init__(self, selected_services, output_path, profile_name="profile"):
        super().__init__()
        self.selected = selected_services
        self.output_path = output_path
        self.profile_name = profile_name

    def run(self):
        try:
            self.progress.emit(25)
            top_uuid = str(uuid.uuid4()).upper()
            rest_uuid = str(uuid.uuid4()).upper()

            payload = {
                "PayloadDescription": f"Disables {len(self.selected)} iOS services.",
                "PayloadDisplayName": self.profile_name,
                "PayloadIdentifier": f"com.voxelium.restrictions.{rest_uuid}",
                "PayloadType": "com.apple.applicationaccess",
                "PayloadUUID": rest_uuid,
                "PayloadVersion": 1,
            }
            
            for name in self.selected:
                key = ALL_RESTRICTIONS.get(name)
                if key:
                    payload[key] = False

            self.progress.emit(50)

            profile = {
                "PayloadContent": [payload],
                "PayloadDescription": f"Disables {len(self.selected)} iOS services.",
                "PayloadDisplayName": f"{self.profile_name} Profile",
                "PayloadIdentifier": f"com.voxelium.{top_uuid}",
                "PayloadRemovalDisallowed": False,
                "PayloadType": "Configuration",
                "PayloadUUID": top_uuid,
                "PayloadVersion": 1,
            }

            with open(self.output_path, "wb") as f:
                plistlib.dump(profile, f, fmt=plistlib.FMT_BINARY)

            self.progress.emit(100)
            self.finished.emit(self.output_path, "")
        except Exception as e:
            self.finished.emit("", str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voxelium")
        self.setMinimumSize(700, 700)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        header = QLabel("<h2>Voxelium</h2><p>Make iPhones BETTER.</p>")
        header.setWordWrap(True)
        header.setTextFormat(Qt.RichText)
        main_layout.addWidget(header)

        top_row = QHBoxLayout()
        
        top_row.addWidget(QLabel("Profile Name:"))
        self.profile_name_edit = QLineEdit()
        self.profile_name_edit.setText("profile")
        self.profile_name_edit.setMaximumWidth(200)
        top_row.addWidget(self.profile_name_edit)
        
        top_row.addStretch()
        
        self.kiosk_cb = QCheckBox("Kiosk Mode")
        self.kiosk_cb.stateChanged.connect(self.toggle_kiosk_mode)
        top_row.addWidget(self.kiosk_cb)
        
        main_layout.addLayout(top_row)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Type to filter services...")
        self.search_edit.textChanged.connect(self.filter_services)
        search_layout.addWidget(self.search_edit)
        
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all)
        self.select_all_btn.setMaximumWidth(100)
        search_layout.addWidget(self.select_all_btn)
        
        self.deselect_all_btn = QPushButton("Deselect All")
        self.deselect_all_btn.clicked.connect(self.deselect_all)
        self.deselect_all_btn.setMaximumWidth(100)
        search_layout.addWidget(self.deselect_all_btn)
        
        main_layout.addLayout(search_layout)

        self.count_label = QLabel(f"Total Services: {len(ALL_RESTRICTIONS)}")
        main_layout.addWidget(self.count_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        self.checkboxes = {}
        self.all_services = sorted(ALL_RESTRICTIONS.keys())
        
        for name in self.all_services:
            cb = QCheckBox(name)
            if name in RISKY_SERVICES:
                cb.setStyleSheet("color: #ff6b6b;")
            cb.stateChanged.connect(self.update_count)
            scroll_layout.addWidget(cb)
            self.checkboxes[name] = cb

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        self.generate_btn = QPushButton("GENERATE PROFILE")
        self.generate_btn.clicked.connect(self.generate_profile)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                padding: 15px;
                background-color: #000000;
                color: white;
                border-radius: 5px;
                font-size: 16px;
                margin: 10px 0px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """)
        main_layout.addWidget(self.generate_btn)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)

        self.status = QLabel("Ready")
        main_layout.addWidget(self.status)

        self.last_profile = None

    def filter_services(self, text):
        text = text.lower()
        for cb in self.checkboxes.values():
            cb.hide()
        
        visible_count = 0
        for name in self.all_services:
            if text in name.lower():
                self.checkboxes[name].show()
                visible_count += 1
        
        self.count_label.setText(f"Showing: {visible_count}/{len(self.all_services)}")

    def select_all(self):
        for cb in self.checkboxes.values():
            if cb.isVisible():
                cb.setChecked(True)

    def deselect_all(self):
        for cb in self.checkboxes.values():
            cb.setChecked(False)

    def update_count(self):
        selected = len(self.get_selected())
        self.count_label.setText(f"Total: {len(self.all_services)} (Selected: {selected})")

    def toggle_kiosk_mode(self, state):
        if state == Qt.Checked:
            for name, cb in self.checkboxes.items():
                if name in KIOSK_SERVICES:
                    cb.setChecked(True)
            self.status.setText("Kiosk Mode enabled")

    def get_selected(self):
        return [name for name, cb in self.checkboxes.items() if cb.isChecked()]

    def generate_profile(self):
        selected = self.get_selected()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select at least one service.")
            return

        risky_selected = [s for s in selected if s in RISKY_SERVICES]
        if risky_selected:
            reply = QMessageBox.question(
                self,
                "Risky Options Selected",
                f"You selected {len(risky_selected)} risky option(s):\n\n" +
                "\n".join(f"• {s}" for s in risky_selected[:10]) +
                ("\n..." if len(risky_selected) > 10 else "") +
                "\n\nThese may affect device functionality.\nContinue?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return

        output_path = os.path.join(SCRIPT_DIR, "voxelium_profile.mobileconfig")
        profile_name = self.profile_name_edit.text() or "profile"
        
        self.generator = ProfileGenerator(selected, output_path, profile_name)
        self.generator.progress.connect(self.progress.setValue)
        self.generator.finished.connect(self.on_generation_finished)

        self.progress.setVisible(True)
        self.status.setText("Generating profile...")
        self.generate_btn.setEnabled(False)
        self.generator.start()

    def on_generation_finished(self, path, error):
        self.progress.setVisible(False)
        self.generate_btn.setEnabled(True)

        if error:
            QMessageBox.critical(self, "Error", f"Failed to generate profile:\n{error}")
            self.status.setText("Generation failed.")
        else:
            self.last_profile = path
            self.status.setText(f"✅ Profile saved to: {path}")
            
            QMessageBox.information(
                self, 
                "Profile Generated", 
                f"Profile saved to:\n{path}\n\n"
                "Next steps:\n"
                "1. Transfer this file to your iPhone (AirDrop/email/iCloud)\n"
                "2. Open the file on your iPhone\n"
                "3. Go to Settings → Profile Downloaded → Install\n\n"
                "To revert: Settings → General → VPN & Device Management → Remove Profile"
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())