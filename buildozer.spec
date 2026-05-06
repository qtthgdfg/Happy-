# buildozer.spec - Complete configuration for background service APK

[app]

# (str) Title of your application
title = System Service

# (str) Package name
package.name = systemservice

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Application requirements
# 🔑 FIXED: Removed python3==3.10.12 version pin from requirements
# The python3 version must match hostpython3, which is controlled by p4a not buildozer
requirements = python3,kivy==2.3.0,pyjnius,android,plyer

# (str) Python version for python-for-android
# 🔑 CRITICAL: This tells p4a exactly which Python version to build
p4a.python_version = 3.10.12

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
# This is CRITICAL for background service execution!
services = Service:service.py

# (str) Service entry point file
service.source = %(source.dir)s/service.py

# (list) List of permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,\
    FOREGROUND_SERVICE,FOREGROUND_SERVICE_DATA_SYNC,FOREGROUND_SERVICE_SPECIAL_USE,\
    WAKE_LOCK,RECEIVE_BOOT_COMPLETED,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,\
    POWER_SAVE_MODE_CHANGED,ACCESS_BACKGROUND_SERVICE,\
    READ_PHONE_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (list) features of the app
android.features = android.hardware.wifi

# (list) Targeted Android SDK version
android.api = 33

# (str) Minimum Android SDK version
android.minapi = 21

# (int) Target NDK version
android.ndk = 25b

# (list) The Android arch to build for
# 🔑 FIXED: Removed space before armeabi-v7a
android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_agreement = True
android.allow_backup = True
android.private_storage = True
android.presplash_color = #000000
android.wakelock = True
android.hide_loading_screen = True
android.enable_androidx = True
          
android.debug = True

# (str) Gradle version
android.gradle_dependencies = 'androidx.core:core:1.10.1'

# ----------------------------------------------------------
# Android SERVICE configuration
# ----------------------------------------------------------

# (str) Foreground service notification channel name
android.notification_channel_name = System Service

# (str) Foreground service notification title
android.notification_title = Running Background Service

# (str) Foreground service notification text
android.notification_text = Service is running in background

# (str) Foreground service notification importance (min, low, default, high, max)
android.notification_importance = low

# (str) Foreground service type
android.foreground_service_type = dataSync

# ----------------------------------------------------------
# CRITICAL - p4a branch for NDK 25b support
# ----------------------------------------------------------
p4a.branch = develop
android.p4a_bootstrap = sdl2

# ----------------------------------------------------------
# Build configuration
# ----------------------------------------------------------

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# ----------------------------------------------------------
# Logging
# ----------------------------------------------------------

# (str) Log level (trace, debug, info, warning, error, critical)
log_level = 2

# (bool) Enable logcat output
android.logcat = 1

# (bool) Create an archive (.apk) release
android.release_artifact = apk

# (str) Keystore path for release
# android.release.keystore = /path/to/keystore

# (str) Keystore alias
# android.release.keyalias = keyalias

# (str) Keystore password
# android.release.keystore_password = password

# (str) Key password
# android.release.key_password = password

[buildozer]
log_level = 2
